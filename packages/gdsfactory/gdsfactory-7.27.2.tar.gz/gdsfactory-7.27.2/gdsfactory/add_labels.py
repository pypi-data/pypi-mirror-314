"""Add Label to each component port."""

from __future__ import annotations

from collections.abc import Callable
from functools import partial

import gdsfactory as gf
from gdsfactory.component import Component, ComponentReference
from gdsfactory.component_layout import _parse_layer
from gdsfactory.port import Port
from gdsfactory.typings import ComponentOrReference, Label, LayerSpec


def get_input_label_text_dash(
    port: Port,
    gc: ComponentReference | Component,
    gc_index: int | None = None,
    component_name: str | None = None,
    prefix: str = "",
    suffix: str = "",
) -> str:
    """Returns text with `GratingName-ComponentName-PortName`."""
    gc_name = gc.name if isinstance(gc, Component) else gc.parent.name
    return f"{prefix}{gc_name}-{component_name or port.parent.name}-{port.name}{suffix}"


def get_input_label_text_dash_loopback(
    port: Port,
    gc: ComponentReference | Component,
    gc_index: int | None = None,
    component_name: str | None = None,
    prefix: str = "",
) -> str:
    """Returns text with `GratingName-ComponentName-Loopback`."""
    gc_name = gc.name if isinstance(gc, Component) else gc.parent.name
    return f"{prefix}{gc_name}-{component_name or port.parent.name}-loopback_{gc_index}"


def get_input_label_text(
    port: Port,
    gc: ComponentReference | Component,
    gc_index: int | None = None,
    component_name: str | None = None,
    component_prefix: str = "",
    prefix: str = "opt",
    suffix: str = "",
) -> str:
    """Returns text string for an optical port based on grating coupler.

    {label_prefix}_{polarization}_{wavelength_nm}_({prefix}{component_name})

    Args:
        port: to label.
        gc: grating coupler component or reference.
        gc_index: grating_coupler index, which grating_coupler we are labelling.
        component_name: optional name.
        component_prefix: component prefix.
        prefix: prefix to add to the label.
    """
    polarization = gc.info.polarization
    wavelength = gc.info.wavelength

    if polarization not in ["te", "tm"]:
        raise ValueError(f"polarization {polarization!r} needs to be [te, tm]")
    if not isinstance(wavelength, int | float) or not 0.5 < wavelength < 5.0:
        raise ValueError(
            f"{wavelength} needs to be > 0.5um and < 5um. Make sure it's in um"
        )

    component_name = component_name or port.parent.name

    text = f"{prefix}_{polarization}_{int(wavelength*1e3)}_({component_prefix}{component_name}){suffix}"
    if isinstance(gc_index, int):
        text += f"_{gc_index}_{port.name}"
    else:
        text = f"_{port.name}"

    return text


get_input_label_text_loopback = partial(get_input_label_text, prefix="loopback_")


def get_input_label(
    port: Port,
    gc: ComponentReference,
    gc_index: int | None = None,
    gc_port_name: str = "o1",
    layer_label: LayerSpec = "TEXT",
    component_name: str | None = None,
    get_input_label_text_function=get_input_label_text,
) -> Label:
    """Returns a label with component info for a given grating coupler.

    Test equipment to extract grating coupler coordinates and match it to the component.

    Args:
        port: port to label.
        gc: grating coupler reference.
        gc_index: grating coupler index.
        gc_port_name: name of grating coupler port.
        layer_label: layer of the label.
        component_name: for the label.
        get_input_label_text_function: function to get input label.
    """
    text = get_input_label_text_function(
        port=port, gc=gc, gc_index=gc_index, component_name=component_name
    )

    if gc_port_name is None:
        gc_port_name = list(gc.ports.values())[0].name

    layer, texttype = gf.get_layer(layer_label)
    return Label(
        text=text,
        origin=gc.ports[gc_port_name].center,
        anchor="o",
        layer=layer,
        texttype=texttype,
    )


