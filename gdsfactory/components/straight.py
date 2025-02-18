"""Straight waveguide."""
from __future__ import annotations

from collections.abc import Callable

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.cross_section import CrossSectionSpec


@gf.cell
def straight(
    length: float = 10.0,
    npoints: int = 2,
    layer: gf.typings.LayerSpec | None = None,
    width: float | None = None,
    add_pins: bool = True,
    cross_section: CrossSectionSpec = "xs_sc",
    add_bbox: Callable | None = None,
) -> Component:
    """Returns a Straight waveguide.

    Args:
        length: straight length (um).
        npoints: number of points.
        layer: layer to use. Defaults to cross_section.layer.
        width: width to use. Defaults to cross_section.width.
        add_pins: add pins to the component.
        cross_section: specification (CrossSection, string or dict).
        add_bbox: function to add bounding box to the component.

    .. code::

        o1 -------------- o2
                length
    """

    p = gf.path.straight(length=length, npoints=npoints)
    x = gf.get_cross_section(cross_section)

    if layer or width:
        x = x.copy(layer=layer or x.layer, width=width or x.width)

    c = Component()
    path = p.extrude(x)
    ref = c << path
    c.add_ports(ref.ports)

    if add_bbox:
        add_bbox(c)
    else:
        x.add_bbox(c, right=0, left=0)
    if add_pins:
        x.add_pins(c)
    c.info["length"] = length
    c.info["width"] = x.sections[0].width
    c.info["cross_section"] = cross_section

    c.add_route_info(cross_section=x, length=length)
    c.absorb(ref)
    return c


if __name__ == "__main__":
    import gdsfactory as gf

    # xs = gf.cross_section.pn()
    # xs = xs.mirror()
    # c = straight(cross_section=xs, info=dict(simulation="eme"))
    # print(c.info["simulation"])
    c = straight(length=0)
    c.show()
    print(c.bbox)
    # c._repr_html_()
    # c.show()
    c.show(show_ports=True)
    print(c.bbox)
