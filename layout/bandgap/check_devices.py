"""DRC and LVS every device cell on its own: python check_devices.py <out_dir> [cell ...]"""
import subprocess
import sys
from pathlib import Path

import klayout.db as kdb

import devices

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
from lvs_fix import convert  # noqa: E402  same rewriting as scripts/lvs_netlist.sh
out = Path(sys.argv[1]).resolve()
out.mkdir(parents=True, exist_ok=True)
names = sys.argv[2:] or None
layout, cells = devices.build(names)
for name, _, _, model in devices.DEVICES:
    if name not in cells:
        continue
    gds = out / f"{name}.gds"
    lay = kdb.Layout()
    lay.dbu = layout.dbu
    c = lay.create_cell(name)
    c.copy_tree(cells[name])
    lay.write(str(gds))
    prefix = model.split()[0]
    if "fet" in prefix:
        line = f"XM1 D G S B {model} nf=1 m=1"
    elif "res" in prefix:
        line = f"XR1 P M B {model} mult=1 m=1"
    elif "cap" in prefix:
        line = f"XC1 T B {model} MF=1 m=1"
    else:
        line = f"XQ1 C BASE E {model} m=1"
    (out / f"{name}.spice").write_text(convert(f".subckt {name}\n{line}\n.ends\n"))
    drc = subprocess.run([REPO / "scripts/run_drc.sh", gds, name, out / "drc"], capture_output=True, text=True)
    lvs = subprocess.run([REPO / "scripts/run_lvs.sh", gds, name, out / f"{name}.spice", out / "lvs"],
                         capture_output=True, text=True)
    d = drc.stdout.strip().splitlines()[1:] or [drc.stderr.strip()[-200:]]
    print(f"{name:22s} DRC: {d[0]:40s} LVS: {'match' if lvs.returncode == 0 else 'MISMATCH'}")
    for extra in d[1:4]:
        print(" " * 28, extra)
