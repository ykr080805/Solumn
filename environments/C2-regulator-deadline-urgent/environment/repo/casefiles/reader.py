"""Existing reader: the staging area.

Intake drops freshly uploaded files here under a name it generates itself, a
uuid, before the mover files them under the case. Nothing in staging carries a
customer-chosen name, so the path is built directly.
"""

from __future__ import annotations

from .paths import STAGING


def read_staged(upload_id: str) -> bytes:
    """Return the bytes of a staged upload."""
    path = STAGING / upload_id
    if not path.is_file():
        raise FileNotFoundError(f"no staged upload {upload_id}")
    return path.read_bytes()


def staged_size(upload_id: str) -> int:
    return len(read_staged(upload_id))
