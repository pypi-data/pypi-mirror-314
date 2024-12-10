from __future__ import annotations

from collections.abc import Iterable
from functools import partial

import numpy as np

import gdsfactory as gf
from gdsfactory.components.bend_euler import bend_euler
from gdsfactory.components.straight import straight as straight_function
from gdsfactory.components.taper import taper as taper_function
from gdsfactory.components.via_corner import via_corner
from gdsfactory.components.wire import wire_corner
from gdsfactory.port import Port
from gdsfactory.routing.get_bundle_from_waypoints import get_bundle_from_waypoints
from gdsfactory.routing.manhattan import _is_horizontal, _is_vertical
from gdsfactory.routing.sort_ports import sort_ports as sort_ports_function
from gdsfactory.typings import (
    STEP_DIRECTIVES,
    ComponentSpec,
    CrossSectionSpec,
    MultiCrossSectionAngleSpec,
    Route,
)


def get_bundle_from_steps(
    ports1: list[Port],
    ports2: list[Port],
    steps: Iterable[dict[str, float]] | None = None,
    bend: ComponentSpec = bend_euler,
    straight: ComponentSpec = straight_function,
    taper: ComponentSpec | None = taper_function,
    cross_section: CrossSectionSpec | MultiCrossSectionAngleSpec = "xs_sc",
    sort_ports: bool = True,
    separation: float | None = None,
    path_length_match_loops: int | None = None,
    path_length_match_extra_length: float = 0.0,
    path_length_match_modify_segment_i: int = -2,
    enforce_port_ordering: bool = True,
    auto_widen: bool = False,
    taper_length: float = 10,
    width_wide: float = 2,
    **kwargs,
) -> list[Route]:
    """Returns a list of routes formed by the given waypoints steps.

    Can add bends instead of corners and optionally tapers in straight sections.
    Tapering to wider straights reduces the optical loss and phase errors.
    `get_bundle_from_steps` is a manual version of `get_bundle`
    and a more convenient version of `get_bundle_from_waypoints`.

    Args:
        port1: start ports (list or dict).
        port2: end ports (list or dict).
        steps: that define the route (x, y, dx, dy) [{'dx': 5}, {'dy': 10}].
        bend: function that returns bends.
        straight: function that returns straight waveguides.
        taper: function that returns tapers.
        cross_section: for routes.
        sort_ports: if True sort ports.
        separation: center to center, defaults to ports1 separation.
        path_length_match_loops: number of loops to match path length.
        path_length_match_extra_length: extra length to add to the path length.
        path_length_match_modify_segment_i: modify the segment i to match path length.
        enforce_port_ordering: if True enforce port ordering.
        auto_widen: if True, auto widen the cross_section.
        taper_length: length of the taper.
        width_wide: width of the wider straight section.
        kwargs: cross_section settings.

    .. plot::
        :include-source:

        from functools import partial
        import gdsfactory as gf

        c = gf.Component("get_route_from_steps_sample")
        w = gf.components.array(
            partial(gf.components.straight, layer=(2, 0)),
            rows=3,
            columns=1,
            spacing=(0, 50),
        )

        left = c << w
        right = c << w
        right.move((200, 100))
        p1 = left.get_ports_list(orientation=0)
        p2 = right.get_ports_list(orientation=180)

        routes = gf.routing.get_bundle_from_steps(
            p1,
            p2,
            steps=[{"x": 150}],
        )

        for route in routes:
            c.add(route.references)
        c.plot()
        c.show(show_ports=True)

    """
    if isinstance(ports1, Port):
        ports1 = [ports1]

    if isinstance(ports2, Port):
        ports2 = [ports2]

    # convert ports dict to list
    if isinstance(ports1, dict):
        ports1 = list(ports1.values())

    if isinstance(ports2, dict):
        ports2 = list(ports2.values())

    if sort_ports:
        ports1, ports2 = sort_ports_function(
            ports1, ports2, enforce_port_ordering=enforce_port_ordering
        )

    waypoints = []
    steps = steps or []

    x, y = ports1[0].center
    for d in steps:
        if not STEP_DIRECTIVES.issuperset(d):
            invalid_step_directives = list(set(d.keys()) - STEP_DIRECTIVES)
            raise ValueError(
                f"Invalid step directives: {invalid_step_directives}."
                f"Valid directives are {list(STEP_DIRECTIVES)}"
            )
        x = d["x"] if "x" in d else x
        x += d.get("dx", 0)
        y = d["y"] if "y" in d else y
        y += d.get("dy", 0)
        waypoints += [(x, y)]

    port2 = ports2[0]
    x2, y2 = port2.center
    orientation = port2.orientation
    if orientation is None:
        p1 = waypoints[-2]
        p0 = waypoints[-1]
        if _is_vertical(p0, p1):
            waypoints += [(y2, y)]
        elif _is_horizontal(p0, p1):
            waypoints += [(x, x2)]
    elif int(orientation) in {0, 180}:
        waypoints += [(x, y2)]
    elif int(orientation) in {90, 270}:
        waypoints += [(x2, y)]
    waypoints = np.array(waypoints)

    if not isinstance(cross_section, list):
        kwargs.pop("end_straight_length", None)
        kwargs.pop("start_straight_length", None)
        x = gf.get_cross_section(cross_section)
        cross_section = x.copy(**kwargs)

        if auto_widen:
            taper = gf.get_component(
                taper,
                length=taper_length,
                width1=x.width,
                width2=width_wide,
                cross_section=cross_section,
            )
        else:
            taper = None
    else:
        taper = None

    return get_bundle_from_waypoints(
        ports1=ports1,
        ports2=ports2,
        waypoints=waypoints,
        bend=bend,
        straight=straight,
        taper=taper,
        cross_section=cross_section,
        separation=separation,
        path_length_match_extra_length=path_length_match_extra_length,
        path_length_match_modify_segment_i=path_length_match_modify_segment_i,
        path_length_match_loops=path_length_match_loops,
    )


get_bundle_from_steps_electrical = partial(
    get_bundle_from_steps, bend=wire_corner, cross_section="xs_metal_routing"
)

get_bundle_from_steps_electrical_multilayer = partial(
    get_bundle_from_steps,
    bend=via_corner,
    cross_section=[
        (gf.cross_section.metal2, (90, 270)),
        ("xs_metal_routing", (0, 180)),
    ],
)


def _demo() -> None:
    c = gf.Component("get_route_from_steps_sample")

    w = gf.components.array(
        partial(gf.components.straight, layer=(2, 0)),
        rows=3,
        columns=1,
        spacing=(0, 50),
    )

    left = c << w
    right = c << w
    right.move((200, 100))
    p1 = left.get_ports_list(orientation=0)
    p2 = right.get_ports_list(orientation=180)

    routes = get_bundle_from_steps_electrical(
        p1,
        p2,
        steps=[{"x": 150}],
    )

    for route in routes:
        c.add(route.references)

    c.show(show_ports=True)


if __name__ == "__main__":
    import gdsfactory as gf

    c = gf.Component("pads_bundle_steps")
    pt = c << gf.components.pad_array(
        partial(gf.components.pad, size=(30, 30)),
        orientation=270,
        columns=3,
        spacing=(50, 0),
    )
    pb = c << gf.components.pad_array(orientation=90, columns=3)
    pt.move((300, 500))

    routes = get_bundle_from_steps_electrical(
        pb.ports, pt.ports, end_straight_length=60, separation=30, steps=[{"dy": 100}]
    )

    for route in routes:
        c.add(route.references)

    c.show(show_ports=True)