get_input_label_dash = partial(
    get_input_label, get_input_label_text_function=get_input_label_text_dash
)


def get_input_label_electrical(
    port: Port,
    gc_index: int = 0,
    component_name: str | None = None,
    layer_label: LayerSpec = "TEXT",
    gc: ComponentReference | None = None,
) -> Label:
    """Returns a label to test component info for a given electrical port.

    This is the label used by T&M to extract grating coupler coordinates
    and match it to the component.

    Args:
        port: to label.
        gc_index: index of the label.
        component_name: Optional component_name.
        layer_label: for label.
        gc: ignored.
    """
    if component_name:
        name = component_name
    elif isinstance(port.parent, gf.Component):
        name = port.parent.name
    else:
        name = port.parent.ref_cell.name

    text = f"elec_{gc_index}_({name})_{port.name}"
    layer_label = gf.get_layer(layer_label)
    layer, texttype = _parse_layer(layer_label)
    return Label(
        text=text,
        origin=port.center,
        anchor="o",
        layer=layer,
        texttype=texttype,
    )


def add_labels(
    component: Component,
    get_label_function: Callable = get_input_label_electrical,
    layer_label: LayerSpec | None = "TEXT",
    gc: Component | None = None,
    **kwargs,
) -> Component:
    """Returns component with labels on ports.

    Args:
        component: to add labels to.
        get_label_function: function to get label.
        layer_label: LayerSpec for the label. None will use the port layer.
        gc: Optional grating coupler.

    Keyword Args:
        layer: port GDS layer.
        prefix: with in port name.
        suffix: select ports with port name suffix.
        orientation: in degrees.
        width: for ports to add label.
        layers_excluded: List of layers to exclude.
        port_type: optical, electrical, ...
        clockwise: if True, sort ports clockwise, False: counter-clockwise.

    Returns:
        original component with labels.
    """
    ports = component.get_ports_list(**kwargs)

    for i, port in enumerate(ports):
        label = get_label_function(
            port=port,
            gc=gc,
            gc_index=i,
            component_name=component.name,
            layer_label=layer_label if layer_label else port.layer,
        )
        component.add(label)

    return component


def add_siepic_labels(
    component: Component,
    model: str = "auto",
    library: str = "auto",
    label_layer: LayerSpec = "DEVREC",
    spice_params: dict | list | str | None = None,
    label_spacing: float = 0.2,
) -> Component:
    """Adds labels and returns the same component.

    Args:
        component: component.
        model: Lumerical Interconnect model.
            'auto' attempts to extract this from the cross_section.
        library: Lumerical Interconnect library.
            'auto' attempts to extract this from the cross_section.
        label_layer: layer for writing SiEPIC labels.
        spice_params: spice parameters (in microns).
            Either pass in a dict with parameter, value pairs, or pass
            a list of values to extract from component info.
        label_spacing: separation distance between labels in um.
    """
    c = component

    labels = []
    if model:
        if model == "auto" and "model" in c.info:
            model = c.info["model"]
        labels.append(f"Component={model}")
    if library:
        if library == "auto" and "library" in c.info:
            library = c.info["library"]
        labels.append(f"Lumerical_INTERCONNECT_library={library}")
    if spice_params and c.info["layout_model_property_pairs"]:
        if spice_params == "auto":
            pairs = c.info["layout_model_property_pairs"]
            spice_params = {pair[1]: c.info[pair[0]] for pair in pairs}
        param_str = ""
        for param in spice_params:
            val = spice_params[param]
            param_str += f"{param}={val:.3f}u "
        labels.append(f"Spice_param:{param_str}")

    for i, text in enumerate(labels):
        c.add_label(
            text=text, position=(0, i * label_spacing), layer=label_layer, anchor="w"
        )
    return c


