#!/usr/bin/env python3
"""
Align two DNA sequences by sliding the shorter along the longer and
counting matches; write the best alignment and its score to a text file.
No interactive input is required.
"""
from pathlib import Path
import csv

DATA_IN = Path(__file__).resolve().parents[1] / "data" / "two_seqs.csv"
OUT_DIR = Path(__file__).resolve().parents[1] / "results"
OUT_FILE = OUT_DIR / "best_alignment.txt"

def read_two_sequences(csv_path: Path):
    with open(csv_path, "r", newline="") as f:
        rows = list(csv.reader(f))
    # 允许：两行两列 或 一行两列
    flat = []
    for r in rows:
        flat.extend([c.strip().upper() for c in r if c.strip()])
    if len(flat) < 2:
        raise ValueError("Input CSV must contain two DNA sequences.")
    return flat[0], flat[1]

def score_alignment(longer: str, shorter: str, offset: int) -> int:
    """Count matches when `shorter` is aligned to `longer` starting at `offset`."""
    score = 0
    for i, base in enumerate(shorter):
        j = i + offset
        if j >= len(longer):  # beyond end
            break
        if base == longer[j]:
            score += 1
    return score

def best_alignment(seq1: str, seq2: str):
    # 确保 longer/shorter
    if len(seq1) >= len(seq2):
        longer, shorter = seq1, seq2
        swapped = False
    else:
        longer, shorter = seq2, seq1
        swapped = True

    best = {"score": -1, "offset": 0}
    for offset in range(len(longer)):  # 将短序列起点滑过长序列的每个位置
        s = score_alignment(longer, shorter, offset)
        if s > best["score"]:
            best.update(score=s, offset=offset)

    # 生成可视化对齐字符串
    aligned_shorter = " " * best["offset"] + shorter
    match_line = []
    for i, ch in enumerate(aligned_shorter):
        if i < len(longer) and ch == longer[i]:
            match_line.append("|")
        else:
            match_line.append(" ")
    match_line = "".join(match_line)

    # 若原序列被交换过，在输出里仍按原顺序展示
    if swapped:
        top = seq2
        bottom = " " * best["offset"] + seq1 if len(seq2) < len(seq1) else aligned_shorter
        # 当交换时重新构造对齐行以与输出两行长度一致
        # 简化处理：统一以 longer 在上、对齐 shorter 在下展示
        top = longer
        bottom = aligned_shorter
        mid = match_line
    else:
        top = longer
        bottom = aligned_shorter
        mid = match_line

    return {
        "score": best["score"],
        "offset": best["offset"],
        "longer": longer,
        "shorter": shorter,
        "top": top,
        "mid": mid,
        "bottom": bottom,
    }

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    s1, s2 = read_two_sequences(DATA_IN)
    res = best_alignment(s1, s2)
    with open(OUT_FILE, "w") as f:
        f.write("# Best alignment result\n")
        f.write(f"Score : {res['score']}\n")
        f.write(f"Offset: {res['offset']}\n\n")
        f.write(res["top"] + "\n")
        f.write(res["mid"] + "\n")
        f.write(res["bottom"] + "\n")
    print(f"[OK] Best alignment written to: {OUT_FILE} (score={res['score']})")

if __name__ == "__main__":
    main()
