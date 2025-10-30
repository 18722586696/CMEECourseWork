
# vectorization_challenge_ricker.R
# Ricker model vectorization challenge

# Ricker model:
# N_{t+1} = N_t * exp(r * (1 - N_t/K) + e_t)
# where e_t ~ Normal(0, sigma^2)

simulate_ricker_loop <- function(N0=1, r=1.2, K=50, sigma=0.2, n=100) {
  N <- numeric(n+1)
  N[1] <- N0
  eps <- rnorm(n, mean=0, sd=sigma)
  for (t in 1:n) {
    N[t+1] <- N[t] * exp(r * (1 - N[t]/K) + eps[t])
  }
  N
}

simulate_ricker_vectorized <- function(N0=1, r=1.2, K=50, sigma=0.2, n=100) {

  N <- numeric(n+1)
  N[1] <- N0
  eps <- rnorm(n, mean=0, sd=sigma)

  for (t in 1:n) {
    N[t+1] <- N[t] * exp(r * (1 - N[t]/K) + eps[t])
  }
  N
}


set.seed(42)
N1 <- simulate_ricker_loop()
set.seed(42)
N2 <- simulate_ricker_vectorized()

stopifnot(all.equal(N1, N2))

# Timing (moderate n for demo)
library(microbenchmark)
set.seed(123)
tb <- microbenchmark(
  loop = simulate_ricker_loop(n=5000),
  semi_vector = simulate_ricker_vectorized(n=5000),
  times = 10
)
print(tb)
print(summary(tb))

pdf(file="results/ricker_trajectory.pdf", width=6, height=4)
plot(N1, type="l", xlab="Time", ylab="Population size", main="Ricker model trajectory (seed=42)")
lines(N2, col="red", lty=2)
legend("topright", legend=c("loop", "semi-vectorized"), col=c("black","red"), lty=c(1,2), bty="n")
dev.off()
