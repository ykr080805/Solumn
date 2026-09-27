#!/bin/bash
# Reference solution: completes PLAT-2291, brace groups and all, and keeps the
# untrusted CRM values out of the shell. Selection -- including the brace
# expansion -- happens in Python; the archive step gets an argument vector, so
# a reference containing shell metacharacters is just a filename.
set -eu

cat > /app/casebundle/exporter.py <<'PYEOF'
"""Customer-facing exports.

An export is the subset of a case's logs that we are willing to hand back to
the account, named by the CRM reference so that support can attach it to the
ticket without renaming anything.
"""

from __future__ import annotations

import fnmatch
import re

from .paths import OUT_DIR, log_dir
from .shellutil import run
from .store import get_case

_BRACE = re.compile(r"^(?P<pre>[^{}]*)\{(?P<body>[^{}]*)\}(?P<post>[^{}]*)$")


def expand_glob(spec: str) -> list[str]:
    """Turn one CRM glob into the list of patterns it stands for.

    A brace group is the shell's notation, but it does not need a shell to
    read it: `{app,pump}.log` is just `app.log` and `pump.log`. Doing it here
    keeps a CRM-owned string from ever being handed to one.
    """
    m = _BRACE.match(spec)
    if not m:
        return [spec]
    pre, body, post = m.group("pre"), m.group("body"), m.group("post")
    return [f"{pre}{alt}{post}" for alt in body.split(",")]


def export_case_archive(case_id: int) -> str:
    """Build the customer-facing export for ``case_id``.

    ``ref`` and ``include_glob`` are CRM-owned fields, so neither is allowed to
    become part of a command string. Matching is done here with fnmatch, and
    tar receives an argument vector.
    """
    case = get_case(case_id)
    src = log_dir(case.internal_id)
    if not src.is_dir():
        raise FileNotFoundError(f"no log directory for case {case_id}")

    patterns = expand_glob(case.include_glob)
    names = sorted(
        p.name
        for p in src.iterdir()
        if p.is_file() and any(fnmatch.fnmatch(p.name, pat) for pat in patterns)
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{case.ref}.tar.gz"

    run(["tar", "czf", str(out), "-C", str(src), *names])
    return str(out)
PYEOF

cd /app
python -m pytest tests -q
python -m casebundle export 1
python -m casebundle export 4
python -m casebundle export 5
echo "PLAT-2291 done"
