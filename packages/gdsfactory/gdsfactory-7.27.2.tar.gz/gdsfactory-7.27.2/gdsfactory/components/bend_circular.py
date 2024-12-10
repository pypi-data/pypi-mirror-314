from __future__ import annotations

from functools import partial

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.path import arc
from gdsfactory.snap import snap_to_grid
from gdsfactory.typings import CrossSectionSpec


@gf.cell
def bend_circular(
    radius: float | None = None,
    angle: float = 90.0,
    npoints: int | None = None,
    cross_section: CrossSectionSpec = "xs_sc",
    **kwargs,
) -> Component:
    """Returns a radial arc.

    Args:
        radius: in um. Defaults to cross_section_radius.
        angle: angle of arc (degrees).
        npoints: number of points.
        layer: layer to use. Defaults to cross_section.layer.
        width: width to use. Defaults to cross_section.width.
        cross_section: spec (CrossSection, string or dict).
        kwargs: additional cross_section arguments.

    .. code::

                  o2
                  |
                 /
                /
               /
       o1_____/
    """
    x = gf.get_cross_section(cross_section, **kwargs)
    radius = radius or x.radius

    p = arc(radius=radius, angle=angle, npoints=npoints)
    c = Component()
    path = p.extrude(x)
    ref = c << path
    c.add_ports(ref.ports)
    c.absorb(ref)

    c.info["length"] = float(snap_to_grid(p.length()))
    c.info["dy"] = snap_to_grid(float(abs(p.points[0][0] - p.points[-1][0])))
    c.info["radius"] = float(radius)
    x.validate_radius(radius)

    c.add_route_info(
        cross_section=x, length=c.info["length"], n_bend_90=abs(angle / 90.0)
    )
    return c


bend_circular180 = partial(bend_circular, angle=180)


if __name__ == "__main__":
    import gdsfactory as gf

    x1 = gf.cross_section.strip(width=1)
    x2 = gf.cross_section.strip(width=2)
    x = gf.cross_section.Transition(cross_section1=x1, cross_section2=x2)

    c = bend_circular(angle=180, cross_section=x, radius=10)
    c.show(show_ports=True)
