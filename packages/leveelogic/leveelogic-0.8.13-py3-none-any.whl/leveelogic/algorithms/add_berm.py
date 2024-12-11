from ..objects.levee import Levee
from ..objects.soil import Soil
from ..objects.soilpolygon import SoilPolygon
from copy import deepcopy
from ..helpers import polyline_polyline_intersections, z_at


def add_berm_method_xz_slopes(
    levee: Levee,
    x: float,
    z: float,
    slope_top: float,
    slope_side: float,
    soil: Soil,
    x_inner_crest: float = None,
    x_inner_toe: float = None,
    add_ditch: bool = False,
    ditch_offset: float = 0.0,
    ditch_slope: float = 2.0,
    ditch_bottom_level: float = 0.0,
    ditch_bottom_width: float = 1.0,
) -> Levee:
    """Generate a berm based on a fixed point that defines the location where the slope changes from
    top slope to side slope with a possibility to add a ditch with given geometrical parameters

    Args:
        levee (Levee): The levee to add the berm to
        x (float): the x coordinate of the topright berm point
        z (float): the z coordinate of the topright berm point
        slope_top (float): the slope on top of the berm
        slope_side (float): the slope on the side of the berm
        soil (Soil): the soil to use for the berm
        x_inner_crest (float, optional): the x coordinate of the inner crest point. Defaults to None.
        x_inner_toe (float, optional): the x coordinate of the inner toe point. Defaults to None.
        add_ditch (bool, optional): flag to add an optional ditch. Defaults to False.
        ditch_offset (float, optional): the offset between the end of the berm and the ditch. Defaults to 0.0.
        ditch_slope (float, optional): the slope for the sides of the ditch. Defaults to 2.0.
        ditch_bottom_level (float, optional): the bottom level of the ditch. Defaults to 0.0.
        ditch_bottom_width (float, optional): the width of the bottom of the ditch. Defaults to 1.0.

    Raises:
        ValueError: Raises an error if invalid geometries are encountered


    Returns:
        Levee: A levee with the berm and optional ditch
    """
    result = deepcopy(levee)

    if x_inner_crest is None and result.x_inner_crest is None:
        raise ValueError(
            "We need the location of the inner crest x coordinates to generate a valid berm"
        )

    if x_inner_toe is None and result.x_inner_toe is None:
        raise ValueError(
            "We need the location of the inner toe x coordinates to generate a valid berm"
        )

    if x_inner_crest is not None and result.x_inner_crest is None:
        result.set_x_inner_crest(x_inner_crest)
    if x_inner_toe is not None and result.x_inner_toe is None:
        result.set_x_inner_toe(x_inner_toe)

    # if soil is new add it to the soils
    if not result.has_soilcode(soil.code):
        result.soils.append(soil)

    # line from x,z to the left
    p1 = (result.left, z + (x - result.left) / slope_top)
    p2 = (x, z)
    line_left = [p1, p2]

    # line from x,z to right
    p3 = (result.right, z - (result.right - x) / slope_side)
    line_right = [p2, p3]

    intersections_right = polyline_polyline_intersections(line_right, result.surface)
    if len(intersections_right) == 0:
        raise ValueError(
            "No intersections between the topright point of the berm and the surface, can not create a berm"
        )

    slope_points_top = [(result.left, z + (x - result.left) / slope_top), (x, z)]
    slope_line_side = [(x, z), (result.right, z - (result.right - x) / slope_side)]

    intersections_top = polyline_polyline_intersections(
        slope_points_top, result.surface
    )
    # only select those between the inner crest and inner toe line
    intersections_top = [
        p for p in intersections_top if x_inner_crest <= p[0] and p[0] <= x_inner_toe
    ]
    if len(intersections_top) == 0:
        raise ValueError(
            "No intersection with the surface found for the top line of the berm and the line between the inner crest and inner toe"
        )

    intersections_side = polyline_polyline_intersections(
        slope_line_side, result.surface
    )
    if len(intersections_side) == 0:
        raise ValueError(
            "No intersections with the surface found for the side line of the berm, check the slope and start point"
        )

    pA = intersections_top[0]
    pB = (x, z)
    pC = intersections_side[-1]

    intersections = polyline_polyline_intersections([pA, pB, pC], result.surface)
    # if we have an uneven number of intersections (but more than 1) remove the last one
    if len(intersections) < 2:
        raise ValueError(
            "No intersections with the surface found for the berm, check the slope and start point"
        )

    if len(intersections) % 2 != 0:
        intersections = intersections[:-1]

    for i in range(0, len(intersections), 2):
        # get the left and right point of the berm
        p1 = intersections[i]
        p2 = intersections[i + 1]

        # check if we need to add the knikpunt of the berm
        if p1[0] < pB[0] and pB[0] < p2[0]:
            points = [p1, pB, p2]
        else:
            points = [p1, p2]

        # now follow the surface back to p1
        points += result._surface_points_between(p1[0], p2[0])[::-1]

        result.soilpolygons.append(SoilPolygon(soilcode=soil.code, points=points))

    # replace ditch next to berm
    if add_ditch:
        result.add_ditch(
            x_start=pC[0] + ditch_offset,
            slope=ditch_slope,
            bottom_level=ditch_bottom_level,
            bottom_width=ditch_bottom_width,
        )

    result._fix_missing_points()

    return result
