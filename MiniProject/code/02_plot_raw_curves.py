#!/usr/bin/env python3
"""Generate exploratory figures for the Population Growth dataset."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_DATA = PROJECT_ROOT / "data" / "cleaned_growth_data.csv"
SUMMARY_TABLE = PROJECT_ROOT / "results" / "tables" / "curve_summary.csv"
FIGURES_DIR = PROJECT_ROOT / "results" / "figures"
TABLES_DIR = PROJECT_ROOT / "results" / "tables"

OBSERVATION_COUNTS_FIGURE = FIGURES_DIR / "curve_observation_distribution.png"
RAW_CURVE_GRID_FIGURE = FIGURES_DIR / "raw_curve_examples.png"
BEST_CURVE_FIGURE = FIGURES_DIR / "selected_curve_preview.png"
PLOT_REPORT = TABLES_DIR / "exploration_report.txt"


def load_curve_summary() -> list[dict[str, str]]:
    with SUMMARY_TABLE.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_curve_points() -> dict[str, list[tuple[float, float]]]:
    grouped_points: dict[str, list[tuple[float, float]]] = defaultdict(list)
    with CLEAN_DATA.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            grouped_points[row["CurveID"]].append((float(row["Time"]), float(row["PopBio"])))

    for curve_id, points in grouped_points.items():
        grouped_points[curve_id] = sorted(points, key=lambda item: item[0])

    return grouped_points


def select_example_curve_ids(summary_rows: list[dict[str, str]], limit: int = 12) -> list[str]:
    eligible_rows = [row for row in summary_rows if int(row["NObservations"]) >= 8]
    if not eligible_rows:
        eligible_rows = summary_rows

    if len(eligible_rows) <= limit:
        return [row["CurveID"] for row in eligible_rows]

    chosen_ids: list[str] = []
    max_index = len(eligible_rows) - 1
    for slot in range(limit):
        candidate_index = round(slot * max_index / (limit - 1))
        curve_id = eligible_rows[candidate_index]["CurveID"]
        if curve_id not in chosen_ids:
            chosen_ids.append(curve_id)

    return chosen_ids


def make_observation_count_figure(summary_rows: list[dict[str, str]]) -> None:
    counts = [int(row["NObservations"]) for row in summary_rows]
    plt.figure(figsize=(8, 5))
    plt.hist(counts, bins=20, color="#3b82f6", edgecolor="white")
    plt.xlabel("Observations per curve")
    plt.ylabel("Number of curves")
    plt.title("Population Growth curve sizes")
    plt.tight_layout()
    plt.savefig(OBSERVATION_COUNTS_FIGURE, dpi=200)
    plt.close()


def make_raw_curve_grid_figure(
    summary_rows: list[dict[str, str]],
    grouped_points: dict[str, list[tuple[float, float]]],
) -> list[str]:
    chosen_ids = select_example_curve_ids(summary_rows, limit=12)
    chosen_lookup = {row["CurveID"]: row for row in summary_rows}

    fig, axes = plt.subplots(3, 4, figsize=(14, 10), sharex=False, sharey=False)
    for axis, curve_id in zip(axes.flatten(), chosen_ids):
        points = grouped_points[curve_id]
        times = [point[0] for point in points]
        popbio = [point[1] for point in points]
        metadata = chosen_lookup[curve_id]

        axis.plot(times, popbio, color="#0f766e", linewidth=1.5)
        axis.scatter(times, popbio, color="#0f766e", s=12)
        axis.set_title(
            f"{curve_id}: {metadata['Species']} @ {float(metadata['Temp']):.0f}C",
            fontsize=8,
        )
        axis.set_xlabel("Time")
        axis.set_ylabel("PopBio")

    for axis in axes.flatten()[len(chosen_ids) :]:
        axis.axis("off")

    fig.suptitle("Raw Population Growth curve examples", fontsize=14)
    fig.tight_layout()
    fig.savefig(RAW_CURVE_GRID_FIGURE, dpi=200)
    plt.close(fig)

    return chosen_ids


def make_best_curve_figure(
    summary_rows: list[dict[str, str]],
    grouped_points: dict[str, list[tuple[float, float]]],
) -> dict[str, str]:
    best_curve = summary_rows[0]
    curve_id = best_curve["CurveID"]
    points = grouped_points[curve_id]
    times = [point[0] for point in points]
    popbio = [point[1] for point in points]

    plt.figure(figsize=(8, 5))
    plt.plot(times, popbio, color="#b91c1c", linewidth=1.8)
    plt.scatter(times, popbio, color="#b91c1c", s=16)
    plt.xlabel(f"Time ({best_curve['TimeUnits']})")
    plt.ylabel(f"PopBio ({best_curve['PopBioUnits']})")
    plt.title(f"Selected nonlinear fitting candidate: {curve_id}")
    plt.tight_layout()
    plt.savefig(BEST_CURVE_FIGURE, dpi=200)
    plt.close()

    return best_curve


def main() -> None:
    if not CLEAN_DATA.exists() or not SUMMARY_TABLE.exists():
        raise FileNotFoundError("Run 01_data_prep.py before generating exploratory plots.")

    summary_rows = load_curve_summary()
    grouped_points = load_curve_points()

    make_observation_count_figure(summary_rows)
    chosen_ids = make_raw_curve_grid_figure(summary_rows, grouped_points)
    best_curve = make_best_curve_figure(summary_rows, grouped_points)

    report_lines = [
        "Population Growth exploratory plotting summary",
        f"Curves plotted in example grid: {', '.join(chosen_ids)}",
        f"Selected nonlinear fitting candidate: {best_curve['CurveID']}",
        f"Candidate label: {best_curve['CurveLabel']}",
        f"Candidate observations: {best_curve['NObservations']}",
    ]
    PLOT_REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Wrote {OBSERVATION_COUNTS_FIGURE}")
    print(f"Wrote {RAW_CURVE_GRID_FIGURE}")
    print(f"Wrote {BEST_CURVE_FIGURE}")
    print(f"Wrote {PLOT_REPORT}")


if __name__ == "__main__":
    main()
