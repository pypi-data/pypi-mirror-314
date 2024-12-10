from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.taper import taper as taper_function
from gdsfactory.typings import ComponentFactory, CrossSectionSpec


@gf.cell
def mmi(
    inputs: int = 1,
    outputs: int = 4,
    width: float | None = None,
    width_taper: float = 1.0,
    length_taper: float = 10.0,
    length_mmi: float = 5.5,
    width_mmi: float = 5,
    gap_input_tapers: float = 0.25,
    gap_output_tapers: float = 0.25,
    taper: ComponentFactory = taper_function,
    cross_section: CrossSectionSpec = "xs_sc",
    input_positions: list[float] | None = None,
    output_positions: list[float] | None = None,
) -> Component:
    r"""mxn MultiMode Interferometer (MMI).

    Args:
        inputs: number of inputs.
        outputs: number of outputs.
        width: input and output straight width. Defaults to cross_section.
        width_taper: interface between input straights and mmi region.
        length_taper: into the mmi region.
        length_mmi: in x direction.
        width_mmi: in y direction.
        gap_input_tapers: gap between input tapers from edge to edge.
        gap_output_tapers: gap between output tapers from edge to edge.
        taper: taper function.
        cross_section: specification (CrossSection, string or dict).
        input_positions: optional positions of the inputs.
        output_positions: optional positions of the outputs.

    .. code::

                   length_mmi
                    <------>
                    ________
                   |        |
                __/          \__
            o2  __            __  o3
                  \          /_ _ _ _
                  |         | _ _ _ _| gap_output_tapers
                __/          \__
            o1  __            __  o4
                  \          /
                   |________|
                 | |
                 <->
            length_taper
    """
    c = Component()
    gap_input_tapers = gf.snap.snap_to_grid(gap_input_tapers, grid_factor=2)
    gap_output_tapers = gf.snap.snap_to_grid(gap_output_tapers, grid_factor=2)
    w_taper = width_taper
    x = gf.get_cross_section(cross_section)
    width = width or x.width
    delta_width = width_mmi - width

    _taper = taper(
        length=length_taper,
        width1=width,
        width2=w_taper,
        cross_section=cross_section,
    )

    y = width_mmi / 2
    c.add_polygon([(0, -y), (length_mmi, -y), (length_mmi, y), (0, y)], layer=x.layer)
    for section in x.sections[1:]:
        layer = section.layer
        y = section.width / 2 + delta_width / 2
        c.add_polygon(
            [
                (-delta_width, -y),
                (length_mmi + delta_width, -y),
                (length_mmi + delta_width, y),
                (-delta_width, y),
            ],
            layer=layer,
        )

    x.add_bbox(c)
    wg_spacing_input = gap_input_tapers + width_taper
    wg_spacing_output = gap_output_tapers + width_taper

    yi = -(inputs - 1) * wg_spacing_input / 2
    yo = -(outputs - 1) * wg_spacing_output / 2

    input_positions = input_positions or [
        yi + i * wg_spacing_input for i in range(inputs)
    ]
    output_positions = output_positions or [
        yo + i * wg_spacing_output for i in range(outputs)
    ]

    ports = [
        gf.Port(
            f"in_{i}",
            orientation=180,
            center=(0, y),
            width=w_taper,
            layer=x.layer,
            cross_section=x,
        )
        for i, y in enumerate(input_positions)
    ]

    ports += [
        gf.Port(
            f"out_{i}",
            orientation=0,
            center=(+length_mmi, y),
            width=w_taper,
            layer=x.layer,
            cross_section=x,
        )
        for i, y in enumerate(output_positions)
    ]

    for port in ports:
        taper_ref = c << _taper
        taper_ref.connect(port="o2", destination=port)
        c.add_port(name=port.name, port=taper_ref.ports["o1"])
        c.absorb(taper_ref)

    c.auto_rename_ports()
    return c


if __name__ == "__main__":
    # import gdsfactory as gf
    # c = gf.components.mmi1x2(cross_section="xs_rc")
    # c = mmi(inputs=2, outputs=4, gap_input_tapers=0.5, input_positions=[-1, 1])
    # c = mmi(cross_section="xs_rc")
    c = mmi(cross_section="xs_rc_bbox")
    # print(len(c.ports))
    c.show(show_ports=True)
