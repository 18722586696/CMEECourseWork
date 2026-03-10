#!/usr/bin/env python3
"""Run the MiniProject workflow from data preparation to report compilation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
REPORT_DIR = ROOT_DIR / "report"


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


def find_latexmk() -> str:
    candidates = [
        "latexmk",
        r"C:\texlive\2024\bin\windows\latexmk.exe",
    ]
    for candidate in candidates:
        try:
            subprocess.run(
                [candidate, "-v"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return candidate
        except (OSError, subprocess.CalledProcessError):
            continue
    raise FileNotFoundError("latexmk was not found. Install TeX Live or add latexmk to PATH.")


def run_step(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd or ROOT_DIR, check=True)


def main() -> None:
    rscript_bin = find_rscript()
    latexmk_bin = find_latexmk()

    run_step([sys.executable, str(ROOT_DIR / "code" / "01_data_prep.py")])
    run_step([sys.executable, str(ROOT_DIR / "code" / "02_plot_raw_curves.py")])
    run_step([rscript_bin, str(ROOT_DIR / "code" / "03_model_fit.R")])
    run_step([sys.executable, str(ROOT_DIR / "code" / "04_analysis_plot.py")])
    run_step([latexmk_bin, "-pdf", "main.tex"], cwd=REPORT_DIR)

    print("MiniProject workflow completed successfully, including report compilation.")


if __name__ == "__main__":
    main()
