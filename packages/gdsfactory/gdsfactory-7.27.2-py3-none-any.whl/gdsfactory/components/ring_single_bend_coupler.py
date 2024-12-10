from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.bend_circular import bend_circular
from gdsfactory.components.bend_euler import bend_euler
from gdsfactory.components.straight import straight
from gdsfactory.typings import ComponentSpec, CrossSectionSpec


@gf.cell
def coupler_bend(
    radius: float = 10.0,
    coupler_gap: float = 0.2,
    coupling_angle_coverage: float = 120.0,
    cross_section: CrossSectionSpec = "xs_sc",
    cross_section_inner: CrossSectionSpec = "xs_sc",
    cross_section_outer: CrossSectionSpec = "xs_sc",
    bend: ComponentSpec = bend_circular,
) -> Component:
    r"""Compact curved coupler with bezier escape.

    TODO: fix for euler bends.

    Args:
        radius: um.
        gap: um.
        angle_inner: of the inner bend, from beginning to end. Depending on the bend chosen, gap may not be preserved.
        angle_outer: of the outer bend, from beginning to end. Depending on the bend chosen, gap may not be preserved.
        bend: for bend.
        cross_section: cross_section.
        cross_section_inner: spec inner bend.
        cross_section_outer: spec outer bend.

    .. code::

            r   4
            |   |
            |  / ___3
            | / /
        2____/ /
        1_____/
    """
    c = Component()

    xi = gf.get_cross_section(cross_section_inner)
    xo = gf.get_cross_section(cross_section_outer)

    angle_inner = 90
    angle_outer = coupling_angle_coverage / 2
    gap = coupler_gap

    width = xo.width / 2 + xi.width / 2
    spacing = gap + width

    bend90_inner_right = gf.get_component(
        bend, radius=radius, cross_section=cross_section_inner, angle=angle_inner
    )
    bend_outer_right = gf.get_component(
        bend,
        radius=radius + spacing,
        cross_section=cross_section_outer,
        angle=angle_outer,
    )
    bend_inner_ref = c << bend90_inner_right
    bend_outer_ref = c << bend_outer_right

    output = gf.get_component(
        bend_euler, angle=angle_outer, cross_section=cross_section
    ).mirror()

    output_ref = c << output
    output_ref.connect("o1", bend_outer_ref.ports["o2"])

    pbw = bend_inner_ref.ports["o1"]
    bend_inner_ref.movey(pbw.center[1] + spacing)

    c.absorb(bend_outer_ref)
    c.absorb(bend_inner_ref)
    c.absorb(output_ref)

    c.add_port("o1", port=bend_outer_ref.ports["o1"])
    c.add_port("o2", port=bend_inner_ref.ports["o1"])
    c.add_port("o3", port=output_ref.ports["o2"])
    c.add_port("o4", port=bend_inner_ref.ports["o2"])
    return c


