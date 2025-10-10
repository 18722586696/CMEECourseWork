#!/usr/bin/env python3
"""
lc1.py — Loop -> List comprehension basics with quick self-tests.
"""
from typing import Iterable, List

def squares_loop(n: int) -> List[int]:
    out = []
    for i in range(n):
        out.append(i*i)
    return out

def squares_comp(n: int) -> List[int]:
    return [i*i for i in range(n)]

def evens_comp(seq: Iterable[int]) -> List[int]:
    return [x for x in seq if x % 2 == 0]

def lens_comp(names: Iterable[str]) -> List[int]:
    return [len(s) for s in names]

def flatten_pairs_comp(pairs: Iterable[tuple]) -> List:
    return [item for p in pairs for item in p]

def unique_sorted_comp(seq: Iterable[int]) -> List[int]:
    # “列表推导 + 去重 + 排序”
    return sorted({x for x in seq})

if __name__ == "__main__":
    print("[lc1] squares_loop(6)      =", squares_loop(6))
    print("[lc1] squares_comp(6)      =", squares_comp(6))
    print("[lc1] evens_comp(range(10))=", evens_comp(range(10)))
    print("[lc1] lens_comp(['a','abcd','']) =", lens_comp(["a","abcd",""]))
    print("[lc1] flatten_pairs_comp([(1,2),(3,4)]) =", flatten_pairs_comp([(1,2),(3,4)]))
    print("[lc1] unique_sorted_comp([3,1,2,3,2]) =", unique_sorted_comp([3,1,2,3,2]))
