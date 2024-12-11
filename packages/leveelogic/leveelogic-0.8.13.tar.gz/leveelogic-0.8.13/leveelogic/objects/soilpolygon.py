from typing import List, Tuple
from shapely.geometry import Polygon

from ..models.datamodel import DataModel
from ..helpers import is_part_of_line


class SoilPolygon(DataModel):
    soilcode: str
    points: List[Tuple[float, float]] = []

    @property
    def lines(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        result = []
        for i in range(1, len(self.points)):
            result.append((self.points[i - 1], self.points[i]))
        result.append((self.points[-1], self.points[0]))

        return result

    def to_shapely(self) -> Polygon:
        return Polygon(self.points)

    def _point_on_lines(self, p: Tuple[float, float]):
        line_indices = []
        for i, line in enumerate(self.lines):
            if line[0] == p or line[1] == p:
                line_indices.append(i)
        return line_indices
