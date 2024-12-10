from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.taper_cross_section import taper_cross_section
from gdsfactory.cross_section import strip
from gdsfactory.typings import CrossSectionSpec, LayerSpecs


@gf.cell
def terminator(
    length: float | None = 50,
    cross_section_input: CrossSectionSpec = strip,
    cross_section_tip: CrossSectionSpec | None = None,
    tapered_width: float = 0.2,
    doping_layers: LayerSpecs | None = ("NPP",),
    doping_offset: float = 1.0,
) -> gf.Component:
    """Returns doped taper to terminate waveguides.

    Args:
        length: distance between input and narrow tapered end.
        cross_section_input: input cross-section.
        cross_section_tip: cross-section at the end of the termination.
        tapered_width: width of the default cross-section at the end of the termination.
            Only used if cross_section_tip is not None.
        doping_layers: optional doping layers to superimpose on the taper. Default N++.
        doping_offset: offset of the doping layer beyond the bbox
    """
    c = Component()

    cross_section_tip = cross_section_tip or gf.get_cross_section(
        cross_section_input, width=tapered_width
    )

    taper = c << gf.get_component(
        taper_cross_section,
        length=length,
        cross_section1=cross_section_input,
        cross_section2=cross_section_tip,
    )

    doping_layers = doping_layers or []

    for layer in doping_layers:
        _ = c << gf.components.bbox(
            bbox=taper.bbox, layer=layer, top=doping_offset, bottom=doping_offset
        )

    c.add_port(name="o1", port=taper.ports["o1"])
    return c


if __name__ == "__main__":
    # c = terminator(cross_section_input=partial(gf.cross_section.strip, width=10))
    c = terminator()
    c.show(show_ports=True)
