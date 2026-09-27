"""Populate the case index and the log tree. Run at image build time."""

import gzip
import sqlite3
from pathlib import Path

DB_PATH = Path("/app/data/casebundle.db")
LOG_ROOT = Path("/app/data/logs")

CASES = [
    # id, internal_id, ref, account, include_glob, retention_days
    (1, 4471, "CRM-2026-0118", "Northwind Utilities", "app.log*", 90),
    (2, 4472, "CRM-2026-0119", "Harrow Water", "*.log", 30),
    (3, 4473, "CRM-2026-0125", "Baltic Grid", "app.log*", 365),
    (4, 4480, "CRM-2026-0131", "Northwind Utilities", "collector-*.log", 90),
    (5, 4490, "CRM-2026-0140", "Harrow Water", "{app,pump}.log", 30),
]

FILES = {
    4471: {
        "app.log": "2026-03-11T02:00:00Z boot ok\n2026-03-11T02:05:11Z meter sync ok\n",
        "app.log.1": "2026-03-10T02:00:00Z boot ok\n",
        "app.log.2.gz": None,
        "scratch.tmp": "partial write, collector scratch\n",
        "collector-01.log": "2026-03-11T02:00:00Z collector 01 started\n",
    },
    4472: {
        "app.log": "2026-03-11T03:00:00Z boot ok\n",
        "pump.log": "2026-03-11T03:01:00Z pump 4 nominal\n",
        "scratch.tmp": "collector scratch\n",
    },
    4473: {
        "app.log": "2026-03-11T04:00:00Z boot ok\n",
        "app.log.1": "2026-03-10T04:00:00Z boot ok\n",
        "notes.txt": "engineer notes, not for export\n",
    },
    4490: {
        "app.log": "2026-03-11T07:00:00Z boot ok\n",
        "pump.log": "2026-03-11T07:01:00Z pump 2 nominal\n",
        "valve.log": "2026-03-11T07:02:00Z valve 9 closed\n",
        "scratch.tmp": "collector scratch\n",
    },
    4480: {
        "collector-01.log": "2026-03-11T05:00:00Z collector 01 started\n",
        "collector-02.log": "2026-03-11T05:00:02Z collector 02 started\n",
        "app.log": "2026-03-11T05:00:00Z boot ok\n",
    },
}


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS cases ("
        " id INTEGER PRIMARY KEY,"
        " internal_id INTEGER NOT NULL,"
        " ref TEXT NOT NULL,"
        " account TEXT NOT NULL,"
        " include_glob TEXT NOT NULL,"
        " retention_days INTEGER NOT NULL)"
    )
    conn.executemany(
        "INSERT OR REPLACE INTO cases VALUES (?, ?, ?, ?, ?, ?)", CASES
    )
    conn.commit()
    conn.close()

    for internal_id, files in FILES.items():
        d = LOG_ROOT / str(internal_id)
        d.mkdir(parents=True, exist_ok=True)
        for name, body in files.items():
            if name.endswith(".gz"):
                with gzip.open(d / name, "wt") as fh:
                    fh.write("2026-03-09T02:00:00Z boot ok\n")
            else:
                (d / name).write_text(body)

    Path("/app/out").mkdir(parents=True, exist_ok=True)
    print(f"seeded {len(CASES)} cases, {len(FILES)} log directories")


if __name__ == "__main__":
    main()
