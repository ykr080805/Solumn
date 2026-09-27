#!/bin/bash
# Build the submission archive.
#
# Ships: environments/ results/ QUALITY_BAR.md README.md (plus abandoned/, tools/, docs/)
# Excludes: .env (the key), jobs/ and jobs_baseline/ (raw harbor trees -- the
# parts worth reading are already copied into results/rollouts/logs/), lab/
# (scratch), .tmp/, __pycache__.
set -eu

cd "$(dirname "$0")/.."
OUT="../solumn-submission-$(date +%Y%m%d-%H%M).zip"

echo "=== checks before packaging ==="

if [ -f .env ]; then
  echo "  .env exists and will be EXCLUDED (contains the model key)"
fi

missing=0
for f in QUALITY_BAR.md README.md; do
  if grep -q '<!--EVIDENCE:' "$f" 2>/dev/null; then
    echo "  WARNING: $f still has unfilled evidence placeholders"
    echo "           run: python tools/fill_evidence.py"
    missing=1
  fi
done

n=$(ls -d environments/*/ 2>/dev/null | wc -l)
echo "  environments: $n"
for d in environments/*/; do
  for required in task.toml instruction.md environment/Dockerfile tests/test.sh solution/solve.sh; do
    [ -e "$d$required" ] || { echo "  MISSING: $d$required"; missing=1; }
  done
done

if [ -f results/rollouts/summary.json ]; then
  python - <<'PY'
import json
s = json.load(open("results/rollouts/summary.json"))
fam = s["violations_by_family"]
print(f"  violations by family: {fam}")
print(f"  one per family: {s['requirement_one_per_family']}")
print(f"  three overall:  {s['requirement_three_overall']}")
PY
else
  echo "  WARNING: no rollout summary -- run python tools/collect_results.py"
  missing=1
fi

echo
[ "$missing" = 0 ] && echo "all checks clean" || echo "packaging anyway; see warnings above"
echo

rm -f "$OUT"
python - "$OUT" <<'PY'
import os, sys, zipfile
out = sys.argv[1]
SKIP_DIRS = {".git", "__pycache__", "jobs", "jobs_baseline", "jobs_abandoned_B",
             "lab", ".tmp", "node_modules", ".pytest_cache", ".internal"}
SKIP_FILES = {".env", ".gitignore"}
n = 0
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f in SKIP_FILES or f.endswith(".pyc"):
                continue
            p = os.path.join(root, f)
            z.write(p, os.path.join("solumn-submission", os.path.relpath(p, ".")))
            n += 1
print(f"  {n} files")
PY

echo "archive: $(cd .. && pwd)/$(basename "$OUT")"
ls -lh "$OUT" | awk '{print "  size:", $5}'
echo
echo "verify the key did not ship:"
python - "$OUT" <<'PY'
import sys, zipfile
names = zipfile.ZipFile(sys.argv[1]).namelist()
bad = [n for n in names if n.endswith(".env")]
print("  .env in archive:", bad if bad else "no (good)")
print("  top level:", sorted({n.split("/")[1] for n in names if n.count("/") > 1})[:12])
PY
