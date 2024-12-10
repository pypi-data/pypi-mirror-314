from __future__ import annotations

from functools import partial

import gdstk
import numpy as np

import gdsfactory as gf
from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@cell
def regular_polygon(
    sides: int = 6,
    side_length: float = 10,
    layer: LayerSpec = "WG",
    port_type: str | None = "placement",
    snap_to_grid: bool = True,
) -> Component:
    """Returns a regular N-sided polygon, with ports on each edge.

    Args:
        sides: number of sides for the polygon.
        side_length: of the edges.
        layer: Specific layer to put polygon geometry on.
        port_type: optical, electrical.
        snap_to_grid: snap ports to grid.
    """
    c = Component()
    polygon = gdstk.regular_polygon((0, 0), side_length, sides)
    c.add_polygon(polygon, layer=layer)
    a = side_length / (2 * np.tan(np.pi / sides))

    if port_type:
        for side_index in range(sides):
            angle = 270 + side_index * 360 / sides
            center = (a * np.cos(np.radians(angle)), a * np.sin(np.radians(angle)))
            if snap_to_grid:
                center = gf.snap.snap_to_grid(center)
            c.add_port(
                name=f"o{side_index+1}",
                center=center,
                width=side_length,
                layer=layer,
                port_type=port_type,
                orientation=angle,
            )

    c.auto_rename_ports()
    return c


hexagon = partial(regular_polygon, sides=6)
octagon = partial(regular_polygon, sides=8)


if __name__ == "__main__":
    # c = regular_polygon(sides=8, side_length=20)
    # c = rectangle(size=(3, 2), centered=True, layer=(2, 3))
    c = octagon(side_length=20)
    c.show(show_ports=True)
