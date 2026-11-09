#!/usr/bin/env bash
# Post-layout simulation: extract parasitics from gds/bandgap.gds and rerun the test decks
# on the extracted netlist, then compare with the schematic results.
#
# Usage: sim/bandgap/pex/run_pex.sh [--extract]
#   --extract  rerun the parasitic extraction (about 6 minutes) into bandgap_pex.spice;
#              otherwise the committed netlist is used
#
# Extraction is KLayout-PEX (kpex, pip package klayout-pex) with its 2.5D engine in RC mode.
# kpex needs KLayout 0.30; the system klayout here is 0.28, so KPEX_KLAYOUT_EXE points at a
# newer one (default ~/opt/bin/klayout-0.30). Run sim/bandgap/run_all.sh first: this script
# compares against its results in sim/bandgap/out/.
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../../.." && pwd)
export PDK_ROOT="${PDK_ROOT:-$HOME/pdk}" PDK=sky130A
KPEX="${KPEX:-$HOME/.venvs/kpex/bin/kpex}"
export KPEX_KLAYOUT_EXE="${KPEX_KLAYOUT_EXE:-$HOME/opt/bin/klayout-0.30}"
lib="$PDK_ROOT/sky130A/libs.tech/combined/sky130.lib.spice"
cd "$here"
mkdir -p out

if [[ "${1:-}" == "--extract" || ! -f bandgap_pex.spice ]]; then
  tmp=$(mktemp -d)
  trap 'rm -rf "$tmp"' EXIT
  "$repo/scripts/lvs_netlist.sh" "$repo/xschem/bandgap_core.sch" "$tmp/sch.spice" > /dev/null
  sed -i 's/^\.subckt bandgap_core /.subckt BANDGAP /' "$tmp/sch.spice"
  # --check n: kpex's own schematic check misreads xschem's micron units and NE; full LVS
  # with scripts/run_lvs.sh is the real comparison
  echo "== extracting (kpex 2.5D, RC)"
  "$KPEX" extract --pdk sky130A --gds "$repo/gds/bandgap.gds" --schematic "$tmp/sch.spice" \
    --cell BANDGAP --2.5D --mode RC --check n --tool-version-checks warn \
    --out-dir "$tmp/run" > out/kpex.log 2>&1
  cp "$tmp/run/bandgap__BANDGAP/BANDGAP_k25d_pex_netlist.spice" bandgap_pex.spice
fi

# Bench: same sources as ../bench.spice, around the extracted subcircuit. Every routed net is
# labelled in the layout, so the extracted subcircuit has a port per net; the internal ones
# get nodes x1_<NET> here (for the DC starting guess and for op.spice's prints).
python3 - <<'EOF'
import re
text = open("bandgap_pex.spice").read().replace("\n+", " ")
ports = re.search(r"(?im)^\.subckt\s+BANDGAP\s+(.*)$", text).group(1).split()
node = {"VDD": "VDD", "VREF": "VREF", "VSS": "0", "sky130_gnd": "0"}
conn = " ".join(node.get(p, f"x1_{p}") for p in ports)
open("bench.spice", "w").write(f"""* Post-layout bench: ../bench.spice with the extracted layout in place of the schematic
.include corner.spice
.include bandgap_pex.spice
.param vdd=1.8
.param tr=10u
VSUP VDD 0 DC {{vdd}} AC 1 PWL(0 0 {{tr}} {{vdd}})
* ports: {' '.join(ports)}  (VSS and the substrate both to ground)
x1 {conn} BANDGAP
CL VREF 0 1p
.nodeset v(VREF)=1.2 v(x1_PB)=1.05 v(x1_A)=0.71 v(x1_B)=0.71
* rshunt: kpex leaves a few isolated tap pieces tied only by capacitors; 1e12 ohm to ground
* gives them a DC value without affecting the circuit
.option reltol=1e-5 rshunt=1e12
""")
EOF

corner() { echo ".lib $lib $1" > corner.spice; }
corner tt
for deck in op temp line psrr startup noise; do
  # op.spice probes internal nodes as x1.<node>; here they are the ports x1_<NODE>
  sed -E 's/x1\.([a-z0-9]+)/x1_\U\1/g' "../$deck.spice" > "$deck.spice"
  echo "== $deck"
  ngspice -b "$deck.spice" > "out/$deck.log" 2>&1
  grep -E '^(v\(|-i\(|offset|power|vmax|vmin|v27|tc_ppm|line|vdd_min|psrr|t_settle|v_final|onoise_total)' \
    "out/$deck.log" | sed 's/^/  /' || true
  if [[ $deck == temp ]]; then sort -g -u out/temp_lo.dat out/temp_hi.dat > out/temp_tt.dat; fi
done
for c in ss ff sf fs; do
  corner "$c"; echo "== temp @ $c"; ngspice -b temp.spice > "out/temp_$c.log" 2>&1
  grep -E '^(v27|tc_ppm)' "out/temp_$c.log" | sed 's/^/  /' || true
  sort -g -u out/temp_lo.dat out/temp_hi.dat > "out/temp_$c.dat"
done
corner tt

python3 - <<'EOF'
import re
def get(path, key):
    try:
        m = re.search(rf"(?m)^{re.escape(key)}\s*=\s*([-0-9.eE+]+)", open(path).read())
        return float(m.group(1)) if m else None
    except FileNotFoundError:
        return None
rows = [("VREF at 27 C (V)", "op", "v(vref)", 1), ("Supply current (uA)", "op", "-i(vsup)", 1e6),
        ("Amplifier offset (mV)", "op", "offset_mv", 1), ("TC (ppm/C)", "temp", "tc_ppm", 1),
        ("Line regulation (mV/V)", "line", "line_mv_per_v", 1), ("Minimum VDD (V)", "line", "vdd_min", 1),
        ("PSRR at 10 kHz (dB)", "psrr", "psrr_10k", 1), ("PSRR at 1 MHz (dB)", "psrr", "psrr_1meg", 1),
        ("Start-up settle (us)", "startup", "t_settle", 1e6), ("Output noise (uV rms)", "noise", "onoise_total", 1e6)]
print(f"\n{'':26s}{'schematic':>12s}{'layout':>12s}")
for name, deck, key, k in rows:
    s, l = get(f"../out/{deck}.log", key), get(f"out/{deck}.log", key)
    fmt = lambda v: "-" if v is None else f"{v * k:12.4g}"
    print(f"{name:26s}{fmt(s)}{fmt(l)}")
EOF
echo "done: logs in $here/out"
