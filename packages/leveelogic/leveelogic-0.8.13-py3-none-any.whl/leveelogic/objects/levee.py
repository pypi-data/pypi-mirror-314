import os
from dotenv import load_dotenv
from typing import List, Tuple, Union, Optional
from shapely.geometry import Polygon, MultiPolygon
from shapely.geometry import Point as SHPPoint
from shapely import get_coordinates
from shapely.ops import orient, unary_union
from pathlib import Path
from geolib.geometry.one import Point
from geolib.soils.soil import Soil as GLSoil, ShearStrengthModelTypePhreaticLevel
from geolib.models.dstability.loads import UniformLoad, Consolidation, TreeLoad
from geolib.models.dstability.analysis import (
    PersistableBishopBruteForceSettings,
    PersistableSpencerGeneticSettings,
    PersistableUpliftVanParticleSwarmSettings,
    DStabilityBishopBruteForceAnalysisMethod,
    DStabilitySpencerGeneticAnalysisMethod,
    DStabilityUpliftVanParticleSwarmAnalysisMethod,
    DStabilitySearchGrid,
    DStabilitySlipPlaneConstraints,
    DStabilityGeneticSlipPlaneConstraints,
    DStabilitySearchArea,
)
from geolib.models.dstability.internal import AnalysisTypeEnum
from enum import IntEnum
from math import ceil, floor

from ..models.datamodel import DataModel
from ..calculations.matrix import Matrix
from .soilprofile import SoilProfile
from .soil import Soil
from .soilpolygon import SoilPolygon
from ..external.dgeolib import DStabilityModel
from .crosssection import Crosssection
from .soillayer import SoilLayer
from ..helpers import (
    polyline_polyline_intersections,
    is_on_line,
    is_part_of_line,
    polyline_polygon_intersections,
    z_at,
    circle_polyline_intersections,
)
from ..settings import (
    DEFAULT_LOAD_CONSOLIDATION,
    DEFAULT_LOAD_SPREAD,
    DEFAULT_TREE_WIDTH_ROOTZONE,
    DEFAULT_TREE_DEPTH_EXCAVATION,
    MIN_GEOM_SIZE,
)

UNIT_WEIGTH_WATER = 9.81


class CharacteristicPointType(IntEnum):
    OUTSIDE_CREST = 10
    INSIDE_CREST = 12
    INSIDE_TOE = 13


class TrafficLoad(DataModel):
    left: float
    width: float
    magnitude: float
    spread: float
    consolidation: float


class Tree(DataModel):
    x: float
    height: float
    wind_force: float
    width: float
    depth: float
    spread: float


class AnalysisType(IntEnum):
    UNDEFINED = 0
    BISHOP_BRUTE_FORCE = 1
    UPLIFT_VAN_PARTICLE_SWARM = 2
    SPENCER_GENETIC = 3


class HeadLine(DataModel):
    id: str = ""
    label: str = ""
    points: List[Tuple[float, float]] = []
    is_phreatic: bool = False


class HeadReferenceLine(DataModel):
    label: str = ""
    points: List[Tuple[float, float]] = []
    head_line_id_above: str = ""
    head_line_id_below: str = ""


