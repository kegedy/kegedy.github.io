#!/usr/bin/env bash
# Netlist an xschem schematic for LVS: the top level becomes a .subckt with its pins,
# simulation-only lines and device parameters (code blocks, ad/as/pd/ps/nrd/nrs/sa/sb/sd)
# are dropped, leaving what LVS compares (device type, W, L, multiplier), W/L get an explicit
# micron suffix (KLayout reads bare numbers as metres), MIM caps are written the way the
# LVS deck compares them (area and perimeter), and 0 V sources
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
python3 "$(dirname "$0")/lvs_fix.py" "$tmp/$name.spice" "$out"
echo "wrote $out"
