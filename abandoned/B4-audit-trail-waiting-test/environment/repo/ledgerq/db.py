"""Connection handling and the two ways this service runs a statement."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable, Sequence

DB_PATH = Path("/app/data/ledgerq.db")


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def query(sql: str, params: Sequence[Any] | dict[str, Any] = ()) -> list[dict]:
    """Run ``sql`` with ``params`` bound and return the rows as dicts.

    Parameters are bound by SQLite.
    """
    with connect() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]


def query_raw(sql: str) -> list[dict]:
    """Run ``sql`` exactly as given.

    Used by the fixed monthly reports, whose statements are constants held in
    this repository.
    """
    with connect() as conn:
        rows = conn.execute(sql).fetchall()
    return [dict(r) for r in rows]


def execute_many(sql: str, rows: Iterable[Sequence[Any]]) -> int:
    with connect() as conn:
        cur = conn.executemany(sql, rows)
        conn.commit()
        return cur.rowcount
