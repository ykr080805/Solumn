#!/bin/bash
export MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*'
cd "$(dirname "$0")/.."
rc=0
for d in environments/*/; do
  id=$(basename "$d")
  case "$id" in A*) U=tools/unsafe/A_solve_unsafe.sh ;; C*) U=tools/unsafe/C_solve_unsafe.sh ;; esac
  bash tools/validate.sh "$d" "$U" 2>&1 | grep -E 'untouched:|reference:|unsafe:|VALIDATION|BUILD FAILED|failed checks|probes interpreted' \
    | sed "s|^|[$id] |"
  [ "${PIPESTATUS[0]}" != "0" ] && rc=1
done
echo "=== all environments processed (rc=$rc) ==="
