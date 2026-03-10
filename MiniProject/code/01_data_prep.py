#!/usr/bin/env python3
"""Prepare the Population Growth dataset for downstream model fitting."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = PROJECT_ROOT / "data" / "logistic_growth_data.csv"
CLEAN_DATA = PROJECT_ROOT / "data" / "cleaned_growth_data.csv"
SUMMARY_TABLE = PROJECT_ROOT / "results" / "tables" / "curve_summary.csv"
PREP_REPORT = PROJECT_ROOT / "results" / "tables" / "data_prep_report.txt"

REQUIRED_COLUMNS = [
    "X",
    "Time",
    "PopBio",
    "Temp",
    "Time_units",
    "PopBio_units",
    "Species",
    "Medium",
    "Rep",
    "Citation",
]


def parse_float(value: str) -> float:
    """Parse a numeric field and raise ValueError on empty input."""
    text = value.strip()
    if not text:
        raise ValueError("Empty numeric field")
    return float(text)


def build_curve_label(row: dict[str, str]) -> str:
    """Create a human-readable label for each unique growth curve."""
    parts = [
        row["Species"].strip(),
        row["Temp"].strip(),
        row["Medium"].strip(),
        row["Rep"].strip(),
        row["Citation"].strip(),
    ]
    return "_".join(parts)


def main() -> None:
    if not RAW_DATA.exists():
        raise FileNotFoundError(f"Missing input file: {RAW_DATA}")

    grouped_rows: dict[str, list[dict[str, object]]] = defaultdict(list)
    skipped_rows = 0

    with RAW_DATA.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing_columns = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
        if missing_columns:
            raise ValueError(f"Input file is missing columns: {missing_columns}")

        for line_number, row in enumerate(reader, start=2):
            try:
                time_value = parse_float(row["Time"])
                popbio_value = parse_float(row["PopBio"])
                temp_value = parse_float(row["Temp"])
            except ValueError:
                skipped_rows += 1
                continue

            text_fields = ["Species", "Medium", "Rep", "Citation", "Time_units", "PopBio_units"]
            if any(not row[field].strip() for field in text_fields):
                skipped_rows += 1
                continue

            curve_label = build_curve_label(row)
            grouped_rows[curve_label].append(
                {
                    "SourceLine": line_number,
                    "X": row["X"].strip(),
                    "Time": time_value,
                    "PopBio": popbio_value,
                    "Temp": temp_value,
                    "Time_units": row["Time_units"].strip(),
                    "PopBio_units": row["PopBio_units"].strip(),
                    "Species": row["Species"].strip(),
                    "Medium": row["Medium"].strip(),
                    "Rep": row["Rep"].strip(),
                    "Citation": row["Citation"].strip(),
                    "CurveLabel": curve_label,
                }
            )

    ordered_labels = sorted(grouped_rows)
    curve_id_lookup = {label: f"C{index:03d}" for index, label in enumerate(ordered_labels, start=1)}

    clean_fieldnames = [
        "CurveID",
        "CurveLabel",
        "ObservationIndex",
        "SourceLine",
        "X",
        "Time",
        "PopBio",
        "Temp",
        "Time_units",
        "PopBio_units",
        "Species",
        "Medium",
        "Rep",
        "Citation",
    ]
    summary_fieldnames = [
        "CurveID",
        "CurveLabel",
        "Species",
        "Temp",
        "Medium",
        "Rep",
        "TimeUnits",
        "PopBioUnits",
        "NObservations",
        "UniqueTimeValues",
        "MinTime",
        "MaxTime",
        "MinPopBio",
        "MaxPopBio",
        "PopBioRange",
    ]

    curve_summaries: list[dict[str, object]] = []
    total_rows_written = 0

    with CLEAN_DATA.open("w", encoding="utf-8", newline="") as clean_handle:
        writer = csv.DictWriter(clean_handle, fieldnames=clean_fieldnames)
        writer.writeheader()

        for label in ordered_labels:
            curve_rows = sorted(grouped_rows[label], key=lambda item: (item["Time"], item["SourceLine"]))
            curve_id = curve_id_lookup[label]

            time_values = [float(item["Time"]) for item in curve_rows]
            popbio_values = [float(item["PopBio"]) for item in curve_rows]
            representative_row = curve_rows[0]

            for observation_index, item in enumerate(curve_rows, start=1):
                writer.writerow(
                    {
                        "CurveID": curve_id,
                        "CurveLabel": item["CurveLabel"],
                        "ObservationIndex": observation_index,
                        "SourceLine": item["SourceLine"],
                        "X": item["X"],
                        "Time": f"{float(item['Time']):.6f}",
                        "PopBio": f"{float(item['PopBio']):.6f}",
                        "Temp": f"{float(item['Temp']):.6f}",
                        "Time_units": item["Time_units"],
                        "PopBio_units": item["PopBio_units"],
                        "Species": item["Species"],
                        "Medium": item["Medium"],
                        "Rep": item["Rep"],
                        "Citation": item["Citation"],
                    }
                )
                total_rows_written += 1

            curve_summaries.append(
                {
                    "CurveID": curve_id,
                    "CurveLabel": label,
                    "Species": representative_row["Species"],
                    "Temp": f"{float(representative_row['Temp']):.6f}",
                    "Medium": representative_row["Medium"],
                    "Rep": representative_row["Rep"],
                    "TimeUnits": representative_row["Time_units"],
                    "PopBioUnits": representative_row["PopBio_units"],
                    "NObservations": len(curve_rows),
                    "UniqueTimeValues": len(set(time_values)),
                    "MinTime": f"{min(time_values):.6f}",
                    "MaxTime": f"{max(time_values):.6f}",
                    "MinPopBio": f"{min(popbio_values):.6f}",
                    "MaxPopBio": f"{max(popbio_values):.6f}",
                    "PopBioRange": f"{(max(popbio_values) - min(popbio_values)):.6f}",
                }
            )

    ranked_summaries = sorted(
        curve_summaries,
        key=lambda item: (
            int(item["NObservations"]),
            int(item["UniqueTimeValues"]),
            float(item["PopBioRange"]),
        ),
        reverse=True,
    )

    with SUMMARY_TABLE.open("w", encoding="utf-8", newline="") as summary_handle:
        writer = csv.DictWriter(summary_handle, fieldnames=summary_fieldnames)
        writer.writeheader()
        writer.writerows(ranked_summaries)

    best_curve = ranked_summaries[0]
    curves_with_ten_points = sum(int(item["NObservations"]) >= 10 for item in ranked_summaries)

    report_lines = [
        "Population Growth data preparation summary",
        f"Input rows processed: {total_rows_written + skipped_rows}",
        f"Rows retained: {total_rows_written}",
        f"Rows skipped: {skipped_rows}",
        f"Unique curves: {len(ranked_summaries)}",
        f"Curves with at least 10 observations: {curves_with_ten_points}",
        "",
        "Selected nonlinear fitting candidate",
        f"CurveID: {best_curve['CurveID']}",
        f"Species: {best_curve['Species']}",
        f"Temperature: {best_curve['Temp']}",
        f"Medium: {best_curve['Medium']}",
        f"Replicate: {best_curve['Rep']}",
        f"Observations: {best_curve['NObservations']}",
        f"Unique time values: {best_curve['UniqueTimeValues']}",
    ]
    PREP_REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Wrote cleaned data to {CLEAN_DATA}")
    print(f"Wrote curve summary to {SUMMARY_TABLE}")
    print(f"Wrote preparation report to {PREP_REPORT}")


if __name__ == "__main__":
    main()
