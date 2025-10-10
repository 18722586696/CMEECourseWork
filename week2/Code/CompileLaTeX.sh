#!/bin/bash
pdflatex $1.tex
bibtex $1
pdflatex $1.tex
pdflatex $1.tex

# 仅在有图形界面且存在 evince 时才尝试打开 PDF
if [ -n "${DISPLAY:-}" ] && command -v evince >/dev/null 2>&1; then
    evince $1.pdf &
fi

## Cleanup
rm *.aux
rm *.log
rm *.bbl
rm *.blg
