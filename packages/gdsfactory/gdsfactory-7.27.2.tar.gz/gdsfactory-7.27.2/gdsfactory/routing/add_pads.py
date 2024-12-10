from __future__ import annotations

from collections.abc import Callable

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.pad import pad_rectangular
from gdsfactory.components.straight_heater_metal import straight_heater_metal
from gdsfactory.port import select_ports_electrical
from gdsfactory.routing.route_fiber_array import route_fiber_array
from gdsfactory.routing.sort_ports import sort_ports_x
from gdsfactory.typings import (
    ComponentSpec,
    CrossSectionSpec,
    LayerSpec,
    Strs,
)


@gf.cell_with_child
def add_pads_bot(
    component: ComponentSpec = straight_heater_metal,
    select_ports: Callable = select_ports_electrical,
    port_names: Strs | None = None,
    component_name: str | None = None,
    cross_section: CrossSectionSpec = "xs_metal_routing",
    get_input_labels_function: Callable | None = None,
    layer_label: LayerSpec = "TEXT",
    pad_port_name: str = "e1",
    pad_port_labels: tuple[str, ...] | None = None,
    pad: ComponentSpec = pad_rectangular,
    bend: ComponentSpec = "wire_corner",
    straight_separation: float = 20.0,
    pad_spacing: float | str = "pad_spacing",
    optical_routing_type: int | None = 1,
    with_loopback: bool = False,
    min_length: float | None = None,
    **kwargs,
) -> Component:
    """Returns new component with ports connected bottom pads.

    Args:
        component: component spec to connect to.
        select_ports: function to select_ports.
        port_names: optional port names. Overrides select_ports.
        component_name: optional for the label.
        cross_section: cross_section spec.
        get_input_labels_function: function to get input labels. None skips labels.
        layer_label: optional layer for grating coupler label.
        pad_port_name: pad input port name.
        pad_port_labels: pad list of labels.
        pad: spec for route terminations.
        bend: bend spec.
        straight_separation: from wire edge to edge.
        pad_spacing: in um. Defaults to pad_spacing constant from the PDK.
        optical_routing_type: None: auto, 0: no extension, 1: standard, 2: check.
        with_loopback: True, adds loopback structures.
        min_length: minimum length for the straight section.

    Keyword Args:
        straight: straight spec.
        taper: taper spec.
        get_input_label_text_loopback_function: function to get input label test.
        get_input_label_text_function: for labels.
        fanout_length: if None, automatic calculation of fanout length.
        max_y0_optical: in um.
        list_port_labels: None, adds TM labels to port indices in this list.
        connected_port_list_ids: names of ports only for type 0 optical routing.
        nb_optical_ports_lines: number of grating coupler lines.
        force_manhattan: False
        excluded_ports: list of port names to exclude when adding gratings.
        grating_indices: list of grating coupler indices.
        routing_straight: function to route.
        routing_method: get_route.
        gc_rotation: fiber coupler rotation in degrees. Defaults to -90.
        input_port_indexes: to connect.

    .. plot::
        :include-source:

        import gdsfactory as gf
        c = gf.c.nxn(
            xsize=600,
            ysize=200,
            north=2,
            south=3,
            wg_width=10,
            layer="M3",
            port_type="electrical",
        )
        cc = gf.routing.add_pads_bot(component=c, port_names=("e1", "e4"), fanout_length=50)
        cc.plot()

    """
    xs = gf.get_cross_section(cross_section)
    min_length = min_length or (xs.width / 2 + straight_separation)

    component_new = Component()
    component = gf.get_component(component)
    component_name = component_name or component.name

    pad_spacing = gf.get_constant(pad_spacing)
    cref = component_new << component
    ports = [cref[port_name] for port_name in port_names] if port_names else None
    ports = ports or select_ports(cref.ports)
    pad_component = gf.get_component(pad)
    if pad_port_name not in pad_component.ports:
        pad_ports = list(pad_component.ports.keys())
        raise ValueError(
            f"pad_port_name = {pad_port_name!r} not in {pad_component.name!r} ports {pad_ports}"
        )

    pad_orientation = int(pad_component[pad_port_name].orientation)
    if pad_orientation != 180:
        raise ValueError(
            f"port.orientation={pad_orientation} for port {pad_port_name!r} needs to be 180 degrees."
        )

    if not ports:
        raise ValueError(
            f"select_ports or port_names did not match any ports in {list(component.ports.keys())}"
        )

    (
        elements,
        pads,
        ports_grating_input_waveguide,
        ports_loopback,
        ports_component,
    ) = route_fiber_array(
        component=component,
        grating_coupler=pad,
        gc_port_name=pad_port_name,
        component_name=component_name,
        cross_section=cross_section,
        select_ports=select_ports,
        get_input_labels_function=get_input_labels_function,
        layer_label=layer_label,
        with_loopback=with_loopback,
        bend=bend,
        straight_separation=straight_separation,
        port_names=port_names,
        fiber_spacing=pad_spacing,
        optical_routing_type=optical_routing_type,
        min_length=min_length,
        **kwargs,
    )
    if len(elements) == 0:
        return component

    for e in elements:
        component_new.add(e)
    for i in pads:
        component_new.add(i)

    component_new.add_ref(component)

    for port in component.ports.values():
        if port not in ports_component:
            component_new.add_port(port.name, port=port)

    ports = sort_ports_x(ports_grating_input_waveguide + ports_loopback)

    if pad_port_labels:
        for gc_port_label, port in zip(pad_port_labels, ports):
            if layer_label:
                component_new.add_label(
                    text=gc_port_label, layer=layer_label, position=port.center
                )

    for i, pad in enumerate(pads[0]):
        component_new.add_port(f"pad_{i+1}", port=pad[pad_port_name])

    component_new.copy_child_info(component)
    return component_new