def add_labels_to_ports(
    component: Component,
    label_layer: LayerSpec | None = "TEXT",
    port_type: str | None = None,
    **kwargs,
) -> Component:
    """Add labels to component ports.

    Args:
        component: to add labels.
        label_layer: layer spec for the label. None will use the port layer.
        port_type: to select ports.

    Keyword Args:
        layer: select ports with GDS layer.
        prefix: select ports with prefix in port name.
        suffix: select ports with port name suffix.
        orientation: select ports with orientation in degrees.
        width: select ports with port width.
        layers_excluded: List of layers to exclude.
        port_type: select ports with port_type (optical, electrical, vertical_te).
        clockwise: if True, sort ports clockwise, False: counter-clockwise.
    """
    ports = component.get_ports_list(port_type=port_type, **kwargs)
    for port in ports:
        component.add_label(
            text=port.name,
            position=port.center,
            layer=label_layer if label_layer else port.layer,
        )

    return component


def add_labels_to_ports_x_y(
    component: Component,
    label_layer: LayerSpec | None = "TEXT",
    port_type: str | None = None,
    **kwargs,
) -> Component:
    """Add labels to component ports. Prepends -x-y coordinates

    Args:
        component: to add labels.
        label_layer: layer spec for the label. None will use the port layer.
        port_type: to select ports.

    keyword Args:
        layer: select ports with GDS layer.
        prefix: select ports with prefix in port name.
        suffix: select ports with port name suffix.
        orientation: select ports with orientation in degrees.
        width: select ports with port width.
        layers_excluded: List of layers to exclude.
        port_type: select ports with port_type (optical, electrical, vertical_te).
        clockwise: if True, sort ports clockwise, False: counter-clockwise.
    """
    ports = component.get_ports_list(port_type=port_type, **kwargs)
    for port in ports:
        x, y = port.center
        component.add_label(
            text=f"{port.name}/{int(x)}/{int(y)}",
            position=port.center,
            layer=label_layer if label_layer else port.layer,
        )

    return component


add_labels_to_ports_electrical = partial(
    add_labels_to_ports,
    port_type="electrical",
)
add_labels_to_ports_optical = partial(
    add_labels_to_ports,
    port_type="optical",
)
add_labels_to_ports_vertical_dc = partial(
    add_labels_to_ports,
    port_type="vertical_dc",
)
add_labels_to_ports_opt = partial(add_labels_to_ports, prefix="opt", port_type=None)


def get_labels(
    component: ComponentOrReference,
    get_label_function: Callable = get_input_label_electrical,
    layer_label: LayerSpec = "TEXT",
    gc: Component | None = None,
    component_name: str | None = None,
    **kwargs,
) -> list[Label]:
    """Returns component labels on ports.

    Args:
        component: to add labels to.
        get_label_function: function to get label.
        layer_label: layer_label.
        gc: Optional grating coupler.
        component_name: optional component name.

    keyword Args:
        layer: port GDS layer.
        prefix: look for prefix in port name.
        suffix: select ports with port name suffix.
        orientation: in degrees.
        width: for ports to add label.
        layers_excluded: List of layers to exclude.
        port_type: optical, electrical, ...
        clockwise: if True, sort ports clockwise, False: counter-clockwise.

    Returns:
        list of component labels.
    """
    labels = []
    ports = component.get_ports_list(**kwargs)
    component_name = component_name or component.name

    for i, port in enumerate(ports):
        label = get_label_function(
            port=port,
            gc=gc,
            gc_index=i,
            component_name=component_name,
            layer_label=layer_label,
        )
        labels.append(label)

    return labels


if __name__ == "__main__":
    # c = gf.components.mzi_phase_shifter()
    # add_labels_ports(c, c.get_ports_list(port_type="electrical"), prefix="pad_")
    # from gdsfactory.tests.test_labels import test_add_labels_electrical
    # c = test_add_labels_optical()
    # c = test_add_labels_electrical()
    # c = gf.routing.add_fiber_single(c)

    c = gf.components.pad(decorator=add_labels_to_ports_vertical_dc)
    c.show(show_ports=True)
