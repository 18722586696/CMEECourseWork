# MiniProject

This directory contains the Population Growth miniproject scaffold for the CMEE coursework.

## Current status

The morning tasks are implemented:

- project scaffold created;
- Population Growth data copied into `data/`;
- data preparation script added;
- exploratory plotting script added;
- LaTeX report skeleton added.

## Directory layout

```text
MiniProject/
|- code/
|- data/
|- results/
|  |- figures/
|  `- tables/
|- report/
|- sandbox/
|- run_MiniProject.sh
`- README.md
```

## Data files

- `data/logistic_growth_data.csv`
- `data/logistic_growth_meta_data.csv`

## Scripts

- `code/01_data_prep.py`: builds curve IDs, writes cleaned data, and exports a curve summary table.
- `code/02_plot_raw_curves.py`: creates raw exploratory figures and selects a candidate curve for nonlinear fitting.
- `run_MiniProject.sh`: runs the currently implemented morning-stage workflow.

## Outputs produced by the morning workflow

- `data/cleaned_growth_data.csv`
- `results/tables/curve_summary.csv`
- `results/tables/data_prep_report.txt`
- `results/tables/exploration_report.txt`
- `results/figures/curve_observation_distribution.png`
- `results/figures/raw_curve_examples.png`
- `results/figures/selected_curve_preview.png`

## How to run

From the `MiniProject/` directory:

```bash
bash run_MiniProject.sh
```

On Windows without a shell wrapper:

```powershell
python code/01_data_prep.py
python code/02_plot_raw_curves.py
```

## Dependencies

- Python 3.11+
- Matplotlib

Later project stages will add the R fitting script, the final analysis script, and report compilation to the workflow.
