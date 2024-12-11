from pyproj import Transformer
from typing import Tuple, List
from math import hypot
from haversine import Unit, haversine


def xy_to_latlon(x: float, y: float, epsg: int = 28992) -> Tuple[float, float]:
    """Convert coordinates from the given epsg to latitude longitude coordinate

    Arguments:
        x (float): x coordinate
        y (float): y coordinate
        epsg (int): EPSG according to https://epsg.io/, defaults to 28992 (Rijksdriehoek coordinaten)

    Returns:
         Tuple[float, float]: latitude, longitude rounded to 6 decimals
    """
    if epsg == 4326:
        return x, y

    try:
        transformer = Transformer.from_crs(epsg, 4326)
        lat, lon = transformer.transform(x, y)
    except Exception as e:
        raise e

    return (round(lat, 7), round(lon, 7))


def xys_to_latlons(
    xys: List[Tuple[float, float]], epsg: int = 28992
) -> List[Tuple[float, float]]:
    """Convert a list of coordinates from the given epsg to latitude longitude coordinates

    Arguments:
        xyx (List[Tuple[float, float]]): xy coordinates
        epsg (int): EPSG according to https://epsg.io/, defaults to 28992 (Rijksdriehoek coordinaten)

    Returns:
         List[Tuple[float, float]]: latitudes, longitudes rounded to 6 decimals
    """
    if epsg == 4326:
        return xys

    try:
        transformer = Transformer.from_crs(epsg, 4326)
        result = [transformer.transform(x, y) for x, y in xys]
    except Exception as e:
        raise e

    return [(round(p[0], 7), round(p[1], 7)) for p in result]


def latlon_to_xy(lat: float, lon: float, epsg=28992) -> Tuple[float, float]:
    """Convert latitude longitude coordinate to given epsg

    Arguments:
        lat (float): latitude
        lon (float): longitude
        epsg (int): EPSG according to https://epsg.io/, defaults to 28992 (Rijksdriehoek coordinaten)

    Returns:
         Tuple[float, float]: x, y in given epsg coordinate system
    """
    try:
        transformer = Transformer.from_crs(4326, epsg)
        x, y = transformer.transform(lat, lon)
    except Exception as e:
        raise e

    return (round(x, 2), round(y, 2))


def latlons_to_xys(
    latlons: List[Tuple[float, float]], epsg=28992
) -> List[Tuple[float, float]]:
    """Convert latitude longitude coordinates to given epsg

    Arguments:
        latlons (List[Tuple[float, float]]): list of longitude / latitude coordinates
        epsg (int): EPSG according to https://epsg.io/, defaults to 28992 (Rijksdriehoek coordinaten)

    Returns:
         List[Tuple[float, float]]: List of x, y coordinates in given epsg coordinate system
    """
    try:
        transformer = Transformer.from_crs(4326, epsg)
        xys = [transformer.transform(lat, lon) for lat, lon in latlons]
    except Exception as e:
        raise e

    return [(round(p[0], 2), round(p[1], 2)) for p in xys]


def xy_regularly_spaced(
    xy: List[Tuple[float, float]], spacing: int = 5
) -> List[Tuple[float, float, float]]:  # c, x, y
    dl = 0
    cxy = [(dl, float(xy[0][0]), float(xy[0][1]))]
    for i in range(1, len(xy)):
        dl += hypot((xy[i][0] - xy[i - 1][0]), (xy[i][1] - xy[i - 1][1]))
        cxy.append((dl, xy[i][0], xy[i][1]))

    def get_xy_at(cxy, c: float):
        for i in range(1, len(cxy)):
            c1, x1, y1 = cxy[i - 1]
            c2, x2, y2 = cxy[i]

            if c1 <= c and c <= c2:
                x = x1 + (c - c1) / (c2 - c1) * (x2 - x1)
                y = y1 + (c - c1) / (c2 - c1) * (y2 - y1)
                return (c, x, y)

    result = []
    for c in range(0, int(cxy[-1][0]) + 1, spacing):
        result.append(get_xy_at(cxy, c))

    return result


def latlons_regularly_spaced(
    latlons: List[Tuple[float, float]], spacing: int = 5
) -> List[Tuple[float, float, float]]:  # c, lat, lon
    dl = 0
    clatlons = [(dl, float(latlons[0][0]), float(latlons[0][1]))]
    for i in range(1, len(latlons)):
        dl += haversine(latlons[i - 1], latlons[i], unit=Unit.METERS)
        clatlons.append((dl, latlons[i][0], latlons[i][1]))

    def get_latlon_at(latlons, c: float):
        for i in range(1, len(latlons)):
            c1, x1, y1 = latlons[i - 1]
            c2, x2, y2 = latlons[i]

            if c1 <= c and c <= c2:
                x = x1 + (c - c1) / (c2 - c1) * (x2 - x1)
                y = y1 + (c - c1) / (c2 - c1) * (y2 - y1)
                return (c, x, y)

    result = []
    for c in range(0, int(clatlons[-1][0]) + 1, spacing):
        result.append(get_latlon_at(clatlons, c))

    return result
