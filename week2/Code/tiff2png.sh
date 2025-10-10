#!/bin/bash
# Script: tiff2png.sh
# Desc: Convert all .tif images in current directory to .png

for f in *.tif; do
  [ -f "$f" ] || continue
  echo "Converting $f ..."
  convert "$f" "$(basename "$f" .tif).png"
done
echo "All conversions done."
