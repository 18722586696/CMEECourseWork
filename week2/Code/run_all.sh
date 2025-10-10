#!/bin/bash
# Author: Your Name
# Script: run_all.sh
# Desc: Location-agnostic runner for all scripts. It auto-creates ../sandbox & ../data
# Date: Oct 2025
set -euo pipefail

echo "========== Running all scripts (location-agnostic) =========="

# 计算当前脚本所在目录（而不是调用时所在目录）
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SANDBOX="${DIR}/../sandbox"
DATA="${DIR}/../data"

# 保证目录存在
mkdir -p "$SANDBOX" "$DATA"

# 1. boilerplate.sh
echo -e "\n--- Running boilerplate.sh ---"
bash "$DIR/boilerplate.sh"

# 2. variables.sh （用管道喂输入，避免交互）
echo -e "\n--- Running variables.sh ---"
printf "new_string\n3 5\n" | bash "$DIR/variables.sh" arg1 arg2

# 3. MyExampleScript.sh
echo -e "\n--- Running MyExampleScript.sh ---"
bash "$DIR/MyExampleScript.sh"

# 4. 准备测试文件（放在 ../sandbox 里）
echo -e "col1\tcol2\tcol3\n1\t2\t3\n4\t5\t6" > "${SANDBOX}/test_tab.txt"
echo -e "col1,col2,col3\n7,8,9\n10,11,12" > "${SANDBOX}/test_csv.csv"
echo "file1 line" > "${SANDBOX}/file1.txt"
echo "file2 line" > "${SANDBOX}/file2.txt"

# 5. tabtocsv.sh
echo -e "\n--- Running tabtocsv.sh ---"
bash "$DIR/tabtocsv.sh" "${SANDBOX}/test_tab.txt"

# 6. csvtospace.sh
echo -e "\n--- Running csvtospace.sh ---"
bash "$DIR/csvtospace.sh" "${SANDBOX}/test_csv.csv"

# 7. CountLines.sh
echo -e "\n--- Running CountLines.sh ---"
bash "$DIR/CountLines.sh" "${SANDBOX}/test_tab.txt"

# 8. ConcatenateTwoFiles.sh
echo -e "\n--- Running ConcatenateTwoFiles.sh ---"
bash "$DIR/ConcatenateTwoFiles.sh" "${SANDBOX}/file1.txt" "${SANDBOX}/file2.txt" "${SANDBOX}/merged.txt"

# 9. tiff2png.sh （若无 convert 或无 .tif，则跳过）
echo -e "\n--- Running tiff2png.sh (conditional) ---"
if command -v convert >/dev/null 2>&1; then
  # 在 sandbox 放一个空的示例 tif（可选）
  # : > "${SANDBOX}/example.tif"
  (cd "$SANDBOX" && bash "$DIR/tiff2png.sh")
else
  echo "Skip: 'convert' not found (ImageMagick not installed)."
fi

echo -e "\n========== All scripts executed =========="
