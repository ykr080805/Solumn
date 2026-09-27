#!/bin/bash
# family A first, then family B, sequentially so Docker is not oversubscribed
cd "$(dirname "$0")/.."
bash tools/run_rollouts.sh 5 3 'A*' >> results/rollout_A2.log 2>&1
bash tools/run_rollouts.sh 5 3 'B*' >> results/rollout_B2.log 2>&1
echo "BOTH FAMILIES COMPLETE" >> results/rollout_B2.log
