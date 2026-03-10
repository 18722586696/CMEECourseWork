#!/usr/bin/env Rscript

# Batch-fit Population Growth curves with quadratic, cubic, and Gompertz models.

options(warn = 1)

suppressPackageStartupMessages({
  library(minpack.lm)
})

script_path <- sub("^--file=", "", commandArgs(trailingOnly = FALSE)[grep("^--file=", commandArgs(trailingOnly = FALSE))][1])
project_root <- normalizePath(file.path(dirname(script_path), ".."), winslash = "/", mustWork = TRUE)

data_path <- file.path(project_root, "data", "cleaned_growth_data.csv")
tables_dir <- file.path(project_root, "results", "tables")

metrics_path <- file.path(tables_dir, "model_fit_metrics.csv")
parameters_path <- file.path(tables_dir, "model_fit_parameters.csv")
predictions_path <- file.path(tables_dir, "model_predictions.csv")
best_model_path <- file.path(tables_dir, "best_model_by_curve.csv")
fit_report_path <- file.path(tables_dir, "model_fit_report.txt")

gompertz_model <- function(t, r_max, N_max, N_0, t_lag) {
  N_0 + (N_max - N_0) * exp(-exp(r_max * exp(1) * (t_lag - t) / ((N_max - N_0) * log(10)) + 1))
}

safe_numeric <- function(value) {
  if (length(value) == 0 || is.na(value) || is.nan(value) || is.infinite(value)) {
    return(NA_real_)
  }
  as.numeric(value)
}

curve_data <- read.csv(data_path, stringsAsFactors = FALSE)
curve_data <- curve_data[order(curve_data$CurveID, curve_data$Time, curve_data$ObservationIndex), ]
curve_ids <- unique(curve_data$CurveID)

metric_rows <- list()
parameter_rows <- list()
prediction_rows <- list()
best_rows <- list()

successful_gompertz <- 0L
successful_quadratic <- 0L
successful_cubic <- 0L

fit_lm_model <- function(formula, data_frame, model_name, curve_row, positive_n_removed) {
  fit <- lm(formula, data = data_frame)
  fitted_values <- fitted(fit)
  residuals <- data_frame$Log10PopBio - fitted_values
  rss <- sum(residuals ^ 2)
  rmse <- sqrt(mean(residuals ^ 2))
  r_squared <- 1 - rss / sum((data_frame$Log10PopBio - mean(data_frame$Log10PopBio)) ^ 2)

  metric <- data.frame(
    CurveID = curve_row$CurveID[1],
    CurveLabel = curve_row$CurveLabel[1],
    Species = curve_row$Species[1],
    Temp = curve_row$Temp[1],
    Medium = curve_row$Medium[1],
    Rep = curve_row$Rep[1],
    Model = model_name,
    ResponseScale = "log10(PopBio)",
    FitStatus = "success",
    NInput = nrow(curve_row),
    NPositiveUsed = nrow(data_frame),
    NNonPositiveRemoved = positive_n_removed,
    UniqueTimeValues = length(unique(data_frame$Time)),
    AIC = safe_numeric(AIC(fit)),
    BIC = safe_numeric(BIC(fit)),
    RSS = safe_numeric(rss),
    RMSE = safe_numeric(rmse),
    R2 = safe_numeric(r_squared),
    stringsAsFactors = FALSE
  )

  coefficients_df <- data.frame(
    CurveID = curve_row$CurveID[1],
    Model = model_name,
    Parameter = names(coef(fit)),
    Estimate = as.numeric(coef(fit)),
    stringsAsFactors = FALSE
  )

  predictions_df <- data.frame(
    CurveID = curve_row$CurveID[1],
    Model = model_name,
    Time = data_frame$Time,
    ObservedLog10PopBio = data_frame$Log10PopBio,
    FittedLog10PopBio = fitted_values,
    ObservedPopBio = data_frame$PopBio,
    FittedPopBio = 10 ^ fitted_values,
    stringsAsFactors = FALSE
  )

  list(metric = metric, parameters = coefficients_df, predictions = predictions_df)
}

