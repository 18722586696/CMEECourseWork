#!/usr/bin/env python3
"""
lc2.py — Slightly trickier list/dict/set comprehensions.
"""
from typing import Dict, Iterable, List, Tuple

def word_lengths(words: Iterable[str]) -> Dict[str, int]:
    return {w: len(w) for w in words}

def vowels_only(s: str) -> List[str]:
    return [ch for ch in s if ch.lower() in "aeiou"]

def cartesian_comp(a: Iterable[int], b: Iterable[int]) -> List[Tuple[int,int]]:
    return [(x,y) for x in a for y in b]

def invert_dict(d: Dict[str, int]) -> Dict[int, List[str]]:
    # value-> list of keys
    inv: Dict[int, List[str]] = {}
    for k, v in d.items():
        inv.setdefault(v, []).append(k)
    return inv

if __name__ == "__main__":
    words = ["eco","evo","bio","python",""]
    print("[lc2] word_lengths:", word_lengths(words))
    print("[lc2] vowels_only('MulQuaBio'):", vowels_only("MulQuaBio"))
    print("[lc2] cartesian_comp([1,2],[10,20]):", cartesian_comp([1,2],[10,20]))
    print("[lc2] invert_dict({'a':1,'b':2,'c':1}):", invert_dict({"a":1,"b":2,"c":1}))
