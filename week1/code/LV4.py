#!/usr/bin/env python3
"""
LV4.py — Discrete-time LV with Gaussian noise on growth rates.
Default: noise on prey growth (r + eps). Optionally also on z (consumer mortality).
"""
import argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def simulate(r=1.0, a=0.5, z=0.3, e=0.75, K=50.0,
             tmax=80, R0=10.0, C0=5.0, sigma=0.05, both=False, seed=1234):
    rng = np.random.default_rng(seed)
    n = int(tmax) + 1
    t = np.arange(n)
    R = np.zeros(n); C = np.zeros(n)
    R[0], C[0] = R0, C0
    for i in range(n-1):
        eps_r = rng.normal(0.0, sigma)
        rr = r + eps_r
        if both:
            eps_z = rng.normal(0.0, sigma)
            zz = max(z + eps_z, 0.0)
        else:
            zz = z
        R[i+1] = max(R[i]*(1 + rr*(1 - R[i]/K) - a*C[i]), 0.0)
        C[i+1] = max(C[i]*(1 - zz + e*a*R[i]), 0.0)
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
    p.add_argument("--sigma", type=float, default=0.05, help="stddev of Gaussian noise")
    p.add_argument("--both", action="store_true", help="also add noise to z")
    p.add_argument("--seed", type=int, default=1234)
    p.add_argument("--pdf", type=str, default=None)
    args = p.parse_args()

    out = Path(args.pdf) if args.pdf else (Path(__file__).resolve().parents[1]/"results"/"LV4.pdf")
    out.parent.mkdir(parents=True, exist_ok=True)

    t, R, C = simulate(args.r,args.a,args.z,args.e,args.K,args.tmax,args.R0,args.C0,args.sigma,args.both,args.seed)
    print(f"Final DT+noise pops -> R: {R[-1]:.6f}, C: {C[-1]:.6f} (t={t[-1]})")

    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(t, R, label="R (prey)")
    ax.plot(t, C, label="C (predator)")
    ax.set_xlabel("Time step"); ax.set_ylabel("Population")
    ax.set_title("Discrete-time LV with Gaussian noise")
    ax.grid(True); ax.legend(loc="best")
    ax.text(0.02,0.95,
            f"r={args.r}, a={args.a}, z={args.z}, e={args.e}, K={args.K}, sigma={args.sigma}, both={args.both}\nR0={args.R0}, C0={args.C0}",
            transform=ax.transAxes, va="top", ha="left")
    fig.tight_layout(); fig.savefig(out)
    print(f"[OK] Saved plot -> {out}")

if __name__ == "__main__":
    main()