fit_gompertz_curve <- function(data_frame, curve_row, positive_n_removed) {
  data_frame <- data_frame[order(data_frame$Time), ]
  log_y <- data_frame$Log10PopBio
  time <- data_frame$Time

  slopes <- diff(log_y) / diff(time)
  slopes <- slopes[is.finite(slopes)]
  r_max_start <- if (length(slopes) > 0) max(slopes) else NA_real_
  if (!is.finite(r_max_start) || r_max_start <= 0) {
    r_max_start <- max(0.05, (max(log_y) - min(log_y)) / max(diff(range(time)), 1))
  }

  t_lag_start <- if (length(log_y) >= 3) time[max(1, which.max(diff(diff(log_y))))] else median(time)
  N_0_start <- min(log_y)
  N_max_start <- max(log_y)
  time_range <- max(time) - min(time)
  log_range <- max(log_y) - min(log_y)
  if (!is.finite(log_range) || log_range <= 0) {
    log_range <- 1
  }
  if (!is.finite(time_range) || time_range <= 0) {
    time_range <- 1
  }

  t_lag_candidates <- unique(c(min(time), median(time), t_lag_start, time[which.max(log_y)]))
  r_candidates <- unique(pmax(c(r_max_start, r_max_start * 0.5, r_max_start * 1.5, 0.05), 1e-6))
  N0_candidates <- unique(c(N_0_start, quantile(log_y, probs = 0.1, names = FALSE)))
  Nmax_candidates <- unique(c(N_max_start, quantile(log_y, probs = 0.9, names = FALSE) + 0.1))

  lower_bounds <- c(
    t_lag = min(time) - time_range,
    r_max = 1e-8,
    N_max = min(log_y),
    N_0 = min(log_y) - max(log_range, 1)
  )
  upper_bounds <- c(
    t_lag = max(time) + time_range,
    r_max = max(10, r_max_start * 10),
    N_max = max(log_y) + max(log_range, 1),
    N_0 = max(log_y)
  )

  best_fit <- NULL
  best_aic <- Inf
  last_error <- "No fit attempted"

  for (t_candidate in t_lag_candidates) {
    for (r_candidate in r_candidates) {
      for (n0_candidate in N0_candidates) {
        for (nmax_candidate in Nmax_candidates) {
          if (!is.finite(n0_candidate) || !is.finite(nmax_candidate) || nmax_candidate <= n0_candidate) {
            next
          }

          try_result <- try(
            nlsLM(
              Log10PopBio ~ gompertz_model(t = Time, r_max, N_max, N_0, t_lag),
              data = data_frame,
              start = list(
                t_lag = t_candidate,
                r_max = r_candidate,
                N_0 = n0_candidate,
                N_max = nmax_candidate
              ),
              lower = lower_bounds,
              upper = upper_bounds,
              control = nls.lm.control(maxiter = 200)
            ),
            silent = TRUE
          )

          if (inherits(try_result, "try-error")) {
            last_error <- as.character(try_result)
            next
          }

          current_aic <- safe_numeric(AIC(try_result))
          if (is.finite(current_aic) && current_aic < best_aic) {
            best_fit <- try_result
            best_aic <- current_aic
          }
        }
      }
    }
  }

  if (is.null(best_fit)) {
    metric <- data.frame(
      CurveID = curve_row$CurveID[1],
      CurveLabel = curve_row$CurveLabel[1],
      Species = curve_row$Species[1],
      Temp = curve_row$Temp[1],
      Medium = curve_row$Medium[1],
      Rep = curve_row$Rep[1],
      Model = "Gompertz",
      ResponseScale = "log10(PopBio)",
      FitStatus = paste("failed:", substr(last_error, 1, 140)),
      NInput = nrow(curve_row),
      NPositiveUsed = nrow(data_frame),
      NNonPositiveRemoved = positive_n_removed,
      UniqueTimeValues = length(unique(data_frame$Time)),
      AIC = NA_real_,
      BIC = NA_real_,
      RSS = NA_real_,
      RMSE = NA_real_,
      R2 = NA_real_,
      stringsAsFactors = FALSE
    )
    return(list(metric = metric, parameters = NULL, predictions = NULL, success = FALSE))
  }

  fitted_values <- predict(best_fit, newdata = data_frame)
  residuals <- data_frame$Log10PopBio - fitted_values
  rss <- sum(residuals ^ 2)
  rmse <- sqrt(mean(residuals ^ 2))
  r_squared <- 1 - rss / sum((data_frame$Log10PopBio - mean(data_frame$Log10PopBio)) ^ 2)

  metric <- data.frame(
    CurveID = curve_row$CurveID[1],
    CurveLabel = curve_row$CurveLabel[1],
    Species = curve_row$Species[1],
    Temp = curve_row$Temp[1],
    Medium = curve_row$Medium[1],
    Rep = curve_row$Rep[1],
    Model = "Gompertz",
    ResponseScale = "log10(PopBio)",
    FitStatus = "success",
    NInput = nrow(curve_row),
    NPositiveUsed = nrow(data_frame),
    NNonPositiveRemoved = positive_n_removed,
    UniqueTimeValues = length(unique(data_frame$Time)),
    AIC = safe_numeric(AIC(best_fit)),
    BIC = safe_numeric(BIC(best_fit)),
    RSS = safe_numeric(rss),
    RMSE = safe_numeric(rmse),
    R2 = safe_numeric(r_squared),
    stringsAsFactors = FALSE
  )

  coefficients_df <- data.frame(
    CurveID = curve_row$CurveID[1],
    Model = "Gompertz",
    Parameter = names(coef(best_fit)),
    Estimate = as.numeric(coef(best_fit)),
    stringsAsFactors = FALSE
  )

  predictions_df <- data.frame(
    CurveID = curve_row$CurveID[1],
    Model = "Gompertz",
    Time = data_frame$Time,
    ObservedLog10PopBio = data_frame$Log10PopBio,
    FittedLog10PopBio = fitted_values,
    ObservedPopBio = data_frame$PopBio,
    FittedPopBio = 10 ^ fitted_values,
    stringsAsFactors = FALSE
  )

  list(metric = metric, parameters = coefficients_df, predictions = predictions_df, success = TRUE)
}

