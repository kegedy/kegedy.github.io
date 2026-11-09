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
python3 make_sat.py   # saturation deck covers every MOSFET in the schematic

corner() { echo ".lib $lib $1" > corner.spice; }
run() {  # run <deck> [corner]
  corner "${2:-tt}"
  ngspice -b "$1.spice" > "out/$1${2:+_$2}.log" 2>&1
  grep -E '^(v\(|-i\(|offset|power|vmax|vmin|v27|tc_ppm|line|vdd_min|psrr|t_settle|v_final|dc_gain|ugf|pm|vn_1k|onoise_total|mu|sigma|sat|VDD =)' \
    "out/$1${2:+_$2}.log" | sed "s/^/  /" || true
}

for deck in op temp line psrr startup loop noise sat; do
  echo "== $deck"; run "$deck"
done

# 2. Process corners: temperature sweep at each corner
for c in tt ss ff sf fs; do
  echo "== temp @ $c"; run temp "$c"
  sort -g -u out/temp_lo.dat out/temp_hi.dat > "out/temp_$c.dat"
done
cp out/temp_tt.dat out/temp.dat

# 3. Saturation check at the temperature extremes
corner tt
for t in -40 125; do
  echo "== sat @ $t C"
  sed "s/^\.include bench.spice/.include bench.spice\n.temp $t/" sat.spice > sat_t.spice
  ngspice -b sat_t.spice > "out/sat_$t.log" 2>&1
  grep -E '^sat' "out/sat_$t.log" | sed "s/^/  /"
done
rm -f sat_t.spice

# 4. Monte Carlo mismatch
echo "== mc"; run mc tt_mm

corner tt
echo "done: logs and data in $here/out (plots: python3 $here/plot.py)"
