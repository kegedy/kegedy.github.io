#!/usr/bin/env bash
# Run every bandgap test in ngspice and write results to sim/bandgap/out/.
#
# Usage: sim/bandgap/run_all.sh
# Needs xschem, ngspice and the sky130A PDK at $PDK_ROOT (default ~/pdk).
# Afterwards, sim/bandgap/plot.py turns out/*.dat into the plots on the website.
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../.." && pwd)
export PDK_ROOT="${PDK_ROOT:-$HOME/pdk}"
lib="$PDK_ROOT/sky130A/libs.tech/combined/sky130.lib.spice"  # the model set xschem uses
cd "$here"
mkdir -p out

# 1. Netlist the testbench with xschem and keep the core subcircuit, so the decks
#    always simulate exactly what is drawn in xschem/bandgap_core.sch.
(cd "$repo/xschem" && xschem --rcfile "$PDK_ROOT/sky130A/libs.tech/xschem/xschemrc" \
    -n -s -q -x -o "$here/out" bandgap_tb.sch > /dev/null 2>&1)
sed -n '/^\.subckt bandgap_core/,/^\.ends/p' out/bandgap_tb.spice > bandgap_core.spice
[ -s bandgap_core.spice ] || { echo "netlisting failed" >&2; exit 1; }

corner() { echo ".lib $lib $1" > corner.spice; }
run() {  # run <deck> [corner]
  corner "${2:-tt}"
  ngspice -b "$1.spice" > "out/$1${2:+_$2}.log" 2>&1
  grep -E '^(v\(|-i\(|offset|power|vmax|vmin|v27|tc_ppm|line|vdd_min|psrr|t_settle|v_final|dc_gain|ugf|pm|vn_1k|onoise_total|mu|sigma)' \
    "out/$1${2:+_$2}.log" | sed "s/^/  /" || true
}

for deck in op temp line psrr startup loop noise; do
  echo "== $deck"; run "$deck"
done

# 2. Process corners: temperature sweep at each corner
for c in tt ss ff sf fs; do
  echo "== temp @ $c"; run temp "$c"; cp out/temp.dat "out/temp_$c.dat"
done
cp out/temp_tt.dat out/temp.dat

# 3. Monte Carlo mismatch
echo "== mc"; run mc tt_mm

corner tt
echo "done: logs and data in $here/out (plots: python3 $here/plot.py)"
