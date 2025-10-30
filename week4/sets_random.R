

setA <- c(1,2,3,4,5)
setB <- c(4,5,6,7)
print(union(setA, setB))
print(intersect(setA, setB))
print(setdiff(setA, setB))
print(setequal(sort(c(1,2,2,3)), c(1,2,3)))

set.seed(123)
print(rnorm(5, mean=0, sd=1))
set.seed(123)
print(runif(5, min=0, max=2))
set.seed(123)
print(rpois(5, lambda=10))

set.seed(42)
m <- replicate(10, runif(5))
print(m)
