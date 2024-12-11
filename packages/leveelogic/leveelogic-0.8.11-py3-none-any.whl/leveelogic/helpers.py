from typing import List, Tuple, Optional
from shapely.geometry import (
    LineString,
    MultiPoint,
    Point,
    GeometryCollection,
    MultiLineString,
)
from shapely import get_coordinates
import math
from pathlib import Path


def line_circle_intersections(
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    circle_center: Tuple[float, float],
    radius: float,
) -> List[Tuple[float, float]]:
    """Finds intersection points between a line segment and a circle.

    Parameters:
        p1, p2: Start and end points of the line segment.
        circle_center: Center of the circle (x, y).
        radius: Radius of the circle.

    Returns:
        A list of intersection points (x, y).
    """
    cx, cy = circle_center
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    A = dx**2 + dy**2
    B = 2 * (dx * (x1 - cx) + dy * (y1 - cy))
    C = (x1 - cx) ** 2 + (y1 - cy) ** 2 - radius**2
    det = B**2 - 4 * A * C
    if det < 0:
        return []  # No intersection

    sqrt_det = math.sqrt(det)
    t1 = (-B + sqrt_det) / (2 * A)
    t2 = (-B - sqrt_det) / (2 * A)
    points = []
    for t in [t1, t2]:
        if 0 <= t <= 1:
            # Calculate intersection point
            ix = x1 + t * dx
            iy = y1 + t * dy
            points.append((ix, iy))
    return points


def circle_polyline_intersections(
    x: float,
    z: float,
    r: float,
    polyline: List[Tuple[float, float]],
) -> List[Tuple[float, float]]:
    """Finds all intersection points between a polyline and a circle.

    Parameters:
        polyline: List of points (x, y) defining the polyline.
        circle_center: Center of the circle (x, y).
        radius: Radius of the circle.

    Returns:
        A list of intersection points (x, y).
    """
    intersections = []
    for i in range(len(polyline) - 1):
        p1, p2 = polyline[i], polyline[i + 1]
        intersections.extend(line_circle_intersections(p1, p2, (x, z), r))
    return intersections


def case_insensitive_glob(filepath: str, fileextension: str) -> List[Path]:
    """Find files in given path with given file extension (case insensitive)

    Arguments:
        filepath (str): path to files
        fileextension (str): file extension to use as a filter (example .gef or .csv)

    Returns:
        List(str): list of files
    """
    p = Path(filepath)
    result = []
    for filename in p.glob("**/*"):
        if str(filename.suffix).lower() == fileextension.lower():
            result.append(filename.absolute())
    return result


def polyline_polygon_intersections(
    points_line: List[Tuple[float, float]],
    points_polygon: List[Tuple[float, float]],
) -> List[Tuple[float, float]]:
    if points_polygon[-1] != points_polygon[0]:
        points_polygon.append(points_polygon[0])
    return polyline_polyline_intersections(points_line, points_polygon)


def polyline_polyline_intersections(
    points_line1: List[Tuple[float, float]],
    points_line2: List[Tuple[float, float]],
) -> List[Tuple[float, float]]:
    result = []

    ls1 = LineString(points_line1)
    ls2 = LineString(points_line2)
    intersections = ls1.intersection(ls2)

    if intersections.is_empty:
        return []
    elif type(intersections) == MultiPoint:
        result = [(g.x, g.y) for g in intersections.geoms]
    elif type(intersections) == Point:
        x, y = intersections.coords.xy
        result = [(x[0], y[0])]
    elif type(intersections) == LineString:
        result += [(p[0], p[1]) for p in get_coordinates(intersections).tolist()]
    elif type(intersections) == GeometryCollection:
        geoms = [g for g in intersections.geoms if type(g) != Point]
        result += [(p[0], p[1]) for p in get_coordinates(geoms).tolist()]
        for p in [g for g in intersections.geoms if type(g) == Point]:
            x, y = p.coords.xy
            result.append((x[0], y[0]))
    elif type(intersections) == MultiLineString:
        geoms = [g for g in intersections.geoms if type(g) != Point]
        if len(geoms) >= 2:
            x1, z1 = geoms[0].coords.xy
            x2, z2 = geoms[1].coords.xy

            if x1 == x2:  # vertical
                x = x1.tolist()[0]
                zs = z1.tolist() + z2.tolist()
                result.append((x, min(zs)))
                result.append((x, max(zs)))
            elif z1 == z2:  # horizontal
                z = z1.tolist()[0]
                xs = x1.tolist() + x2.tolist()
                result.append((min(xs), z))
                result.append((max(xs), z))
            else:
                raise ValueError(
                    f"Unimplemented intersection type '{type(intersections)}' that is not a horizontal or vertical line or consists of more than 2 lines"
                )
        else:
            raise ValueError(
                f"Unimplemented intersection type '{type(intersections)}' with varying x or z coordinates"
            )
    else:
        raise ValueError(
            f"Unimplemented intersection type '{type(intersections)}' {points_line1}"
        )

    # do not include points that are on line1 or line2
    # final_result = [float(p) for p in result if not p in points_line1 or p in points_line2]

    # if len(final_result) == 0:
    #    return []

    return sorted(result, key=lambda x: x[0])


