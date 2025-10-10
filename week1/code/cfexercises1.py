#!/usr/bin/env python3
"""
cfexercises1.py — Control-flow exercises rewritten as a reusable module.

Run directly to see demo evaluations; import to reuse functions elsewhere.
"""
__author__ = "Your Name <you@example.com>"
__version__ = "0.1.0"

from typing import List

def foo_1(x: float = 4.0) -> float:
    """Square root (example control-flow kept trivial)."""
    return x ** 0.5

def foo_2(x: float, y: float):
    """Return the larger of two numbers."""
    return x if x > y else y

def foo_3(x: float, y: float, z: float) -> List[float]:
    """Return [x,y,z] sorted ascending (no .sort used to mirror notes)."""
    if x > y: x, y = y, x
    if x > z: x, z = z, x
    if y > z: y, z = z, y
    return [x, y, z]

def foo_4(n: int) -> int:
    """Factorial via for-loop; handles 0! = 1."""
    if n < 0:
        raise ValueError("n must be >= 0")
    out = 1
    for i in range(1, n+1):
        out *= i
    return out

def foo_5(n: int) -> int:
    """Factorial via recursion; handles 0! = 1."""
    if n < 0:
        raise ValueError("n must be >= 0")
    if n in (0, 1):
        return 1
    return n * foo_5(n-1)

def foo_6(n: int) -> int:
    """Factorial via while-loop; handles 0! = 1."""
    if n < 0:
        raise ValueError("n must be >= 0")
    out = 1
    while n >= 1:
        out *= n
        n -= 1
    return out

def _demo():
    print("foo_1(9)   ->", foo_1(9))
    print("foo_2(7,3) ->", foo_2(7,3))
    print("foo_3(9,1,5) ->", foo_3(9,1,5))
    print("foo_4(5)   ->", foo_4(5))
    print("foo_5(10)  ->", foo_5(10))  # 文档示例中的测试方式
    print("foo_6(6)   ->", foo_6(6))

if __name__ == "__main__":
    _demo()
