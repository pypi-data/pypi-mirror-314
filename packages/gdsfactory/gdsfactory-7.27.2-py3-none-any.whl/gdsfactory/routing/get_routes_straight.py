from __future__ import annotations

import warnings

import gdsfactory as gf
from gdsfactory.components.straight import straight
from gdsfactory.difftest import difftest
from gdsfactory.port import Port
from gdsfactory.typings import ComponentSpec, Routes


def get_routes_straight(
    ports: list[Port] | dict[str, Port],
    straight: ComponentSpec = straight,
    **kwargs,
) -> Routes:
    """Returns routes made by 180 degree straights.

    Args:
        ports: List or dict of ports.
        straight: function for straight.
        kwargs: waveguide settings.

    .. plot::
        :include-source:

        import gdsfactory as gf

        c = gf.Component("get_routes_straight")
        pad_array = gf.components.pad_array()
        c1 = c << pad_array
        c2 = c << pad_array
        c2.ymax = -200

        routes = gf.routing.get_routes_straight(ports=c1.get_ports_list(), length=200)
        c.add(routes.references)
        c.plot()

    """
    warnings.warn(
        "This function is deprecated and will be removed in next major release."
    )
    ports = list(ports.values()) if isinstance(ports, dict) else ports
    straight = straight(**kwargs)
    references = [straight.ref() for _ in ports]
    references = [
        ref.connect(
            "o1",
            port,
            allow_width_mismatch=True,
            allow_layer_mismatch=True,
            allow_type_mismatch=True,
        )
        for port, ref in zip(ports, references)
    ]
    ports = [ref.ports["o2"] for ref in references]
    lengths = [straight.info["length"]] * len(ports)
    return Routes(references=references, ports=ports, lengths=lengths)


def test_get_routes_straight(check: bool = True) -> None:
    c = gf.Component("get_routes_straight")
    pad_array = gf.components.pad_array()
    c1 = c << pad_array
    c2 = c << pad_array
    c2.ymax = -200

    routes = get_routes_straight(ports=c1.get_ports_list(), length=200)
    c.add(routes.references)
    if check:
        difftest(c)


if __name__ == "__main__":
    c = gf.Component("get_routes_straight")
    pad_array = gf.components.pad_array()
    c1 = c << pad_array
    c2 = c << pad_array
    c2.ymax = -200

    routes = get_routes_straight(ports=c1.get_ports_list(), length=200)
    c.add(routes.references)
    c.show()
