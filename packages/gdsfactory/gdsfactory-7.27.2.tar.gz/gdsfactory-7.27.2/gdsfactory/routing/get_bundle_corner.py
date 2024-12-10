from __future__ import annotations

import numpy as np

from gdsfactory.component_layout import _rotate_points, pprint_ports
from gdsfactory.components.straight import straight as straight_function
from gdsfactory.port import Port
from gdsfactory.routing.get_route import get_route_from_waypoints
from gdsfactory.routing.manhattan import RouteError, generate_manhattan_waypoints
from gdsfactory.routing.path_length_matching import path_length_matched_points
from gdsfactory.routing.validation import make_error_traces, validate_connections
from gdsfactory.typings import ComponentSpec, Route


def _groups(ports, cut, axis="X"):
    if axis == "Y":
        group1 = [p for p in ports if p.x <= cut]
        group2 = [p for p in ports if p.x > cut]
    else:
        group1 = [p for p in ports if p.y <= cut]
        group2 = [p for p in ports if p.y > cut]

    return group1, group2


def _transform_port(
    point, orientation, origin=(0, 0), rotation=None, x_reflection=False
):
    new_point = np.array(point)
    new_orientation = orientation

    if x_reflection:
        new_point[1] = -new_point[1]
        new_orientation = -orientation
    if rotation is not None:
        new_point = _rotate_points(new_point, angle=rotation, center=[0, 0])
        new_orientation += rotation
    if origin is not None:
        new_point = new_point + np.array(origin)
    new_orientation = new_orientation % 360

    return new_point, new_orientation


def _transform_ports(ports, rotation, origin=(0, 0), x_reflection=False):
    ports_transformed = []
    for p in ports:
        new_port = p.copy()
        new_center, new_orientation = _transform_port(
            p.center, p.orientation, origin, rotation, x_reflection
        )
        new_port.center = new_center
        new_port.new_orientation = new_orientation
        ports_transformed.append(new_port)

    return ports_transformed


def get_bundle_corner(
    ports1: list[Port],
    ports2: list[Port],
    separation: float = 5.0,
    path_length_match_loops: int | None = None,
    path_length_match_extra_length: float = 0.0,
    path_length_match_modify_segment_i: int = -2,
    enforce_port_ordering: bool = True,
    straight: ComponentSpec = straight_function,
    auto_widen: bool = False,
    auto_widen_minimum_length: float = 100,
    taper_length: float = 10,
    width_wide: float = 2,
    **kwargs,
) -> list[Route]:
    r"""Connect banks of ports with either 90Deg or 270Deg angle between them.

    Args:
        ports1: list of start ports.
        ports2: list of end ports.
        separation: in um.
        path_length_match_loops: optional number of loops for path length matching.
        path_length_match_extra_length: extra length (um) for path length matching.
        path_length_match_modify_segment_i: segment to increase length.
        enforce_port_ordering: If True, enforce that the ports are connected in the specific order.

    Returns:
        returns a list of elements which can be added to a component.
        `[route_filter(r) for r in routes]` where routes is a list of coordinates list
        e.g with default `get_route_from_waypoints`.


    ::

        Bend-types

        90 Deg bend
                   A1 A2      AN
                   | |  ...  |
                   | |      /
                  / /      /
                 / /      /
          B1 ----/ /    _/
          B2 -----/     /
                       /
            ...      _/
          BN --------/


        270 Deg bend
            /------------\
           /              \
          /  /-------\     \
         /  /         \     \
        |  /   /--\    |    |
        | /  /   |     | ...|
        | | /    B1    B2   BN
        | | |
        | \ \--- A1
        |  ----- A2
        |    ...
         \------ AN


    """
    _p1, _p2 = ports1, ports2

    try:
        routes = _get_bundle_corner_waypoints(
            ports1,
            ports2,
            routing_func=generate_manhattan_waypoints,
            separation=separation,
            **kwargs,
        )
    except RouteError as e:
        return make_error_traces(ports1, ports2, str(e))
    if path_length_match_loops:
        routes = [np.array(route) for route in routes]
        routes = path_length_matched_points(
            routes,
            extra_length=path_length_match_extra_length,
            nb_loops=path_length_match_loops,
            modify_segment_i=path_length_match_modify_segment_i,
            **kwargs,
        )

    routes = [
        get_route_from_waypoints(
            r,
            auto_widen=auto_widen,
            auto_widen_minimum_length=auto_widen_minimum_length,
            taper_length=taper_length,
            width_wide=width_wide,
            straight=straight,
            **kwargs,
        )
        for r in routes
    ]
    if enforce_port_ordering:
        routes = validate_connections(_p1, _p2, routes)
    return routes


