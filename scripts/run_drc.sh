#!/usr/bin/env bash
# Run the sky130 KLayout DRC deck (sky130A_mr.drc, manufacturing rules) on a GDS file.
#
# Usage: scripts/run_drc.sh <layout.gds> [top_cell] [out_dir]
#   default out_dir: drc/ next to the GDS. Writes <top_cell>_drc.lyrdb, which you can open
#   in KLayout (Tools > Marker Browser > File > Open) to step through each violation.
#
# Needs KLayout and the sky130A PDK at $PDK_ROOT (default ~/pdk).
# Set FEOL/BEOL/OFFGRID/FLOATING_MET=false to skip a rule group (all on by default,
# floating-metal checks off).
set -euo pipefail

[ $# -ge 1 ] || { sed -n '2,10p' "$0"; exit 2; }
gds=$(realpath "$1")
top=${2:-}
out=$(realpath -m "${3:-$(dirname "$gds")/drc}")
deck="${PDK_ROOT:-$HOME/pdk}/sky130A/libs.tech/klayout/drc/sky130A_mr.drc"
name=${top:-$(basename "${gds%.gds}")}
report="$out/${name}_drc.lyrdb"
mkdir -p "$out"

args=(-b -r "$deck" -rd input="$gds" -rd report="$report"
      -rd feol="${FEOL:-true}" -rd beol="${BEOL:-true}"
      -rd offgrid="${OFFGRID:-true}" -rd floating_met="${FLOATING_MET:-false}")
[ -n "$top" ] && args+=(-rd top_cell="$top")

echo "DRC: $gds${top:+ (cell $top)}"
klayout "${args[@]}" > "$out/${name}_drc.log" 2>&1 || { tail -20 "$out/${name}_drc.log"; exit 1; }

# Summarize the marker database: violations per rule
python3 - "$report" <<'PY'
import sys
import xml.etree.ElementTree as ET
from collections import Counter

root = ET.parse(sys.argv[1]).getroot()
desc = {c.findtext("name"): (c.findtext("description") or "") for c in root.iter("category")}
hits = Counter(i.findtext("category").strip("'") for i in root.iter("item"))
if not hits:
    print("DRC clean: 0 violations")
    sys.exit(0)
print(f"{sum(hits.values())} violations in {len(hits)} rules:")
for rule, n in hits.most_common():
    print(f"  {n:6d}  {rule:20s} {desc.get(rule, '')[:70]}")
sys.exit(1)
PY
