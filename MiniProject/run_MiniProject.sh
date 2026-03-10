#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python "$ROOT_DIR/code/01_data_prep.py"
python "$ROOT_DIR/code/02_plot_raw_curves.py"

echo "Morning workflow completed successfully."