@gf.cell_with_child
def add_pads_top(
    component: ComponentSpec = straight_heater_metal, **kwargs
) -> Component:
    """Returns new component with ports connected top pads.

    Args:
        component: component spec to connect to.

    Keyword Args:
        select_ports: function to select_ports.
        port_names: optional port names. Overrides select_ports.
        component_name: optional for the label.
        cross_section: cross_section function.
        get_input_labels_function: function to get input labels. None skips labels.
        layer_label: optional layer for grating coupler label.
        pad_port_name: pad input port name.
        pad_port_labels: pad list of labels.
        pad: spec for route terminations.
        bend: bend spec.
        straight_separation: from edge to edge.
        straight: straight spec.
        taper: taper spec.
        get_input_label_text_loopback_function: function to get input label test.
        get_input_label_text_function: for labels.
        fanout_length: if None, automatic calculation of fanout length.
        max_y0_optical: in um.
        with_loopback: True, adds loopback structures.
        list_port_labels: None, adds TM labels to port indices in this list.
        connected_port_list_ids: names of ports only for type 0 optical routing.
        nb_optical_ports_lines: number of grating coupler lines.
        force_manhattan: False
        excluded_ports: list of port names to exclude when adding gratings.
        grating_indices: list of grating coupler indices.
        routing_straight: function to route.
        routing_method: get_route.
        optical_routing_type: None: auto, 0: no extension, 1: standard, 2: check.
        gc_rotation: fiber coupler rotation in degrees. Defaults to -90.
        input_port_indexes: to connect.

    .. plot::
        :include-source:

        import gdsfactory as gf
        c = gf.c.nxn(
            xsize=600,
            ysize=200,
            north=2,
            south=3,
            wg_width=10,
            layer="M3",
            port_type="electrical",
        )
        cc = gf.routing.add_pads_top(component=c, port_names=("e1", "e4"), fanout_length=50)
        cc.plot()

    """
    c = Component()
    _c = add_pads_bot(component=component, **kwargs)
    ref = c << _c
    ref.mirror_y()
    c.add_ports(ref.ports)
    c.copy_child_info(_c)
    return c


if __name__ == "__main__":
    # c = gf.components.pad()
    # c = gf.components.straight_heater_metal(length=100.0)
    # c = gf.components.straight(length=100.0)

    # cc = add_pads_top(component=c, port_names=("e1",))
    # cc = add_pads_top(component=c, port_names=("e1", "e2"), fanout_length=50)
    # c = gf.c.nxn(
    #     xsize=600,
    #     ysize=200,
    #     north=2,
    #     south=3,
    #     wg_width=10,
    #     layer="M3",
    #     port_type="electrical",
    # )
    c = gf.components.ring_single_heater(
        gap=0.2, radius=10, length_x=4, via_stack_offset=(2, 0)
    )
    cc = add_pads_bot(component=c, with_loopback=True, straight_to_grating_spacing=100)
    cc = gf.routing.add_fiber_array(cc)
    cc.pprint_ports()
    cc.show(show_ports=True)
