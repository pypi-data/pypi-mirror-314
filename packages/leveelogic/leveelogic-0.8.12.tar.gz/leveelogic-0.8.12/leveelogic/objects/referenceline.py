from typing import List, Tuple
import shapefile
from shapely.geometry import shape
from pyproj import Transformer
from math import hypot
from pathlib import Path

from ..models.datamodel import DataModel


class ReferenceLine(DataModel):
    name: str = ""
    points: List[Tuple[float, float, float, float, float]] = (
        []
    )  # chainage, x, y, lat, lon

    @classmethod
    def from_shape(cls, filename: str) -> "ReferenceLine":
        # open as shapefile and get coordinates
        result = ReferenceLine(name=Path(filename).stem)
        try:

            shape = shapefile.Reader(filename)
            if len(shape.shapeRecords()) > 1:
                raise ValueError(
                    "This shapefile contains multiple geometries, cannot handle that."
                )
            dl = 0
            transformer = Transformer.from_crs(28992, 4326)
            for i, p in enumerate(shape.shapeRecords()[0].shape.points):
                if i > 0:
                    pprev = result.points[-1]
                    dl += hypot((pprev[-2] - p[0]), (pprev[-1] - p[1]))
                else:
                    pprev = p
                lat, lon = transformer.transform(p[0], p[1])
                result.points.append(
                    (
                        round(dl, 2),
                        round(lat, 6),
                        round(lon, 6),
                        round(p[0], 2),
                        round(p[1], 2),
                    )
                )
            return result
        except Exception as e:
            raise ValueError(f"Error reading shapefile; '{e}'")

    @property
    def clatlon(self) -> List[Tuple[float, float, float]]:
        return [(p[0], p[1], p[2]) for p in self.points]

    @property
    def cxy(self) -> List[Tuple[float, float, float]]:
        return [(p[0], p[3], p[4]) for p in self.points]
