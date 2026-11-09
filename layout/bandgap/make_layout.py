"""Place the bandgap's devices into gds/bandgap.gds (top cell BANDGAP).

Every device in xschem/bandgap_core.sch is placed in a floorplan, then route.py wires every
net from the schematic's LVS netlist and labels the pins VDD, VSS and VREF.

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

import re
import subprocess
import sys
import tempfile
from pathlib import Path

import klayout.db as kdb

import devices
import route
import terminals

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
PINS = ["VDD", "VSS", "VREF"]
# schematic pin order for each device kind -> the LVS deck's terminal names in the layout
ORDER = {"fet": ["D", "G", "S", "B"], "pnp": ["C", "B", "E"], "res": ["A", "B"], "cap": ["A", "B"]}


def schematic_nets():
    """{instance: (kind, {terminal: net})} from the same LVS netlist run_lvs.sh compares against."""
    with tempfile.TemporaryDirectory() as tmp:
        net = Path(tmp) / "bandgap_core.spice"
        subprocess.run([REPO / "scripts/lvs_netlist.sh", REPO / "xschem/bandgap_core.sch", net],
                       check=True, capture_output=True)
        lines = net.read_text().splitlines()
    out = {}
    for line in lines:
        tok = line.split()
        if not tok or not tok[0][0] in "XC" or tok[0].startswith("*"):
            continue
        model = next((t for t in tok if t.startswith("sky130_fd_pr__")), None)
        if model is None:
            continue
        kind = ("fet" if "fet" in model else "pnp" if "pnp" in model else "res" if "res" in model else "cap")
        nets = tok[1:1 + {"fet": 4, "pnp": 3, "res": 2, "cap": 2}[kind]]
        name = tok[0][1:] if tok[0][0] == "X" else tok[0]
        # parallel PNP units: lvs_fix.py writes xschem's m=N as the emitter count NE=N
        m = re.search(r"\bNE=(\d+)", line) or re.search(r"\bm=(\d+)", line)
        mult = int(m.group(1)) if m and kind == "pnp" else 1
        names = [name] if mult == 1 else [f"{name}_{k}" for k in range(1, mult + 1)]
        for n in names:
            out[n] = (kind, dict(zip(ORDER[kind], nets)))
    return out


def main(out):
    layout, cells = devices.build()
    top = layout.create_cell("BANDGAP")
    text = layout.layer(*TEXT)
    placed = {}
    insts = {}

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
        insts[inst] = (cell_name, t)
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

    # ---- wiring ----
    nets = schematic_nets()
    missing = set(nets) ^ set(insts)
    if missing:
        raise RuntimeError(f"schematic and layout instances differ: {sorted(missing)}")
    models = {name: m for name, _, _, m in devices.DEVICES}
    terms = terminals.extract(layout, cells, models)
    router = route.Router(layout, top)
    shapes = {}     # {layer: {net: Region}} of device metal, for obstacles
    access = []     # (net, terminal shapes in top coordinates)
    for inst, (kind, tnets) in sorted(nets.items()):
        cell_name, t = insts[inst]
        tdbu = kdb.ICplxTrans(t.to_itrans(layout.dbu))
        for term, net in tnets.items():
            ts = {lay: reg.transformed(tdbu) for lay, reg in terms[cell_name][term].items()}
            for lay, reg in ts.items():
                shapes.setdefault(lay, {}).setdefault(net, kdb.Region())
                shapes[lay][net] += reg
            access.append((inst, term, net, ts))
    router.add_obstacles(shapes)
    for inst, term, net, ts in access:
        try:
            router.access(net, ts)
        except RuntimeError as e:
            raise RuntimeError(f"{inst}.{term}: {e}") from None
    order = sorted(router.pins, key=lambda n: (n in ("VDD", "VSS"), len(router.pins[n])))
    tries = router.route_all(order)
    router.write_shapes(sorted(router.routes))   # every net, so extraction keeps schematic names

    layout.write(str(out))
    b = top.dbbox()
    nwire = sum(len(p) for ps in router.routes.values() for p in ps)
    print(f"wrote {out}: BANDGAP {b.width():.1f} x {b.height():.1f} um = {b.area() / 1e6:.4f} mm2, "
          f"{len(placed)} devices, {len(router.routes)} nets routed ({nwire} grid steps, attempt {tries})")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "gds" / "bandgap.gds")
