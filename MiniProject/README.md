# MiniProject

This directory contains the Population Growth miniproject scaffold for the CMEE coursework.

## Current status

The morning and afternoon tasks are implemented:

- project scaffold created;
- Population Growth data copied into `data/`;
- data preparation script added;
- exploratory plotting script added;
- batch model fitting script added;
- model comparison plotting script added;
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
- `code/03_model_fit.R`: fits quadratic, cubic, and Gompertz models on `log10(PopBio)` for each curve.
- `code/04_analysis_plot.py`: summarizes model-fitting outcomes and exports core afternoon figures.
- `run_MiniProject.py`: runs the full workflow in the current Windows/Python environment.
- `run_MiniProject.sh`: runs the currently implemented workflow.

## Outputs produced by the current workflow

- `data/cleaned_growth_data.csv`
- `results/tables/curve_summary.csv`
- `results/tables/data_prep_report.txt`
- `results/tables/exploration_report.txt`
- `results/figures/curve_observation_distribution.png`
- `results/figures/raw_curve_examples.png`
- `results/figures/selected_curve_preview.png`
- `results/tables/model_fit_metrics.csv`
- `results/tables/model_fit_parameters.csv`
- `results/tables/model_predictions.csv`
- `results/tables/best_model_by_curve.csv`
- `results/tables/model_fit_report.txt`
- `results/tables/analysis_summary.txt`
- `results/figures/model_win_counts.png`
- `results/figures/model_aic_distribution.png`
- `results/figures/best_curve_model_fits.png`

## How to run

From the `MiniProject/` directory:

```powershell
python run_MiniProject.py
```

Alternative shell wrapper:

```bash
bash run_MiniProject.sh
```

Manual step-by-step execution:

```powershell
python code/01_data_prep.py
python code/02_plot_raw_curves.py
& 'C:\Program Files\R\R-4.5.2\bin\Rscript.exe' code/03_model_fit.R
python code/04_analysis_plot.py
```

## Dependencies

- Python 3.11+
- Matplotlib
- R 4.5+
- R package `minpack.lm`

Later project stages will connect the fitted outputs to the final report text and submission-ready LaTeX workflow.
