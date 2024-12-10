from gdsfactory.technology.layer_map import LayerMap

Layer = tuple[int, int]


class GenericLayerMap(LayerMap):
    """Generic layermap based on the book:

    Lukas Chrostowski, Michael Hochberg, "Silicon Photonics Design",
    Cambridge University Press 2015, page 353

    You will need to create a new LayerMap with your specific foundry layers.
    """

    WAFER: Layer = (99999, 0)

    WG: Layer = (1, 0)
    WGCLAD: Layer = (111, 0)
    SLAB150: Layer = (2, 0)
    SHALLOW_ETCH: Layer = (2, 6)
    SLAB90: Layer = (3, 0)
    DEEP_ETCH: Layer = (3, 6)
    DEEPTRENCH: Layer = (4, 0)
    GE: Layer = (5, 0)
    UNDERCUT: Layer = (6, 0)
    WGN: Layer = (34, 0)
    WGN_CLAD: Layer = (36, 0)

    N: Layer = (20, 0)
    NP: Layer = (22, 0)
    NPP: Layer = (24, 0)
    P: Layer = (21, 0)
    PP: Layer = (23, 0)
    PPP: Layer = (25, 0)
    GEN: Layer = (26, 0)
    GEP: Layer = (27, 0)

    HEATER: Layer = (47, 0)
    M1: Layer = (41, 0)
    M2: Layer = (45, 0)
    M3: Layer = (49, 0)
    MTOP: Layer = (49, 0)
    VIAC: Layer = (40, 0)
    VIA1: Layer = (44, 0)
    VIA2: Layer = (43, 0)
    PADOPEN: Layer = (46, 0)

    DICING: Layer = (100, 0)
    NO_TILE_SI: Layer = (71, 0)
    PADDING: Layer = (67, 0)
    DEVREC: Layer = (68, 0)
    FLOORPLAN: Layer = (64, 0)
    TEXT: Layer = (66, 0)
    PORT: Layer = (1, 10)
    PORTE: Layer = (1, 11)
    PORTH: Layer = (70, 0)
    SHOW_PORTS: Layer = (1, 12)
    TE: Layer = (203, 0)
    TM: Layer = (204, 0)
    DRC_MARKER: Layer = (205, 0)

    WG_PIN: Layer = (1, 10)
    M1_PIN: Layer = (41, 10)
    M2_PIN: Layer = (45, 10)
    M3_PIN: Layer = (49, 10)

    SOURCE: Layer = (110, 0)
    MONITOR: Layer = (101, 0)


LAYER = GenericLayerMap()


if __name__ == "__main__":
    print(LAYER.LABEL_SETTINGS)