def is_on_line(point_a, point_b, point_c, tolerance=1e-6):
    """
    This function checks if point_c lies on the line formed by point_a and point_b,
    considering a tolerance for floating-point errors and handling vertical lines.

    Args:
    point_a: A tuple of two floats (x, y) representing coordinates.
    point_b: A tuple of two floats (x, y) representing coordinates.
    point_c: A tuple of two floats (x, y) representing coordinates.
    tolerance: A small value to account for floating-point errors (default: 1e-6).

    Returns:
    True if point_c is on the line within the tolerance, False otherwise.
    """
    # Check for collinearity (all three points are aligned)
    if point_c[0] <= min(point_a[0], point_b[0]):
        return False
    if point_c[0] >= max(point_a[0], point_b[0]):
        return False
    if point_c[1] <= min(point_a[1], point_b[1]):
        return False
    if point_c[1] >= max(point_a[1], point_b[1]):
        return False

    if point_a[0] == point_b[0] and point_a[0] == point_c[0]:
        return True
    if point_a[1] == point_b[1] and point_a[1] == point_c[1]:
        return True

    # Handle the case of a vertical line (where x-coordinates of A and B are the same)
    if abs(point_a[0] - point_b[0]) <= tolerance:
        return abs(point_c[0] - point_a[0]) <= tolerance
    else:
        # Calculate the slope and check if C's y-coordinate is within tolerance of the line equation
        slope = (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])
        return (
            abs(point_c[1] - (slope * (point_c[0] - point_a[0]) + point_a[1]))
            <= tolerance
        )


def is_part_of_line(point_a, point_b, point_c, tolerance=1e-6) -> bool:
    """Check if point c is either a or b

    Args:
        point_a (_type_): A tuple of two floats (x, y) representing coordinates
        point_b (_type_): A tuple of two floats (x, y) representing coordinates
        point_c (_type_): A tuple of two floats (x, y) representing coordinates
        tolerance (_type_, optional): A small value to account for floating-point errors. Defaults to 1e-6.

    Returns:
        bool: True is point c is point a or point b (within the given tolerance)
    """
    dLA = math.hypot(point_a[0] - point_c[0], point_a[1] - point_c[1])
    dLB = math.hypot(point_b[0] - point_c[0], point_b[1] - point_c[1])
    return dLA <= tolerance or dLB <= tolerance


def z_at(x: float, line: List[Tuple[float, float]]) -> Optional[float]:
    for i in range(1, len(line)):
        x1, z1 = line[i - 1]
        x2, z2 = line[i]

        if x1 <= x and x <= x2:
            return z1 + (x - x1) / (x2 - x1) * (z2 - z1)

    return None


def distance_to_line(
    point: Tuple[float, float], line_points: List[Tuple[float, float]]
):
    """Calculates the shortest distance from a point to a line defined by a list of points.

    Args:
        point: A tuple representing the x,y coordinates of the point.
        line_points: A list of tuples representing the x,y coordinates of the points on the line.

    Returns:
        The shortest distance from the point to the line.
    """

    if len(line_points) < 2:
        raise ValueError("Line must have at least two points.")

    # Extract the first two points from the line for calculations
    p1, p2 = line_points[:2]

    # Calculate the vector representing the line
    line_vector = (p2[0] - p1[0], p2[1] - p1[1])

    # Calculate the vector from the first point on the line to the given point
    point_vector = (point[0] - p1[0], point[1] - p1[1])

    # Calculate the projection of the point vector onto the line vector
    projection = (
        point_vector[0] * line_vector[0] + point_vector[1] * line_vector[1]
    ) / (line_vector[0] ** 2 + line_vector[1] ** 2)

    # Calculate the perpendicular distance from the point to the line
    distance = math.sqrt(
        (point_vector[0] - projection * line_vector[0]) ** 2
        + (point_vector[1] - projection * line_vector[1]) ** 2
    )

    return distance
