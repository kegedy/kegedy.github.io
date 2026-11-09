"""Place the bandgap's devices into gds/bandgap.gds (top cell BANDGAP).

First pass: every device in xschem/bandgap_core.sch is placed in a floorplan, but nothing is
wired yet, so DRC applies and LVS does not.

  Top row     PMOS: mirror M1-M3 and bias mirror M12 side by side (matched), amp load
              M7/M8, start-up pull-up M9
  Middle row  NMOS: amp input pair M5/M6 side by side, tail M4 and bias diode M13,
              start-up M10/M11
  Resistor band  RCA/RCB laid on their side, one above the other (matched pair), with
              R2 and R1 on their side beside them
  Bottom row  Q1-Q2 as a 3 x 3 common-centroid array (Q1 in the centre, the eight Q2
              units around it), Q3 beside it, and the MIM compensation cap

Usage: ~/.venvs/sky130-pcells/bin/python layout/bandgap/make_layout.py [out.gds]
"""

import sys
from pathlib import Path

import klayout.db as kdb

import devices

REPO = Path(__file__).resolve().parents[2]
GAP = 2.0       # um between neighbouring devices (clears n-well and tap spacing rules)
ROW_GAP = 4.0   # um between rows, left free for routing
PNP_PITCH = 8.0  # um, 3 x 3 PNP array

# (instance, device cell) in schematic order within each row
PMOS_ROW = [("M1", "PMOS_LVT_8x4"), ("M2", "PMOS_LVT_8x4"), ("M3", "PMOS_LVT_8x4"),
            ("M12", "PMOS_LVT_8x4"), ("M7", "PMOS_LVT_4x4"), ("M8", "PMOS_LVT_4x4"),
            ("M9", "PMOS_0p42x8")]
NMOS_ROW = [("M5", "NMOS_LVT_16x4"), ("M6", "NMOS_LVT_16x4"), ("M4", "NMOS_8x4"),
            ("M13", "NMOS_8x4"), ("M10", "NMOS_1x1"), ("M11", "NMOS_0p42x1")]
TEXT = (83, 44)  # sky130 text.drawing: instance names, ignored by DRC and LVS


def main(out):
    layout, cells = devices.build()
    top = layout.create_cell("BANDGAP")
    text = layout.layer(*TEXT)
    placed = {}

    def place(inst, cell_name, x, y, rot=0):
        """Put the cell's (rotated by rot degrees) bounding box lower-left corner at (x, y) um."""
        cell = cells[cell_name]
        b = cell.dbbox().transformed(kdb.DCplxTrans(1, rot, False, 0, 0))
        t = kdb.DCplxTrans(1, rot, False, x - b.left, y - b.bottom)
        b = cell.dbbox()
        top.insert(kdb.DCellInstArray(cell.cell_index(), t))
        bb = b.transformed(t)
        top.shapes(text).insert(kdb.DText(inst, kdb.DTrans(bb.center())))
        placed[inst] = bb
        return bb

    def row(items, y):
        x = 0.0
        height = 0.0
        for inst, name in items:
            bb = place(inst, name, x, y)
            x = bb.right + GAP
            height = max(height, bb.height())
        return y + height

    # Bottom row: PNP array, Q3, cap
    q2 = iter(range(1, 9))
    for r in range(3):
        for c in range(3):
            inst = "Q1" if (r, c) == (1, 1) else f"Q2_{next(q2)}"
            place(inst, "PNP_3p40", c * PNP_PITCH, r * PNP_PITCH)
    x = 3 * PNP_PITCH + GAP
    place("Q3", "PNP_3p40", x, PNP_PITCH)
    place("C1", "MIM_30x30", placed["Q3"].right + 2 * GAP, 0.0)
    y = max(b.top for b in placed.values()) + ROW_GAP

    # Resistor band: everything on its side; RCA above RCB, then R2 and R1
    rcb = place("RCB", "RES_XH_2p85_L60", 0.0, y, 90)
    rca = place("RCA", "RES_XH_2p85_L60", 0.0, rcb.top + GAP, 90)
    x = rca.right + GAP
    place("R2", "RES_XH_0p35_L17p77", x, y, 90)
    place("R1", "RES_XH_0p35_L2", placed["R2"].right + GAP, y, 90)
    y = max(b.top for b in placed.values()) + ROW_GAP

    # Middle and top rows
    y = row(NMOS_ROW, y) + ROW_GAP
    row(PMOS_ROW, y)

    layout.write(str(out))
    b = top.dbbox()
    print(f"wrote {out}: BANDGAP {b.width():.1f} x {b.height():.1f} um = {b.area() / 1e6:.4f} mm2, "
          f"{len(placed)} devices")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "gds" / "bandgap.gds")
