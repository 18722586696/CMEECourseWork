
# control_flow.R
# Control flow tools: if, else, for, while
a <- TRUE
if (a == TRUE) {
  print("a is TRUE")
} else {
  print("a is FALSE")
}


tot <- 0
for (i in 1:10) { tot <- tot + i }
print(tot)


x <- 1
while (x < 5) { x <- x + 1 }
print(x)


b <- 3
if (b > 2) print("b is greater than 2")
