"""Read component from a numpy.ndarray."""

from __future__ import annotations

import pathlib

import numpy as np

from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.config import PATH
from gdsfactory.geometry.boolean import boolean


def compute_area_signed(pr) -> float:
    """Return the signed area enclosed by a ring using the linear time.

    algorithm at http://www.cgafaq.info/wiki/Polygon_Area. A value >= 0
    indicates a counter-clockwise oriented ring.

    """
    xs, ys = map(list, zip(*pr))
    xs.append(xs[1])
    ys.append(ys[1])
    return sum(xs[i] * (ys[i + 1] - ys[i - 1]) for i in range(1, len(pr))) / 2.0


@cell
def from_np(
    ndarray: np.ndarray,
    nm_per_pixel: int = 20,
    layer: tuple[int, int] = (1, 0),
    threshold: float = 0.99,
    invert: bool = True,
    border_pad_num_pixels: int = 2,
    border_pad_pixel_value: float | None = None,
) -> Component:
    """Returns Component from a np.ndarray.

    Extracts contours skimage.measure.find_contours using `threshold`.

    Args:
        ndarray: 2D ndarray representing the device layout.
        nm_per_pixel: scale_factor.
        layer: layer tuple to output gds.
        threshold: value along which to find contours in the array.
        invert: invert the mask.
        border_pad_num_pixels: number of pixels to pad image border with. A value of 2 is usually sufficient to capture contours along the image border.
        border_pad_pixel_value: set value of padding pixels (optional). This is passed to np.pad through the 'constant_values' argument.

    """
    from skimage import measure

    c = Component()
    d = Component()

    pad_kwargs = {}
    if border_pad_pixel_value is not None:
        pad_kwargs = {"constant_values": border_pad_pixel_value}

    ndarray = np.pad(ndarray, border_pad_num_pixels, **pad_kwargs)
    contours = measure.find_contours(ndarray, threshold)
    assert len(contours) > 0, (
        f"no contours found for threshold = {threshold}, maybe you can reduce the"
        " threshold"
    )

    for contour in contours:
        area = compute_area_signed(contour)
        points = contour * 1e-3 * nm_per_pixel
        if area < 0:
            c.add_polygon(points, layer=layer)
        else:
            d.add_polygon(points, layer=layer)

    return boolean(c, d, operation="not", layer=layer) if invert else d


@cell
def from_image(
    image_path: str | pathlib.Path = PATH.module / "samples" / "images" / "logo.png",
    nm_per_pixel: int = 20,
    layer: tuple[int, int] = (1, 0),
    threshold: float = 0.99,
    invert: bool = True,
    border_pad_num_pixels: int = 2,
    border_pad_pixel_value: float | None = None,
) -> Component:
    """Returns Component from a png image.

    Args:
        image_path: png file path.
        nm_per_pixel: scale_factor.
        layer: layer tuple to output gds.
        threshold: value along which to find contours in the array.
        invert: invert the mask. True by default.
        border_pad_num_pixels: number of pixels to pad image border with. A value of 2 is usually sufficient to capture contours along the image border.
        border_pad_pixel_value: set value of padding pixels (optional). This is passed to np.pad through the 'constant_values' argument.
    """
    import matplotlib.pyplot as plt

    # Load the image using matplotlib
    img = plt.imread(image_path)

    if len(img.shape) == 3:
        img = 0.2989 * img[:, :, 0] + 0.5870 * img[:, :, 1] + 0.1140 * img[:, :, 2]

    # Convert image to numpy array (in fact, plt.imread already returns a numpy array)
    img_array = np.array(img)

    return from_np(
        img_array,
        nm_per_pixel=nm_per_pixel,
        layer=layer,
        threshold=threshold,
        invert=invert,
        border_pad_num_pixels=border_pad_num_pixels,
        border_pad_pixel_value=border_pad_pixel_value,
    )


if __name__ == "__main__":
    # import gdsfactory as gf
    # c1 = gf.components.straight()
    # c1 = gf.components.bend_circular()
    # c1 = gf.components.ring_single()
    # img = c1.to_np()
    # c2 = from_np(img)
    # c2.show()

    c = from_image(
        PATH.module / "samples" / "images" / "logo.png", nm_per_pixel=500, invert=True
    )
    c.show()
