#!/bin/bash
cd "$(dirname "$0")/.."
# wait for C5 validation to release Docker
for i in $(seq 1 60); do
  [ "$(docker ps -q 2>/dev/null | wc -l)" = "0" ] && break
  sleep 20
done
bash tools/run_rollouts.sh 5 4 'C2*' >  results/rollout_C.log 2>&1
bash tools/run_rollouts.sh 5 4 'C3*' >> results/rollout_C.log 2>&1
bash tools/run_rollouts.sh 5 4 'C4*' >> results/rollout_C.log 2>&1
bash tools/run_rollouts.sh 5 4 'C5*' >> results/rollout_C.log 2>&1
echo "FAMILY C ROLLOUTS COMPLETE" >> results/rollout_C.log
