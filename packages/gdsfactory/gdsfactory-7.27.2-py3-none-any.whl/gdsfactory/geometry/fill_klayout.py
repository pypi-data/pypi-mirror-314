"""Dummy fill to keep density constant using klayout."""

from __future__ import annotations

import gdsfactory as gf
from gdsfactory.typings import LayerSpec, LayerSpecs, PathType


def fill(
    gdspath,
    layer_to_fill: LayerSpec,
    layer_to_fill_margin: float = 0,
    layers_to_avoid: tuple[LayerSpec, float] | None = None,
    cell_name: str | None = None,
    fill_cell_name: str = "fill_cell",
    create_new_fill_cell: bool = False,
    include_original: bool = False,
    fill_layers: LayerSpecs | None = None,
    fill_size: tuple[float, float] = (10, 10),
    fill_spacing: tuple[float, float] = (20, 20),
    fill_name: str | None = None,
    gdspath_out: PathType | None = None,
) -> str:
    """Write gds file with fill.

    Args:
        gdspath: GDS input.
        layer_to_fill: Layer that defines the region to fill.
        layer_to_fill_margin: in um.
        layers_to_avoid: Layer to avoid to margin (((1, 0), 3.5), (LAYER.SLAB, 2)).
        cell_name: Optional cell to fill. Defaults to top cell.
        fill_cell_name: Optional cell name to use as fill.
        create_new_fill_cell: creates new fill cell, otherwise uses fill_cell_name from gdspath.
        include_original: True include original gdspath. False returns only fill.
        fill_layers: if create_new_fill_cell=True, defines new fill layers.
        fill_size: if create_new_fill_cell=True, defines new fill size.
        fill_spacing: fill pitch in x and y.
        fill_name: name of the cell containing all fill cells. Defaults to Cell_fill.
        gdspath_out: Optional GDS output. Defaults to input.
    """
    import kfactory as kf
    import klayout.db as kdb
    from kfactory import KCLayout

    temp_kcl = KCLayout(name=str(gdspath))
    temp_kcl.read(gdspath)
    cellname = cell_name or temp_kcl.top_cell().name
    cell = temp_kcl[cellname]
    fill_name = fill_name or f"{cell.name}_fill"

    c = kf.KCell(fill_name)

    if create_new_fill_cell:
        # if temp_kcl.has_cell(fill_cell_name):
        #     raise ValueError(f"{fill_cell_name!r} already in {str(gdspath)!r}")

        if not fill_layers:
            raise ValueError(
                "You need to pass fill_layers if create_new_fill_cell=True"
            )
        fill_cell = kf.KCell(fill_cell_name)
        for layer in fill_layers:
            layer = gf.get_layer(layer)
            layer = kf.kcl.layer(*layer)
            _ = fill_cell << kf.cells.straight.straight(
                width=fill_size[0], length=fill_size[1], layer=layer
            )
    else:
        fill_cell = temp_kcl[fill_cell_name]

    fill_cell_index = fill_cell.cell_index()  # fill cell index
    fill_cell_box = fill_cell.bbox().enlarged(
        fill_spacing[0] / 2 * 1e3, fill_spacing[1] / 2 * 1e3
    )
    fill_margin = kf.kdb.Point(0, 0)

    layer_to_fill = gf.get_layer(layer_to_fill)
    layer_to_fill = cell.kcl.layer(*layer_to_fill)
    region = kdb.Region()
    region_avoid_all = kdb.Region()

    if layers_to_avoid:
        for layer, margin in layers_to_avoid:
            layer = gf.get_layer(layer)
            layer = kf.kcl.layer(*layer)
            region_avoid = kdb.Region()
            region_avoid.insert(
                cell.begin_shapes_rec(layer)
            ) if layer != layer_to_fill else None
            region_avoid = region_avoid.size(margin * 1e3)
            region_avoid_all = region_avoid_all + region_avoid

    region.insert(cell.begin_shapes_rec(layer_to_fill))
    region.size(-layer_to_fill_margin * 1e3)
    region_to_fill = region - region_avoid_all

    c.fill_region(
        region_to_fill,
        fill_cell_index,
        fill_cell_box,
        fill_margin,
    )

    if include_original:
        _ = c << cell

    gdspath_out = gdspath_out or gdspath
    c.write(str(gdspath_out))
    return fill_name


@gf.cell
def cell_with_pad():
    c = gf.Component()
    c << gf.components.mzi(decorator=gf.add_padding)
    pad = c << gf.components.pad(size=(2, 2))
    pad.movey(10)
    return c


if __name__ == "__main__":
    c = cell_with_pad()
    c.show()
    gdspath = c.write_gds("mzi_fill.gds")

    use_fill_cell = False
    use_fill_cell = True
    spacing = 50

    if use_fill_cell:
        fill(
            gdspath,
            fill_layers=("WG",),
            layer_to_fill=(67, 0),
            layers_to_avoid=(((1, 0), 0), ((49, 0), 0)),
            # layers_to_avoid=(((1, 0), 0),),
            fill_cell_name="pad_size2__2",
            create_new_fill_cell=False,
            fill_spacing=(spacing, spacing),
            fill_size=(1, 1),
            include_original=True,
            layer_to_fill_margin=25,
        )
    else:
        fill(
            gdspath,
            fill_layers=("WG",),
            layer_to_fill=(67, 0),
            layers_to_avoid=(((1, 0), 0),),
            fill_cell_name="fill_cell",
            create_new_fill_cell=True,
            fill_spacing=(1, 1),
            fill_size=(1, 1),
            layer_to_fill_margin=25,
            include_original=True,
        )
    gf.show(gdspath)
