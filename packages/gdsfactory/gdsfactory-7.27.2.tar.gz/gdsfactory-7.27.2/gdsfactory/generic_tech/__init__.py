from __future__ import annotations

import typing
from functools import cache

from gdsfactory.config import PATH
from gdsfactory.generic_tech.layer_map import GenericLayerMap as LayerMap
from gdsfactory.generic_tech.layer_stack import LAYER_STACK
from gdsfactory.technology import LayerViews

if typing.TYPE_CHECKING:
    from gdsfactory.pdk import Pdk

LAYER = LayerMap()

PORT_MARKER_LAYER_TO_TYPE = {
    LAYER.PORT: "optical",
    LAYER.PORTE: "dc",
    LAYER.TE: "vertical_te",
    LAYER.TM: "vertical_tm",
}

PORT_LAYER_TO_TYPE = {
    LAYER.WG: "optical",
    LAYER.WGN: "optical",
    LAYER.SLAB150: "optical",
    LAYER.M1: "dc",
    LAYER.M2: "dc",
    LAYER.M3: "dc",
    LAYER.TE: "vertical_te",
    LAYER.TM: "vertical_tm",
}

PORT_TYPE_TO_MARKER_LAYER = {v: k for k, v in PORT_MARKER_LAYER_TO_TYPE.items()}

LAYER_TRANSITIONS = {
    LAYER.WG: "taper",
    LAYER.M3: "taper",
    # (LAYER.)
}

LAYER_CONNECTIVITY = [
    ("NPP", "VIAC", "M1"),
    ("PPP", "VIAC", "M1"),
    ("M1", "VIA1", "M2"),
    ("M2", "VIA2", "M3"),
]


@cache
def get_generic_pdk() -> Pdk:
    from gdsfactory.components import cells
    from gdsfactory.cross_section import cross_sections
    from gdsfactory.generic_tech.containers import containers
    from gdsfactory.generic_tech.simulation_settings import materials_index
    from gdsfactory.pdk import Pdk, constants

    LAYER_VIEWS = LayerViews(filepath=PATH.klayout_yaml)

    cells = cells.copy()
    cells.update(containers)

    return Pdk(
        name="generic",
        cells=cells,
        cross_sections=cross_sections,
        layers=dict(LAYER),
        layer_stack=LAYER_STACK,
        layer_views=LAYER_VIEWS,
        layer_transitions=LAYER_TRANSITIONS,
        materials_index=materials_index,
        constants=constants,
        connectivity=LAYER_CONNECTIVITY,
        enforce_width_mismatch_layers=[LAYER.WG],
    )


if __name__ == "__main__":
    from gdsfactory.technology.klayout_tech import KLayoutTechnology

    LAYER_VIEWS = LayerViews(filepath=PATH.klayout_yaml)
    connectivity = [
        ("HEATER", "VIA1", "M2"),
        ("M1", "VIA1", "M2"),
        ("M2", "VIA2", "M3"),
    ]

    t = KLayoutTechnology(
        name="generic_tech",
        layer_map=dict(LAYER),
        layer_views=LAYER_VIEWS,
        layer_stack=LAYER_STACK,
        connectivity=connectivity,
    )
    t.write_tech(tech_dir=PATH.klayout)

    layer_views = LayerViews(filepath=PATH.klayout_yaml)
    layer_views.to_lyp(PATH.klayout_lyp)

    # pdk = get_generic_pdk()
    # pdk.layer_views.to_yaml('layer_views2.yaml')
    # print(pdk.name)
