from __future__ import annotations

import warnings

from gdsfactory.components.bend_s import bend_s
from gdsfactory.port import Port
from gdsfactory.typings import ComponentFactory, Route


def get_route_sbend(
    port1: Port,
    port2: Port,
    *,
    bend_s: ComponentFactory = bend_s,
    allow_layer_mismatch: bool = False,
    allow_width_mismatch: bool = False,
    allow_type_mismatch: bool = False,
    **kwargs,
) -> Route:
    """Returns an Sbend Route to connect two ports.

    Args:
        port1: start port.
        port2: end port.
        bend_s: S-bend component factory.

    Keyword Args:
        npoints: number of points.
        with_cladding_box: square bounding box to avoid DRC errors.
        cross_section: function.
        allow_layer_mismatch: allow layer mismatch.
        allow_width_mismatch: allow width mismatch.
        allow_type_mismatch: allow type mismatch.
        kwargs: cross_section settings.

    .. plot::
        :include-source:

        import gdsfactory as gf

        c = gf.Component("demo_route_sbend")
        mmi1 = c << gf.components.mmi1x2()
        mmi2 = c << gf.components.mmi1x2()
        mmi2.movex(50)
        mmi2.movey(5)
        route = gf.routing.get_route_sbend(mmi1.ports['o2'], mmi2.ports['o1'])
        c.add(route.references)
        c.plot()

    """
    ysize = port2.center[1] - port1.center[1]
    xsize = port2.center[0] - port1.center[0]

    # We need to act differently if the route is orthogonal in x
    # or orthogonal in y

    size = (xsize, ysize) if port1.orientation in [0, 180] else (ysize, -xsize)
    bend = bend_s(size=size, **kwargs)

    bend_ref = bend.ref()
    bend_ref.connect(
        list(bend_ref.ports.keys())[0],
        port1,
        allow_layer_mismatch=allow_layer_mismatch,
        allow_width_mismatch=allow_width_mismatch,
        allow_type_mismatch=allow_type_mismatch,
    )

    if port1.orientation is not None and port2.orientation is not None:
        orthogonality_error = abs(abs(port1.orientation - port2.orientation) - 180)
        if orthogonality_error > 0.1:
            from gdsfactory.routing.manhattan import get_route_error

            warnings.warn(
                f"Ports need to have orthogonal orientation {orthogonality_error}\n"
                f"port1 = {port1.orientation} deg and port2 = {port2.orientation}"
            )
            points = [port1.center, port2.center]
            return get_route_error(points)

    return Route(
        references=[bend_ref],
        length=bend.info["length"],
        ports=(port1, port2),
    )


if __name__ == "__main__":
    # import gdsfactory as gf
    # from gdsfactory.routing.sort_ports import sort_ports

    # c = gf.Component("test_get_route_sbend")
    # pitch = 2.0
    # ys_left = [0, 10, 20]
    # N = len(ys_left)
    # ys_right = [(i - N / 2) * pitch for i in range(N)]

    # right_ports = [
    #     gf.Port(f"R_{i}", (0, ys_right[i]), width=0.5, orientation=180, layer=(1, 0))
    #     for i in range(N)
    # ]
    # left_ports = [
    #     gf.Port(f"L_{i}", (-50, ys_left[i]), width=0.5, orientation=0, layer=(1, 0))
    #     for i in range(N)
    # ]
    # left_ports.reverse()
    # right_ports, left_ports = sort_ports(right_ports, left_ports)

    # for p1, p2 in zip(right_ports, left_ports):
    #     route = get_route_sbend(p1, p2, layer=(2, 0))
    #     c.add(route.references)

    # c.show(show_ports=True)

    import gdsfactory as gf

    c = gf.Component("demo_route_sbend")
    mmi1 = c << gf.components.mmi1x2()
    mmi2 = c << gf.components.mmi1x2()
    # mmi2.movex(30)
    mmi2.movey(100)
    route = gf.routing.get_route_sbend(mmi1.ports["o1"], mmi2.ports["o1"])
    c.add(route.references)
    c.show()
