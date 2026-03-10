#!/usr/bin/env python3
"""Run the MiniProject workflow from data preparation to afternoon summaries."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent


def find_rscript() -> str:
    candidates = [
        "Rscript",
        r"C:\Program Files\R\R-4.5.2\bin\Rscript.exe",
    ]
    for candidate in candidates:
        try:
            subprocess.run(
                [candidate, "--version"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return candidate
        except (OSError, subprocess.CalledProcessError):
            continue
    raise FileNotFoundError("Rscript was not found. Install R or add Rscript to PATH.")


def run_step(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT_DIR, check=True)


def main() -> None:
    rscript_bin = find_rscript()

    run_step([sys.executable, str(ROOT_DIR / "code" / "01_data_prep.py")])
    run_step([sys.executable, str(ROOT_DIR / "code" / "02_plot_raw_curves.py")])
    run_step([rscript_bin, str(ROOT_DIR / "code" / "03_model_fit.R")])
    run_step([sys.executable, str(ROOT_DIR / "code" / "04_analysis_plot.py")])

    print("MiniProject workflow completed successfully.")


if __name__ == "__main__":
    main()