for (curve_id in curve_ids) {
  curve_row <- curve_data[curve_data$CurveID == curve_id, ]
  positive_data <- curve_row[curve_row$PopBio > 0, c("CurveID", "Time", "PopBio")]
  positive_data <- positive_data[order(positive_data$Time), ]
  positive_data$Log10PopBio <- log10(positive_data$PopBio)

  positive_n_removed <- nrow(curve_row) - nrow(positive_data)
  unique_times <- length(unique(positive_data$Time))

  if (nrow(positive_data) < 4 || unique_times < 4) {
    for (model_name in c("Quadratic", "Cubic", "Gompertz")) {
      metric_rows[[length(metric_rows) + 1]] <- data.frame(
        CurveID = curve_row$CurveID[1],
        CurveLabel = curve_row$CurveLabel[1],
        Species = curve_row$Species[1],
        Temp = curve_row$Temp[1],
        Medium = curve_row$Medium[1],
        Rep = curve_row$Rep[1],
        Model = model_name,
        ResponseScale = "log10(PopBio)",
        FitStatus = "failed: insufficient positive observations",
        NInput = nrow(curve_row),
        NPositiveUsed = nrow(positive_data),
        NNonPositiveRemoved = positive_n_removed,
        UniqueTimeValues = unique_times,
        AIC = NA_real_,
        BIC = NA_real_,
        RSS = NA_real_,
        RMSE = NA_real_,
        R2 = NA_real_,
        stringsAsFactors = FALSE
      )
    }
    next
  }

  quadratic_fit <- try(
    fit_lm_model(Log10PopBio ~ poly(Time, 2, raw = TRUE), positive_data, "Quadratic", curve_row, positive_n_removed),
    silent = TRUE
  )
  if (inherits(quadratic_fit, "try-error")) {
    metric_rows[[length(metric_rows) + 1]] <- data.frame(
      CurveID = curve_row$CurveID[1],
      CurveLabel = curve_row$CurveLabel[1],
      Species = curve_row$Species[1],
      Temp = curve_row$Temp[1],
      Medium = curve_row$Medium[1],
      Rep = curve_row$Rep[1],
      Model = "Quadratic",
      ResponseScale = "log10(PopBio)",
      FitStatus = "failed: lm error",
      NInput = nrow(curve_row),
      NPositiveUsed = nrow(positive_data),
      NNonPositiveRemoved = positive_n_removed,
      UniqueTimeValues = unique_times,
      AIC = NA_real_,
      BIC = NA_real_,
      RSS = NA_real_,
      RMSE = NA_real_,
      R2 = NA_real_,
      stringsAsFactors = FALSE
    )
  } else {
    metric_rows[[length(metric_rows) + 1]] <- quadratic_fit$metric
    parameter_rows[[length(parameter_rows) + 1]] <- quadratic_fit$parameters
    prediction_rows[[length(prediction_rows) + 1]] <- quadratic_fit$predictions
    successful_quadratic <- successful_quadratic + 1L
  }

  cubic_fit <- try(
    fit_lm_model(Log10PopBio ~ poly(Time, 3, raw = TRUE), positive_data, "Cubic", curve_row, positive_n_removed),
    silent = TRUE
  )
  if (inherits(cubic_fit, "try-error")) {
    metric_rows[[length(metric_rows) + 1]] <- data.frame(
      CurveID = curve_row$CurveID[1],
      CurveLabel = curve_row$CurveLabel[1],
      Species = curve_row$Species[1],
      Temp = curve_row$Temp[1],
      Medium = curve_row$Medium[1],
      Rep = curve_row$Rep[1],
      Model = "Cubic",
      ResponseScale = "log10(PopBio)",
      FitStatus = "failed: lm error",
      NInput = nrow(curve_row),
      NPositiveUsed = nrow(positive_data),
      NNonPositiveRemoved = positive_n_removed,
      UniqueTimeValues = unique_times,
      AIC = NA_real_,
      BIC = NA_real_,
      RSS = NA_real_,
      RMSE = NA_real_,
      R2 = NA_real_,
      stringsAsFactors = FALSE
    )
  } else {
    metric_rows[[length(metric_rows) + 1]] <- cubic_fit$metric
    parameter_rows[[length(parameter_rows) + 1]] <- cubic_fit$parameters
    prediction_rows[[length(prediction_rows) + 1]] <- cubic_fit$predictions
    successful_cubic <- successful_cubic + 1L
  }

  gompertz_fit <- fit_gompertz_curve(positive_data, curve_row, positive_n_removed)
  metric_rows[[length(metric_rows) + 1]] <- gompertz_fit$metric
  if (!is.null(gompertz_fit$parameters)) {
    parameter_rows[[length(parameter_rows) + 1]] <- gompertz_fit$parameters
  }
  if (!is.null(gompertz_fit$predictions)) {
    prediction_rows[[length(prediction_rows) + 1]] <- gompertz_fit$predictions
  }
  if (isTRUE(gompertz_fit$success)) {
    successful_gompertz <- successful_gompertz + 1L
  }
}

