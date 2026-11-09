"""Device cells for the bandgap layout, drawn with the sky130 PDK's own KLayout generators.

Each schematic device type becomes one cell in a Layout, built by the PDK code in
$PDK_ROOT/sky130A/libs.tech/klayout/python/cells (the same generators behind KLayout's
SKY130 PCell menu). The PNP is the PDK's fixed GDS cell.

The generators target gdsfactory 8.1 (see layout/requirements.txt); newer releases changed
the API they use.
"""

import os
import sys
from pathlib import Path

PDK = Path(os.environ.get("PDK_ROOT", Path.home() / "pdk")) / "sky130A"
sys.path.insert(0, str(PDK / "libs.tech/klayout/python"))

import klayout.db as kdb  # noqa: E402
from cells.draw_cap import draw_mim_cap  # noqa: E402
from cells.draw_fet import draw_nfet, draw_pfet  # noqa: E402
from cells.res_poly_child import res_poly_draw  # noqa: E402

RES_EXTRA_L = 0.12
PNP_GDS = PDK / "libs.tech/klayout/python/cells/fixed_devices/bjt/pnp/sky130_fd_pr__pnp_05v5_W3p40L3p40.gds"


def _clean(layout):
    """Drop empty layers (the generators leave a placeholder layer 99999 that GDS can't store)."""
    for li in list(layout.layer_indexes()):
        if all(c.bbox_per_layer(li).empty() for c in layout.each_cell()):
            layout.delete_layer(li)


def fet(layout, name, kind, w, l, nf=1):
    """kind: nfet_01v8, nfet_01v8_lvt, pfet_01v8 or pfet_01v8_lvt. Bulk is tied with a tap."""
    cell = layout.create_cell(name)
    draw = draw_nfet if kind.startswith("nfet") else draw_pfet
    draw(cell, l=l, w=w, nf=nf, type=f"sky130_fd_pr__{kind}", bulk="bulk tie")
    return cell


def res_xhigh(layout, name, width, l):
    """width: one of 0p35, 0p69, 1p41, 2p85, 5p73 (the res_xhigh_po_* families)."""
    cell = layout.create_cell(name)
    w = float(width.replace("p", "."))
    # The generator draws the resistor body 0.12 um longer than asked (LVS measures it), so
    # ask for 0.12 um less to get the schematic's length
    l = l - RES_EXTRA_L
    res_poly_draw(f"sky130_fd_pr__res_xhigh_po_{width}").your_res(
        cell, l=l, w=w, type=f"sky130_fd_pr__res_xhigh_po_{width}", gr=0)
    return cell


def mim(layout, name, w, l):
    cell = layout.create_cell(name)
    draw_mim_cap(cell, l=l, w=w, type="sky130_fd_pr__model__cap_mim")
    return cell


def pnp(layout, name):
    src = kdb.Layout()
    src.read(str(PNP_GDS))
    top = src.top_cell()
    cell = layout.create_cell(name)
    cell.copy_tree(top)
    # The PDK cell carries text labels (Collector, Base, Emitter) that LVS would turn into
    # net names and pins in every PNP; the bandgap's own pin labels go on the top cell.
    for li in layout.layer_indexes():
        texts = [s for s in cell.shapes(li).each() if s.is_text()]
        for t in texts:
            cell.shapes(li).erase(t)
    return cell


# Every device type in xschem/bandgap_core.sch: (cell name, builder, args, LVS model line)
DEVICES = [
    ("PMOS_LVT_8x4", fet, ("pfet_01v8_lvt", 8, 4), "sky130_fd_pr__pfet_01v8_lvt L=4u W=8u"),
    ("PMOS_LVT_4x4", fet, ("pfet_01v8_lvt", 4, 4), "sky130_fd_pr__pfet_01v8_lvt L=4u W=4u"),
    ("PMOS_0p42x8", fet, ("pfet_01v8", 0.42, 8), "sky130_fd_pr__pfet_01v8 L=8u W=0.42u"),
    ("NMOS_LVT_16x4", fet, ("nfet_01v8_lvt", 16, 4), "sky130_fd_pr__nfet_01v8_lvt L=4u W=16u"),
    ("NMOS_8x4", fet, ("nfet_01v8", 8, 4), "sky130_fd_pr__nfet_01v8 L=4u W=8u"),
    ("NMOS_1x1", fet, ("nfet_01v8", 1, 1), "sky130_fd_pr__nfet_01v8 L=1u W=1u"),
    ("NMOS_0p42x1", fet, ("nfet_01v8", 0.42, 1), "sky130_fd_pr__nfet_01v8 L=1u W=0.42u"),
    ("RES_XH_0p35_L2", res_xhigh, ("0p35", 2), "sky130_fd_pr__res_xhigh_po_0p35 L=2u"),
    ("RES_XH_0p35_L17p77", res_xhigh, ("0p35", 17.77), "sky130_fd_pr__res_xhigh_po_0p35 L=17.77u"),
    ("RES_XH_2p85_L60", res_xhigh, ("2p85", 60), "sky130_fd_pr__res_xhigh_po_2p85 L=60u"),
    ("MIM_30x30", mim, (30, 30), "sky130_fd_pr__cap_mim_m3_1 W=30u L=30u"),
    ("PNP_3p40", pnp, (), "sky130_fd_pr__pnp_05v5_W3p40L3p40"),
]


def build(names=None):
    layout = kdb.Layout()
    layout.dbu = 0.001
    cells = {}
    for name, fn, args, _ in DEVICES:
        if names is None or name in names:
            cells[name] = fn(layout, name, *args)
    _clean(layout)
    return layout, cells


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "devices.gds")
    layout, cells = build()
    layout.write(str(out))
    for name, c in cells.items():
        b = c.dbbox()
        print(f"{name:22s} {b.width():7.2f} x {b.height():7.2f} um")
