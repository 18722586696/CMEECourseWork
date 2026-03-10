# MiniProject

This directory contains the completed Population Growth miniproject for the CMEE coursework.

## Current status

The workflow, analysis outputs, and report are complete:

- project scaffold created;
- Population Growth data copied into `data/`;
- data preparation script added;
- exploratory plotting script added;
- batch model fitting script added;
- model comparison plotting script added;
- submission-ready LaTeX report added and compiled.

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
|- run_MiniProject.py
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
- `run_MiniProject.py`: runs the full workflow and compiles the LaTeX report in the verified Windows environment.

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
- `report/main.pdf`

## How to run

From the `MiniProject/` directory:

```powershell
python run_MiniProject.py
```

Compile the report only:

```powershell
cd report
latexmk -pdf main.tex
```

Manual step-by-step execution:

```powershell
python code/01_data_prep.py
python code/02_plot_raw_curves.py
& 'C:\Program Files\R\R-4.5.2\bin\Rscript.exe' code/03_model_fit.R
python code/04_analysis_plot.py
cd report
latexmk -pdf main.tex
```

## Environment note

The final project was developed and verified in a Windows environment. A shell-based top-level runner was removed because direct bash invocation of the required Windows R and LaTeX executables was not reliable in the local setup. The single supported entry point for marking is therefore `python run_MiniProject.py`.

## Dependencies

- Python 3.11+
- Matplotlib
- R 4.5+
- R package `minpack.lm`
- TeX Live / LaTeX with `latexmk`
