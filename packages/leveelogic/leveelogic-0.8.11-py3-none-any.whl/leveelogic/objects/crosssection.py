from typing import List, Tuple

from ..models.datamodel import DataModel


class Crosssection(DataModel):
    points: List[Tuple[float, float]] = []

    @property
    def left(self):
        return min([p[0] for p in self.points])

    @property
    def right(self):
        return max([p[0] for p in self.points])

    @property
    def top(self):
        return max([p[1] for p in self.points])

    @property
    def bottom(self):
        return min([p[1] for p in self.points])
