from ..models.datamodel import DataModel


class SoilLayer(DataModel):
    top: float
    bottom: float
    soilcode: str

    @property
    def height(self) -> float:
        """Get the height of the soillayer

        Returns:
            float: The height of the soillayer
        """
        return self.top - self.bottom

    @property
    def mid(self) -> float:
        return (self.top + self.bottom) / 2.0
