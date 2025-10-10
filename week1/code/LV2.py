#!/usr/bin/env python3
"""
LV2.py — Lotka–Volterra with prey density dependence (carrying capacity K).
Takes parameters from CLI, saves a PDF, prints final (non-zero) populations.

Model:
    dR/dt = r*R*(1 - R/K) - a*C*R
    dC/dt = -z*C + e*a*C*R
"""
import argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")  # no GUI
import matplotlib.pyplot as plt

def simulate(r=1.0, a=0.5, z=0.3, e=0.75, K=50.0,
             tmax=60.0, dt=0.01, R0=10.0, C0=5.0):
    n = int(tmax / dt) + 1
    t = np.linspace(0.0, tmax, n)
    R = np.zeros(n); C = np.zeros(n)
    R[0], C[0] = float(R0), float(C0)
    for i in range(n - 1):
        dR = r*R[i]*(1 - R[i]/K) - a*C[i]*R[i]
        dC = -z*C[i] + e*a*C[i]*R[i]
        R[i+1] = max(R[i] + dR*dt, 0.0)
        C[i+1] = max(C[i] + dC*dt, 0.0)
    return t, R, C

def main():
    p = argparse.ArgumentParser(
        description="LV with prey density dependence (K). Saves PDF and prints final populations."
    )
    p.add_argument("--r", type=float, default=1.0)
    p.add_argument("--a", type=float, default=0.5)
    p.add_argument("--z", type=float, default=0.3)
    p.add_argument("--e", type=float, default=0.75)
    p.add_argument("--K", type=float, default=50.0)
    p.add_argument("--tmax", type=float, default=60.0)
    p.add_argument("--dt", type=float, default=0.01)
    p.add_argument("--R0", type=float, default=10.0)
    p.add_argument("--C0", type=float, default=5.0)
    p.add_argument("--pdf", type=str, default=None,
                   help="Output PDF path; default ../results/LV2.pdf")
    args = p.parse_args()

    out_path = Path(args.pdf) if args.pdf else (Path(__file__).resolve().parents[1] / "results" / "LV2.pdf")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    t, R, C = simulate(args.r, args.a, args.z, args.e, args.K, args.tmax, args.dt, args.R0, args.C0)

    # print final (non-zero) populations
    print(f"Final populations -> R: {R[-1]:.6f}, C: {C[-1]:.6f} (t={t[-1]:.2f})")

    # plot
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(t, R, label="Resource R (prey)")
    ax.plot(t, C, label="Consumer C (predator)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Population")
    ax.set_title("Lotka–Volterra with Prey Density Dependence (K)")
    ax.grid(True)
    ax.legend(loc="best")
    ax.text(
        0.02, 0.95,
        f"r={args.r}, a={args.a}, z={args.z}, e={args.e}, K={args.K}\n"
        f"R0={args.R0}, C0={args.C0}, tmax={args.tmax}, dt={args.dt}",
        transform=ax.transAxes, ha="left", va="top"
    )
    fig.tight_layout()
    fig.savefig(out_path)
    print(f"[OK] Saved plot -> {out_path}")

if __name__ == "__main__":
    main()
