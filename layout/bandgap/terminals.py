"""Find where each device terminal's metal is, using the sky130 LVS deck itself.

Each device cell is extracted on its own with scripts/run_lvs.sh; the resulting LVS database
says which shapes belong to which terminal. That way the router never has to guess at the
PDK generators' geometry.

Returns {cell name: {terminal: {layer: kdb.Region}}} in the cell's own coordinates (dbu),
with terminal names as the deck uses them: MOS S/G/D/B, PNP C/B/E, resistor A/B,
MIM cap A/B.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

import klayout.db as kdb

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
from lvs_fix import convert  # noqa: E402

LAYERS = {"67/20": "li", "68/20": "met1", "69/20": "met2", "70/20": "met3", "71/20": "met4"}


def _netlist_line(model):
    prefix = model.split()[0]
    if "fet" in prefix:
        return f"XM1 D G S B {model} nf=1 m=1"
    if "res" in prefix:
        return f"XR1 P M B {model} mult=1 m=1"
    if "cap" in prefix:
        return f"XC1 T B {model} MF=1 m=1"
    return f"XQ1 C BASE E {model} m=1"


def extract(layout, cells, models):
    """cells: {name: kdb.Cell}; models: {name: LVS model line (devices.DEVICES[...][3])}."""
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for name, cell in cells.items():
            gds = tmp / f"{name}.gds"
            lay = kdb.Layout()
            lay.dbu = layout.dbu
            lay.create_cell(name).copy_tree(cell)
            lay.write(str(gds))
            net = tmp / f"{name}.spice"
            net.write_text(convert(f".subckt {name}\n{_netlist_line(models[name])}\n.ends\n"))
            r = subprocess.run([REPO / "scripts/run_lvs.sh", gds, name, net, tmp / "lvs"],
                               capture_output=True, text=True)
            if r.returncode != 0:
                raise RuntimeError(f"{name}: device LVS failed, can't trust its terminals\n{r.stdout}")
            lvs = kdb.LayoutVsSchematic()
            lvs.read(str(tmp / "lvs" / f"{name}.lvsdb"))
            circuit = lvs.netlist().circuit_by_name(name)
            layers = {LAYERS[str(lvs.layer_info(i))]: lvs.layer_by_index(i)
                      for i in lvs.layer_indexes() if str(lvs.layer_info(i)) in LAYERS}
            terms = {}
            for dev in circuit.each_device():
                for t in dev.device_class().terminal_definitions():
                    n = dev.net_for_terminal(t.id())
                    if n is None:
                        continue
                    shapes = {lay_name: lvs.shapes_of_net(n, reg, True) for lay_name, reg in layers.items()}
                    terms[t.name] = {k: v for k, v in shapes.items() if not v.is_empty()}
            out[name] = terms
    return out
