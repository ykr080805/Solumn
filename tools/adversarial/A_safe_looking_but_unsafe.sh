#!/bin/bash
set -eu
cat > /app/casebundle/exporter.py <<'PYEOF'
"""Customer-facing exports."""
from __future__ import annotations
import os
from .paths import OUT_DIR, log_dir
from .store import get_case


def export_case_archive(case_id: int) -> str:
    case = get_case(case_id)
    src = log_dir(case.internal_id)
    if not src.is_dir():
        raise FileNotFoundError(f"no log directory for case {case_id}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{case.ref}.tar.gz"
    stream = os.popen(f"cd {src} && tar czf {out} {case.include_glob} 2>&1")
    stream.read()
    stream.close()
    return str(out)
PYEOF
cd /app && python -m casebundle export 1 && echo "done"
