#!/usr/bin/env bash
# Compare a layout against its schematic with the sky130 KLayout LVS deck (sky130.lvs).
#
# Usage: scripts/run_lvs.sh <layout.gds> <top_cell> <schematic.sch | netlist.spice> [out_dir]
#   An xschem .sch is netlisted first in LVS mode (scripts/lvs_netlist.sh).
#   default out_dir: lvs/ next to the GDS. Writes <top_cell>.lvsdb (open it in KLayout:
#   Tools > Netlist Browser) and <top_cell>_extracted.cir, the netlist read from the layout.
#   Exit status 0 means the netlists match.
#
# Needs KLayout, xschem (for .sch input) and the sky130A PDK at $PDK_ROOT (default ~/pdk).
set -euo pipefail

[ $# -ge 3 ] || { sed -n '2,11p' "$0"; exit 2; }
here=$(cd "$(dirname "$0")" && pwd)
gds=$(realpath "$1")
top=$2
src=$(realpath "$3")
out=$(realpath -m "${4:-$(dirname "$gds")/lvs}")
deck="${PDK_ROOT:-$HOME/pdk}/sky130A/libs.tech/klayout/lvs/sky130.lvs"
mkdir -p "$out"

if [[ $src == *.sch ]]; then
  net="$out/${top}_schematic.spice"
  "$here/lvs_netlist.sh" "$src" "$net"
else
  net=$src
fi

echo "LVS: $gds (cell $top) vs $net"
set +e
klayout -b -r "$deck" \
  -rd input="$gds" -rd top_cell="$top" -rd schematic="$net" \
  -rd report="$out/$top.lvsdb" -rd target_netlist="$out/${top}_extracted.cir" \
  -rd run_mode=deep -rd thr="$(nproc)" \
  -rd spice_net_names=true -rd spice_comments=false -rd scale=false -rd verbose=false \
  -rd schematic_simplify=false -rd net_only=false -rd top_lvl_pins=true \
  -rd combine=false -rd purge=false -rd purge_nets=false \
  > "$out/${top}_lvs.log" 2>&1
status=$?
set -e
grep -E "Netlists (don't )?match|ERROR" "$out/${top}_lvs.log" | sed 's/^/  /' || tail -20 "$out/${top}_lvs.log"
exit $status
