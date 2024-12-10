"""Wires for electrical manhattan routes."""

from __future__ import annotations

from functools import partial

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.straight import straight
from gdsfactory.typings import CrossSectionSpec, LayerSpec

wire_straight = partial(straight, cross_section="xs_metal_routing")


@gf.cell
def wire_corner(
    cross_section: CrossSectionSpec = "xs_metal_routing",
    **kwargs,
) -> Component:
    """Returns 45 degrees electrical corner wire.

    Args:
        cross_section: spec.
        kwarg: cross_section settings.
    """
    x = gf.get_cross_section(cross_section, **kwargs)
    layer = x.layer
    width = x.width

    c = Component()
    a = width / 2
    xpts = [-a, a, a, -a]
    ypts = [-a, -a, a, a]

    c.add_polygon([xpts, ypts], layer=layer)

    c.add_port(
        name="e1",
        center=(0, 0),
        width=width,
        orientation=180,
        layer=layer,
        port_type="electrical",
        cross_section=x,
    )
    c.add_port(
        name="e2",
        center=(0, 0),
        width=width,
        orientation=90,
        layer=layer,
        port_type="electrical",
        cross_section=x,
    )

    c.info["length"] = width
    c.info["dy"] = width
    return c


@gf.cell
def wire_corner45(
    cross_section: CrossSectionSpec | None = "xs_metal_routing",
    width: float | None = None,
    layer: LayerSpec | None = None,
    radius: float = 10,
    with_corner90_ports: bool = True,
) -> Component:
    """Returns 90 degrees electrical corner wire.

    Args:
        cross_section: spec.
        width: width of the wire.
        layer: layer of the wire.
        radius: radius of the corner.
        with_corner90_ports: if True adds ports at 90 degrees.
    """
    if cross_section is None:
        if width is None or layer is None:
            raise ValueError(
                "Either cross_section or width  and layer needs to be specified"
            )

    x = gf.get_cross_section(cross_section)
    layer = layer or x.layer
    width = width if width else x.width
    radius = x.radius if radius is None else radius
    if radius is None:
        raise ValueError(
            "Radius needs to be specified in wire_corner45 or in the cross_section."
        )

    c = Component()

    a = width / 2

    xpts = [0, radius + a, radius + a, -np.sqrt(2) * width]
    ypts = [-a, radius, radius + np.sqrt(2) * width, -a]

    c.add_polygon([xpts, ypts], layer=layer)

    w = gf.snap.snap_to_grid(width * np.sqrt(2))

    if with_corner90_ports:
        c.add_port(
            name="e1",
            center=(0, 0),
            width=width,
            orientation=180,
            layer=layer,
            port_type="electrical",
        )
        c.add_port(
            name="e2",
            center=(radius, radius),
            width=width,
            orientation=90,
            layer=layer,
            port_type="electrical",
        )

    else:
        c.add_port(
            name="e1",
            center=(-w / 2, -a),
            width=w,
            orientation=270,
            layer=layer,
            port_type="electrical",
        )
        c.add_port(
            name="e2",
            center=(radius + a, radius + w / 2),
            width=w,
            orientation=0,
            layer=layer,
            port_type="electrical",
        )
    c.info["length"] = float(np.sqrt(2) * radius)
    return c


@gf.cell
def wire_corner_sections(
    cross_section: CrossSectionSpec = "xs_metal_routing",
) -> Component:
    """Returns 90 degrees electrical corner wire, where all cross_section sections properly represented.

    Works well with symmetric cross_sections, not quite ready for asymmetric.

    Args:
        cross_section: spec.
    """
    x = gf.get_cross_section(cross_section)

    xmin, ymax = x.get_xmin_xmax()

    main_section = x.sections[0]

    all_sections = [main_section]
    all_sections.extend(x.sections)

    c = Component()

    for section in all_sections:
        layer = section.layer
        width = section.width
        offset = section.offset
        b = width / 2

        xpts = [xmin, offset - b, offset - b, offset + b, offset + b, xmin]
        ypts = [
            -offset + b,
            -offset + b,
            ymax,
            ymax,
            -offset - b,
            -offset - b,
        ]

        c.add_polygon([xpts, ypts], layer=layer)

    c.add_port(
        name="e1",
        center=(xmin, -(xmin + ymax) / 2),
        orientation=180,
        cross_section=x,
        layer=x.layer,
    )
    c.add_port(
        name="e2",
        center=((xmin + ymax) / 2, ymax),
        orientation=90,
        cross_section=x,
        layer=x.layer,
    )
    c.info["length"] = ymax - xmin
    c.info["dy"] = ymax - xmin
    return c


if __name__ == "__main__":
    # c = wire_straight()

    # xsection = gf.cross_section.cross_section(
    #     width=1,
    #     offset=0,
    #     layer="MTOP",
    #     bbox_layers = ("M1", "M2"),
    #     bbox_offsets = (1, 2),
    # )

    # c = wire_corner(cross_section=xsection, with_bbox=True)
    # c.show(show_ports=True)
    # section1 = gf.cross_section.Section(width=0.4, layer="M1", offset=0.5)
    # section2 = gf.cross_section.Section(width=0.4, layer="M1", offset=-0.5)
    # xsection = gf.cross_section.cross_section(
    #     width=0.4, offset=0, layer="M1", sections=[section1, section2]
    # )

    # # c = wire_corner_sections(cross_section=metal_slotted)
    # # c.show(show_ports=True)
    # # c.pprint_ports()
    # # c.pprint()

    # metal_slotted_bbox = metal_slotted(
    #     bbox_layers=("M1", "M2"),
    #     bbox_offsets=(2, 4),
    # )

    # port1 = gf.Port(
    #     name="init",
    #     orientation=270,
    #     center=(0, 0),
    #     cross_section=gf.get_cross_section(metal_slotted),
    # )
    # port2 = gf.Port(
    #     name="final",
    #     orientation=0,
    #     center=(-100, -100),
    #     cross_section=gf.get_cross_section(metal_slotted),
    # )

    # c = gf.Component()
    # route = gf.routing.get_route_electrical(
    #     input_port=port1,
    #     output_port=port2,
    #     bend=wire_corner_sections(cross_section=metal_slotted_bbox),
    #     cross_section=metal_slotted_bbox,
    # )
    # c.add(route.references)
    c = wire_corner45(width=1)
    c.show(show_ports=True)

    # print(yaml.dump(c.to_dict()))