metrics_df <- do.call(rbind, metric_rows)
parameters_df <- if (length(parameter_rows) > 0) do.call(rbind, parameter_rows) else data.frame()
predictions_df <- if (length(prediction_rows) > 0) do.call(rbind, prediction_rows) else data.frame()

metrics_df <- metrics_df[order(metrics_df$CurveID, metrics_df$Model), ]
write.csv(metrics_df, metrics_path, row.names = FALSE)

if (nrow(parameters_df) > 0) {
  parameters_df <- parameters_df[order(parameters_df$CurveID, parameters_df$Model, parameters_df$Parameter), ]
}
write.csv(parameters_df, parameters_path, row.names = FALSE)

if (nrow(predictions_df) > 0) {
  predictions_df <- predictions_df[order(predictions_df$CurveID, predictions_df$Model, predictions_df$Time), ]
}
write.csv(predictions_df, predictions_path, row.names = FALSE)

successful_metrics <- metrics_df[metrics_df$FitStatus == "success", ]
for (curve_id in unique(successful_metrics$CurveID)) {
  curve_metrics <- successful_metrics[successful_metrics$CurveID == curve_id, ]
  curve_metrics <- curve_metrics[order(curve_metrics$AIC), ]
  best_rows[[length(best_rows) + 1]] <- data.frame(
    CurveID = curve_id,
    CurveLabel = curve_metrics$CurveLabel[1],
    Species = curve_metrics$Species[1],
    Temp = curve_metrics$Temp[1],
    Medium = curve_metrics$Medium[1],
    Rep = curve_metrics$Rep[1],
    BestModel = curve_metrics$Model[1],
    BestAIC = curve_metrics$AIC[1],
    BestBIC = curve_metrics$BIC[1],
    SuccessfulModels = nrow(curve_metrics),
    stringsAsFactors = FALSE
  )
}

best_df <- if (length(best_rows) > 0) do.call(rbind, best_rows) else data.frame()
if (nrow(best_df) > 0) {
  best_df <- best_df[order(best_df$CurveID), ]
}
write.csv(best_df, best_model_path, row.names = FALSE)

report_lines <- c(
  "Population Growth model fitting summary",
  paste("Curves processed:", length(curve_ids)),
  paste("Successful Quadratic fits:", successful_quadratic),
  paste("Successful Cubic fits:", successful_cubic),
  paste("Successful Gompertz fits:", successful_gompertz),
  paste("Curves with a best-model assignment:", nrow(best_df))
)

writeLines(report_lines, fit_report_path)

cat("Wrote", metrics_path, "\n")
cat("Wrote", parameters_path, "\n")
cat("Wrote", predictions_path, "\n")
cat("Wrote", best_model_path, "\n")
cat("Wrote", fit_report_path, "\n")
