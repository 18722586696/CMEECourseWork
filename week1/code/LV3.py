#!/usr/bin/env python3
"""
LV3.py — Discrete-time LV with prey density-dependence (K).
Print final populations and save a PDF time-series plot (no GUI).
"""
import argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def simulate(r=1.0, a=0.5, z=0.3, e=0.75, K=50.0,
             tmax=80, R0=10.0, C0=5.0):
    n = int(tmax) + 1
    t = np.arange(n)
    R = np.zeros(n); C = np.zeros(n)
    R[0], C[0] = R0, C0
    for i in range(n-1):
        R[i+1] = max(R[i]*(1 + r*(1 - R[i]/K) - a*C[i]), 0.0)
        C[i+1] = max(C[i]*(1 - z + e*a*R[i]), 0.0)
    return t, R, C

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--r", type=float, default=1.0)
    p.add_argument("--a", type=float, default=0.5)
    p.add_argument("--z", type=float, default=0.3)
    p.add_argument("--e", type=float, default=0.75)
    p.add_argument("--K", type=float, default=50.0)
    p.add_argument("--tmax", type=int, default=80)
    p.add_argument("--R0", type=float, default=10.0)
    p.add_argument("--C0", type=float, default=5.0)
    p.add_argument("--pdf", type=str, default=None)
    args = p.parse_args()

    out = Path(args.pdf) if args.pdf else (Path(__file__).resolve().parents[1]/"results"/"LV3.pdf")
    out.parent.mkdir(parents=True, exist_ok=True)

    t, R, C = simulate(args.r,args.a,args.z,args.e,args.K,args.tmax,args.R0,args.C0)
    print(f"Final DT pops -> R: {R[-1]:.6f}, C: {C[-1]:.6f} (t={t[-1]})")

    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(t, R, label="R (prey)")
    ax.plot(t, C, label="C (predator)")
    ax.set_xlabel("Time step"); ax.set_ylabel("Population")
    ax.set_title("Discrete-time LV (with K)")
    ax.grid(True); ax.legend(loc="best")
    ax.text(0.02,0.95,f"r={args.r}, a={args.a}, z={args.z}, e={args.e}, K={args.K}\nR0={args.R0}, C0={args.C0}",
            transform=ax.transAxes, va="top", ha="left")
    fig.tight_layout(); fig.savefig(out)
    print(f"[OK] Saved plot -> {out}")

if __name__ == "__main__":
    main()
