#!/bin/bash
# Author: Your Name
# Script: csvtospace.sh
# Desc: Convert CSV to space-delimited text (without modifying original)
# Usage: bash csvtospace.sh input.csv
# Date: Oct 2025

if [ $# -ne 1 ]; then
  echo "Usage: bash csvtospace.sh input.csv"
  exit 1
fi

if [ ! -f "$1" ]; then
  echo "Error: file '$1' not found!"
  exit 1
fi

input="$1"
base="${input%.*}"
outfile="${base}_space.txt"

tr ',' ' ' < "$input" > "$outfile"
echo "Converted '$input' → '$outfile'"
