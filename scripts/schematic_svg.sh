#!/usr/bin/env bash
# Export an xschem schematic to SVG for <SchematicViewer>, in xschem's own look.
#
# Usage: scripts/schematic_svg.sh xschem/<name>.sch [out.svg]
#   default output: static/schematics/<name>.svg
#
# Needs xschem, the sky130A PDK at $PDK_ROOT (default ~/pdk), and a display (WSLg/X11):
# without one xschem falls back to rough font metrics and right-aligned labels like
# input pin names overlap their pins.
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
sch=$(realpath "$1")
name=$(basename "${sch%.sch}")
out=$(realpath -m "${2:-$repo/static/schematics/$name.svg}")
rc="${PDK_ROOT:-$HOME/pdk}/sky130A/libs.tech/xschem/xschemrc"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

# Layers 15 and 17 hold the sky130 device symbols' simulation annotations
# (id=, gm=, vgs=, vds=), which only show placeholders without simulation data.
cat > "$tmp/export.tcl" <<EOF
set enable_layer(15) 0
set enable_layer(17) 0
xschem enable_layers
xschem zoom_full
xschem zoom_out
xschem print svg $tmp/out.svg
exit
EOF

(cd "$(dirname "$sch")" && xschem --rcfile "$rc" --script "$tmp/export.tcl" "$sch" > /dev/null 2>&1)

# xschem writes a fixed width/height; replace with a viewBox so the SVG scales and can be zoomed
mkdir -p "$(dirname "$out")"
python3 - "$tmp/out.svg" "$out" <<'EOF'
import re
import sys

svg = open(sys.argv[1]).read()
size = re.search(r'width="([\d.]+)" height="([\d.]+)"', svg)
svg = svg.replace(size.group(0), f'viewBox="0 0 {size.group(1)} {size.group(2)}"', 1)
open(sys.argv[2], "w").write(svg)
EOF
echo "wrote $out"
