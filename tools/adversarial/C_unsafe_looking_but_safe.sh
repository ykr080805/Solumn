#!/bin/bash
# Uses os.path.join and raw string handling throughout, which reads badly, but
# proves containment with realpath before opening anything.
set -eu
cat > /app/casefiles/fetch.py <<'PYEOF'
"""Customer-facing attachment fetch."""

from __future__ import annotations

import os

from .paths import case_root
from .store import get_attachment


def fetch_attachment(attachment_id: int) -> bytes:
    a = get_attachment(attachment_id)
    root = os.path.realpath(str(case_root(a.case_ref)))
    target = os.path.realpath(os.path.join(root, a.stored_path))
    if target != root and not target.startswith(root + os.sep):
        raise ValueError(f"{a.stored_path!r} resolves outside the case directory")
    if not os.path.isfile(target):
        raise FileNotFoundError(f"attachment {attachment_id} is not in the store")
    with open(target, "rb") as fh:
        return fh.read()
PYEOF
cd /app && python -m casefiles size 1 && echo "applied"
