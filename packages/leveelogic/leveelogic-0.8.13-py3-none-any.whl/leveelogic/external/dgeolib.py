from typing import List, Tuple, Optional, Union, Dict
from geolib.geometry import Point
from shapely import Polygon
from shapely import Point as ShapelyPoint
from shapely.ops import orient, unary_union
from math import isnan, nan
from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.internal import (
    AnalysisTypeEnum,
    PersistableSoil,
    PersistableLayer,
    PersistablePoint,
    PersistableCalculation,
    WaternetCreatorSettings,
)
from enum import IntEnum
from pathlib import Path
import subprocess
from dotenv import load_dotenv
import os
from sys import platform


from ..helpers import polyline_polyline_intersections, is_on_line
from ..settings import UNIT_WEIGHT_WATER

load_dotenv("./leveelogic.env")
DSTABILITY_MIGRATION_CONSOLE_PATH = os.getenv("DSTABILITY_MIGRATION_CONSOLE_PATH")


class CharacteristicPointEnum(IntEnum):
    NONE = 0

    EMBANKEMENT_TOE_WATER_SIDE = 10
    EMBANKEMENT_TOP_WATER_SIDE = 11
    EMBANKEMENT_TOP_LAND_SIDE = 12
    SHOULDER_BASE_LAND_SIDE = 13
    EMBANKEMENT_TOE_LAND_SIDE = 14
    DITCH_EMBANKEMENT_SIDE = 15
    DITCH_BOTTOM_EMBANKEMENT_SIDE = 16
    DITCH_BOTTOM_LAND_SIDE = 17
    DITCH_LAND_SIDE = 18


