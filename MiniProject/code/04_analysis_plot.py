#!/usr/bin/env python3
"""Summarize model-fitting results and produce core afternoon figures."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TABLES_DIR = PROJECT_ROOT / "results" / "tables"
FIGURES_DIR = PROJECT_ROOT / "results" / "figures"

METRICS_PATH = TABLES_DIR / "model_fit_metrics.csv"
PREDICTIONS_PATH = TABLES_DIR / "model_predictions.csv"
BEST_MODEL_PATH = TABLES_DIR / "best_model_by_curve.csv"
AFTERNOON_REPORT_PATH = TABLES_DIR / "analysis_summary.txt"
PREP_REPORT_PATH = TABLES_DIR / "data_prep_report.txt"

MODEL_WIN_FIGURE = FIGURES_DIR / "model_win_counts.png"
AIC_FIGURE = FIGURES_DIR / "model_aic_distribution.png"
BEST_CURVE_FIGURE = FIGURES_DIR / "best_curve_model_fits.png"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def make_model_win_figure(best_rows: list[dict[str, str]]) -> Counter:
    wins = Counter(row["BestModel"] for row in best_rows)
    models = ["Quadratic", "Cubic", "Gompertz"]
    counts = [wins.get(model, 0) for model in models]

    plt.figure(figsize=(8, 5))
    plt.bar(models, counts, color=["#94a3b8", "#0ea5e9", "#ef4444"])
    plt.ylabel("Curves won by lowest AIC")
    plt.title("Best model counts across Population Growth curves")
    plt.tight_layout()
    plt.savefig(MODEL_WIN_FIGURE, dpi=200)
    plt.close()

    return wins


def make_aic_distribution_figure(metric_rows: list[dict[str, str]]) -> dict[str, list[float]]:
    grouped_aic: dict[str, list[float]] = defaultdict(list)
    for row in metric_rows:
        if row["FitStatus"] == "success" and row["AIC"] not in {"", "NA", "NaN"}:
            grouped_aic[row["Model"]].append(float(row["AIC"]))

    models = ["Quadratic", "Cubic", "Gompertz"]
    data = [grouped_aic.get(model, []) for model in models]

    plt.figure(figsize=(8, 5))
    plt.boxplot(data, tick_labels=models)
    plt.ylabel("AIC")
    plt.title("AIC distribution for successful model fits")
    plt.tight_layout()
    plt.savefig(AIC_FIGURE, dpi=200)
    plt.close()

    return grouped_aic


def make_best_curve_figure(
    best_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
) -> str:
    preferred_curve_id = ""
    if PREP_REPORT_PATH.exists():
        for line in PREP_REPORT_PATH.read_text(encoding="utf-8").splitlines():
            if line.startswith("CurveID:"):
                preferred_curve_id = line.split(":", 1)[1].strip()
                break

    best_curve_row = None
    if preferred_curve_id:
        for row in best_rows:
            if row["CurveID"] == preferred_curve_id:
                best_curve_row = row
                break

    if best_curve_row is None:
        for row in best_rows:
            if row["BestModel"] == "Gompertz":
                best_curve_row = row
                break

    if best_curve_row is None:
        for row in best_rows:
            if row["CurveID"] == preferred_curve_id:
                best_curve_row = row
                break

    if best_curve_row is None and best_rows:
        best_curve_row = best_rows[0]
    if best_curve_row is None:
        return ""

    curve_id = best_curve_row["CurveID"]
    grouped_predictions: dict[str, list[tuple[float, float, float]]] = defaultdict(list)
    observed_points = []

    for row in prediction_rows:
        if row["CurveID"] != curve_id:
            continue
        time_value = float(row["Time"])
        observed_log = float(row["ObservedLog10PopBio"])
        fitted_log = float(row["FittedLog10PopBio"])
        observed_points.append((time_value, observed_log))
        grouped_predictions[row["Model"]].append((time_value, observed_log, fitted_log))

    plt.figure(figsize=(8, 5))
    observed_points = sorted(set(observed_points), key=lambda item: item[0])
    plt.scatter(
        [point[0] for point in observed_points],
        [point[1] for point in observed_points],
        color="black",
        s=20,
        label="Observed log10(PopBio)",
    )

    colors = {
        "Quadratic": "#94a3b8",
        "Cubic": "#0ea5e9",
        "Gompertz": "#ef4444",
    }
    for model_name in ["Quadratic", "Cubic", "Gompertz"]:
        rows = sorted(grouped_predictions.get(model_name, []), key=lambda item: item[0])
        if not rows:
            continue
        plt.plot(
            [item[0] for item in rows],
            [item[2] for item in rows],
            linewidth=2,
            color=colors[model_name],
            label=model_name,
        )

    plt.xlabel("Time")
    plt.ylabel("log10(PopBio)")
    plt.title(f"Model fits for example curve {curve_id}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(BEST_CURVE_FIGURE, dpi=200)
    plt.close()

    return curve_id


def write_summary(
    metric_rows: list[dict[str, str]],
    best_rows: list[dict[str, str]],
    wins: Counter,
    grouped_aic: dict[str, list[float]],
    best_curve_id: str,
) -> None:
    success_counts = Counter()

    for row in metric_rows:
        if row["FitStatus"] == "success":
            success_counts[row["Model"]] += 1

    lines = [
        "Population Growth analysis summary",
        f"Successful Quadratic fits: {success_counts.get('Quadratic', 0)}",
        f"Successful Cubic fits: {success_counts.get('Cubic', 0)}",
        f"Successful Gompertz fits: {success_counts.get('Gompertz', 0)}",
        f"Best-model assignments: {len(best_rows)}",
        f"Quadratic wins: {wins.get('Quadratic', 0)}",
        f"Cubic wins: {wins.get('Cubic', 0)}",
        f"Gompertz wins: {wins.get('Gompertz', 0)}",
        f"Example curve plotted: {best_curve_id or 'none'}",
    ]

    for model_name in ["Quadratic", "Cubic", "Gompertz"]:
        aic_values = grouped_aic.get(model_name, [])
        if aic_values:
            lines.append(f"Mean AIC for {model_name}: {mean(aic_values):.4f}")

    AFTERNOON_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    if not (METRICS_PATH.exists() and PREDICTIONS_PATH.exists() and BEST_MODEL_PATH.exists()):
        raise FileNotFoundError("Run 03_model_fit.R before generating the analysis figures.")

    metric_rows = read_csv(METRICS_PATH)
    prediction_rows = read_csv(PREDICTIONS_PATH)
    best_rows = read_csv(BEST_MODEL_PATH)

    wins = make_model_win_figure(best_rows)
    grouped_aic = make_aic_distribution_figure(metric_rows)
    best_curve_id = make_best_curve_figure(best_rows, prediction_rows)
    write_summary(metric_rows, best_rows, wins, grouped_aic, best_curve_id)

    print(f"Wrote {MODEL_WIN_FIGURE}")
    print(f"Wrote {AIC_FIGURE}")
    print(f"Wrote {BEST_CURVE_FIGURE}")
    print(f"Wrote {AFTERNOON_REPORT_PATH}")


if __name__ == "__main__":
    main()
