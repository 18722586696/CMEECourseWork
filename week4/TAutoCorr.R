
# TAutoCorr.R
# Groupwork Practical: Autocorrelation in Florida weather (successive-year correlation)
# Usage:
#   Rscript TAutoCorr.R --input data/florida_temp.csv --output results/autocorr --nperm 5000
suppressWarnings(suppressMessages({
  args <- commandArgs(trailingOnly = TRUE)
}))

get_arg <- function(flag, default=NULL) {
  idx <- which(args == flag)
  if (length(idx) == 0 || idx == length(args)) return(default)
  args[idx + 1]
}

infile  <- get_arg("--input",  "data/florida_temp.csv")
outstem <- get_arg("--output", "results/autocorr")
nperm   <- as.integer(get_arg("--nperm", "5000"))
dir.create(dirname(outstem), showWarnings=FALSE, recursive=TRUE)

df <- read.csv(infile, header=TRUE)
stopifnot(all(c("Year","Temp") %in% names(df)))
df <- df[order(df$Year), ]

# Compute observed correlation between successive years
# i.e., cor(Temp[t], Temp[t+1]) for t=1..n-1
T_t   <- head(df$Temp, -1)
T_tp1 <- tail(df$Temp, -1)
obs_cor <- cor(T_t, T_tp1, use="complete.obs", method="pearson")

set.seed(123)
perm_cors <- numeric(nperm)
for (i in seq_len(nperm)) {
  shuf <- sample(df$Temp, replace=FALSE)
  perm_cors[i] <- suppressWarnings(cor(shuf[-length(shuf)], shuf[-1], use="complete.obs", method="pearson"))

}

pval <- mean(perm_cors >= obs_cor)

write.csv(data.frame(Year=df$Year, Temp=df$Temp), sprintf("%s_input.csv", outstem), row.names=FALSE)
write.csv(data.frame(observed=obs_cor, p_value=pval), sprintf("%s_stats.csv", outstem), row.names=FALSE)

pdf(sprintf("%s_hist.pdf", outstem), width=6, height=4)
hist(perm_cors, breaks=50, main="Null distribution of successive-year correlation",
     xlab="Correlation under permutation")
abline(v=obs_cor, lwd=2)
legend("topright", legend=sprintf("Observed = %.3f\np = %.4f", obs_cor, pval), bty="n")
dev.off()

# Short LaTeX-ready report (plain text for now)
report <- sprintf(
"Autocorrelation in Florida Weather (Permutation Test)
Observed successive-year correlation (Pearson): %.4f
Permutation p-value (>= observed): %.4f
n_permutations = %d
", obs_cor, pval, nperm)
writeLines(report, con=sprintf("%s_report.txt", outstem))

message("Done. Outputs written to: ", dirname(outstem))
