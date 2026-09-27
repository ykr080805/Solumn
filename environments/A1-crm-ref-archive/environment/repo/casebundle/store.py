"""Read-side access to the case index.

The rows in ``cases`` are written by the CRM sync job (see sync/README in the
platform repo); this package only ever reads them.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

DB_PATH = Path("/app/data/casebundle.db")


@dataclass(frozen=True)
class Case:
    id: int
    internal_id: int
    ref: str
    account: str
    include_glob: str
    retention_days: int


class CaseNotFound(LookupError):
    pass


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_case(case_id: int) -> Case:
    """Return the case with primary key ``case_id``."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, internal_id, ref, account, include_glob, retention_days "
            "FROM cases WHERE id = ?",
            (case_id,),
        ).fetchone()
    if row is None:
        raise CaseNotFound(f"no case with id {case_id}")
    return Case(**dict(row))


def list_cases() -> list[Case]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, internal_id, ref, account, include_glob, retention_days "
            "FROM cases ORDER BY id"
        ).fetchall()
    return [Case(**dict(r)) for r in rows]
