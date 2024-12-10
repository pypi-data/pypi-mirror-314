"""Bends with grating couplers inside the spiral.

maybe: need to add grating coupler loopback as well
"""

from __future__ import annotations

import numpy as np
from numpy import float64

import gdsfactory as gf
from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.bend_euler import bend_euler
from gdsfactory.routing.manhattan import round_corners
from gdsfactory.typings import ComponentSpec, CrossSectionSpec


def get_bend_port_distances(bend: Component) -> tuple[float64, float64]:
    """Returns distance between bend ports."""
    p0, p1 = bend.ports.values()
    return abs(p0.x - p1.x), abs(p0.y - p1.y)


@cell
def spiral_external_io(
    N: int = 6,
    x_inner_length_cutback: float = 300.0,
    x_inner_offset: float = 0.0,
    y_straight_inner_top: float = 0.0,
    xspacing: float = 3.0,
    yspacing: float = 3.0,
    bend: ComponentSpec = bend_euler,
    length: float | None = None,
    cross_section: CrossSectionSpec = "xs_sc",
    with_inner_ports: bool = False,
    y_straight_outer_offset: float = 0.0,
    inner_loop_spacing_offset: float = 0.0,
    mirror_straight: bool = False,
    **kwargs,
) -> Component:
    """Returns spiral with input and output ports outside the spiral.

    Args:
        N: number of loops.
        x_inner_length_cutback: x inner length.
        x_inner_offset: x inner offset.
        y_straight_inner_top: y straight inner top.
        xspacing: center to center x-spacing.
        yspacing: center to center y-spacing.
        bend: function.
        length: length in um, it is the approximates total length.
        cross_section: spec.
        with_inner_ports: if True, removes the internal S-bend and exposes new ports
        y_straight_outer_offset: amount to add/remove to the last points at the outer output of the spiral
        inner_loop_spacing_offset: extra difference between the inner ports
        mirror_straight: if True, mirrors the straight cross section in round_corners (can help when xs is asymmetric)
        kwargs: cross_section settings.
    """
    if length:
        x_inner_length_cutback = length / (4 * (N - 1))

    y_straight_inner_top += 5
    x_inner_length_cutback += x_inner_offset

    xs = gf.get_cross_section(cross_section, **kwargs)

    _bend180 = gf.get_component(bend, angle=180, cross_section=xs)
    _bend90 = gf.get_component(bend, angle=90, cross_section=xs)

    # If with_arc_floorplan is not True, the radius doesn't represent the actual size of the bend
    bend_radius = _bend90.xsize - xs.width / 2
    rx, ry = get_bend_port_distances(_bend90)
    _, rx180 = get_bend_port_distances(_bend180)  # rx180, second arg since we rotate

    component = Component()
    inner_loop_spacing = 2 * bend_radius + 5.0 + inner_loop_spacing_offset

    # Create manhattan path going from west grating to westmost port of bend 180
    x_inner_length = x_inner_length_cutback + 5.0 + xspacing

    y_inner_bend = y_straight_inner_top - bend_radius - 5.0
    x_inner_loop = x_inner_length - 5.0
    p1 = (x_inner_loop, y_inner_bend)
    p2 = (x_inner_loop + inner_loop_spacing, y_inner_bend)

    _pt = np.array(p1)
    pts_w = [_pt]

    for i in range(N):
        y1 = y_straight_inner_top + ry + (2 * i + 1) * yspacing
        x2 = inner_loop_spacing + 2 * rx + x_inner_length + (2 * i + 1) * xspacing
        y3 = -ry - (2 * i + 2) * yspacing
        y3 += 0 if i < N - 1 else y_straight_outer_offset
        x4 = -(2 * i + 1) * xspacing
        if i == N - 1:
            x4 = x4 - rx180 + xspacing

        _pt1 = np.array([_pt[0], y1])
        _pt2 = np.array([x2, _pt1[1]])
        _pt3 = np.array([_pt2[0], y3])
        _pt4 = np.array([x4, _pt3[1]])
        _pt5 = np.array([_pt4[0], 0])
        _pt = _pt5

        pts_w += [_pt1, _pt2, _pt3, _pt4, _pt5]

    pts_w = pts_w[:-2]

    # Create manhattan path going from east grating to eastmost port of bend 180
    _pt = np.array(p2)
    pts_e = [_pt]

    for i in range(N):
        y1 = y_straight_inner_top + ry + (2 * i) * yspacing
        x2 = inner_loop_spacing + 2 * rx + x_inner_length + 2 * i * xspacing
        y3 = -ry - (2 * i + 1) * yspacing
        y3 += 0 if i < N - 1 else y_straight_outer_offset
        x4 = -2 * i * xspacing

        _pt1 = np.array([_pt[0], y1])
        _pt2 = np.array([x2, _pt1[1]])
        _pt3 = np.array([_pt2[0], y3])
        _pt4 = np.array([x4, _pt3[1]])
        _pt5 = np.array([_pt4[0], 0])
        _pt = _pt5

        pts_e += [_pt1, _pt2, _pt3, _pt4, _pt5]

    pts_e = pts_e[:-2]

    # Join the two bits of paths and extrude the spiral geometry
    if not with_inner_ports:
        route = round_corners(
            pts_w[::-1] + pts_e,
            bend=bend,
            cross_section=cross_section,
            **kwargs,
        )
        component.add(route.references)
        component.add_port("o2", port=route.ports[0])
        component.add_port("o1", port=route.ports[1])

        length = route.length
    # If inner ports, do not join and layout routes separately
    else:
        pts_w[1][0] += bend_radius
        pts_e[1][0] += bend_radius
        route_west = round_corners(
            pts_w[1:],
            bend=bend,
            cross_section=cross_section,
            mirror_straight=mirror_straight,
            **kwargs,
        )
        route_east = round_corners(
            pts_e[1:],
            bend=bend,
            cross_section=cross_section,
            mirror_straight=mirror_straight,
            **kwargs,
        )
        component.add(route_west.references)
        component.add(route_east.references)
        component.add_port("o2", port=route_west.ports[0])
        component.add_port("o1", port=route_east.ports[1])
        component.add_port("o4", port=route_west.ports[1])
        component.add_port("o3", port=route_east.ports[0])
        length = route_west.length + route_east.length

    component.info["length"] = length

    return component


if __name__ == "__main__":
    spacing = 3
    c = spiral_external_io(
        # N=15,
        # xspacing=spacing,
        # yspacing=spacing,
        # with_inner_ports=True,
        # x_inner_length_cutback=0,
        # y_straight_inner_top=0,
        # x_inner_offset=0,
    )
    c.show(show_ports=True)
