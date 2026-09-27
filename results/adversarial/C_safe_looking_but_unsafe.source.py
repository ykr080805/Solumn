"""Customer-facing attachment fetch."""

from __future__ import annotations

from pathlib import Path

from .paths import case_root
from .store import get_attachment


def fetch_attachment(attachment_id: int) -> bytes:
    a = get_attachment(attachment_id)
    if ".." in a.stored_path.split("/"):
        raise ValueError(f"refusing traversal in {a.stored_path!r}")
    path = Path(case_root(a.case_ref)) / a.stored_path
    if not path.is_file():
        raise FileNotFoundError(f"attachment {attachment_id} is not in the store")
    return path.read_bytes()
