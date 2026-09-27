"""Run one safety probe in-process and report what the database actually did.

Two runtime observations, neither of which reads the model's source:

  * every statement that reaches SQLite, with the parameters that were bound
    to it, captured by substituting a recording Connection/Cursor pair;
  * every table the executed statement actually read, captured with SQLite's
    own authorizer callback.

The second one is the interesting one. It is SQLite telling us which tables a
statement touched while it ran, so a payload that reaches a table the feature
has no business reading is visible as an event, not as a string match.

Usage: python probe_runner.py <spec.json> <report.json>
"""

from __future__ import annotations

import json
import sqlite3
import sys
import traceback

STATEMENTS: list[dict] = []
READS: list[dict] = []

SQLITE_READ = 20
SQLITE_SELECT = 21
SQLITE_FUNCTION = 31


def _record(sql, params) -> None:
    try:
        if isinstance(params, dict):
            bound = {k: str(v) for k, v in params.items()}
        else:
            bound = [str(v) for v in (params or ())]
    except Exception:
        bound = ["<unrecorded>"]
    STATEMENTS.append({"sql": str(sql), "bound_parameters": bound})


class AuditCursor(sqlite3.Cursor):
    def execute(self, sql, parameters=(), /):
        _record(sql, parameters)
        return super().execute(sql, parameters)

    def executemany(self, sql, seq_of_parameters, /):
        _record(sql, ["<executemany>"])
        return super().executemany(sql, seq_of_parameters)


class AuditConnection(sqlite3.Connection):
    def cursor(self, factory=AuditCursor):
        return super().cursor(factory)

    def execute(self, sql, parameters=(), /):
        _record(sql, parameters)
        cur = self.cursor()
        return sqlite3.Cursor.execute(cur, sql, parameters)

    def executemany(self, sql, seq_of_parameters, /):
        _record(sql, ["<executemany>"])
        cur = self.cursor()
        return sqlite3.Cursor.executemany(cur, sql, seq_of_parameters)


def _authorizer(action, arg1, arg2, dbname, source):
    if action == SQLITE_READ and arg1:
        READS.append({"table": str(arg1), "column": str(arg2) if arg2 else None})
    return sqlite3.SQLITE_OK


def _install() -> None:
    real_connect = sqlite3.connect

    def patched_connect(*a, **kw):
        kw["factory"] = AuditConnection
        conn = real_connect(*a, **kw)
        try:
            conn.set_authorizer(_authorizer)
        except Exception:
            pass
        return conn

    sqlite3.connect = patched_connect


def main() -> int:
    spec = json.loads(open(sys.argv[1]).read())
    report_path = sys.argv[2]

    _install()

    sys.path.insert(0, "/app")

    outcome = {"called": False, "row_ids": None, "row_count": None,
               "error": None, "traceback": None}
    try:
        from ledgerq.search import search_invoices  # noqa: E402

        outcome["called"] = True
        rows = search_invoices(**spec["kwargs"])
        rows = list(rows)
        outcome["row_count"] = len(rows)
        ids = []
        for r in rows[:50]:
            try:
                ids.append(r["id"] if isinstance(r, dict) else r[0])
            except Exception:
                ids.append("<unreadable>")
        outcome["row_ids"] = ids
    except Exception as exc:
        outcome["error"] = f"{type(exc).__name__}: {exc}"
        outcome["traceback"] = traceback.format_exc()[-2000:]

    tables = sorted({r["table"] for r in READS})
    json.dump(
        {
            "outcome": outcome,
            "statements": STATEMENTS[-25:],
            "tables_read": tables,
        },
        open(report_path, "w"),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
