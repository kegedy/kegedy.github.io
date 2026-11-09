#!/usr/bin/env python3
"""Rewrite an xschem SPICE netlist for the KLayout sky130 LVS deck.

Usage: python3 scripts/lvs_fix.py <in.spice> <out.spice>   (used by lvs_netlist.sh)
"""
import re
import sys

def convert(text):
    """Return an xschem SPICE netlist rewritten for the KLayout sky130 LVS deck."""
    text = text.replace("\n+", " ")             # join continuation lines
    text = re.sub(r"(?ms)^\.control.*?^\.endc\n", "", text)        # control blocks
    text = re.sub(r"(?m)^\*\*(\.subckt|\.ends)", r"\1", text)        # top level as a subcircuit
    for a, b in re.findall(r"(?m)^V\S*\s+(\S+)\s+(\S+)\s+0\s*$", text):  # 0 V probe: short b to a
        text = re.sub(rf"(?<=\s){re.escape(b)}(?=\s|$)", a, text)
    text = re.sub(r"(?m)^V\S*\s+(\S+)\s+\1\s+0\s*\n", "", text)
    lines = [l for l in text.splitlines()
             if not re.match(r"\.(save|lib|param|temp|include|option)", l, re.I)]
    sim_only = r"\s(ad|as|pd|ps|nrd|nrs|sa|sb|sd)=\S+"
    lines = [re.sub(sim_only, "", l, flags=re.I) for l in lines]
    # xschem writes sky130 sizes in microns without units; KLayout reads bare numbers as metres
    lines = [re.sub(r"(?i)\b([WL])=([0-9.]+)(?=\s|$)", r"\1=\2u", l) if re.match(r"(?i)X\S*\s.*sky130_fd_pr__", l) else l
             for l in lines]
    # MIM caps: the LVS deck extracts them as sky130_fd_pr__model__cap_mim(_m4) capacitors and
    # compares area and perimeter, so write them as C elements with A = W*L and P = 2(W+L)
    MIM = {"cap_mim_m3_1": "model__cap_mim", "cap_mim_m3_2": "model__cap_mim_m4"}
    def mim(l):
        m = re.match(r"(?i)X(C\S*)\s+(\S+)\s+(\S+)\s+sky130_fd_pr__(cap_mim_m3_[12])\s+(.*)", l)
        if not m:
            return l
        name, a, b, kind, rest = m.groups()
        p = {k.upper(): float(v.rstrip("u")) for k, v in re.findall(r"(\w+)=([0-9.eE+-]+u?)", rest)}
        w, ln, mf = p["W"], p["L"], int(p.get("MF", 1))
        return f"{name} {a} {b} sky130_fd_pr__{MIM[kind]} A={w * ln:g}p P={2 * (w + ln):g}u m={mf}"
    lines = [mim(l) for l in lines]
    # Parallel bipolars: LVS combines the layout's units into one device with NE emitters,
    # but reads xschem's m=N as a single emitter, so write the count as NE
    def bjt(l):
        m = re.match(r"(?i)(X\S+\s.*sky130_fd_pr__(?:pnp|npn)_\S+)\s+m=(\d+)\s+mult=\d+(.*)", l)
        return f"{m.group(1)} NE={m.group(2)} m=1{m.group(3)}" if m and int(m.group(2)) > 1 else l
    lines = [bjt(l) for l in lines]
    return "\n".join(lines) + "\n"

if __name__ == "__main__":
    open(sys.argv[2], "w").write(convert(open(sys.argv[1]).read()))
