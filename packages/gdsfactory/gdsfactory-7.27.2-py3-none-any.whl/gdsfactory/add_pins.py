"""Add_pin adds a Pin to a port, add_pins adds Pins to all ports.

- pins
- outline

Some functions modify a component without changing its name.
Make sure these functions are inside a new Component or called as a decorator
They without modifying the cell name
"""

from __future__ import annotations

import inspect
import itertools
import json
from collections.abc import Callable
from functools import partial
from typing import TYPE_CHECKING

import gdstk
import numpy as np
from numpy import ndarray
from omegaconf import OmegaConf

from gdsfactory.cell import container
from gdsfactory.port import select_ports_electrical, select_ports_optical

if TYPE_CHECKING:
    from gdsfactory.component import Component
    from gdsfactory.component_reference import ComponentReference
    from gdsfactory.port import Port

Layer = tuple[int, int]
Layers = tuple[Layer, ...]
LayerSpec = Layer | str | int | None
LayerSpecs = tuple[LayerSpec, ...]
nm = 1e-3


def _rotate(v: ndarray, m: ndarray) -> ndarray:
    return np.dot(m, v)


def add_bbox(
    component: Component,
    bbox_layer: LayerSpec = "DEVREC",
) -> Component:
    """Add bbox on outline.

    Args:
        component: component to add bbox.
        bbox_layer: bbox layer.
    """
    from gdsfactory.pdk import get_layer

    bbox_layer = get_layer(bbox_layer)
    polygons = component.get_polygons(as_array=False)
    polygons_ = gdstk.boolean(
        polygons, [], "or", layer=bbox_layer[0], datatype=bbox_layer[1]
    )

    component.add(polygons_)

    return component


def add_bbox_siepic(
    component: Component,
    bbox_layer: LayerSpec = "DEVREC",
    remove_layers: LayerSpecs = ("PORT", "PORTE"),
) -> Component:
    """Add bounding box device recognition layer.

    Args:
        component: to add bbox.
        bbox_layer: bounding box.
        remove_layers: remove other layers.
    """
    from gdsfactory.pdk import get_layer

    bbox_layer = get_layer(bbox_layer)
    remove_layers = remove_layers or []
    remove_layers = list(remove_layers) + [bbox_layer]
    remove_layers = [get_layer(layer) for layer in remove_layers]
    component = component.remove_layers(layers=remove_layers, recursive=False)

    if bbox_layer:
        component.add_padding(default=0, layers=(bbox_layer,))
    return component


def get_pin_triangle_polygon_tip(
    port: Port,
) -> tuple[list[float], tuple[float, float]]:
    """Returns triangle polygon and tip position."""
    p = port
    port_face = p.info.get("face", None)

    orientation = p.orientation or 0

    if orientation is None:
        raise ValueError("Port {port.name!r} needs to have an orientation.")

    ca = np.cos(orientation * np.pi / 180)
    sa = np.sin(orientation * np.pi / 180)
    rot_mat = np.array([[ca, -sa], [sa, ca]])
    d = p.width / 2

    dtip = np.array([d, 0])

    if port_face:
        dtop = port_face[0]
        dbot = port_face[-1]
    else:
        dbot = np.array([0, -d])
        dtop = np.array([0, d])

    p0 = p.center + _rotate(dbot, rot_mat)
    p1 = p.center + _rotate(dtop, rot_mat)
    port_face = [p0, p1]

    ptip = p.center + _rotate(dtip, rot_mat)

    polygon = list(port_face) + [ptip]
    polygon = np.stack(polygon)
    return polygon, ptip


def add_pin_triangle(
    component: Component,
    port: Port,
    layer: LayerSpec = "PORT",
    layer_label: LayerSpec = "TEXT",
) -> None:
    """Add triangle pin with a right angle, pointing out of the port.

    Args:
        component: to add pin.
        port: Port.
        layer: for the pin marker.
        layer_label: for the label.
    """
    polygon, ptip = get_pin_triangle_polygon_tip(port=port)
    component.add_polygon(polygon, layer=layer)

    if layer_label:
        component.add_label(
            text=str(port.name),
            position=ptip,
            layer=layer_label,
        )


