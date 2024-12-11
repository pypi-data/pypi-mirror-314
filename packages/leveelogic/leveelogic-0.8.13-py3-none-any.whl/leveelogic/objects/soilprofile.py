from typing import List, Optional, Tuple


from ..models.datamodel import DataModel
from .soillayer import SoilLayer
from .soilpolygon import SoilPolygon
from .soilcollection import SoilCollection
from ..settings import UNIT_WEIGHT_WATER
from .stresses import Stresses


class SoilProfile(DataModel):
    soillayers: List[SoilLayer] = []

    @property
    def top(self):
        return self.soillayers[0].top

    @property
    def bottom(self):
        return self.soillayers[-1].bottom

    def merge(self):
        """Merge the soillayers if two or more consecutive soillayers are of the same type"""
        result = []
        for i in range(len(self.soillayers)):
            if i == 0:
                result.append(self.soillayers[i])
            else:
                if self.soillayers[i].soilcode == result[-1].soilcode:
                    result[-1].bottom = self.soillayers[i].bottom
                else:
                    result.append(self.soillayers[i])
        self.soillayers = result

    def to_soilpolygons(self, left: float, right: float) -> List[SoilPolygon]:
        result = []
        for layer in self.soillayers:
            result.append(
                SoilPolygon(
                    points=[
                        (left, layer.top),
                        (right, layer.top),
                        (right, layer.bottom),
                        (left, layer.bottom),
                    ],
                    soilcode=layer.soilcode,
                )
            )
        return result

    def set_top(self, top: float):
        self.soillayers[0].top = top

    def set_bottom(self, bottom: float):
        self.soillayers[-1].bottom = bottom

    def stresses(
        self,
        soil_collection: SoilCollection,
        phreatic_level: float,
        load: float = 0.0,
    ) -> Stresses:  # z, s_tot, u, s_eff
        result = Stresses()

        s_tot = load
        u = 0.0

        if self.top < phreatic_level:
            result.add(z=phreatic_level, s_tot=s_tot, u=0.0)
            u += (phreatic_level - self.top) * UNIT_WEIGHT_WATER

        result.add(z=self.top, s_tot=s_tot + u, u=u)

        for layer in self.soillayers:
            soil = soil_collection.get(layer.soilcode)
            if layer.top <= phreatic_level:
                u += layer.height * UNIT_WEIGHT_WATER
                s_tot += layer.height * soil.ys
                result.add(z=layer.bottom, s_tot=s_tot, u=u)
            elif layer.bottom >= phreatic_level:
                s_tot += layer.height * soil.yd
                result.add(z=layer.bottom, s_tot=s_tot, u=0.0)
            else:
                s_tot += (layer.top - phreatic_level) * soil.yd
                result.add(z=phreatic_level, s_tot=s_tot, u=0.0)
                s_tot += (phreatic_level - layer.bottom) * soil.ys
                u += (phreatic_level - layer.bottom) * UNIT_WEIGHT_WATER
                result.add(z=layer.bottom, s_tot=s_tot, u=u)

        return result

    def settlement(
        self,
        load: Optional[float] = None,
        spread: Optional[float] = None,
        phreatic_level: Optional[float] = None,
        new_phreatic_level: Optional[float] = None,
    ) -> List[Tuple[float, float]]:
        pass
