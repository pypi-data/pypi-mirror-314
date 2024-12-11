from ..objects.levee import Levee
from copy import deepcopy
from ..helpers import polyline_polyline_intersections, z_at


def add_phreatic_level_method_offset(
    levee: Levee,
    river_level: float,
    polder_level: float,
    offset_a: float = 0.0,
    offset_b: float = 0.0,
    offset_surface: float = 0.1,
    x_outer_crest: float = None,
    x_inner_crest: float = None,
    x_inner_toe: float = None,
    x_ditch_left: float = None,
    x_ditch_right: float = None,
) -> Levee:
    """Generate a phreaticline based on crest points and offsets

    Args:
        levee (Levee): The levee to use as the base
        river_level (float): The river level
        polder_level (float): The polder level
        offset_a (float, optional): The offset from the river level at the outer crest point. Defaults to 0.0.
        offset_b (float, optional): The offset from the river level at the inner crest point. Defaults to 0.0.
        offset_surface (float, optional): The offset from the surface (will never exceed the surface level of the levee). Defaults to 0.1.
        x_outer_crest (float, optional): The x coordinate of the outer crest point. Defaults to None.
        x_inner_crest (float, optional): The x coordinate of the inner crest point. Defaults to None.
        x_inner_toe (float, optional): The x coordinate of the inner toe point. Defaults to None.
        x_ditch_left (float, optional): The leftmost point of the ditch. Defaults to None.
        x_ditch_right (float, optional): The rightmost point of the ditch. Defaults to None.

    Raises:
        ValueError: if points are not assigned but need to be assigned

    Returns:
        Levee: A copy of the given Levee with the new phreatic line
    """
    # create a copy of the input
    result = deepcopy(levee)

    # input checking
    if x_outer_crest is None and levee.x_outer_crest is None:
        raise ValueError(
            "We need the x coordinate of the outer crest point but none is given"
        )

    if x_inner_crest is None and levee.x_inner_crest is None:
        raise ValueError(
            "We need the x coordinate of the inner crest point but none is given"
        )

    if x_inner_toe is None and levee.x_inner_toe is None:
        raise ValueError(
            "We need the x coordinate of the inner toe point but none is given"
        )

    # check if we have ditch coordinates if they are not given as function arguments
    if x_ditch_left is None and levee.x_ditch_left is not None:
        x_ditch_left = levee.x_ditch_left

    if x_ditch_right is None and levee.x_ditch_right is not None:
        x_ditch_right = levee.x_ditch_right

    # left most point has river level
    p1 = (levee.left, river_level)
    # find the first intersection with the surface left of x_outer_crest
    intersections = polyline_polyline_intersections(
        [p1, (levee.right, river_level)], levee.surface
    )
    if len(intersections) == 0:
        raise ValueError(
            f"No ntersections with the surface found at riverlevel {river_level:.2f}"
        )
    intersections = [p for p in intersections if p[0] < x_outer_crest]
    if len(intersections) == 0:
        raise ValueError(
            f"No ntersections with the surface left of the outer crest point ({x_outer_crest}) found at riverlevel {river_level:.2f}"
        )
    p2 = intersections[-1]
    # point at outer crest at given offset from river level
    p3 = (x_outer_crest, river_level + offset_a)
    # point at inner crest at given offset from river level
    p4 = (x_inner_crest, river_level + offset_b)
    # point at inner toe at polder level
    p5 = (x_inner_toe, polder_level)
    # point at the right side of the geometry
    p6 = (levee.right, polder_level)

    # now adjust for the surface offset (only for points right of x_outer_crest)
    # also make sure previous points are always higher than later points (from p4)
    pl_points = [[p[0], p[1]] for p in [p1, p2, p3, p4, p5, p6]]

    # get surface points
    xs_surface = [p[0] for p in levee.surface if p[0] > x_outer_crest]
    xs_surface += [x_outer_crest, x_inner_crest, x_inner_toe]
    xs_surface = sorted(xs_surface)

    # create the final pl line
    final_pl_points = [p1, p2]
    for x in xs_surface:
        z_pl = None
        if x_ditch_right is not None and x_ditch_right is not None:
            if x_ditch_left <= x and x <= x_ditch_right:
                z_pl = polder_level

        if z_pl is None:
            z_pl = z_at(x, pl_points)
            z_surface = z_at(x, levee.surface)
            if z_pl > z_surface:
                z_pl = z_surface - offset_surface
        final_pl_points.append((x, z_pl))

    result.add_phreatic_line(final_pl_points)
    return result
