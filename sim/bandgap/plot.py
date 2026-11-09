#!/usr/bin/env python3
"""Turn sim/bandgap/out/*.dat into the PNG plots on the website (docs/bandgap/img/).

Usage: python3 sim/bandgap/plot.py   (after run_all.sh)
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

here = Path(__file__).resolve().parent
out = here / "out"
img = here.parent.parent / "docs" / "bandgap" / "img"
img.mkdir(parents=True, exist_ok=True)

# Categorical slots in fixed order, plus surface/ink tokens
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False,
    "lines.linewidth": 2, "font.size": 11, "axes.titlesize": 12, "axes.titleweight": "bold",
    "legend.frameon": False,
})


def load(name):
    return np.loadtxt(out / f"{name}.dat")


def save(fig, name):
    fig.tight_layout()
    fig.savefig(img / f"{name}.png", dpi=150)
    plt.close(fig)
    print("wrote", img / f"{name}.png")


# Temperature, all corners
fig, ax = plt.subplots(figsize=(7, 4))
for color, c in zip(SERIES, ["tt", "ss", "ff", "sf", "fs"]):
    d = load(f"temp_{c}")
    ax.plot(d[:, 0], d[:, 1], color=color, label=c)
ax.set(title="VREF vs temperature, five process corners", xlabel="Temperature (°C)", ylabel="VREF (V)")
ax.legend(ncol=5, loc="lower center")
save(fig, "temp")

# Line regulation
d = load("line")
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(d[:, 0], d[:, 1], color=SERIES[0])
ax.axvspan(1.62, 1.98, color=GRID, alpha=0.6, lw=0)
ax.text(1.80, 0.15, "1.8 V ±10%", ha="center", color=INK2)
ax.set(title="VREF vs supply voltage", xlabel="VDD (V)", ylabel="VREF (V)")
save(fig, "line")

# PSRR
d = load("psrr")
fig, ax = plt.subplots(figsize=(7, 4))
ax.semilogx(d[:, 0], d[:, 1], color=SERIES[0])
ax.set(title="Power-supply rejection (VREF / VDD)", xlabel="Frequency (Hz)", ylabel="Gain (dB)")
save(fig, "psrr")

# Start-up
d = load("startup")
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(d[:, 0] * 1e6, d[:, 1], color=SERIES[1], label="VDD")
ax.plot(d[:, 2] * 1e6, d[:, 3], color=SERIES[0], label="VREF")
ax.set(title="Start-up with a 10 µs VDD ramp", xlabel="Time (µs)", ylabel="Voltage (V)", xlim=(0, 40))
ax.text(30, 1.82, "VDD", color=INK2, va="bottom")
ax.text(30, 1.22, "VREF", color=INK2, va="bottom")
ax.legend(loc="lower right")
save(fig, "startup")

# Loop gain: two charts sharing x, never two y-scales on one
d = load("loop")
fig, (a1, a2) = plt.subplots(2, 1, figsize=(7, 5.5), sharex=True)
a1.semilogx(d[:, 0], d[:, 1], color=SERIES[0])
a1.axhline(0, color=INK2, lw=1)
a1.set(title="Loop gain", ylabel="Magnitude (dB)")
a2.semilogx(d[:, 2], d[:, 3], color=SERIES[0])
a2.set(xlabel="Frequency (Hz)", ylabel="Phase (°)")
save(fig, "loop")

# Noise
d = load("noise")
fig, ax = plt.subplots(figsize=(7, 4))
ax.loglog(d[:, 0], d[:, 1] * 1e9, color=SERIES[0])
for f in (10, 1e3, 1e5):
    print(f"noise at {f:g} Hz: {np.interp(np.log10(f), np.log10(d[:, 0]), d[:, 1]) * 1e9:.0f} nV/rtHz")
ax.set(title="Output noise density at VREF", xlabel="Frequency (Hz)", ylabel="Noise (nV/√Hz)")
save(fig, "noise")

# Monte Carlo
v = np.array([float(l.split("=")[1]) for l in open(out / "mc.txt") if "=" in l])
mu, sd = v.mean(), v.std()
fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(v * 1e3, bins=25, color=SERIES[0], edgecolor=SURFACE, linewidth=2)
ax.axvline(mu * 1e3, color=INK, lw=1)
ax.set(title=f"Mismatch Monte Carlo, {len(v)} runs: mean {mu*1e3:.1f} mV, σ {sd*1e3:.1f} mV",
       xlabel="VREF (mV)", ylabel="Runs")
ax.grid(axis="x", visible=False)
save(fig, "mc")
print(f"mc: n={len(v)} mean={mu:.4f} V sigma={sd*1e3:.2f} mV min={v.min():.4f} max={v.max():.4f}")

# Post-layout comparison (pex/run_pex.sh): schematic vs extracted layout, small multiples
pex = here / "pex" / "out"
if (pex / "temp_tt.dat").exists():
    sch_lay = [("Schematic", out, SERIES[0]), ("Layout (extracted RC)", pex, SERIES[1])]
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    (at, ap), (asu, an) = axes
    for label, base, color in sch_lay:
        d = np.loadtxt(base / ("temp_tt.dat" if base == pex else "temp.dat"))
        at.plot(d[:, 0], d[:, 1], color=color, label=label)
        d = np.loadtxt(base / "psrr.dat")
        ap.semilogx(d[:, 0], d[:, 1], color=color)
        d = np.loadtxt(base / "startup.dat")
        asu.plot(d[:, 2] * 1e6, d[:, 3], color=color)
        d = np.loadtxt(base / "noise.dat")
        an.loglog(d[:, 0], d[:, 1] * 1e9, color=color)
    at.set(title="VREF vs temperature (tt)", xlabel="Temperature (°C)", ylabel="VREF (V)")
    ap.set(title="PSRR", xlabel="Frequency (Hz)", ylabel="VREF / VDD (dB)")
    asu.set(title="Start-up, 10 µs VDD ramp", xlabel="Time (µs)", ylabel="VREF (V)", xlim=(0, 20))
    an.set(title="Output noise density", xlabel="Frequency (Hz)", ylabel="Noise (nV/√Hz)")
    fig.legend(*at.get_legend_handles_labels(), loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(img / "pex.png", dpi=150)
    plt.close(fig)
    print("wrote", img / "pex.png")