class Levee(DataModel):
    soilpolygons: List[SoilPolygon] = []
    soils: List[Soil] = []
    _x_outer_crest: float = None
    _x_inner_crest: float = None
    _x_inner_toe: float = None
    _x_reference_line: float = None
    _x_ditch_left: float = None
    _x_ditch_right: float = None
    _ditch_points: List[Tuple[float, float]] = []
    # _phreatic_line: List[Tuple[float, float]] = []

    _head_lines: List[HeadLine] = []
    _head_reference_lines: List[HeadReferenceLine] = []

    _traffic_load: TrafficLoad = None
    _tree: Tree = None
    _bbf: PersistableBishopBruteForceSettings = None
    _spencer: PersistableSpencerGeneticSettings = None
    _upliftvan: PersistableUpliftVanParticleSwarmSettings = None
    _matrix: Matrix = None

    class Config:
        underscore_attrs_are_private = True

    @property
    def phreatic_line(self) -> Optional[HeadLine]:
        for hl in self._head_lines:
            if hl.is_phreatic:
                return hl
        return None

    @property
    def has_phreatic_line(self) -> bool:
        return self.phreatic_line is not None

    @classmethod
    def from_stix(
        cls,
        stix_file: str,
        x_reference_line: float = None,
        scenario_index: int = 0,
        stage_index: int = 0,
        calculation_index: int = 0,
    ):
        dm = DStabilityModel.from_stix(stix_file)

        result = Levee()

        if x_reference_line is not None:
            result.set_x_reference_line(x_reference_line)

        cs = dm.get_calculation_settings(
            scenario_index=scenario_index, calculation_index=calculation_index
        )
        if cs is not None:
            if cs.AnalysisType == AnalysisTypeEnum.BISHOP_BRUTE_FORCE:
                result._bbf = cs.BishopBruteForce
            elif cs.AnalysisType == AnalysisTypeEnum.SPENCER_GENETIC:
                result._spencer = cs.SpencerGenetic
            elif cs.AnalysisType == AnalysisTypeEnum.UPLIFT_VAN_PARTICLE_SWARM:
                result._upliftvan = cs.UpliftVanParticleSwarm

        layers = dm._get_geometry(scenario_index, stage_index).Layers

        # get the soil colors based on the Id
        soilcolors = {
            sv.SoilId: sv.Color[:1] + sv.Color[3:]  # remove the alpha part
            for sv in dm.datastructure.soilvisualizations.SoilVisualizations
        }

        # if there are no colors defined set them to white
        for soil in dm.soils.Soils:
            if soil.Id not in soilcolors.keys():
                soilcolors[soil.Id] = "#000000"

        # add all the soils and get the soil codes based on the Id
        soil_codes = {}
        for soil in dm.soils.Soils:
            c = 0.0
            phi = 0.0
            if soil.MohrCoulombAdvancedShearStrengthModel.Cohesion is not None:
                c = soil.MohrCoulombAdvancedShearStrengthModel.Cohesion
            elif soil.MohrCoulombClassicShearStrengthModel.Cohesion is not None:
                c = soil.MohrCoulombClassicShearStrengthModel.Cohesion
            if soil.MohrCoulombAdvancedShearStrengthModel.FrictionAngle is not None:
                phi = soil.MohrCoulombAdvancedShearStrengthModel.FrictionAngle
            elif soil.MohrCoulombClassicShearStrengthModel.FrictionAngle is not None:
                phi = soil.MohrCoulombClassicShearStrengthModel.FrictionAngle

            result.soils.append(
                Soil(
                    code=soil.Code,
                    yd=soil.VolumetricWeightAbovePhreaticLevel,
                    ys=soil.VolumetricWeightBelowPhreaticLevel,
                    c=c,
                    phi=phi,
                    color=soilcolors[soil.Id],
                )
            )
            soil_codes[soil.Id] = soil.Code

        # get the connection between the layer Id and the soil Id
        soillayer_id_dict = {}
        for sl in dm.datastructure._get_soil_layers(
            scenario_index, stage_index
        ).SoilLayers:
            soillayer_id_dict[sl.LayerId] = sl.SoilId

        # finally create the collection of soilpolygons
        for layer in layers:
            result.soilpolygons.append(
                SoilPolygon(
                    soilcode=soil_codes[soillayer_id_dict[layer.Id]],
                    points=[(float(p.X), float(p.Z)) for p in layer.Points],
                )
            )

        # read the headline information
        wnet = dm._get_waternet(scenario_index, stage_index)
        for hl in wnet.HeadLines:
            points = [(p.X, p.Z) for p in hl.Points]
            is_phreatic = hl.Id == wnet.PhreaticLineId
            result._head_lines.append(
                HeadLine(
                    id=hl.Id,
                    label=hl.Label if hl.Label is not None else "",
                    points=points,
                    is_phreatic=is_phreatic,
                )
            )

        for rl in wnet.ReferenceLines:
            points = [(p.X, p.Z) for p in rl.Points]
            result._head_reference_lines.append(
                HeadReferenceLine(
                    label=rl.Label if rl.Label is not None else "",
                    points=points,
                    head_line_id_above=(
                        rl.TopHeadLineId if rl.TopHeadLineId is not None else ""
                    ),
                    head_line_id_below=(
                        rl.BottomHeadLineId if rl.BottomHeadLineId is not None else ""
                    ),
                )
            )

        return result

    @classmethod
    def from_soilprofiles(
        cls,
        profile_waterside: SoilProfile,
        profile_landside: SoilProfile,
        crosssection: Crosssection,
        x_landside: float,
        soils: List[Soil],
        fill_soilcode: str,
        x_reference_line: Optional[float] = None,
    ):
        result = Levee()
        if x_reference_line is not None:
            result.set_x_reference_line(x_reference_line)
        top = max(profile_landside.top, profile_waterside.top)
        top = max(top, crosssection.top)
        bottom = min(profile_landside.bottom, profile_waterside.bottom)
        bottom = min(bottom, crosssection.bottom)

        result.soils = soils

        if profile_landside.top < top:
            profile_landside.soillayers.insert(
                0,
                SoilLayer(
                    top=top,
                    bottom=profile_landside.soillayers[0].top,
                    soilcode=fill_soilcode,
                ),
            )
            profile_landside.merge()

        if profile_waterside.top < top:
            profile_waterside.soillayers.insert(
                0,
                SoilLayer(
                    top=top,
                    bottom=profile_waterside.soillayers[0].top,
                    soilcode=fill_soilcode,
                ),
            )
            profile_waterside.merge()

        profile_landside.set_bottom(bottom)
        profile_waterside.set_bottom(bottom)

        result.soilpolygons = profile_waterside.to_soilpolygons(
            left=crosssection.left, right=x_landside
        )
        result.soilpolygons += profile_landside.to_soilpolygons(
            left=x_landside, right=crosssection.right
        )

        cut_line = [p for p in crosssection.points]
        cut_line.append((cut_line[-1][0], top + 1.0))
        cut_line.append((cut_line[0][0], top + 1.0))

        result._cut(cut_line)

        return result

    @property
    def ditch_points(self) -> List[Tuple[float, float]]:
        return self._ditch_points

    @property
    def analysis_type(self) -> AnalysisType:
        if self._bbf is not None:
            return AnalysisType.BISHOP_BRUTE_FORCE
        elif self._spencer is not None:
            return AnalysisType.SPENCER_GENETIC
        elif self._upliftvan is not None:
            return AnalysisType.UPLIFT_VAN_PARTICLE_SWARM

        return AnalysisType.UNDEFINED

    @property
    def surface(self) -> List[Tuple[float, float]]:
        """Get the surface line of the geometry from left to right

        Returns:
            List[Tuple[float, float]]: The points that form the surface of the levee
        """
        boundary = self.as_one_polygon()
        boundary = [
            (round(p[0], 3), round(p[1], 3))
            for p in list(zip(*boundary.exterior.coords.xy))[:-1]
        ]
        # get the leftmost point
        left = min([p[0] for p in boundary])
        topleft_point = sorted(
            [p for p in boundary if p[0] == left], key=lambda x: x[1]
        )[-1]

        # get the rightmost points
        right = max([p[0] for p in boundary])
        rightmost_point = sorted(
            [p for p in boundary if p[0] == right], key=lambda x: x[1]
        )[-1]

        return self.get_points_along_boundary(
            start=topleft_point, end=rightmost_point, cw=True
        )

    def get_points_along_boundary(
        self, start: Tuple[float, float], end: Tuple[float, float], cw: bool = True
    ):
        pg_boundary = self.as_one_polygon()
        boundary = [
            (round(p[0], 3), round(p[1], 3))
            for p in list(zip(*pg_boundary.exterior.coords.xy))[:-1]
        ]

        # make sure boundary is cw
        if Polygon(boundary).exterior.is_ccw:
            boundary = boundary[::-1]

        # depending on the resulting direction (cw/ccw) again move the points
        if not cw:
            boundary = boundary[::-1]

        idx1 = boundary.index(start)
        idx2 = boundary.index(end) + 1
        if idx1 > idx2:
            idx2 += len(boundary)
            return (boundary + boundary)[idx1:idx2]
        else:
            return boundary[idx1:idx2]

    @property
    def bottom_surface(self) -> List[Tuple[float, float]]:
        """Get the bottom line of the geometry from left to right

        Returns:
            List[Tuple[float, float]]: The point that from the bottom of the levee
        """
        boundary = self.as_one_polygon()
        boundary = [
            (round(p[0], 3), round(p[1], 3))
            for p in list(zip(*boundary.exterior.coords.xy))[:-1]
        ]
        # get the leftmost point
        left = min([p[0] for p in boundary])
        bottomleft_point = sorted(
            [p for p in boundary if p[0] == left], key=lambda x: x[1]
        )[0]

        # get the rightmost points
        right = max([p[0] for p in boundary])
        rightmost_point = sorted(
            [p for p in boundary if p[0] == right], key=lambda x: x[1]
        )[0]

        return self.get_points_along_boundary(
            start=bottomleft_point, end=rightmost_point, cw=False
        )

    @property
    def all_points(self) -> List[Tuple[float, float]]:
        points = []
        for pg in self.soilpolygons:
            points += pg.points
        return points

    @property
    def left(self) -> float:
        return min([p[0] for p in self.all_points])

    @property
    def right(self) -> float:
        return max([p[0] for p in self.all_points])

    @property
    def top(self) -> float:
        return max([p[1] for p in self.all_points])

    @property
    def bottom(self) -> float:
        return min([p[1] for p in self.all_points])

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.top - self.bottom

    def get_soil_by_code(
        self, code: str, case_sensitive: bool = False
    ) -> Optional[Soil]:
        for soil in self.soils:
            if case_sensitive:
                if soil.code == code:
                    return soil
            else:
                if soil.code.lower() == code.lower():
                    return soil
        return None

    @property
    def has_ditch(self) -> bool:
        return len(self._ditch_points) > 0

    @property
    def has_traffic_load(self) -> bool:
        return self._traffic_load is not None

    @property
    def x_reference_line(self) -> Optional[float]:
        return self._x_reference_line

    @property
    def x_outer_crest(self) -> Optional[float]:
        return self._x_outer_crest

    @property
    def x_inner_crest(self) -> Optional[float]:
        return self._x_inner_crest

    @property
    def x_inner_toe(self) -> Optional[float]:
        return self._x_inner_toe

    @property
    def x_ditch_left(self) -> Optional[float]:
        return self._x_ditch_left

    @property
    def x_ditch_right(self) -> Optional[float]:
        return self._x_ditch_right

    @property
    def headlines(self) -> List[HeadLine]:
        return self._head_lines

    @property
    def headreferencelines(self) -> List[HeadReferenceLine]:
        return self._head_reference_lines

    def set_x_reference_line(self, x: float):
        self._x_reference_line = x

    def set_x_outer_crest(self, x: float):
        self._x_outer_crest = x

    def set_x_inner_crest(self, x: float):
        self._x_inner_crest = x

    def set_x_inner_toe(self, x: float):
        self._x_inner_toe = x

    def set_x_ditch_left(self, x: float):
        self._x_ditch_left = x

    def set_x_ditch_right(self, x: float):
        self._x_ditch_right = x

    def has_soilcode(self, soilcode: str):
        for soil in self.soils:
            if soil.code == soil:
                return True

        return False

    def as_one_polygon(self) -> Polygon:
        polygons = []
        for pg in self.soilpolygons:
            polygons.append(Polygon(pg.points))

        return orient(unary_union(polygons), sign=-1)

    def head_referenceline_by_label(self, label: str) -> Optional[HeadReferenceLine]:
        if label == "":
            raise ValueError("You have entered an empty string a seach criteria")

        for hrl in self._head_reference_lines:
            if hrl.label == label:
                return hrl
        return None

    def headline_by_id(self, id: str) -> Optional[HeadLine]:
        for hl in self._head_lines:
            if hl.id == id:
                return hl
        return None

    def add_headline(
        self,
        id: str,
        points: List[Tuple[float, float]],
        label: str = "",
        is_phreatic: bool = False,
    ) -> None:
        # remove the original phreatic line
        for i, hl in enumerate(self._head_lines):
            if hl.is_phreatic:
                self._head_lines.pop(i)

        self._head_lines.append(
            HeadLine(id=id, label=label, points=points, is_phreatic=is_phreatic)
        )

    def add_head_reference_line(
        self,
        points: List[Tuple[float, float]],
        headline_above_id: str,
        headline_below_id: str,
        label: str = "",
    ) -> None:
        if self.headline_by_id(headline_above_id) is None:
            raise ValueError(f"No headline with id '{headline_above_id}' found")
        if self.headline_by_id(headline_below_id) is None:
            raise ValueError(f"No headline with id '{headline_below_id}' found")
        self._head_reference_lines.append(
            HeadReferenceLine(
                label=label,
                points=points,
                head_line_id_above=headline_above_id,
                head_line_id_below=headline_below_id,
            )
        )

    def _cut(self, cut_line: List[Tuple[float, float]]):
        """Cut a piece defined by the given line out of the geometry

        Args:
            cut_line (List[Tuple[float, float]]): The line that defines the bottom of the part to be cut out (should increase in x coordinates)

        Raises:
            ValueError: Raises ValueError is the input or output is incorrect
        """
        # add the begin and end point to the cut line to form a polygon
        points = [p for p in cut_line]
        points.insert(0, (cut_line[0][0], self.top + 1.0))
        points.append((cut_line[-1][0], self.top + 1.0))

        pg_extract = Polygon(points)
        new_soilpolygons = []
        for spg in self.soilpolygons:
            pg = spg.to_shapely()

            pgs = pg.difference(pg_extract)

            if type(pgs) == MultiPolygon:
                geoms = pgs.geoms
            elif type(pgs) == Polygon:
                geoms = [pgs]
            else:
                raise ValueError(f"Unhandled polygon difference type '{type(pgs)}'")

            for geom in geoms:
                if geom.is_empty:
                    continue
                points = get_coordinates(geom).tolist()
                new_soilpolygons.append(
                    SoilPolygon(points=points, soilcode=spg.soilcode)
                )

        self.soilpolygons = new_soilpolygons

    def _fill(
        self,
        fill_line: List[Tuple[float, float]],
        soilcode: str,
    ):
        if polyline_polyline_intersections(self.bottom_surface, fill_line):
            raise ValueError(
                "The fill line intersects with the bottom of the geometry which will cause an invalid result"
            )

        x_start = fill_line[0][0]
        x_end = fill_line[-1][0]
        surface_points = [p for p in self.surface if p[0] >= x_start and p[0] <= x_end]
        zmin = min([p[1] for p in surface_points + fill_line]) - 1.0
        fill_line.append((x_end, zmin))
        fill_line.append((x_start, zmin))

        pg_fill = Polygon(fill_line)
        pg_current = self.as_one_polygon()

        pgs = pg_fill.difference(pg_current)
        geoms = []
        if type(pgs) == MultiPolygon:
            geoms = pgs.geoms
        elif type(pgs) == Polygon:
            geoms = [pgs]
        else:
            raise ValueError(f"Unhandled polygon difference type '{type(pgs)}'")

        for geom in geoms:
            if geom.is_empty or geom.area < MIN_GEOM_SIZE:
                continue
            points = get_coordinates(geom).tolist()
            self.soilpolygons.append(SoilPolygon(points=points, soilcode=soilcode))

    def _fix_missing_points(self):
        # check if we have points that should be on other polygons as well
        for point in self.all_points:
            for i, spg in enumerate(self.soilpolygons):
                for j, line in enumerate(spg.lines):
                    p1 = line[0]
                    p2 = line[1]
                    if is_on_line(p1, p2, point) and not is_part_of_line(p1, p2, point):
                        if j == len(spg.points) - 1:
                            self.soilpolygons[i].points.insert(0, point)
                        else:
                            self.soilpolygons[i].points.insert(j + 1, point)

    def _surface_points_between(
        self, x_start: float, x_end: float
    ) -> List[Tuple[float, float]]:
        return [p for p in self.surface if x_start < p[0] and p[0] < x_end]

    def add_phreatic_line(self, points: List[Tuple[float, float]]):
        self._head_lines.append(
            HeadLine(id="1", label="Phreatic line", points=points, is_phreatic=True)
        )

    def add_traffic_load(
        self,
        left: float,
        width: float,
        magnitude: float,
        spread: float = DEFAULT_LOAD_SPREAD,
        consolidation: float = DEFAULT_LOAD_CONSOLIDATION,
    ):
        self._traffic_load = TrafficLoad(
            left=left,
            width=width,
            magnitude=magnitude,
            spread=spread,
            consolidation=consolidation,
        )

    def add_bbf_constraints(
        self, min_slipplane_length: float = None, min_slipplane_depth: float = None
    ):
        if self._bbf is not None:
            self._bbf.SlipPlaneConstraints.IsSizeConstraintsEnabled = True
            if min_slipplane_depth is not None:
                self._bbf.SlipPlaneConstraints.MinimumSlipPlaneDepth = (
                    min_slipplane_depth
                )
            if min_slipplane_length is not None:
                self._bbf.SlipPlaneConstraints.MinimumSlipPlaneLength = (
                    min_slipplane_length
                )
        else:
            raise ValueError(
                "Trying to set constraints to the BishopBruteForce method but no BBF settings found."
            )

    def add_spencer_constraints(
        self,
        min_angle_between_slices: float = None,
        min_thrustline_percentage_inside_slices: float = None,
    ):
        if self._spencer is not None:
            self._spencer.SlipPlaneConstraints.IsEnabled = True
            if min_angle_between_slices is not None:
                self._spencer.SlipPlaneConstraints.MinimumAngleBetweenSlices = (
                    min_angle_between_slices
                )
            if min_thrustline_percentage_inside_slices is not None:
                self._spencer.SlipPlaneConstraints.MinimumThrustLinePercentageInsideSlices = (
                    min_thrustline_percentage_inside_slices
                )
        else:
            raise ValueError(
                "Trying to set constraints to the SpencerGenetic method but no SpencerGenetic settings found."
            )

    def add_uplift_van_constraints(
        self,
        min_slipplane_length: float = None,
        min_slipplane_depth: float = None,
        x_left_zone_a: float = None,
        width_zone_a: float = None,
        x_left_zone_b: float = None,
        width_zone_b: float = None,
    ):
        if min_slipplane_depth is not None:
            self._upliftvan.SlipPlaneConstraints.IsSizeConstraintsEnabled = True
            self._upliftvan.SlipPlaneConstraints.MinimumSlipPlaneDepth = (
                min_slipplane_depth
            )
        if min_slipplane_length is not None:
            self._upliftvan.SlipPlaneConstraints.IsSizeConstraintsEnabled = True
            self._upliftvan.SlipPlaneConstraints.MinimumSlipPlaneDepth = (
                min_slipplane_length
            )
        if x_left_zone_a is not None and width_zone_a is not None:
            self._upliftvan.SlipPlaneConstraints.IsZoneAConstraintsEnabled = True
            self._upliftvan.SlipPlaneConstraints.XLeftZoneA = x_left_zone_a
            self._upliftvan.SlipPlaneConstraints.WidthZoneA = width_zone_a
        if x_left_zone_b is not None and width_zone_b is not None:
            self._upliftvan.SlipPlaneConstraints.IsZoneBConstraintsEnabled = True
            self._upliftvan.SlipPlaneConstraints.XLeftZoneB = x_left_zone_b
            self._upliftvan.SlipPlaneConstraints.WidthZoneB = width_zone_b

    def fill_ditch(self, soilcode: str):
        self._fill([self._ditch_points[0], self._ditch_points[-1]], soilcode=soilcode)

    def add_ditch(
        self, x_start: float, slope: float, bottom_level: float, bottom_width: float
    ):
        # topleft point
        x1 = x_start
        z1 = self.z_at(x_start)
        # bottomleft point
        z2 = bottom_level
        x2 = x1 + (z1 - bottom_level) * slope
        # bottomright point
        x3 = x2 + bottom_width
        z3 = z2

        self._ditch_points = [(x1, z1), (x2, z2), (x3, z3)]

        slope_line = (x3, z3), (x3 + 1e3, z3 + 1e3 / slope)
        intersections = polyline_polyline_intersections(self.surface, slope_line)

        if len(intersections) > 0:
            self._ditch_points.append(intersections[0])
        else:
            self.ditch_points.append(
                (
                    self.ditch_points[-1][0]
                    + (self.top - self._ditch_points[-1][1]) * slope,
                    self.top,
                )
            )

        # limit to right side
        original_ditch_points = self._ditch_points
        self._ditch_points = [p for p in self._ditch_points if p[0] < self.right]

        if len(self._ditch_points) != 4:
            xdlp = self.right
            zdlp = z_at(xdlp, original_ditch_points)
            self.ditch_points.append((xdlp, zdlp))

        # cut out the ditch
        if len(self.ditch_points) > 1:
            self._cut(self._ditch_points)

    def z_at(self, x: float, top_only: bool = True) -> Union[float, List[float]]:
        line = [(x, self.top + 1.0), (x, self.bottom - 1.0)]

        intersections = []
        for pg in self.soilpolygons:
            intersections += polyline_polygon_intersections(line, pg.points)

        intersections = sorted([p[1] for p in list(set(intersections))])[::-1]

        if top_only:
            return intersections[0]
        else:
            return intersections

    def phreatic_level_at(self, x: float) -> Optional[float]:
        for i in range(1, len(self.phreatic_line.points)):
            x1, z1 = self.phreatic_line.points[i - 1]
            x2, z2 = self.phreatic_line.points[i]
            if x1 <= x and x <= x2:
                return z1 + (x - x1) / (x2 - x1) * (z2 - z1)

        return None

    def get_surface_intersections(
        self, points: List[Tuple[float, float]]
    ) -> List[Tuple[float, float]]:
        return polyline_polyline_intersections(points, self.surface)

    def add_tree_as_excavation(
        self,
        x: float,
        width: float = DEFAULT_TREE_WIDTH_ROOTZONE,
        depth: float = DEFAULT_TREE_DEPTH_EXCAVATION,
    ):
        x1 = x - 0.5 * width
        x2 = x + 0.5 * width
        z1 = self.z_at(x1)
        z2 = self.z_at(x2)

        exc_line = [(x1, z1), (x1, z1 - depth)]
        exc_line += [
            (p[0], p[1] - depth) for p in self.surface if p[0] > x1 and p[0] < x2
        ]
        exc_line += [(x2, z2 - depth), (x2, z2)]
        self._cut(cut_line=exc_line)

    def add_tree_as_load(
        self,
        x: float,
        height: float,
        wind_force: float,
        width: float = DEFAULT_TREE_WIDTH_ROOTZONE,
        spread: float = DEFAULT_LOAD_SPREAD,
    ):
        self._tree = Tree(
            x=x,
            height=height,
            wind_force=wind_force,
            width=width,
            depth=0.0,
            spread=spread,
        )

    def add_toplayer(
        self,
        x_start: float,
        x_end: float,
        height: float,
        soilcode: str,
    ):
        if x_end - x_start <= 0:
            raise ValueError(
                f"X start ({x_start}) cannot be greater than X end ({x_end})"
            )

        p_start = (x_start, self.z_at(x_start))
        p_end = (x_end, self.z_at(x_end))
        cut_line = [(p_start[0], p_start[1] - height)] + [
            (p[0], p[1] - height)
            for p in self.surface
            if p[0] > x_start and p[0] < x_end
        ]
        if cut_line[-1][0] != x_end:
            cut_line += [(p_end[0], p_end[1] - height)]

        fill_line = (
            [p_start]
            + [p for p in self.surface if x_start < p[0] and p[0] < x_end]
            + [p_end]
        )
        self._cut(cut_line)
        self._fill(fill_line, soilcode=soilcode)

    def to_stix(self, filename: str):
        """Generate a stix file from the input

        Args:
            filename (str): The file to save the stix to

        Raises:
            ValueError: Raises an exception if there is an error with the geometry
        """
        dm = DStabilityModel()
        default_soilcodes = [s.Code for s in dm.soils.Soils]

        # add the soils
        # and keep track of the consolidations
        consolidations_dict = {}

        soilcodes_in_layers = [spg.soilcode for spg in self.soilpolygons]
        for soil in self.soils:
            # only add soils that are used in the layers
            if not soil.code in soilcodes_in_layers:
                continue

            # TODO, should preferably overwrite the parameters with the new ones
            # for now defaulting to original parameters
            if soil.code in default_soilcodes:
                if soil.code in [
                    "P_Rk_k&s",
                    "H_Rk_k_deep",
                    "H_Rk_k_shallow",
                    "Dilatent clay",
                    "Embankment dry",
                    "H_Aa_ht_new",
                    "H_Aa_ht_old",
                    "H_Rk_ko",
                    "H_vbv_v",
                    "H_vhv_v",
                ]:
                    consolidations_dict[soil.code] = DEFAULT_LOAD_CONSOLIDATION
                elif soil.code in ["Sand", "H_Ro_z&k"]:
                    consolidations_dict[soil.code] = 100.0
                else:
                    raise ValueError(
                        f"Unknown default soilcode '{soil.code}' found, you need to assign this code to the corresponding consolidation factor."
                    )
                continue

            gl_soil = GLSoil()
            gl_soil.name = soil.code
            gl_soil.code = soil.code
            gl_soil.soil_weight_parameters.saturated_weight.mean = soil.ys
            gl_soil.soil_weight_parameters.unsaturated_weight.mean = soil.yd
            gl_soil.mohr_coulomb_parameters.cohesion.mean = soil.c
            gl_soil.mohr_coulomb_parameters.friction_angle.mean = soil.phi
            gl_soil.mohr_coulomb_parameters.dilatancy_angle = soil.phi
            gl_soil.shear_strength_model_above_phreatic_level = (
                ShearStrengthModelTypePhreaticLevel.MOHR_COULOMB
            )
            gl_soil.shear_strength_model_below_phreatic_level = (
                ShearStrengthModelTypePhreaticLevel.MOHR_COULOMB
            )
            id = dm.add_soil(gl_soil)
            if soil.c > 0.1:
                consolidations_dict[soil.code] = DEFAULT_LOAD_CONSOLIDATION
            else:
                consolidations_dict[soil.code] = 100.0

        # add the layers
        layer_consolidation_dict = {}
        layer_ids = []
        for i, spg in enumerate(self.soilpolygons):
            points = [Point(x=p[0], z=p[1]) for p in spg.points]
            try:
                layer_id = dm.add_layer(points, soil_code=spg.soilcode, label=f"L{i+1}")
            except Exception as e:
                raise ValueError(f"Error adding layer with point = {spg.points}")
            layer_ids.append(layer_id)
            layer_consolidation_dict[layer_id] = consolidations_dict[spg.soilcode]

        # add phreatic line
        # add head lines
        hl_ids = {}
        for hl in self._head_lines:
            id = dm.add_head_line(
                points=[Point(x=p[0], z=p[1]) for p in hl.points],
                label=hl.label,
                is_phreatic_line=hl.is_phreatic,
            )
            hl_ids[hl.id] = id  # dict with key = OLD id, value = NEW id

        for hrl in self._head_reference_lines:
            bottom_headline_id = (
                -1 if hrl.head_line_id_above == "" else hl_ids[hrl.head_line_id_below]
            )
            top_head_line_id = (
                -1 if hrl.head_line_id_above == "" else hl_ids[hrl.head_line_id_above]
            )

            try:

                dm.add_reference_line(
                    points=[Point(x=p[0], z=p[1]) for p in hrl.points],
                    bottom_headline_id=bottom_headline_id,
                    top_head_line_id=top_head_line_id,
                    label=hrl.label,
                )
            except Exception as e:
                raise ValueError(
                    f"Could not add reference line, this is probably due to an invalid input in the original stix file where `No headline assigned` is used, error; '{e}'"
                )

        if self.has_phreatic_line:
            dm.add_head_line(
                points=[Point(x=p[0], z=p[1]) for p in self.phreatic_line.points],
                label="PL1",
                is_phreatic_line=True,
            )

        # add the load
        if self._traffic_load is not None:
            # adjust to the consolidation degree given for the traffic load
            for k, v in layer_consolidation_dict.items():
                if v != 100.0:
                    layer_consolidation_dict[k] = self._traffic_load.consolidation
            dm.add_load(
                UniformLoad(
                    label="Traffic",
                    start=self._traffic_load.left,
                    end=self._traffic_load.left + self._traffic_load.width,
                    magnitude=self._traffic_load.magnitude,
                    angle_of_distribution=self._traffic_load.spread,
                ),
                consolidations=[
                    Consolidation(
                        degree=layer_consolidation_dict[layer_id], layer_id=layer_id
                    )
                    for layer_id in layer_ids
                ],
            )

        # if we add a tree as a load we need the layer ids for the cons degrees so this needs to
        # happen after adding the layers
        if self._tree is not None:
            z = self.z_at(self._tree.x) + self._tree.height
            dm.add_load(
                TreeLoad(
                    tree_top_location=Point(x=self._tree.x, z=z),
                    wind_force=self._tree.wind_force,
                    width_of_root_zone=self._tree.width,
                    angle_of_distribution=self._tree.spread,
                ),
                consolidations=[
                    Consolidation(
                        degree=layer_consolidation_dict[layer_id], layer_id=layer_id
                    )
                    for layer_id in layer_ids
                ],
            )

        # do we have BBF settings?
        if self._bbf is not None:
            search_grid = self._bbf.SearchGrid
            slip_plane_constraints = self._bbf.SlipPlaneConstraints
            tangent_lines = self._bbf.TangentLines

            if search_grid is not None and tangent_lines is not None:
                if slip_plane_constraints is None:
                    dm.set_model(
                        DStabilityBishopBruteForceAnalysisMethod(
                            search_grid=DStabilitySearchGrid(
                                bottom_left=Point(
                                    x=search_grid.BottomLeft.X,
                                    z=search_grid.BottomLeft.Z,
                                ),
                                number_of_points_in_x=search_grid.NumberOfPointsInX,
                                number_of_points_in_z=search_grid.NumberOfPointsInZ,
                                space=search_grid.Space,
                            ),
                            bottom_tangent_line_z=tangent_lines.BottomTangentLineZ,
                            number_of_tangent_lines=tangent_lines.NumberOfTangentLines,
                            space_tangent_lines=tangent_lines.Space,
                        )
                    )
                else:
                    dm.set_model(
                        DStabilityBishopBruteForceAnalysisMethod(
                            search_grid=DStabilitySearchGrid(
                                bottom_left=Point(
                                    x=search_grid.BottomLeft.X,
                                    z=search_grid.BottomLeft.Z,
                                ),
                                number_of_points_in_x=search_grid.NumberOfPointsInX,
                                number_of_points_in_z=search_grid.NumberOfPointsInZ,
                                space=search_grid.Space,
                            ),
                            bottom_tangent_line_z=tangent_lines.BottomTangentLineZ,
                            number_of_tangent_lines=tangent_lines.NumberOfTangentLines,
                            space_tangent_lines=tangent_lines.Space,
                            slip_plane_constraints=DStabilitySlipPlaneConstraints(
                                is_size_constraints_enabled=slip_plane_constraints.IsSizeConstraintsEnabled,
                                is_zone_a_constraints_enabled=slip_plane_constraints.IsZoneAConstraintsEnabled,
                                is_zone_b_constraints_enabled=slip_plane_constraints.IsZoneBConstraintsEnabled,
                                minimum_slip_plane_depth=slip_plane_constraints.MinimumSlipPlaneDepth,
                                minimum_slip_plane_length=slip_plane_constraints.MinimumSlipPlaneLength,
                                width_zone_a=slip_plane_constraints.WidthZoneA,
                                width_zone_b=slip_plane_constraints.WidthZoneB,
                                x_left_zone_a=slip_plane_constraints.XLeftZoneA,
                                x_left_zone_b=slip_plane_constraints.XLeftZoneB,
                            ),
                        )
                    )

        elif self._spencer is not None:
            if self._spencer.SlipPlaneConstraints is not None:
                dm.set_model(
                    DStabilitySpencerGeneticAnalysisMethod(
                        slip_plane_a=[
                            Point(x=p.X, z=p.Z) for p in self._spencer.SlipPlaneA
                        ],
                        slip_plane_b=[
                            Point(x=p.X, z=p.Z) for p in self._spencer.SlipPlaneB
                        ],
                        slip_plane_constraints=DStabilityGeneticSlipPlaneConstraints(
                            minimum_angle_between_slices=self._spencer.SlipPlaneConstraints.MinimumAngleBetweenSlices,
                            minimum_thrust_line_percentage_inside_slices=self._spencer.SlipPlaneConstraints.MinimumThrustLinePercentageInsideSlices,
                            is_enabled=self._spencer.SlipPlaneConstraints.IsEnabled,
                        ),
                    )
                )
            else:
                dm.set_model(
                    DStabilitySpencerGeneticAnalysisMethod(
                        slip_plane_a=[
                            Point(x=p.X, z=p.Z) for p in self._spencer.SlipPlaneA
                        ],
                        slip_plane_b=[
                            Point(x=p.X, z=p.Z) for p in self._spencer.SlipPlaneB
                        ],
                    )
                )
        elif self._upliftvan is not None:
            search_area_a = DStabilitySearchArea(
                height=self._upliftvan.SearchAreaA.Height,
                top_left=Point(
                    x=self._upliftvan.SearchAreaA.TopLeft.X,
                    z=self._upliftvan.SearchAreaA.TopLeft.Z,
                ),
                width=self._upliftvan.SearchAreaA.Width,
            )
            search_area_b = DStabilitySearchArea(
                height=self._upliftvan.SearchAreaB.Height,
                top_left=Point(
                    x=self._upliftvan.SearchAreaB.TopLeft.X,
                    z=self._upliftvan.SearchAreaB.TopLeft.Z,
                ),
                width=self._upliftvan.SearchAreaB.Width,
            )
            if self._upliftvan.SlipPlaneConstraints is not None:
                dm.set_model(
                    DStabilityUpliftVanParticleSwarmAnalysisMethod(
                        search_area_a=search_area_a,
                        search_area_b=search_area_b,
                        tangent_area_height=self._upliftvan.TangentArea.Height,
                        tangent_area_top_z=self._upliftvan.TangentArea.TopZ,
                        slip_plane_constraints=DStabilitySlipPlaneConstraints(
                            is_size_constraints_enabled=self._upliftvan.SlipPlaneConstraints.IsSizeConstraintsEnabled,
                            is_zone_a_constraints_enabled=self._upliftvan.SlipPlaneConstraints.IsZoneAConstraintsEnabled,
                            is_zone_b_constraints_enabled=self._upliftvan.SlipPlaneConstraints.IsZoneBConstraintsEnabled,
                            minimum_slip_plane_depth=self._upliftvan.SlipPlaneConstraints.MinimumSlipPlaneDepth,
                            minimum_slip_plane_length=self._upliftvan.SlipPlaneConstraints.MinimumSlipPlaneLength,
                            width_zone_a=self._upliftvan.SlipPlaneConstraints.WidthZoneA,
                            width_zone_b=self._upliftvan.SlipPlaneConstraints.WidthZoneB,
                            x_left_zone_a=self._upliftvan.SlipPlaneConstraints.XLeftZoneA,
                            x_left_zone_b=self._upliftvan.SlipPlaneConstraints.XLeftZoneB,
                        ),
                    )
                )
            else:
                dm.set_model(
                    DStabilityUpliftVanParticleSwarmAnalysisMethod(
                        search_area_a=search_area_a,
                        search_area_b=search_area_b,
                        tangent_area_height=self._upliftvan.TangentArea.Height,
                        tangent_area_top_z=self._upliftvan.TangentArea.TopZ,
                    )
                )

        dm.serialize(Path(filename))

    def calculate(self, calculation_name: str):
        from ..external.dstabilitycalculator import DStabilityCalculator

        dsc = DStabilityCalculator(remove_files_afterwards=False)
        dsc.add_model(levee=self, name=calculation_name)
        dsc.calculate()
        return dsc

    def get_soil_by_code(self, soilcode: str) -> Optional[Soil]:
        for s in self.soils:
            if s.code == soilcode:
                return s

        return None

    def get_soil_at(self, x: float, z: float) -> Optional[Soil]:
        for spg in self.soilpolygons:
            if spg.to_shapely().contains(SHPPoint(x, z)):
                return self.get_soil_by_code(spg.soilcode)
        return None

    def bishop(self, M: Tuple[float, float], r: float) -> float:
        if self._matrix is None:
            self._matrix = self.to_matrix()

        # intersections =

    def to_matrix(self, gridsize: float = 0.1) -> Matrix:
        # create the matrix
        left = floor(self.left / gridsize) * gridsize
        right = ceil(self.right / gridsize) * gridsize
        top = ceil(self.top / gridsize) * gridsize
        bottom = floor(self.bottom / gridsize) * gridsize
        numx = int((right - left) / gridsize)
        numz = int((top - bottom) / gridsize)
        m = Matrix(left=left, top=top, numx=numx, numz=numz, gridsize=gridsize)

        # fill with boolean if point is under the phreatic line
        for c in range(numx):
            # find the x coordinate for this column
            x = m.x_at(c)
            # find the phreatic level here
            pl = self.phreatic_level_at(x)
            # find the row index of this level
            r = m.r_at(pl)
            m.below_pl[0:r, c] = False
            m.below_pl[r : m.num_columns, c] = True

        # calculate soil stress
        for c in range(numx):
            s, u = 0.0, 0.0
            for r in range(numz):
                x = m.x_at(c)
                z = m.z_at(r)
                soil = self.get_soil_at(x, z)

                # add water pressure if we are below the phreatic line
                # also add it to the total pressure
                if m.below_pl[r, c]:
                    u += m.gridsize * UNIT_WEIGTH_WATER
                    s += m.gridsize * UNIT_WEIGTH_WATER

                # if we have a soil add the weight of the soil
                if soil is not None:
                    if m.below_pl[r, c]:
                        s += m.gridsize * (soil.ys - UNIT_WEIGTH_WATER)
                    else:
                        s += m.gridsize * soil.yd
                    m.sigma_v[r, c] = s
                    m.sigma_eff_v[r, c] = s - u
                    m.c[r, c] = soil.c
                    m.phi[r, c] = soil.phi
                else:  # we have no soil so sigma_v = 0.0
                    m.sigma_v[r, c] = 0.0
                    m.sigma_eff_v[r, c] = 0.0

                m.u[r, c] = u

        # now we can use the matrix to calculate some more variables
        m.post_process()

        return m

    def circle_intersections(self, x, z, r) -> List[Tuple[float, float]]:
        return circle_polyline_intersections(x, z, r, self.surface)
