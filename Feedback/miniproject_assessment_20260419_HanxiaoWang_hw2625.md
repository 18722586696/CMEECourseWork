# MiniProject Assessment for Hanxiao Wang

## Computing

### A1 — Project Organisation

The project is laid out clearly, with `code/`, `data/`, `results/`, `report/`, `run_MiniProject.py`, `README.md`, and `.gitignore` all present, which makes the submission easy to inspect and navigate. The README gives the directory layout, names the main scripts, and lists core dependencies and language versions, but it stops short of explaining what each package is for, so a new user still has to infer why `matplotlib` or `minpack.lm` are needed. The main organisational deduction comes from committed outputs in `results/figures/` and `results/tables/`, including generated plots and `model_predictions.csv`; that weakens the reproducibility story because the repository mixes source with regenerated products.

### A2 — Single-Script Reproducibility

#### Workflow & Solution Quality

`run_MiniProject.py` stops before any analysis step runs because `find_latexmk()` raises `FileNotFoundError` when `latexmk` is unavailable in the grading environment. The script itself is a genuine top-level runner: it calls `code/01_data_prep.py`, `code/02_plot_raw_curves.py`, `code/03_model_fit.R`, `code/04_analysis_plot.py`, and then `latexmk -pdf main.tex`, so the intended end-to-end sequence is correctly orchestrated in one place. The main weakness is robustness, because the script checks for LaTeX before running data preparation and model fitting, which means a missing TeX installation prevents validation of every earlier stage as well; a stronger pattern would run the analytical stages first and treat report compilation as a final step with clearer stage-specific logging. The README also frames the workflow as verified in Windows, and the runner contains Windows-specific fallback paths for `Rscript` and `latexmk`, so future submissions would benefit from a small preflight dependency report and a more platform-neutral failure mode. It is also worth asking whether every non-core dependency is truly necessary for this submission, especially the hard requirement on `latexmk` at startup, because removing or softening non-essential dependencies would improve reproducibility.

### A3 — Code Quality & Style

#### Script-level Technical Feedback

The codebase is strongly modularised, with 24 function definitions across Python and R, and the decomposition is easy to follow: `run_MiniProject.py` uses `find_rscript`, `find_latexmk`, and `run_step` to manage orchestration, while `code/03_model_fit.R` separates `gompertz_model`, `fit_lm_model`, and `fit_gompertz_curve` into distinct fitting tasks. `code/02_plot_raw_curves.py` and `code/04_analysis_plot.py` also split plotting into focused helpers such as `make_observation_count_figure` and `make_model_win_figure`, which keeps the workflow readable and avoids copy-paste. The main drag on this criterion is documentation: 1,109 lines of code with only 6 comment lines gives a comment density of 0.005, so the logic is mostly recoverable from naming rather than explanation, and the largest file, `code/03_model_fit.R` at 433 lines, would benefit from more explicit sectioning and function contracts. Refactor `code/03_model_fit.R` into smaller helpers for start-value generation, fit summarisation, and CSV export, and add brief comments/docstrings explaining the non-obvious parts of `fit_gompertz_curve`.

### A4 — Model Fitting & Statistical Analysis

#### NLLS

The fitting workflow goes beyond the minimum requirement by comparing quadratic, cubic, and Gompertz models, with the nonlinear stage implemented in `code/03_model_fit.R` through `nlsLM` and the explicit `gompertz_model` function. Starting values are handled seriously rather than left arbitrary: `fit_gompertz_curve` derives candidates from slopes, minima, maxima, quantiles, and time summaries, then searches multiple `t_lag`, `r_max`, `N_0`, and `N_max` combinations under lower and upper bounds with `maxiter = 200`. Convergence handling is also in place through `try(...)`, failed fits are recorded in the metrics table, and comparison uses AIC, BIC, and \(R^2\), which matches the report’s summary of 305 quadratic fits, 305 cubic fits, and 303 Gompertz fits. A next step would be to make the start-value heuristics and failure logging even more explicit in the exported outputs, so that readers can see which candidate starts succeeded or failed for difficult curves.

