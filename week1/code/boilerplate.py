#!/usr/bin/env python3
"""
boilerplate.py — a template for all Python scripts in The MulQuaBio course.

Demonstrates good coding practice:
- Shebang for portability.
- Module-level docstring (describes purpose, author, version, usage).
- Imports at top.
- main() function encapsulation.
- sys.argv for command-line argument reading.
- __name__ guard.
"""

__author__ = "Your Name <you@example.com>"
__version__ = "0.1.0"
__license__ = "MIT"
__status__ = "Development"

# ---- imports ----
import sys
from pathlib import Path

# ---- functions ----
def greet(name: str = "world") -> str:
    """Return a simple greeting message."""
    return f"Hello, {name}!"

# ---- main ----
def main(argv=None):
    """
    Entry point for command-line execution.

    Parameters
    ----------
    argv : list, optional
        Command-line arguments (defaults to sys.argv[1:]).

    Returns
    -------
    int
        Exit status code (0 for success).
    """
    if argv is None:
        argv = sys.argv[1:]

    # handle arguments
    if len(argv) == 0:
        name = "world"
    else:
        name = argv[0]

    message = greet(name)
    print(message)

    # create an example output file (shows file I/O)
    outdir = Path(__file__).resolve().parents[1] / "results"
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / "boilerplate_output.txt"
    with open(outfile, "w") as f:
        f.write(message + "\n")

    print(f"[OK] Message written to {outfile}")
    return 0

# ---- script execution ----
if __name__ == "__main__":
    sys.exit(main())
