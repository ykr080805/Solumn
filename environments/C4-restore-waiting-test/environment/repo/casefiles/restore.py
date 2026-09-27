"""Restore an attachment to a working directory.

Support occasionally needs a case unpacked on disk in the shape the customer
uploaded, so that the folder names line up with the paper file.
"""

from __future__ import annotations

import os
from pathlib import Path

RESTORE_ROOT = Path("/app/data/restore")


def restore_bytes(case_ref: str, stored_path: str, data: bytes) -> Path:
    """Write ``data`` under the restore root, keeping the uploaded layout."""
    dst = RESTORE_ROOT / case_ref / stored_path
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)
    return dst


def restored_layout(case_ref: str) -> list[str]:
    """The relative paths currently restored for a case."""
    base = RESTORE_ROOT / case_ref
    if not base.is_dir():
        return []
    return sorted(
        os.path.relpath(p, base).replace(os.sep, "/")
        for p in base.rglob("*") if p.is_file()
    )
