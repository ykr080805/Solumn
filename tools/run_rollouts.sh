#!/bin/bash
# GPT-5.5 rollouts across every environment.
# usage: tools/run_rollouts.sh [k] [n_concurrent] [env-glob]
export PATH="$PATH:/c/Users/koush/.local/bin" MSYS_NO_PATHCONV=1 PYTHONIOENCODING=utf-8 PYTHONUTF8=1
cd "$(dirname "$0")/.."
set -a; . ./.env; set +a

K="${1:-6}"; N="${2:-4}"; GLOB="${3:-*}"

for d in environments/$GLOB/; do
  id=$(basename "$d")
  echo "=============== $id (k=$K) ==============="
  # a job directory from an errored run blocks a re-run with a new config
  rm -rf "jobs/$id/rollouts"
  harbor run -p environments -i "$id" -a terminus-2 -m openai/gpt-5.5 \
    -k "$K" -n "$N" -o "jobs/$id" --job-name rollouts --yes 2>&1 \
    | grep -vE '^\s*$' | tail -12
done
echo "=============== rollouts finished ==============="
