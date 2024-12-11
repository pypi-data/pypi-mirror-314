from typing import Optional
from ..models.datamodel import DataModel


class Soil(DataModel):
    code: str
    yd: float
    ys: float
    c: float
    phi: float
    color: str

    Cp: Optional[float] = None
    Cap: Optional[float] = None
    Cs: Optional[float] = None
    Cas: Optional[float] = None
    cv: Optional[float] = None
    pop: Optional[float] = None
    ocr: Optional[float] = None
