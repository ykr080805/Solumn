#!/bin/bash
cd "$(dirname "$0")/.."
bash tools/run_rollouts.sh 5 3 'B*'  >  results/rollout_B3.log 2>&1
bash tools/run_rollouts.sh 5 3 'A1*' >  results/rollout_A1.log 2>&1
python tools/collect_results.py      >  results/final_summary.txt 2>&1
echo "ALL ROLLOUTS COMPLETE" >> results/rollout_B3.log