def add_pin_rectangle_inside(
    component: Component,
    port: Port,
    pin_length: float = 0.1,
    layer: LayerSpec = "PORT",
    layer_label: LayerSpec | None = "TEXT",
    label_function: Callable[[Component, str, Port], str] | None = None,
) -> None:
    """Add square pin towards the inside of the port.

    Args:
        component: to add pins.
        port: Port.
        pin_length: length of the pin marker for the port.
        layer: for the pin marker.
        layer_label: layer for the label. None will use the port layer.
        label_function: function to return label text according to the ``component`` and ``port``.

    Note:
        Either ``layer_label`` or ``label_function`` must be something else than None for labels to be added.

    .. code::

           _______________
          |               |
          |               |
          |               |
          ||              |
          ||              |
          |               |
          |      __       |
          |_______________|
    """
    a = port.orientation or 0
    ca = np.cos(a * np.pi / 180)
    sa = np.sin(a * np.pi / 180)
    rot_mat = np.array([[ca, -sa], [sa, ca]])

    d = port.width / 2

    dbot = np.array([0, -d])
    dtop = np.array([0, +d])
    dbotin = np.array([-pin_length, -d])
    dtopin = np.array([-pin_length, +d])

    p0 = port.center + _rotate(dbot, rot_mat)
    p1 = port.center + _rotate(dtop, rot_mat)
    ptopin = port.center + _rotate(dtopin, rot_mat)
    pbotin = port.center + _rotate(dbotin, rot_mat)
    polygon = [p0, p1, ptopin, pbotin]
    component.add_polygon(polygon, layer=layer)
    if any((layer_label, label_function)):
        # Find name of function that called add_pins or alternatively add_pin_rectangle_inside (in this preference)
        # TODO: very hacky, find a better way in the future
        rough_component_name = (
            next(
                itertools.chain(
                    itertools.islice(
                        itertools.dropwhile(
                            lambda f: "add_pins" not in f.function, inspect.stack()
                        ),
                        2,
                        None,
                    ),
                    itertools.islice(
                        itertools.dropwhile(
                            lambda f: "add_pin_rectangle_inside" not in f.function,
                            inspect.stack(),
                        ),
                        1,
                        None,
                    ),
                )
            ).function
            if label_function
            else None
        )  # don't compute if not needed
        component.add_label(
            text=label_function(component, rough_component_name, port)
            if label_function
            else str(port.name),
            position=port.center,
            layer=layer_label if layer_label else port.layer,
        )


def add_pin_rectangle_double(
    component: Component,
    port: Port,
    pin_length: float = 0.1,
    layer: LayerSpec = "PORT",
    layer_label: LayerSpec = "TEXT",
) -> None:
    """Add two square pins: one inside with label, one outside.

    Args:
        component: to add pins.
        port: Port.
        pin_length: length of the pin marker for the port.
        layer: for the pin marker.
        layer_label: for the label.

    .. code::

           _______________
          |               |
          |               |
          |               |
         |||              |
         |||              |
          |               |
          |      __       |
          |_______________|
                 __
    """
    p = port
    a = p.orientation
    ca = np.cos(a * np.pi / 180)
    sa = np.sin(a * np.pi / 180)
    rot_mat = np.array([[ca, -sa], [sa, ca]])

    # outer square
    d = p.width / 2
    dbot = np.array([0, -d])
    dtop = np.array([0, d])
    dbotin = np.array([pin_length / 2, -d])
    dtopin = np.array([pin_length / 2, +d])
    p0 = p.center + _rotate(dbot, rot_mat)
    p1 = p.center + _rotate(dtop, rot_mat)
    ptopin = p.center + _rotate(dtopin, rot_mat)
    pbotin = p.center + _rotate(dbotin, rot_mat)
    polygon = [p0, p1, ptopin, pbotin]
    component.add_polygon(polygon, layer=layer)

    # inner square
    d = p.width / 2
    dbot = np.array([0, -d])
    dtop = np.array([0, d])
    dbotin = np.array([-pin_length / 2, -d])
    dtopin = np.array([-pin_length / 2, +d])
    p0 = p.center + _rotate(dbot, rot_mat)
    p1 = p.center + _rotate(dtop, rot_mat)
    ptopin = p.center + _rotate(dtopin, rot_mat)
    pbotin = p.center + _rotate(dbotin, rot_mat)
    polygon = [p0, p1, ptopin, pbotin]
    component.add_polygon(polygon, layer=layer)

    x = (p0[0] + ptopin[0]) / 2
    y = (ptopin[1] + pbotin[1]) / 2
    if layer_label:
        component.add_label(
            text=str(p.name),
            position=(x, y),
            layer=layer_label,
        )


