#!/usr/bin/env python3
"""
Vectorize2.py — compare loop vs NumPy vectorization on L2 norm (sum of squares).
Prints per-N function timings with a stable, greppable format.
"""
import time, math
import numpy as np

def l2_loop(a: np.ndarray) -> float:
    s = 0.0
    for i in range(len(a)):
        s += a[i] * a[i]
    return math.sqrt(s)

def l2_vect(a: np.ndarray) -> float:
    return float(np.linalg.norm(a))

def bench_once(fn, *args, repeats=5):
    tmin = math.inf
    for _ in range(repeats):
        t0 = time.perf_counter()
        _ = fn(*args)
        t = (time.perf_counter() - t0) * 1000.0
        if t < tmin: tmin = t
    return tmin

def main():
    rng = np.random.default_rng(123)
    sizes = [10**k for k in range(1, 7)]
    for N in sizes:
        a = rng.random(N, dtype=np.float64)
        t_loop = bench_once(l2_loop, a)
        t_vect = bench_once(l2_vect, a)
        print(f"TIMING Vectorize2 loop N={N} ms={t_loop:.4f}")
        print(f"TIMING Vectorize2 vect N={N} ms={t_vect:.4f}")

if __name__ == "__main__":
    main()
