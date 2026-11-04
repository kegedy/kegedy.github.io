"""Generate gds/bjt.gds, an illustrative (not DRC-clean) sky130 vertical PNP.

The vertical PNP is built from layers every CMOS process already has: a p+ emitter
inside an n-well (the base, contacted through an n+ tap ring), with the p-substrate as
the collector (contacted through an outer p+ tap ring). Emitter is 3.4 x 3.4 um, like
sky130_fd_pr__pnp_05v5_W3p40L3p40.

Usage: python kweb/make_bjt.py
"""

from pathlib import Path

import klayout.db as kdb

# sky130 (layer, datatype)
NWELL = (64, 20)
DIFF = (65, 20)
TAP = (65, 44)
LICON = (66, 44)
LI1 = (67, 20)
MCON = (67, 44)
MET1 = (68, 20)
NSDM = (93, 44)
PSDM = (94, 20)

layout = kdb.Layout()
layout.dbu = 0.001
top = layout.create_cell("PNP")


def box(layer, x1, y1, x2, y2):
    top.shapes(layout.layer(*layer)).insert(kdb.DBox(x1, y1, x2, y2))


def ring(layer, x1, y1, x2, y2, w):
    """Square ring whose outer edge is (x1, y1, x2, y2) and width is w."""
    box(layer, x1, y1, x2, y1 + w)
    box(layer, x1, y2 - w, x2, y2)
    box(layer, x1, y1 + w, x1 + w, y2 - w)
    box(layer, x2 - w, y1 + w, x2, y2 - w)


def row(layer, x1, x2, y, size=0.17, pitch=0.34):
    """Contacts centred on y, spread evenly between x1 and x2."""
    n = int((x2 - x1 - size) / pitch) + 1
    start = (x1 + x2) / 2 - (n - 1) * pitch / 2
    for i in range(n):
        x = start + i * pitch
        box(layer, x - size / 2, y - size / 2, x + size / 2, y + size / 2)


def col(layer, x, y1, y2, size=0.17, pitch=0.34):
    n = int((y2 - y1 - size) / pitch) + 1
    start = (y1 + y2) / 2 - (n - 1) * pitch / 2
    for i in range(n):
        y = start + i * pitch
        box(layer, x - size / 2, y - size / 2, x + size / 2, y + size / 2)


def ring_contacts(layer, x1, y1, x2, y2, w):
    """Contacts down the middle of each side of a ring."""
    c = w / 2
    row(layer, x1 + w, x2 - w, y1 + c)
    row(layer, x1 + w, x2 - w, y2 - c)
    col(layer, x1 + c, y1 + w, y2 - w)
    col(layer, x2 - c, y1 + w, y2 - w)


# Emitter: p+ diffusion in the n-well, contacted by an array of licon
E = (0.0, 0.0, 3.4, 3.4)
box(DIFF, *E)
box(PSDM, E[0] - 0.125, E[1] - 0.125, E[2] + 0.125, E[3] + 0.125)
for y in (0.4, 0.9, 1.45, 1.95, 2.5, 3.0):
    row(LICON, 0.2, 3.2, y)
box(LI1, 0.1, 0.1, 3.3, 3.3)
for y in (0.6, 1.2, 1.7, 2.2, 2.8):
    row(MCON, 0.3, 3.1, y)
box(MET1, 0.1, 0.1, 3.3, 3.3)

# Base: n-well with an n+ tap ring
B = (-1.2, -1.2, 4.6, 4.6)
BW = 0.5
box(NWELL, -1.6, -1.6, 5.0, 5.0)
ring(TAP, *B, BW)
ring(NSDM, B[0] - 0.125, B[1] - 0.125, B[2] + 0.125, B[3] + 0.125, BW + 0.25)
ring_contacts(LICON, *B, BW)
ring(LI1, *B, BW)
ring_contacts(MCON, *B, BW)
ring(MET1, *B, BW)

# Collector: p-substrate, contacted by a p+ tap ring outside the well
C = (-2.6, -2.6, 6.0, 6.0)
CW = 0.5
ring(TAP, *C, CW)
ring(PSDM, C[0] - 0.125, C[1] - 0.125, C[2] + 0.125, C[3] + 0.125, CW + 0.25)
ring_contacts(LICON, *C, CW)
ring(LI1, *C, CW)
ring_contacts(MCON, *C, CW)
ring(MET1, *C, CW)

for text, x, y in (("E", 1.7, 1.7), ("B", 1.7, -0.95), ("C", 1.7, -2.35)):
    top.shapes(layout.layer(*MET1)).insert(kdb.DText(text, x, y))

out = Path(__file__).resolve().parent.parent / "gds" / "bjt.gds"
layout.write(str(out))
print(f"wrote {out}")
