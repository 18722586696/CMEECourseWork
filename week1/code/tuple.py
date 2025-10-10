#!/usr/bin/env python3
"""
tuple.py — Tuple basics: packing/unpacking; tuples as dict keys.
"""
from typing import Dict, List, Tuple

def swap(a, b):
    # tuple packing/unpacking
    a, b = b, a
    return a, b

def coords_to_dict(coords: List[Tuple[int,int]], label: str="P") -> Dict[Tuple[int,int], str]:
    # 使用 tuple 作为 key
    return {xy: f"{label}{i}" for i, xy in enumerate(coords, 1)}

def unzip_pairs(pairs: List[Tuple]) -> Tuple[List, List]:
    # 解包 zip(*pairs)
    left, right = zip(*pairs) if pairs else ([], [])
    return list(left), list(right)

if __name__ == "__main__":
    print("[tuple] swap(1,9) =>", swap(1,9))
    print("[tuple] coords_to_dict([(0,0),(1,2)]) =>", coords_to_dict([(0,0),(1,2)]))
    print("[tuple] unzip_pairs =>", unzip_pairs([("a",1),("b",2)]))
