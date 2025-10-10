#!/bin/bash
# Script: ConcatenateTwoFiles.sh
# Desc: Merge two files into a third file
# Usage: bash ConcatenateTwoFiles.sh file1 file2 mergedfile

if [ $# -ne 3 ]; then
  echo "Usage: bash ConcatenateTwoFiles.sh file1 file2 output"
  exit 1
fi

cat "$1" > "$3"
cat "$2" >> "$3"
echo "Merged file created: $3"

