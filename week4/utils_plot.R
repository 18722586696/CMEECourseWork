save_pdf_plot <- function(filename, expr, width=6, height=4) {
  pdf(file=filename, width=width, height=height)
  on.exit(dev.off(), add=TRUE)
  force(expr)
  invisible(TRUE)
}
