from __future__ import annotations

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.text_rectangular import text_rectangular
from gdsfactory.constants import _glyph, _indent, _width
from gdsfactory.typings import Coordinate, LayerSpec, LayerSpecs


@gf.cell
def text(
    text: str = "abcd",
    size: float = 10.0,
    position: Coordinate = (0, 0),
    justify: str = "left",
    layer: LayerSpec = "WG",
    layers: LayerSpecs | None = None,
) -> Component:
    """Text shapes.

    Args:
        text: string.
        size: in um.
        position: x, y position.
        justify: left, right, center.
        layer: for the text.
        layers: optional for duplicating the text.
    """
    scaling = size / 1000
    xoffset = position[0]
    yoffset = position[1]
    t = gf.Component()
    layers = layers or [layer]

    for line in text.split("\n"):
        label = gf.Component()
        for c in line:
            ascii_val = ord(c)
            if c == " ":
                xoffset += 500 * scaling
            elif 33 <= ascii_val <= 126:
                for poly in _glyph[ascii_val]:
                    xpts = np.array(poly)[:, 0] * scaling
                    ypts = np.array(poly)[:, 1] * scaling
                    for layer in layers:
                        label.add_polygon([xpts + xoffset, ypts + yoffset], layer=layer)
                xoffset += (_width[ascii_val] + _indent[ascii_val]) * scaling
            else:
                raise ValueError(f"No character with ascii value {ascii_val!r}")
        t.add_ref(label)
        yoffset -= 1500 * scaling
        xoffset = position[0]
    justify = justify.lower()
    for label in t.references:
        if justify == "left":
            label.xmin = position[0]
        elif justify == "right":
            label.xmax = position[0]
        elif justify == "center":
            label.move(origin=label.center, destination=position, axis="x")
        else:
            raise ValueError(
                f"justify = {justify!r} not in ('center', 'right', 'left')"
            )
    return t.flatten()


@gf.cell
def text_lines(
    text: tuple[str, ...] = ("Chip", "01"),
    size: float = 0.4,
    layer: LayerSpec = "WG",
) -> Component:
    """Returns a Component from a text lines.

    Args:
        text: list of strings.
        size: text size.
        layer: text layer.
    """
    c = gf.Component()

    for i, texti in enumerate(text):
        t = text_rectangular(text=texti, size=size, layer=layer)
        tref = c.add_ref(t)
        tref.movey(-6 * size * (i + 1))
    return c


if __name__ == "__main__":
    # c1 = gf.components.text("hello", size=10, layer=(1, 0))
    # c2 = gf.components.text("10.0")
    c = text(
        text=".[,ABCDEFGHIKKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:/",
        size=4.0,
        justify="right",
        position=(0, 0),
        layers=[(1, 0), (2, 0)],
    )
    # c = text_lines(text=["a", "b"], size=10)
    # c = text_lines()
    # c2.show(show_ports=True)
    # c.plot()
    c.show()
