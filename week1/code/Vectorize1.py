#!/usr/bin/env python3
"""
Vectorize1.py — compare loop vs NumPy vectorization on elementwise product & sum.
Prints per-N function timings with a stable, greppable format.
"""
import time, math
import numpy as np

def product_loop(a: np.ndarray, b: np.ndarray) -> float:
    s = 0.0
    for i in range(len(a)):
        s += a[i] * b[i]
    return s

def product_vect(a: np.ndarray, b: np.ndarray) -> float:
    return float((a * b).sum())

def bench_once(fn, *args, repeats=5):
    tmin = math.inf
    for _ in range(repeats):
        t0 = time.perf_counter()
        _ = fn(*args)
        t = (time.perf_counter() - t0) * 1000.0  # ms
        if t < tmin: tmin = t
    return tmin

def main():
    rng = np.random.default_rng(42)
    sizes = [10**k for k in range(1, 7)]  # 10..1,000,000
    for N in sizes:
        a = rng.random(N, dtype=np.float64)
        b = rng.random(N, dtype=np.float64)
        t_loop = bench_once(product_loop, a, b)
        t_vect = bench_once(product_vect, a, b)
        print(f"TIMING Vectorize1 loop N={N} ms={t_loop:.4f}")
        print(f"TIMING Vectorize1 vect N={N} ms={t_vect:.4f}")

if __name__ == "__main__":
    main()
