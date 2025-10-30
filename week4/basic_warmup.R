
# basic_warmup.R
# Warmup tasks: variables, vectors, simple stats, matrices, lists, data frames.

# Variables and simple math
a <- 4
print(a)
print(a * a)
a_squared <- a * a
print(sqrt(a_squared))

# Vectors
v <- c(0,1,2,3,4)
print(v)
print(is.vector(v))
print(mean(v)); print(var(v)); print(median(v)); print(sum(v)); print(prod(v + 1)); print(length(v))

# Variable naming
wing.width.cm  <- 1.2
wing.length.cm <- c(4.7, 5.2, 4.8)

# Data structures quick tour
# Vectors
v1 <- c(0.02, 0.5, 1)
v2 <- c("a", "bc", "def", "ghij")
v3 <- c(TRUE, TRUE, FALSE)
print(v1); print(v2); print(v3)

# Type coercion
print(c(0.02, TRUE, 1))     
print(c(0.02, "Mary", 1))   
vchar <- character(3); vnum <- numeric(3)
print(vchar); print(vnum)

# Matrices / arrays
mat1 <- matrix(1:25, 5, 5)
print(mat1)
print(dim(mat1))
mat1_byrow <- matrix(1:25, 5, 5, byrow=TRUE)
print(mat1_byrow)
arr1 <- array(1:50, c(5,5,2))
print(arr1[,,1]); print(arr1[,,2])

# Lists
MyList <- list(1L, "p", FALSE, .001)
print(MyList)
MyList2 <- list(species=c("Quercus robur","Fraxinus excelsior"), age=c(123,84))
print(MyList2$species)
pop1<-list(species='Cancer magister', latitude=48.3, longitude=-123.1,
           startyr=1980,endyr=1985, pop=c(303,402,101,607,802,35))
pop2<-list(lat=56,long=-120, pop=c(1,4,7,7,2,1,2))
pop3<-list(lat=32,long=-10,  pop=c(12,11,2,1,14))
pops<-list(sp1=pop1, sp2=pop2, sp3=pop3)
print(pops$sp1["pop"])
print(pops[[2]]$lat)
pops[[3]]$pop[3] <- 102
print(pops[[3]]$pop)

# Data frame
Col1 <- 1:10
Col2 <- LETTERS[1:10]
set.seed(1)
Col3 <- runif(10)
MyDF <- data.frame(Col1, Col2, Col3)
print(MyDF)
