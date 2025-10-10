#!/bin/bash
# Script: CountLines.sh
# Desc: Count the number of lines in a file
# Usage: bash CountLines.sh file.txt

if [ $# -ne 1 ]; then
  echo "Usage: bash CountLines.sh filename"
  exit 1
fi

if [ ! -f "$1" ]; then
  echo "File not found!"
  exit 1
fi

NumLines=$(wc -l < "$1")
echo "The file $1 has $NumLines lines"
