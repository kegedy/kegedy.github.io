"""Generate gds/example_inverter.gds, an illustrative (not DRC-clean) sky130 inverter.

Usage: python kweb/make_example_gds.py
"""

from pathlib import Path

import klayout.db as kdb

# sky130 (layer, datatype)
NWELL = (64, 20)
DIFF = (65, 20)
POLY = (66, 20)
LICON = (66, 44)
LI1 = (67, 20)
MCON = (67, 44)
MET1 = (68, 20)
NSDM = (93, 44)
PSDM = (94, 20)

layout = kdb.Layout()
layout.dbu = 0.001
top = layout.create_cell("INVERTER")


def box(layer, x1, y1, x2, y2):
    top.shapes(layout.layer(*layer)).insert(kdb.DBox(x1, y1, x2, y2))


def contacts(layer, x, y1, y2, size=0.17, pitch=0.34):
    y = y1
    while y + size <= y2:
        box(layer, x - size / 2, y, x + size / 2, y + size)
        y += pitch


# NMOS (W=1.0) and PMOS (W=2.0)
box(DIFF, 0.0, 0.5, 1.2, 1.5)
box(NSDM, -0.13, 0.37, 1.33, 1.63)
box(NWELL, -0.4, 2.1, 1.6, 5.0)
box(DIFF, 0.0, 2.5, 1.2, 4.5)
box(PSDM, -0.13, 2.37, 1.33, 4.63)

# Shared gate
box(POLY, 0.525, 0.3, 0.675, 4.7)
box(POLY, 0.3, 1.8, 0.675, 2.2)
box(LICON, 0.4, 1.915, 0.57, 2.085)
box(LI1, -0.6, 1.85, 0.62, 2.15)

# Sources to rails, drains tied to output
for y1, y2 in ((0.5, 1.5), (2.5, 4.5)):
    contacts(LICON, 0.2, y1 + 0.1, y2)
    contacts(LICON, 1.0, y1 + 0.1, y2)
box(LI1, 0.1, 0.0, 0.3, 1.5)
box(LI1, 0.1, 2.5, 0.3, 5.0)
box(LI1, 0.9, 0.5, 1.1, 4.5)
box(LI1, 0.9, 1.85, 1.8, 2.15)

# met1 rails
box(MET1, -0.3, -0.3, 1.5, 0.2)
box(MET1, -0.3, 4.8, 1.5, 5.3)
for x in (0.11, 0.45, 0.79, 1.13):
    box(MCON, x - 0.085, -0.135, x + 0.085, 0.035)
    box(MCON, x - 0.085, 4.965, x + 0.085, 5.135)
box(LI1, -0.3, -0.2, 1.5, 0.1)
box(LI1, -0.3, 4.9, 1.5, 5.2)

for text, layer, x, y in (
    ("VDD", MET1, 0.6, 5.05),
    ("GND", MET1, 0.6, -0.05),
    ("IN", LI1, -0.45, 2.0),
    ("OUT", LI1, 1.65, 2.0),
):
    top.shapes(layout.layer(*layer)).insert(kdb.DText(text, x, y))

out = Path(__file__).resolve().parent.parent / "gds" / "example_inverter.gds"
layout.write(str(out))
print(f"wrote {out}")