def add_pin_rectangle(
    component: Component,
    port: Port,
    pin_length: float = 0.1,
    layer: LayerSpec = "PORT",
    layer_label: LayerSpec = "TEXT",
    port_margin: float = 0.0,
) -> None:
    """Add half out pin to a component.

    Args:
        component: to add pin.
        port: Port.
        pin_length: length of the pin marker for the port.
        layer: for the pin marker.
        layer_label: for the label.
        port_margin: margin to port edge.

    .. code::

           _______________
          |               |
          |               |
          |               |
         |||              |
         |||              |
          |               |
          |      __       |
          |_______________|
                 __
    """
    p = port
    a = p.orientation
    ca = np.cos(a * np.pi / 180)
    sa = np.sin(a * np.pi / 180)
    rot_mat = np.array([[ca, -sa], [sa, ca]])

    d = p.width / 2 + port_margin

    dbot = np.array([pin_length / 2, -d])
    dtop = np.array([pin_length / 2, d])
    dbotin = np.array([-pin_length / 2, -d])
    dtopin = np.array([-pin_length / 2, +d])

    p0 = p.center + _rotate(dbot, rot_mat)
    p1 = p.center + _rotate(dtop, rot_mat)
    ptopin = p.center + _rotate(dtopin, rot_mat)
    pbotin = p.center + _rotate(dbotin, rot_mat)
    polygon = [p0, p1, ptopin, pbotin]
    component.add_polygon(polygon, layer=layer)

    if layer_label:
        component.add_label(
            text=str(p.name),
            position=p.center,
            layer=layer_label,
        )


def add_pin_path(
    component: Component,
    port: Port,
    pin_length: float = 2 * nm,
    layer: LayerSpec = "PORT",
    layer_label: LayerSpec | None = None,
) -> None:
    """Add half out path pin to a component.

    This port type is compatible with SiEPIC pdk.

    Args:
        component: to add pin.
        port: Port.
        pin_length: length of the pin marker for the port.
        layer: for the pin marker.
        layer_label: optional layer label. Defaults to layer.

    .. code::

           _______________
          |               |
          |               |
          |               |
         |||              |
         |||              |
          |               |
          |      __       |
          |_______________|
                 __
    """
    from gdsfactory.pdk import get_layer

    layer_label = layer_label or layer
    p = port
    a = p.orientation
    ca = np.cos(a * np.pi / 180)
    sa = np.sin(a * np.pi / 180)
    rot_mat = np.array([[ca, -sa], [sa, ca]])

    d0 = np.array([-pin_length / 2, 0])
    d1 = np.array([+pin_length / 2, 0])

    p0 = p.center + _rotate(d0, rot_mat)
    p1 = p.center + _rotate(d1, rot_mat)

    points = [p0, p1]
    layer = get_layer(layer)
    path = gdstk.FlexPath(
        points,
        width=p.width,
        layer=layer[0],
        datatype=layer[1],
        simple_path=True,
        tolerance=1e-3,
    )
    component.add(path)

    component.add_label(
        text=str(p.name), position=p.center, layer=layer_label, anchor="sw"
    )


def add_outline(
    component: Component,
    reference: ComponentReference | None = None,
    layer: LayerSpec = "DEVREC",
    **kwargs,
) -> None:
    """Adds devices outline bounding box in layer.

    Args:
        component: where to add the markers.
        reference: to read outline from.
        layer: to add padding.

    Keyword Args:
        default: default padding.
        top: North padding.
        bottom: padding.
        right: padding.
        left: padding.
    """
    from gdsfactory.add_padding import get_padding_points

    c = reference or component
    if hasattr(component, "parent"):
        component = component.parent
    points = get_padding_points(component=c, default=0, **kwargs)
    component.add_polygon(points, layer=layer)


def add_pins_siepic(
    component: Component,
    function: Callable = add_pin_path,
    port_type: str = "optical",
    layer_pin: LayerSpec = "PORT",
    pin_length: float = 10 * nm,
) -> Component:
    """Add pins.

    Enables you to run SiEPIC verification tools:
    To Run verification install SiEPIC-tools KLayout package
    then hit V shortcut in KLayout to run verification

    - ensure no disconnected pins
    - netlist extraction

    Args:
        component: to add pins.
        function: to add pin.
        port_type: optical, electrical, ...
        layer_pin: pin layer.
        pin_length: length of the pin marker for the port.
    """
    for p in component.get_ports_list(port_type=port_type):
        function(component=component, port=p, layer=layer_pin, pin_length=pin_length)

    return component


add_pins_siepic_optical = add_pins_siepic
add_pins_siepic_electrical = partial(
    add_pins_siepic, port_type="electrical", layer_pin="PORTE"
)


