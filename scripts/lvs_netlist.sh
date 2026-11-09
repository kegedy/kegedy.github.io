#!/usr/bin/env bash
# Netlist an xschem schematic for LVS: the top level becomes a .subckt with its pins,
# simulation-only lines and device parameters (code blocks, ad/as/pd/ps/nrd/nrs/sa/sb/sd)
# are dropped, leaving what LVS compares (device type, W, L, multiplier), and 0 V sources
# (test probes such as the bandgap's loop-break Vloop) become shorts.
#
# Usage: scripts/lvs_netlist.sh xschem/<name>.sch [out.spice]
#   default output: lvs/<name>.spice next to the schematic
set -euo pipefail

sch=$(realpath "$1")
name=$(basename "${sch%.sch}")
out=$(realpath -m "${2:-$(dirname "$sch")/lvs/$name.spice}")
rc="${PDK_ROOT:-$HOME/pdk}/sky130A/libs.tech/xschem/xschemrc"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

(cd "$(dirname "$sch")" && xschem --rcfile "$rc" -x -q -n -s -o "$tmp" \
   "$sch" > /dev/null 2>&1)
mkdir -p "$(dirname "$out")"
python3 - "$tmp/$name.spice" "$out" <<'PY'
import re
import sys

text = open(sys.argv[1]).read().replace("\n+", " ")             # join continuation lines
text = re.sub(r"(?ms)^\.control.*?^\.endc\n", "", text)        # control blocks
text = re.sub(r"(?m)^\*\*(\.subckt|\.ends)", r"\1", text)        # top level as a subcircuit
for a, b in re.findall(r"(?m)^V\S*\s+(\S+)\s+(\S+)\s+0\s*$", text):  # 0 V probe: short b to a
    text = re.sub(rf"(?<=\s){re.escape(b)}(?=\s|$)", a, text)
text = re.sub(r"(?m)^V\S*\s+(\S+)\s+\1\s+0\s*\n", "", text)
lines = [l for l in text.splitlines()
         if not re.match(r"\.(save|lib|param|temp|include|option)", l, re.I)]
sim_only = r"\s(ad|as|pd|ps|nrd|nrs|sa|sb|sd)=\S+"
open(sys.argv[2], "w").write("\n".join(re.sub(sim_only, "", l, flags=re.I) for l in lines) + "\n")
PY
echo "wrote $out"
