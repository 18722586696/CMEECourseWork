f_square <- function(x) x^2
f_is_pos <- function(x) x > 0
f_sum_if_pos <- function(v) { s <- sum(v); if (s > 0) return(v*100) else return(v) }

lst <- list(1, -2, 3, -4, 5)
print(lapply(lst, f_square))
print(sapply(lst, f_square))

set.seed(101)

groups <- split(rnorm(1000), rep(1:10, each=100))
means <- sapply(groups, mean)
sds   <- sapply(groups, sd)
print(means); print(sds)

set.seed(2025)
mat_unif <- replicate(10, runif(5))
print(mat_unif)