def add_pins(
    component: Component,
    reference: ComponentReference | None = None,
    function: Callable = add_pin_rectangle_inside,
    select_ports: Callable | None = None,
    **kwargs,
) -> Component:
    """Add Pin port markers.

    Warning:
        Be careful with this function as it modifies the component in-place.

    Args:
        component: :class:`Component` to add pins to in-place.
        reference: Optional :class:`ComponentReference` to infer ports from instead of given ``component``.
        function: Function that adds pins to a component given a ``component`` and ``port`` combination.
        select_ports: Function to filter ports to a selection

    Keyword Args:
        pin_length: length of the pin marker for the port.
        layer: layer for the pin marker.
        layer_label: add label for the pin marker.
        label_function: function to return label text according to the ``component`` and ``port``.
    """
    reference = reference or component
    ports = (
        select_ports(reference.ports).values()
        if select_ports
        else reference.get_ports_list()
    )
    for port in ports:
        function(component=component, port=port, **kwargs)
    return component


add_pins_optical = partial(add_pins, select_ports=select_ports_optical)
add_pins_electrical = partial(add_pins, select_ports=select_ports_electrical)

add_pins_triangle = partial(add_pins, function=add_pin_triangle)
add_pins_center = partial(add_pins, function=add_pin_rectangle)
add_pin_inside1nm = partial(
    add_pin_rectangle_inside, pin_length=1 * nm, layer_label=None
)
add_pin_inside2nm = partial(
    add_pin_rectangle_inside, pin_length=2 * nm, layer_label=None
)
add_pin_inside2um = partial(add_pin_rectangle_inside, pin_length=2, layer_label=None)
add_pins_inside1nm = partial(add_pins, function=add_pin_inside1nm)
add_pins_inside2nm = partial(add_pins, function=add_pin_inside2nm)
add_pins_inside2um = partial(add_pins, function=add_pin_inside2um)

add_pins_container = partial(container, function=add_pins)
add_pins_container_center = partial(container, function=add_pins_center)
add_pins_container_siepic = partial(container, function=add_pins_siepic)


def add_settings_label(
    component: Component,
    reference: ComponentReference,
    layer_label: LayerSpec = "LABEL_SETTINGS",
) -> None:
    """Add settings in label.

    Args:
        component: to add pins.
        reference: ComponentReference.
        layer_label: layer spec.
    """
    from gdsfactory.pdk import get_layer

    layer_label = get_layer(layer_label)

    settings_dict = OmegaConf.to_container(reference.settings)
    settings_string = f"settings={json.dumps(settings_dict)}"
    if len(settings_string) > 1024:
        raise ValueError(f"label > 1024 characters: {settings_string}")
    component.add_label(
        position=reference.center, text=settings_string, layer=layer_label
    )


def add_instance_label(
    component: Component,
    reference: ComponentReference,
    instance_name: str | None = None,
    layer: LayerSpec = "LABEL_INSTANCE",
) -> None:
    """Adds label to a reference in a component."""
    instance_name = (
        instance_name
        or f"{reference.parent.name},{int(reference.x)},{int(reference.y)}"
    )

    component.add_label(
        text=instance_name,
        position=reference.center,
        layer=layer,
    )


def add_pins_and_outline(
    component: Component,
    reference: ComponentReference | None = None,
    add_outline_function: Callable | None = add_outline,
    add_pins_function: Callable | None = add_pins,
    add_settings_function: Callable | None = add_settings_label,
    add_instance_label_function: Callable | None = add_settings_label,
) -> None:
    """Add markers.

    - outline
    - pins for the ports
    - label for the name
    - label for the settings

    Args:
        component: where to add the markers.
        reference: to add pins.
        add_outline_function.
        add_pins_function: to add pins to ports.
        add_settings_function: to add outline around the component.
        add_instance_label_function: labels each instance.
    """
    if add_outline_function:
        add_outline_function(component=component, reference=reference)
    if add_pins_function:
        add_pins_function(component=component, reference=reference)
    if add_settings_function:
        add_settings_function(component=component, reference=reference)
    if add_instance_label_function:
        add_instance_label_function(component=component, reference=reference)


if __name__ == "__main__":
    import gdsfactory as gf

    # c = test_add_pins()
    # c.show(show_ports=True)
    # c = gf.components.straight(length=2)
    # c.show(show_ports_suborts=True)
    # p1 = len(c1.get_polygons())
    # p2 = len(c2.get_polygons())
    # assert p2 == p1 + 2
    # c1 = gf.components.straight_heater_metal(length=2)
    c = gf.components.straight()
    c2 = add_pins_container(component=c)
    # cc.show(show_ports=False)
    c2.show(show_ports=False)
