#!/usr/bin/env python3
"""
LV1.py — Basic continuous-time Lotka–Volterra model (predator–prey)
Generates two PDF figures (time series & phase-plane) in ../results/ without showing them.

Model (as in the notes):
    dR/dt = r*R - a*C*R
    dC/dt = -z*C + e*a*C*R
"""

from pathlib import Path
import numpy as np
import scipy.integrate as integrate
import matplotlib
matplotlib.use("Agg")  # ensure no GUI backend is needed
import matplotlib.pyplot as plt

# -----------------------
# Parameters & ICs
# -----------------------
r = 1.0     # intrinsic growth rate of resource (prey)
a = 0.5     # search/attack rate
z = 0.3     # consumer (predator) mortality
e = 0.75    # consumer efficiency
R0 = 10.0   # initial resource density
C0 = 5.0    # initial consumer density
t0, tmax, dt = 0.0, 60.0, 0.01

# Output paths
OUT_DIR = Path(__file__).resolve().parents[1] / "results"
FIG1 = OUT_DIR / "LV_model_timeseries.pdf"
FIG2 = OUT_DIR / "LV_model_phaseplane.pdf"

# -----------------------
# ODE system
# -----------------------
def dCR_dt(pop, t=0.0):
    R, C = pop
    dR = r*R - a*C*R
    dC = -z*C + e*a*C*R
    return np.array([dR, dC])

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # time grid & solve
    t = np.arange(t0, tmax + dt, dt)
    pops, infodict = integrate.odeint(dCR_dt, y0=(R0, C0), t=t, full_output=True)

    # ---------------
    # Figure 1: time series
    # ---------------
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    ax1.plot(t, pops[:, 0], "g-", label="Resource R (prey)")
    ax1.plot(t, pops[:, 1], "b-", label="Consumer C (predator)")
    ax1.grid(True)
    ax1.legend(loc="best")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Population density")
    ax1.set_title("Lotka–Volterra (time series)")
    # Optional: include params in the plot for clarity
    txt = f"r={r}, a={a}, z={z}, e={e}; R0={R0}, C0={C0}"
    ax1.text(0.02, 0.95, txt, transform=ax1.transAxes, va="top", ha="left")
    fig1.tight_layout()
    fig1.savefig(FIG1)
    plt.close(fig1)

    # ---------------
    # Figure 2 (“Fig. 15”): phase-plane (C vs R)
    # ---------------
    R = pops[:, 0]
    C = pops[:, 1]
    fig2, ax2 = plt.subplots(figsize=(5.2, 5.2))
    ax2.plot(R, C, "-")
    ax2.set_xlabel("Resource R")
    ax2.set_ylabel("Consumer C")
    ax2.set_title("Lotka–Volterra (phase plane)")
    ax2.grid(True)
    fig2.tight_layout()
    fig2.savefig(FIG2)
    plt.close(fig2)

    # A small success message (not required by the notes, but handy)
    print(f"[OK] Saved: {FIG1.name}, {FIG2.name} -> {OUT_DIR}")

if __name__ == "__main__":
    main()
