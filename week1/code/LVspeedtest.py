#!/usr/bin/env python3
"""
run_LV.py — Run & profile LV1.py (CT), LV2.py (CT+K), LV3.py (DT+K), LV4.py (DT+K+noise).
Print wall-clock timings and cProfile summaries (top tail).
"""
import subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable

LV1 = HERE / "LV1.py"
LV2 = HERE / "LV2.py"
LV3 = HERE / "LV3.py"
LV4 = HERE / "LV4.py"

COMMON_CT = ["--r","1.0","--a","0.5","--z","0.3","--e","0.75","--tmax","80","--dt","0.005","--R0","10","--C0","5"]
LV2_ONLY   = ["--K","50"]
COMMON_DT = ["--r","1.0","--a","0.5","--z","0.3","--e","0.75","--tmax","80","--R0","10","--C0","5","--K","50"]
LV4_ONLY  = ["--sigma","0.05","--seed","1"]

def run_timed(cmd):
    t0 = time.perf_counter()
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    dt = time.perf_counter() - t0
    return p.returncode, dt, p.stdout.strip(), p.stderr.strip()

def profile_script(script, args):
    cmd = [PY, "-m", "cProfile", "-s", "tottime", str(script), *args]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()

def section(title): print("\n" + title + "\n" + "="*len(title))

def do_one(name, script, args):
    rc, secs, out, err = run_timed([PY, str(script), *args])
    print(f"[{name}] rc={rc}, time={secs:.3f}s")
    if out: print(f"[{name}] stdout:", out)
    if err: print(f"[{name}] stderr:", err)
    prc, prof, perr = profile_script(script, args)
    tail = "\n".join(prof.splitlines()[-15:])
    print(f"[{name} profile]\n{tail}")
    if perr: print(f"[{name} profile stderr]\n{perr}")

def main():
    for f in (LV1,LV2,LV3,LV4):
        if not f.exists():
            print(f"WARNING: {f.name} not found — skipping its tests.")

    section("Wall-clock timing & profile")
    if LV1.exists(): do_one("LV1", LV1, COMMON_CT)
    if LV2.exists(): do_one("LV2", LV2, [*COMMON_CT, *LV2_ONLY])
    if LV3.exists(): do_one("LV3", LV3, COMMON_DT)
    if LV4.exists(): do_one("LV4", LV4, [*COMMON_DT, *LV4_ONLY])

if __name__ == "__main__":
    main()
