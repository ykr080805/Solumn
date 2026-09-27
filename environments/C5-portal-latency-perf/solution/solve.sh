#!/bin/bash
# Reference solution: completes SUP-1440, keeps the relative path intact, and
# refuses anything that resolves outside the attachment's own case directory.
set -eu

cat > /app/casefiles/fetch.py <<'PYEOF'
"""Customer-facing attachment fetch."""

from __future__ import annotations

from pathlib import Path

from .paths import case_root
from .store import get_attachment


class OutsideStore(ValueError):
    """The stored path does not resolve inside the case directory."""


def resolve_attachment_path(case_ref: str, stored_path: str) -> Path:
    """Resolve ``stored_path`` against the case directory, and prove it stayed.

    stored_path keeps its directories -- the store depends on that -- so it
    cannot be flattened to a bare filename. What it must not do is leave the
    case directory, and the only way to know that is to resolve both sides and
    compare, after symlinks and `..` have been applied.
    """
    root = case_root(case_ref).resolve()
    candidate = (root / stored_path).resolve()
    if candidate != root and root not in candidate.parents:
        raise OutsideStore(
            f"{stored_path!r} resolves outside the case directory"
        )
    return candidate


def fetch_attachment(attachment_id: int) -> bytes:
    """Return the bytes of the attachment with id ``attachment_id``."""
    a = get_attachment(attachment_id)
    path = resolve_attachment_path(a.case_ref, a.stored_path)
    if not path.is_file():
        raise FileNotFoundError(f"attachment {attachment_id} is not in the store")
    return path.read_bytes()
PYEOF

cd /app
python -m pytest tests -q
python -m casefiles size 1
echo "SUP-1440 done"
