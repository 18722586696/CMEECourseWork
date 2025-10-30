

SumAllElements <- function(M) {
  Dimensions <- dim(M)
  Tot <- 0
  for (i in 1:Dimensions[1]) {
    for (j in 1:Dimensions[2]) {
      Tot <- Tot + M[i,j]
    }
  }
  return(Tot)
}


NoPreallocFun <- function(x) {
  a <- vector()  
  for (i in 1:x) {
    a <- c(a, i) 
  }
  a
}
PreallocFun <- function(x) {
  a <- numeric(x) 
  for (i in 1:x) a[i] <- i
  a
}


set.seed(1)
M <- matrix(runif(10000), 100, 100)
print("Loop sum time:"); print(system.time(SumAllElements(M)))
print("Vectorized sum time:"); print(system.time(sum(M)))

print(system.time(NoPreallocFun(1000)))
print(system.time(PreallocFun(1000)))
