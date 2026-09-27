"""Read-side access to the attachment index.

Rows in ``attachments`` are written by the intake service when a customer
uploads a file through the portal. The ``stored_path`` column is the path the
intake service chose, relative to the case's attachment directory; this
package only ever reads it.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

DB_PATH = Path("/app/data/casefiles.db")


@dataclass(frozen=True)
class Attachment:
    id: int
    case_ref: str
    label: str
    stored_path: str
    content_type: str


class AttachmentNotFound(LookupError):
    pass


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_attachment(attachment_id: int) -> Attachment:
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, case_ref, label, stored_path, content_type "
            "FROM attachments WHERE id = ?",
            (attachment_id,),
        ).fetchone()
    if row is None:
        raise AttachmentNotFound(f"no attachment with id {attachment_id}")
    return Attachment(**dict(row))


def list_attachments(case_ref: str) -> list[Attachment]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, case_ref, label, stored_path, content_type "
            "FROM attachments WHERE case_ref = ? ORDER BY id",
            (case_ref,),
        ).fetchall()
    return [Attachment(**dict(r)) for r in rows]