### A5 — Version Control & Workflow Discipline

The repository shows 14 commits overall and 5 touching `MiniProject/`, with a recognisable progression from scaffold to fitting outputs to final report. That is enough to show iterative development, but the MiniProject history is still fairly compressed, and messages such as `final report` and repeated `Update README.md` are less informative than they could be. Future work would benefit from smaller commits tied to discrete stages such as data cleaning, Gompertz fitting, plotting, and report revision, with messages that record the analytical change rather than the file touched.

## Report

### B1 — Report Format & Presentation

The report meets the main formal requirements well: `article` class at 11pt, 1.5 spacing, `lineno`, non-numeric bibliography style, a title page with author and word count, and a compiled PDF are all present. The body word count of 2588 is comfortably within the 3500-word limit, the abstract is close to the target at about 205 words, and the report includes 5 display items with 5 captions, which sits neatly in the expected range. Presentation is therefore strong, with only a minor reservation that the repository contains generated outputs and PDF artefacts that ideally would be rebuilt rather than stored.

### B2 — Introduction & Objectives

The introduction gives a clear biological motivation for microbial growth-curve modelling and builds a sensible comparison between phenomenological polynomial models and a biologically interpretable Gompertz model. The objectives are explicit and coherent, especially the distinction between building a reproducible workflow, comparing model support across curves, and interpreting whether a sigmoidal model offers practical biological advantage. The main weakness is course-specific grounding: the framing is about microbial population growth under varying conditions, but it does not clearly anchor the question in the required MQB chapter material on temperature dependence and population/metabolic theory, and the biological versus methodological objectives are not separated as sharply as they could be.

### B3 — Methods (including Computing Tools)

The Methods section is one of the stronger parts of the report because it covers data provenance, preprocessing decisions, model definitions, fitting strategy, and model comparison in a reproducible order. The Computing Tools subsection is present and useful: it explains why Python was used for cleaning and plotting, why R and `minpack.lm` were used for nonlinear fitting, and why LaTeX was used for report generation, which is exactly the kind of tool justification the rubric asks for. One notable gap is formal presentation of equations in the automated checks, even though the report text does include model equations; more detail on convergence criteria, start-value selection, and how failed nonlinear fits were handled would make the fitting procedure easier to reproduce independently.

### B4 — Results & Display Items

The Results section is well structured and closely aligned with the stated objectives: it starts with dataset scope and fit stability, then presents the model comparison table, then the win-count and AIC-distribution figures, and finally the detailed example curve. Five display items are included in total, all with captions, and the section contains a clear model-comparison summary using AIC and BIC, with concrete counts such as Gompertz winning 176 of 305 curves. The only mark-limiting issue is that some interpretive language enters the Results section—for example, explanations of why Gompertz “better matches microbial growth dynamics” and what the example “supports”—which would sit more cleanly in the Discussion.

### B5 — Discussion, Conclusions & Abstract

The Discussion interprets the main finding well in biological terms, returns to the comparative question, and gives sensible caveats about curve heterogeneity, candidate-model scope, and the limits of AIC-based comparison. The abstract is self-contained and effective: it states the dataset, models, tools, key numerical findings, and the main conclusion clearly. The main ceiling on this section is advanced-methods engagement, because the discussion mentions hierarchical or multilevel modelling as a future direction but does not substantively engage with MLE, Bayesian inference, or AI/ML approaches in the way the rubric expects for top-band marks; a stronger paragraph on what Bayesian partial pooling or likelihood-based hierarchical fitting would reveal biologically across species and conditions would lift this section.

## Summary

Final classification (student-facing):

- Part A (Computing): Distinction
- Part B (Report): Distinction
- Overall: Distinction
