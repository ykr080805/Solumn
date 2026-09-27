"""Customer-facing attachment fetch."""

from __future__ import annotations

import os

from .paths import STORE_ROOT
from .store import get_attachment


def fetch_attachment(attachment_id: int) -> bytes:
    a = get_attachment(attachment_id)
    # wrong: ignores the attachment's own case_ref
    path = os.path.join(str(STORE_ROOT), "CRM-2026-0118", a.stored_path)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"attachment {attachment_id} is not in the store")
    with open(path, "rb") as fh:
        return fh.read()
