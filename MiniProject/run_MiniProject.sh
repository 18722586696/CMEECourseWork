#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v Rscript >/dev/null 2>&1; then
  RSCRIPT_BIN="Rscript"
elif [ -x "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe" ]; then
  RSCRIPT_BIN="/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
else
  echo "Rscript was not found. Install R or add Rscript to PATH." >&2
  exit 1
fi

python "$ROOT_DIR/code/01_data_prep.py"
python "$ROOT_DIR/code/02_plot_raw_curves.py"
rm -f \
  "$ROOT_DIR/results/tables/model_fit_metrics.csv" \
  "$ROOT_DIR/results/tables/model_fit_parameters.csv" \
  "$ROOT_DIR/results/tables/model_predictions.csv" \
  "$ROOT_DIR/results/tables/best_model_by_curve.csv" \
  "$ROOT_DIR/results/tables/model_fit_report.txt" \
  "$ROOT_DIR/results/tables/analysis_summary.txt"
if [ "$RSCRIPT_BIN" = "Rscript" ]; then
  "$RSCRIPT_BIN" "$ROOT_DIR/code/03_model_fit.R"
else
  "$RSCRIPT_BIN" -NoProfile -ExecutionPolicy Bypass -File "$(wslpath -w "$ROOT_DIR/code/run_model_fit_windows.ps1")" || true
fi

if [ ! -f "$ROOT_DIR/results/tables/model_fit_metrics.csv" ]; then
  echo "Model fitting outputs were not generated." >&2
  exit 1
fi

python "$ROOT_DIR/code/04_analysis_plot.py"

echo "MiniProject workflow completed successfully."
