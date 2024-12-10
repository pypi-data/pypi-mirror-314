from __future__ import annotations

from functools import partial

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.bend_euler import bend_euler180
from gdsfactory.components.component_sequence import component_sequence
from gdsfactory.components.straight import straight
from gdsfactory.components.taper import taper
from gdsfactory.components.taper_from_csv import taper_from_csv
from gdsfactory.typings import ComponentSpec, CrossSectionSpec


@gf.cell
def cutback_component(
    component: ComponentSpec = taper_from_csv,
    cols: int = 4,
    rows: int = 5,
    port1: str = "o1",
    port2: str = "o2",
    bend180: ComponentSpec = bend_euler180,
    mirror: bool = False,
    mirror1: bool = False,
    mirror2: bool = False,
    straight_length: float | None = None,
    straight_length_pair: float | None = None,
    cross_section: CrossSectionSpec = "xs_sc",
    ports_map: dict[str, tuple[str, str]] | None = None,
    **kwargs,
) -> Component:
    """Returns a daisy chain of components for measuring their loss.

    Works only for components with 2 ports (input, output).

    The number of components is given by cols * rows * 4.

    Args:
        component: for cutback.
        cols: number of columns.
        rows: number of rows.
        port1: name of first optical port.
        port2: name of second optical port.
        bend180: ubend.
        mirror: Flips component. Useful when 'o2' is the port that you want to route to.
        mirror1: mirrors first component.
        mirror2: mirrors second component.
        straight_length: length of the straight section between cutbacks.
        straight_length_pair: length of the straight section between each component pair.
        cross_section: specification (CrossSection, string or dict).
        ports_map: (optional) extra port mapping for the underlying component_sequence using the convention.
            {port_name: (alias_name, port_name)}
            An and Bn are the aliases for the components here, with n integers.
        kwargs: component settings.
    """
    xs = gf.get_cross_section(cross_section)

    component = gf.get_component(component, **kwargs)
    bendu = gf.get_component(bend180, cross_section=xs)
    straight_length = gf.snap.snap_to_grid2x(straight_length or xs.radius * 2)
    straight_length_pair = gf.snap.snap_to_grid2x(straight_length_pair or 0)

    straight_component = straight(length=straight_length, cross_section=xs)
    straight_pair = straight(length=straight_length_pair, cross_section=xs)

    # Define a map between symbols and (component, input port, output port)
    symbol_to_component = {
        "A": (component, port1, port2),
        "B": (component, port2, port1),
        "D": (bendu, "o1", "o2"),
        "C": (bendu, "o2", "o1"),
        "-": (straight_component, "o1", "o2"),
        "_": (straight_component, "o2", "o1"),
        ".": (straight_pair, "o2", "o1"),
    }

    # Generate the sequence of staircases

    s = ""
    for i in range(rows):
        a = "!A" if mirror1 else "A"
        b = "!B" if mirror2 else "B"

        s += f"{a}.{b}" * cols if straight_length_pair else (a + b) * cols
        if mirror:
            s += "C" if i % 2 == 0 else "D"
        else:
            s += "D" if i % 2 == 0 else "C"

    s = s[:-1]
    s += "-_"

    for i in range(rows):
        s += f"{a}.{b}" * cols if straight_length_pair else (a + b) * cols
        s += "D" if (i + rows) % 2 == 0 else "C"

    s = s[:-1]

    seq = component_sequence(
        sequence=s, symbol_to_component=symbol_to_component, ports_map=ports_map
    )

    c = gf.Component()
    ref = c << seq
    c.add_ports(ref.ports)

    n = s.count("A") + s.count("B")
    c.info["components"] = n
    return c


# straight_wide = partial(straight, width=3, length=20)
# bend180_wide = partial(bend_euler180, width=3)
component_flipped = partial(taper, width2=0.5, width1=3)
straight_long = partial(straight, length=20)
cutback_component_mirror = partial(cutback_component, mirror=True)


if __name__ == "__main__":
    c = cutback_component()
    # c = cutback_component_mirror(component=component_flipped)
    # c = gf.routing.add_fiber_single(c)

    cols = range(1, 3)
    rows = range(1, 3)
    cs = [cutback_component(cols=col, rows=row) for col in cols for row in rows]
    ncomponent_expected = [4 * col * row for col in cols for row in rows]
    ncomponents = [c.info["components"] for c in cs]
    print(ncomponents, ncomponent_expected)

    c.show(show_ports=True)