@gf.cell
def coupler_ring_bend(
    radius: float = 10.0,
    coupler_gap: float = 0.2,
    coupling_angle_coverage: float = 90.0,
    length_x: float = 0.0,
    cross_section: CrossSectionSpec = "xs_sc",
    cross_section_inner: CrossSectionSpec = "xs_sc",
    cross_section_outer: CrossSectionSpec = "xs_sc",
    bend: ComponentSpec = bend_circular,
) -> Component:
    r"""Two back-to-back coupler_bend.

    Args:
        radius: um.
        gap: um.
        angle_inner: of the inner bend, from beginning to end. Depending on the bend chosen, gap may not be preserved.
        angle_outer: of the outer bend, from beginning to end. Depending on the bend chosen, gap may not be preserved.
        bend: for bend.
        length_x: horizontal straight length.
        cross_section: cross_section.
        cross_section_inner: spec inner bend.
        cross_section_outer: spec outer bend.
        kwargs:
    """
    c = Component()
    cp = coupler_bend(
        radius=radius,
        coupler_gap=coupler_gap,
        coupling_angle_coverage=coupling_angle_coverage,
        cross_section=cross_section,
        cross_section_inner=cross_section_inner,
        cross_section_outer=cross_section_outer,
        bend=bend,
    )
    sin = gf.get_component(straight, length=length_x, cross_section=cross_section_inner)
    sout = gf.get_component(
        straight, length=length_x, cross_section=cross_section_outer
    )

    coupler_right = c << cp
    coupler_left = c << cp.mirror()
    straight_inner = c << sin
    straight_inner.movex(-length_x / 2)
    straight_outer = c << sout
    straight_outer.movex(-length_x / 2)

    coupler_left.connect("o1", straight_outer.ports["o1"])
    straight_inner.connect("o1", coupler_left.ports["o2"])
    coupler_right.connect("o2", straight_inner.ports["o2"])
    straight_outer.connect("o2", coupler_right.ports["o1"])

    c.absorb(coupler_right)
    c.absorb(coupler_left)
    c.absorb(straight_inner)
    c.absorb(straight_outer)

    c.add_port("o1", port=coupler_left.ports["o3"])
    c.add_port("o2", port=coupler_left.ports["o4"])
    c.add_port("o4", port=coupler_right.ports["o3"])
    c.add_port("o3", port=coupler_right.ports["o4"])
    return c


@gf.cell
def ring_single_bend_coupler(
    radius: float = 5.0,
    gap: float = 0.2,
    coupling_angle_coverage: float = 180.0,
    bend: ComponentSpec = bend_circular,
    length_x: float = 0.6,
    length_y: float = 0.6,
    cross_section: CrossSectionSpec = "xs_sc",
    cross_section_inner: CrossSectionSpec = "xs_sc",
    cross_section_outer: CrossSectionSpec = "xs_sc",
    **kwargs,
) -> Component:
    r"""Returns ring with curved coupler.

    TODO: enable euler bends.

    Args:
        radius: um.
        gap: um.
        angle_inner: of the inner bend, from beginning to end. Depending on the bend chosen, gap may not be preserved.
        angle_outer: of the outer bend, from beginning to end. Depending on the bend chosen, gap may not be preserved.
        bend: for bend.
        length_x: horizontal straight length.
        length_y: vertical straight length.
        cross_section: cross_section.
        cross_section_inner: spec inner bend.
        cross_section_outer: spec outer bend.
        kwargs: cross_section settings.
    """
    c = Component()

    cb = c << coupler_ring_bend(
        radius=radius,
        coupler_gap=gap,
        coupling_angle_coverage=coupling_angle_coverage,
        length_x=length_x,
        cross_section=cross_section,
        cross_section_inner=cross_section_inner,
        cross_section_outer=cross_section_outer,
        bend=bend,
    )

    cross_section = cross_section_inner
    sx = gf.get_component(
        straight, length=length_x, cross_section=cross_section, **kwargs
    )
    sy = gf.get_component(
        straight, length=length_y, cross_section=cross_section, **kwargs
    )
    b = gf.get_component(bend, cross_section=cross_section, radius=radius, **kwargs)
    sl = c << sy
    sr = c << sy
    bl = c << b
    br = c << b
    st = c << sx

    sl.connect(port="o1", destination=cb.ports["o2"])
    bl.connect(port="o2", destination=sl.ports["o2"])
    st.connect(port="o2", destination=bl.ports["o1"])
    br.connect(port="o2", destination=st.ports["o1"])
    sr.connect(port="o1", destination=br.ports["o1"])
    sr.connect(port="o2", destination=cb.ports["o3"])

    c.add_port("o2", port=cb.ports["o4"])
    c.add_port("o1", port=cb.ports["o1"])
    return c


if __name__ == "__main__":
    # c = coupler_bend(radius=5)
    # c = coupler_ring_bend()
    c = ring_single_bend_coupler(
        cross_section_inner="xs_rc", cross_section_outer="xs_rc", cross_section="xs_rc"
    )
    c.assert_ports_on_grid()
    c.show(show_ports=True)
