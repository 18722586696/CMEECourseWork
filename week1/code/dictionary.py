#!/usr/bin/env python3
"""
dictionary.py — Common dictionary patterns.
"""
from typing import Dict, Iterable, List, Tuple
from collections import defaultdict

def count_tokens(tokens: Iterable[str]) -> Dict[str, int]:
    cnt: Dict[str, int] = defaultdict(int)
    for t in tokens:
        cnt[t] += 1
    return dict(cnt)

def list_of_tuples_to_dict(pairs: Iterable[Tuple[str, int]]) -> Dict[str, int]:
    return {k: v for k, v in pairs}

def dict_to_sorted_items(d: Dict[str,int]) -> List[Tuple[str,int]]:
    return sorted(d.items(), key=lambda kv: (kv[1], kv[0]))

def merge_sum(d1: Dict[str,int], d2: Dict[str,int]) -> Dict[str,int]:
    out = dict(d1)
    for k, v in d2.items():
        out[k] = out.get(k, 0) + v
    return out

if __name__ == "__main__":
    toks = ["a","b","a","c","b","a"]
    print("[dict] count_tokens:", count_tokens(toks))
    pairs = [("x",2),("y",1)]
    print("[dict] list_of_tuples_to_dict:", list_of_tuples_to_dict(pairs))
    print("[dict] dict_to_sorted_items:", dict_to_sorted_items({"x":2,"y":1,"z":1}))
    print("[dict] merge_sum:", merge_sum({"a":1,"b":2},{"b":5,"c":3}))
