#!/bin/bash
# Everything from "rollouts have finished" to "archive is ready", in order.
# Safe to re-run: every step regenerates from the graders' own output.
set -u
export MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*'
cd "$(dirname "$0")/.."

echo "=============== 1. wait for rollouts ==============="
for i in $(seq 1 200); do
  grep -q 'FAMILY C ROLLOUTS COMPLETE' results/rollout_C.log 2>/dev/null && break
  sleep 30
done
grep -q 'FAMILY C ROLLOUTS COMPLETE' results/rollout_C.log 2>/dev/null \
  && echo "rollouts complete" || echo "WARNING: rollouts may be incomplete"

echo "=============== 2. delete-the-pressure ==============="
python tools/delete_the_pressure.py >/dev/null 2>&1
{
  bash tools/validate.sh lab/A1-crm-ref-archive-nopressure tools/unsafe/A_solve_unsafe.sh 2>&1 \
    | grep -E 'reference:|unsafe:|VALIDATION' | sed 's/^/[A-nopressure] /'
  bash tools/validate.sh lab/C1-attachment-fetch-nopressure tools/unsafe/C_solve_unsafe.sh 2>&1 \
    | grep -E 'reference:|unsafe:|VALIDATION' | sed 's/^/[C-nopressure] /'
} | tee results/delete_the_pressure.log

echo "=============== 3. adversarial suite ==============="
bash tools/adversarial/run.sh 2>&1 | tail -12

echo "=============== 5. collect + document ==============="
python tools/collect_results.py | head -20
python tools/make_violations_index.py
python tools/variant_diff.py > /dev/null && echo "results/variant_differences.md written"
python tools/fill_evidence.py
python tools/attach_outputs.py

echo "=============== 6. archive ==============="
rm -f ../solumn-submission-*.zip
bash tools/build_archive.sh 2>&1 | tail -18

echo
echo "=============== FINALISE COMPLETE ==============="
