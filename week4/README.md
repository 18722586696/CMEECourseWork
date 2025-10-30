
# Solutions: Biological Computing in R — Practicals

This folder contains R scripts that complete the starred (★) tasks and Practicals from the **MulQuaBio** "Biological Computing in R" chapter. Each script is self‑contained and can be sourced with `Rscript <file.R>`.

## Files

- `basic_warmup.R` — Variables, vectors, simple operations, data structures warmup.
- `sets_random.R` — Set operations, random numbers, and seeding; `replicate()` demo.
- `control_flow.R` — `if`, `for`, `while`, and simple branching examples.
- `functions_practical.R` — Example functions and usage patterns.
- `sample.R` — Vectorization with `lapply/sapply`, random sampling, and seed control.
- `vectorization_challenge_ricker.R` — **Vectorization challenge**: Ricker model implemented both with loops and in vectorized form; compares runtime and equivalence of results.
- `TAutoCorr.R` — **Groupwork Practical**: Autocorrelation in Florida weather — permutation test for correlation in successive years; saves a PDF plot and a short report.
- `utils_plot.R` — Tiny helper for consistent base plots exported to PDF.

## How to run (Linux/macOS/Windows PowerShell)

```bash
# from this folder:
Rscript basic_warmup.R
Rscript sets_random.R
Rscript control_flow.R
Rscript functions_practical.R
Rscript sample.R
Rscript vectorization_challenge_ricker.R

# For the autocorrelation practical:
# Provide a CSV with columns: Year, Temp (any station/region). Example path shown below.
Rscript TAutoCorr.R --input data/florida_temp.csv --output results/autocorr
```

Outputs (CSVs, PDFs) will be written under `results/`.