def _get_bundle_corner_waypoints(
    ports1,
    ports2,
    routing_func=generate_manhattan_waypoints,
    separation: float = 5.0,
    **kwargs,
):
    ports1 = ports1.copy()
    ports2 = ports2.copy()
    nb_ports = len(ports1)
    connections = []

    for p in ports1:
        p.orientation = p.orientation % 360

    for p in ports2:
        p.orientation = p.orientation % 360

    port_angles1 = {p.orientation for p in ports1}
    port_angles2 = {p.orientation for p in ports2}

    assert len(ports2) == nb_ports, f"ports1 = {len(ports1)} must match {len(ports2)}"
    assert (
        len(port_angles1) <= 1
    ), f"ports1 should have the same angle. Got {port_angles1}"
    assert (
        len(port_angles2) <= 1
    ), f"ports2 should have the same angle. Got {port_angles2}"

    a_start = ports1[0].orientation
    a_end = ports2[0].orientation

    da = a_end - a_start
    assert (da) % 180 == 90, (
        "corner_bundle can  only route port banks between orthogonal axes."
        f"Got angles of {a_start} and {a_end}"
    )

    # Rotate all ports to be in the configuration where start_angle = 0

    origin = ports1[0].center
    ports1_transformed = _transform_ports(ports1, rotation=-a_start, origin=origin)
    ports2_transformed = _transform_ports(ports2, rotation=-a_start, origin=origin)

    # a_end_tr = ports2_transformed[0].orientation % 360

    ys = [p.y for p in ports1_transformed]
    ye = [p.y for p in ports2_transformed]

    xs = [p.x for p in ports1_transformed]
    xe = [p.x for p in ports2_transformed]

    are_above = max(ys) < min(ye)
    are_below = min(ys) > max(ye)

    are_right = max(xs) < min(xe)
    are_left = min(xs) > max(xe)

    if not (are_above or are_below):
        raise ValueError(
            f"corner_bundle error: Ports must be either above or below. "
            f"{pprint_ports(ports1)}, {pprint_ports(ports2)}"
        )

    if not (are_right or are_left):
        raise ValueError(
            f"corner_bundle error: Ports must be either right or left. "
            f"{pprint_ports(ports1)}, {pprint_ports(ports2)}"
        )

    start_sort_type = ["Y", "-X", "-Y", "X"]

    da = da % 360

    if da == 270:
        da = -90

    is_routable_270 = ((are_below and are_left) or (are_above and are_right)) and (
        da == -90
    )
    is_routable_90 = ((are_below and are_right) or (are_above and are_left)) and (
        da == 90
    )
    if not (is_routable_270 or is_routable_90):
        message = (
            f"Ports not routable with corner_bundle: da={da}; are_below={are_below};"
            f"are_above={are_above}; are_left={are_left}; are_right={are_right}. "
            "Consider applying a U turn first and then to to the 90Deg or 270Deg connection"
        )
        raise RouteError(message)

    end_sort_type = ["Y", "-X", "-Y", "X"] if da > 0 else ["-Y", "X", "Y", "-X"]
    start_angle_sort_index = a_start // 90
    end_angle_sort_index = a_end // 90

    # flip sort for a few specific cases:
    if are_above and are_left and da == 90:
        start_angle_sort_index = start_angle_sort_index + 2
        start_angle_sort_index = start_angle_sort_index % 4

    if are_below and are_right and da == 90:
        end_angle_sort_index = end_angle_sort_index + 2
        end_angle_sort_index = end_angle_sort_index % 4

    start_angle_sort_type = start_sort_type[int(start_angle_sort_index)]
    end_angle_sort_type = end_sort_type[int(end_angle_sort_index)]

    type2key = {
        "X": lambda p: p.x,
        "Y": lambda p: p.y,
        "-X": lambda p: -p.x,
        "-Y": lambda p: -p.y,
    }

    # print(a_start, a_end, start_angle_sort_type, end_angle_sort_type)
    ports1.sort(key=type2key[start_angle_sort_type])
    ports2.sort(key=type2key[end_angle_sort_type])

    kwargs.pop("start_straight_length", "")
    kwargs.pop("end_straight_length", "")
    for i, (p1, p2) in enumerate(zip(ports1, ports2)):
        conn = routing_func(
            p1,
            p2,
            start_straight_length=i * separation,
            end_straight_length=i * separation,
            **kwargs,
        )
        connections += [conn]
    return connections


if __name__ == "__main__":
    import gdsfactory as gf
    from gdsfactory.routing import get_routes_bend180

    c = gf.Component("get_routes_bend180")
    pad_array = gf.components.pad_array(orientation=270)
    c1 = c << pad_array
    c2 = c << pad_array
    c2.rotate(90)
    c2.movex(1000)
    c2.ymax = -200

    routes_bend180 = get_routes_bend180(
        ports=c2.get_ports_list(),
        radius=75 / 2,
    )
    c.add(routes_bend180.references)

    routes = gf.routing.get_bundle(
        ports1=c1.get_ports_list(),
        ports2=routes_bend180.ports,
    )
    for route in routes:
        c.add(route.references)

    c.show(show_ports=True)
