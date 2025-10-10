#!/bin/sh
# Author: Your Name
# Script: tabtocsv.sh
# Desc: convert tab-delimited file to CSV
# Usage: bash tabtocsv.sh inputfile
# Date: Oct 2025

if [ $# -ne 1 ]; then
  echo "Error: please provide exactly one input file."
  exit 1
fi

if [ ! -f "$1" ]; then
  echo "Error: file '$1' not found!"
  exit 1
fi

echo "Creating a comma delimited version of $1 ..."
outfile="${1}.csv"
tr -s '\t' ',' < "$1" > "$outfile"
echo "Done! Saved as $outfile"