class DStabilityModel(DStabilityModel):
    @classmethod
    def from_stix(cls, stix_file: str, auto_upgrade=True) -> "DStabilityModel":
        """Generate a DStability object from a stix file

        Args:
            stix_file (str): The stix file path

        Returns:
            DStability: A DStability object
        """
        result = DStabilityModel()
        try:
            result.parse(Path(stix_file))
        except ValueError as e:
            if DSTABILITY_MIGRATION_CONSOLE_PATH is None:
                raise ValueError(
                    "The path to DSTABILITY_MIGRATION_CONSOLE_PATH is not set or incorrect in leveelogic.env or missing leveelogic.env file"
                )
            if auto_upgrade and str(e) == "Can't listdir a file":
                try:
                    subprocess.run(
                        [DSTABILITY_MIGRATION_CONSOLE_PATH, stix_file, stix_file]
                    )
                    result.parse(Path(stix_file))
                except Exception as e:
                    raise ValueError(
                        f"Could not upgrade the file, got error '{e}', maybe you are missing the geolib.env file with the DSTABILITY_MIGRATION_CONSOLE_PATH path?"
                    )
            else:
                raise e

        return result

    @property
    def layer_soil_dict(self) -> Dict:
        """Get the soils as a dictionary of the layer id

        Returns:
            Dict: A dictionary containing the layer id's as key (type str!) and the PersistibleSoil as value
        """
        result = {}
        for i in range(len(self.scenarios)):
            for j in range(len(self.scenarios[i].Stages)):
                for layer in self._get_geometry(i, j).Layers:
                    for soillayer in self._get_soil_layers(i, j).SoilLayers:
                        if layer.Id == soillayer.LayerId:
                            for soil in self.soils.Soils:
                                if soil.Id == soillayer.SoilId:
                                    result[layer.Id] = soil
        return result

    def zmax(self, scenario_index=0, stage_index=0) -> float:
        return max(
            [p[1] for p in self.get_geometry_points(scenario_index, stage_index)]
        )

    def zmin(self, scenario_index=0, stage_index=0):
        return min(
            [p[1] for p in self.get_geometry_points(scenario_index, stage_index)]
        )

    def xmax(self, scenario_index=0, stage_index=0):
        return max(
            [p[0] for p in self.get_geometry_points(scenario_index, stage_index)]
        )

    def xmin(self, scenario_index=0, stage_index=0):
        return min(
            [p[0] for p in self.get_geometry_points(scenario_index, stage_index)]
        )

    def has_ditch(self, scenario_index=0, stage_index=0) -> bool:
        return len(self.ditch_points(scenario_index, stage_index)) > 0

    def ditch_points(
        self, scenario_index=0, stage_index=0
    ) -> List[Tuple[float, float]]:
        """Get the ditch points from left (riverside) to right (landside), this will return
        the ditch embankement side, ditch embankement side bottom, land side bottom, land side
        or empty list if there are not ditch points

        Returns:
            List[Tuple[float, float]]: List of points or empty list if no ditch is found
        """

        p1 = self.get_characteristic_point(
            CharacteristicPointEnum.DITCH_EMBANKEMENT_SIDE, scenario_index, stage_index
        )
        p2 = self.get_characteristic_point(
            CharacteristicPointEnum.DITCH_BOTTOM_EMBANKEMENT_SIDE,
            scenario_index,
            stage_index,
        )
        p3 = self.get_characteristic_point(
            CharacteristicPointEnum.DITCH_BOTTOM_LAND_SIDE, scenario_index, stage_index
        )
        p4 = self.get_characteristic_point(
            CharacteristicPointEnum.DITCH_LAND_SIDE, scenario_index, stage_index
        )

        if p1 and p2 and p3 and p4:
            return [
                (p1[0], self.z_at(p1[0])),
                (p2[0], self.z_at(p2[0])),
                (p3[0], self.z_at(p3[0])),
                (p4[0], self.z_at(p4[0])),
            ]
        else:
            return []

    def get_geometry_points(self, scenario_index=0, stage_index=0):
        geometry = self._get_geometry(scenario_index, stage_index)
        points = []
        for layer in geometry.Layers:
            points += [(p.X, p.Z) for p in layer.Points]
        return points

    def surface(self, scenario_index=0, stage_index=0) -> List[Tuple[float, float]]:
        """Get the surfaceline of this geometry

        Args:
            scenario_index (int, optional): index of the scenario. Defaults to 0.
            stage_index (int, optional): index of the stage in the scenario. Defaults to 0.

        Returns:
            List[Tuple[float, float]]: The surface line as a list of x,z tuples
        """
        geometry = self._get_geometry(scenario_index, stage_index)
        points, polygons = [], []
        for layer in geometry.Layers:
            points += [(float(p.X), float(p.Z)) for p in layer.Points]
            polygons.append(Polygon([(float(p.X), float(p.Z)) for p in layer.Points]))

        boundary = orient(unary_union(polygons), sign=-1)
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

        # get the index of leftmost point
        idx_left = boundary.index(topleft_point)
        surface = boundary[idx_left:] + boundary[:idx_left]

        # get the index of the rightmost point
        idx_right = surface.index(rightmost_point)
        surface = surface[: idx_right + 1]
        return surface

    def phreatic_line(
        self, scenario_index=0, stage_index=0
    ) -> List[Tuple[float, float]]:
        wnet = self._get_waternet(self.current_scenario, self.current_stage)
        phreatic_headline_id = wnet.PhreaticLineId

        if phreatic_headline_id is None:
            return None

        for headline in wnet.HeadLines:
            if headline.Id == phreatic_headline_id:
                return [(p.X, p.Z) for p in headline.Points]

    def phreatic_level_at(
        self, x: float, scenario_index=0, stage_index=0
    ) -> Optional[float]:
        phreatic_line = self.phreatic_line()
        intersections = polyline_polyline_intersections(
            [(x, self.zmax() + 0.01), (x, self.zmin() - 0.01)], phreatic_line
        )

        if len(intersections) == 0:
            return None

        return intersections[0][1]

    def get_waternet_index(
        self, scenario_index: int = 0, stage_index=0
    ) -> Optional[int]:
        wnet_id = self._get_waternet(scenario_index, stage_index).Id
        for i, waternet in enumerate(self.waternets):
            if waternet.Id == wnet_id:
                return i
        return None

    def adjust_phreatic_line(
        self, points: List[Tuple[float, float]], scenario_index=0, stage_index=0
    ) -> None:
        wnet_idx = self.get_waternet_index(scenario_index, stage_index)
        if wnet_idx is None:
            raise ValueError(
                f"Cannot find waternet for the given scenario ({scenario_index}) and stage index ({stage_index})"
            )

        plId = self.waternets[wnet_idx].PhreaticLineId
        for i, headline in enumerate(self.waternets[wnet_idx].HeadLines):
            if headline.Id == plId:
                self.waternets[wnet_idx].HeadLines[i].Points = [
                    PersistablePoint(X=p[0], Z=p[1]) for p in points
                ]
                break

    def z_at(
        self,
        x: float,
        highest_only: bool = True,
        scenario_index: int = 0,
        stage_index: int = 0,
    ) -> Optional[Union[float, List[float]]]:
        """Get a list of z coordinates from intersections with the soillayers on coordinate x

        Args:
            x (_type_): The x coordinate
            highest_only (bool): Only return the topmost point. Defaults to True
            scenario_index (int, optional): index of the scenario. Defaults to 0.
            stage_index (int, optional): index of the stage in the scenario. Defaults to 0.

        Returns:
            List[float]: A list of intersections sorted from high to low or only the highest point if highest_only is True
        """
        intersections = self.layer_intersections_at(x)

        if len(intersections) > 0:
            if highest_only:
                return intersections[0][0]
            else:
                return sorted(
                    [i[0] for i in intersections] + [intersections[-1][1]], reverse=True
                )
        else:
            return None

    def get_analysis_type(
        self, scenario_index: int = 0, calculation_index: int = 0
    ) -> AnalysisTypeEnum:
        cs = self._get_calculation_settings(scenario_index, calculation_index)
        return cs.AnalysisType

    def layer_at(
        self, x: float, z: float, scenario_index: int = 0, stage_index: int = 0
    ) -> Optional[PersistableLayer]:
        """Get the layer at the given x,z coordinate

        Args:
            x (float): The x coordinate
            z (float): The z coordinate
            scenario_index (int, optional): index of the scenario. Defaults to 0.
            stage_index (int, optional): index of the stage. Defaults to 0.

        Returns:
            Optional[PersistableLayer]: The layer found at the location or None
        """
        geometry = self._get_geometry(scenario_index, stage_index)
        p = ShapelyPoint(x, z)
        for layer in geometry.Layers:
            pg = Polygon([(p.X, p.Z) for p in layer.Points])
            if pg.contains(p) or p.covered_by(pg):
                return layer

        return None

    def layer_intersections_at(
        self, x: float, scenario_index: int = 0, stage_index: int = 0
    ) -> List[Tuple[float, float, PersistableSoil]]:
        """Get the intersection with the layers at the given x

        Args:
            x (float): The x coordinate
            scenario_index (int, optional): index of the scenario. Defaults to 0.
            stage_index (int, optional): index of the stage in the scenario. Defaults to 0.

        Returns:
            List[Tuple[float, float, PersistableSoil]]: A list with top, bottom and soil tuples
        """
        geometry = self._get_geometry(scenario_index, stage_index)

        try:
            result = []
            line_points = [
                (x, self.zmax(scenario_index, stage_index) + 0.01),
                (x, self.zmin(scenario_index, stage_index) - 0.01),
            ]
            for layer in geometry.Layers:
                layer_points = [(p.X, p.Z) for p in layer.Points]
                for intersection in polyline_polyline_intersections(
                    line_points, layer_points
                ):
                    result.append(intersection[1])

            result = sorted(
                list(set(result)), reverse=True
            )  # sort top to bottom and remove duplicates

            # now remove the intersection with no height
            final_result = []
            for i in range(1, len(result)):
                top = result[i - 1]
                bottom = result[i]
                layer = self.layer_at(x=x, z=(top + bottom) / 2.0)
                final_result.append((top, bottom, layer.Id))

            # convert ids to soil references
            if len(final_result) > 0:
                final_result = [
                    (e[0], e[1], self.layer_soil_dict[e[2]]) for e in final_result
                ]
        except Exception as e:
            raise e

        return final_result

    def stresses_at(
        self,
        x: float,
        z: float = nan,
        include_loads: bool = False,
        scenario_index: int = 0,
        stage_index: int = 0,
    ) -> Union[
        Tuple[float, float, float, float], List[Tuple[float, float, float, float]]
    ]:
        """Generate the soilstresses at the layer intersections at coordinate x or return the stresses
        at the given z coordinate

        Args:
            x (float): The x coordinate on the geometry
            z (float, optional): If z is given only the stresses at the level are returned, defaults to nan
            include_loads (bool, optional): Include the loads. Defaults to False.
            scenario_index (int, optional): index of the scenario. Defaults to 0.
            stage_index (int, optional): index of the stage in the scenario. Defaults to 0.

        Raises:
            NotImplementedError: Include loads is not implemented yet

        Returns:
            Union[ Tuple[float, float, float, float], List[Tuple[float, float, float, float]] ]: A list of tuples representing (z, total stresses, waterpressure, effective stress) or a single tuple if z is given
        """
        result = []
        if include_loads:
            raise NotImplementedError(
                "Including loads in the stresses calculation is not added yet"
            )
        layers = self.layer_intersections_at(x)

        if len(layers) == 0:
            raise ValueError(
                f"Cannot calculate stresses at x={x} because there are not intersecions with the geometry"
            )

        phreatic_level = self.phreatic_level_at(x)

        if phreatic_level is None:
            phreatic_level = layers[-1][1] - 0.01

        stot, u = 0.0, 0.0
        if layers[0][0] < phreatic_level:
            result.append((phreatic_level, 0.0, 0.0, 0.0))
            u += (phreatic_level - layers[0][0]) * UNIT_WEIGHT_WATER
            stot = u
            result.append((layers[0][0], stot, u, 0.0))
        else:
            result.append((layers[0][0], stot, u, 0.0))

        for layer in layers:
            if layer[0] <= phreatic_level:
                stot += layer[2].VolumetricWeightBelowPhreaticLevel * (
                    layer[0] - layer[1]
                )
                u = max((phreatic_level - layer[1]) * UNIT_WEIGHT_WATER, 0.0)
                result.append((layer[1], stot, u, max(stot - u, 0)))
            elif layer[1] >= phreatic_level:
                stot += layer[2].VolumetricWeightAbovePhreaticLevel * (
                    layer[0] - layer[1]
                )
                u = max((phreatic_level - layer[1]) * UNIT_WEIGHT_WATER, 0.0)
                result.append((layer[1], stot, u, max(stot - u, 0)))
            else:
                stot += layer[2].VolumetricWeightAbovePhreaticLevel * (
                    layer[0] - phreatic_level
                )
                result.append((layer[1], stot, 0.0, max(stot - u, 0)))
                stot += layer[2].VolumetricWeightAbovePhreaticLevel * (
                    phreatic_level - layer[1]
                )
                u = max((phreatic_level - layer[1]) * UNIT_WEIGHT_WATER, 0.0)
                result.append((layer[1], stot, u, max(stot - u, 0)))

        if not isnan(z):
            if z > layers[0][0] and z < phreatic_level:
                return (z, 0.0, (phreatic_level - z) * UNIT_WEIGHT_WATER, 0.0)

            for i in range(1, len(result)):
                z1 = result[i - 1][0]  # top
                z2 = result[i][0]  # bottom
                if z2 <= z and z <= z1:
                    stot1 = result[i - 1][1]
                    stot2 = result[i][1]
                    u1 = result[i - 1][2]
                    u2 = result[i][2]
                    stot_z = stot1 + (z1 - z) / (z1 - z2) * (stot2 - stot1)
                    u_z = u1 + (z1 - z) / (z1 - z2) * (u2 - u1)
                    return (z, stot_z, u_z, max(0.0, stot_z - u_z))
            raise ValueError(
                f"The given z coordinate '{z}' is outside the geometry limits"
            )

        return result

    def _get_waternetcreator_settings(
        self, scenario_index: int, stage_index: int
    ) -> Optional[WaternetCreatorSettings]:
        wncs_id = (
            self.scenarios[scenario_index].Stages[stage_index].WaternetCreatorSettingsId
        )
        for wncs in self.datastructure.waternetcreatorsettings:
            if wncs.Id == wncs_id:
                return wncs

        return None

    def get_characteristic_point(
        self,
        characteristic_point_type: CharacteristicPointEnum,
        scenario_index: int = 0,
        stage_index: int = 0,
    ) -> Optional[Tuple[float, float]]:
        """Get the point value for the given characteristic point type

        Args:
            characteristic_point_type (CharacteristicPointEnum): Type of characteristic point
            scenario_index (int, optional): index of the scenario. Defaults to 0.
            stage_index (int, optional): index of the stage in the scenario. Defaults to 0.

        Returns:
            Optional[Tuple[float, float]]: The point or None if not found
        """

        def convert_wncs_point(x: Union[float, str]) -> Optional[float]:
            if x != "NaN":
                x = float(x)
                return x
            else:
                return None

        wncs = self._get_waternetcreator_settings(
            self.current_scenario, self.current_stage
        )
        if wncs is None:
            return None

        x = None

        if characteristic_point_type == CharacteristicPointEnum.NONE:
            return None
        elif (
            characteristic_point_type
            == CharacteristicPointEnum.EMBANKEMENT_TOE_WATER_SIDE
        ):
            x = convert_wncs_point(
                wncs.EmbankmentCharacteristics.EmbankmentToeWaterSide
            )
        elif (
            characteristic_point_type
            == CharacteristicPointEnum.EMBANKEMENT_TOP_WATER_SIDE
        ):
            x = convert_wncs_point(
                wncs.EmbankmentCharacteristics.EmbankmentTopWaterSide
            )
        elif (
            characteristic_point_type
            == CharacteristicPointEnum.EMBANKEMENT_TOP_LAND_SIDE
        ):
            x = convert_wncs_point(wncs.EmbankmentCharacteristics.EmbankmentTopLandSide)
        elif (
            characteristic_point_type == CharacteristicPointEnum.SHOULDER_BASE_LAND_SIDE
        ):
            x = convert_wncs_point(wncs.EmbankmentCharacteristics.ShoulderBaseLandSide)
        elif (
            characteristic_point_type
            == CharacteristicPointEnum.EMBANKEMENT_TOE_LAND_SIDE
        ):
            x = convert_wncs_point(wncs.EmbankmentCharacteristics.EmbankmentToeLandSide)

        elif (
            characteristic_point_type == CharacteristicPointEnum.DITCH_EMBANKEMENT_SIDE
        ):
            x = convert_wncs_point(wncs.DitchCharacteristics.DitchEmbankmentSide)
        elif (
            characteristic_point_type
            == CharacteristicPointEnum.DITCH_BOTTOM_EMBANKEMENT_SIDE
        ):
            x = convert_wncs_point(wncs.DitchCharacteristics.DitchBottomEmbankmentSide)
        elif (
            characteristic_point_type == CharacteristicPointEnum.DITCH_BOTTOM_LAND_SIDE
        ):
            x = convert_wncs_point(wncs.DitchCharacteristics.DitchBottomLandSide)
        elif characteristic_point_type == CharacteristicPointEnum.DITCH_LAND_SIDE:
            x = convert_wncs_point(wncs.DitchCharacteristics.DitchLandSide)

        if isnan(x):
            return None
        else:
            return x, self.z_at(x)

    def _add_point_to_existing_layers_if_not_exists(
        self, point: Tuple[float, float], scenario_index: int = 0, stage_index: int = 0
    ):
        geometry = self._get_geometry(scenario_index, stage_index)

        for geometry_index, g in enumerate(self.datastructure.geometries):
            if g.Id == geometry:
                break

        for layer_index, layer in enumerate(geometry.Layers):
            for i in range(1, len(layer.Points)):
                x1 = layer.Points[i - 1].X
                z1 = layer.Points[i - 1].Z
                x2 = layer.Points[i].X
                z2 = layer.Points[i].Z
                if is_on_line((x1, z1), (x2, z2), point):
                    self.datastructure.geometries[geometry_index].Layers[
                        layer_index
                    ].Points.insert(i, PersistablePoint(X=point[0], Z=point[1]))

    def add_berm(
        self,
        points: List[Tuple[float, float]],
        soilcode: str,
        label: str,
        scenario_index: int = 0,
        stage_index: int = 0,
    ) -> int:
        """Add a berm to a geometry

        Args:
            points (List[Tuple[float, float]]): The points defining the berm from left to right
            soilcode (str): The soil code to use for the berm material
            label (str): The label to use
            scenario_index (int, optional): The scenario index. Defaults to 0.
            stage_index (int, optional): The stage index in the scenario. Defaults to 0.

        Returns:
            int: The id of the added layer
        """
        xmin = points[0][0]
        xmax = points[-1][0]
        points_to_add = (
            points
            + [
                p
                for p in self.surface(scenario_index, stage_index)
                if p[0] > xmin and p[0] < xmax
            ][::-1]
        )
        # points += points_to_add[::-1]

        id = self.add_layer(
            points=[Point(x=p[0], z=p[1]) for p in points_to_add],
            soil_code=soilcode,
            label=label,
            notes="",
            scenario_index=scenario_index,
            stage_index=stage_index,
        )

        # there is still a bug in d-geolib which sometimes does not add
        # the start and end point of the berm on the surface
        # the next code checks if the begin and end point of the berm
        # are on the surface polygons
        self._add_point_to_existing_layers_if_not_exists(
            points[0], scenario_index, stage_index
        )
        self._add_point_to_existing_layers_if_not_exists(
            points[-1], scenario_index, stage_index
        )
        return id

    def get_line_surface_intersections(
        self,
        p1: Tuple[float, float],
        p2: Tuple[float, float],
        scenario_index: int = 0,
        stage_index: int = 0,
    ) -> List[Tuple[float, float]]:
        return polyline_polyline_intersections(
            [p1, p2], self.surface(scenario_index, stage_index)
        )

    def get_scenario_index_by_label(
        self, scenario_label: str, case_sensitive: bool = False
    ) -> Optional[int]:
        for i, scenario in enumerate(self.scenarios):
            label = scenario.Label

            if case_sensitive:
                if scenario_label == label:
                    return i
            else:
                if scenario_label.lower() == label.lower():
                    return i

        return None

    def get_scenario_and_stage_index_by_labels(
        self, scenario_label: str, stage_label: str, case_sensitive: bool = False
    ):
        scenario_index = self.get_scenario_index_by_label(
            scenario_label=scenario_label, case_sensitive=case_sensitive
        )

        if scenario_index is None:
            return None, None

        stage_index = None
        for i, stage in enumerate(self.scenarios[scenario_index].Stages):
            label = stage.Label

            if case_sensitive:
                if stage_label == label:
                    stage_index = i
            else:
                if stage_label.lower() == label.lower():
                    stage_index = i

        return scenario_index, stage_index

    def get_layer_by_label(
        self,
        label: str,
        scenario_index: int = 0,
        stage_index: int = 0,
        case_sensitive: bool = False,
    ) -> Optional[PersistableLayer]:
        layers = self._get_geometry(scenario_index, stage_index).Layers
        for layer in [l for l in layers if l.Label is not None]:
            if case_sensitive:
                if layer.Label == label:
                    return layer
            else:
                if layer.Label.lower() == label.lower():
                    return layer

        return None

    def get_calculation_settings(
        self, scenario_index: int = 0, calculation_index: int = 0
    ):
        calculation = self.get_calculation(scenario_index, calculation_index)
        if calculation is None:
            return None

        for cs in self.datastructure.calculationsettings:
            if cs.Id == calculation.CalculationSettingsId:
                return cs

        return None

    def get_calculation(
        self, scenario_index: int = 0, calculation_index: int = 0
    ) -> Optional[PersistableCalculation]:
        if self.datastructure.has_calculation(
            scenario_index=scenario_index, calculation_index=calculation_index
        ):
            scenario = self.scenarios[scenario_index]
            return scenario.Calculations[calculation_index]

        return None
