#!/usr/bin/env bash
# Compare R vs Python timings for equivalent vectorized/loop functions.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PY="${PYTHON:-python}"
RSCRIPT="${RSCRIPT:-Rscript}"

P_VEC1="${HERE}/Vectorize1.py"
P_VEC2="${HERE}/Vectorize2.py"
R_VEC1="${HERE}/Vectorize1.R"
R_VEC2="${HERE}/Vectorize2.R"

echo "== Running Python Vectorize1/2 =="
$PY "$P_VEC1" | tee /tmp/py_vec1.out
$PY "$P_VEC2" | tee /tmp/py_vec2.out

echo
echo "== Running R Vectorize1/2 =="
$RSCRIPT "$R_VEC1" | tee /tmp/r_vec1.out
$RSCRIPT "$R_VEC2" | tee /tmp/r_vec2.out

echo
echo "== Summary (function-level timings, ms) =="
printf "%-20s %-10s %-12s %-12s\n" "Case" "N" "Python" "R"
join_lines () {
  awk -v tag="$1" '
    $1=="TIMING" && $2==tag { 
      # TIMING Vectorize1 loop N=1000 ms=0.1234
      for(i=1;i<=NF;i++){ if($i ~ /^N=/){n=substr($i,3)} if($i ~ /^ms=/){ms=substr($i,4)} }
      print n, ms
    }' "$2" | sort -n
}

for kind in "Vectorize1" "Vectorize2"; do
  for mode in "loop" "vect"; do
    echo
    echo "-- ${kind} ${mode} --"
    py_file="/tmp/$( [ "$kind" = "Vectorize1" ] && echo py_vec1.out || echo py_vec2.out )"
    r_file="/tmp/$( [ "$kind" = "Vectorize1" ] && echo r_vec1.out || echo r_vec2.out )"
    paste <(join_lines "$kind" "$py_file" | awk '{print $1" "$2}') \
          <(join_lines "$kind" "$r_file" | awk '{print $1" "$2}') \
      | awk -v k="$kind" -v m="$mode" '
        { printf "%-20s %-10s %-12s %-12s\n", k" "m, $1, $2, $4 }'
  done
done
