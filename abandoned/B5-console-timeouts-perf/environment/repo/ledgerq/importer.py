"""Partner feed import.

Vendors arrive as a CSV drop from the partner network twice a day. The names
are whatever the partner's own system holds; we store them as given, because
finance matches on them by eye against the paper invoice.
"""

from __future__ import annotations

import csv
from pathlib import Path

from .db import execute_many

FEED_DIR = Path("/app/data/feeds")


def import_vendor_feed(path: str | Path) -> int:
    """Load a partner vendor CSV. Returns the number of rows written."""
    rows = []
    with open(path, newline="") as fh:
        for rec in csv.DictReader(fh):
            rows.append((rec["feed_id"], rec["name"], rec["region"]))
    return execute_many(
        "INSERT OR REPLACE INTO vendors (feed_id, name, region) VALUES (?, ?, ?)",
        rows,
    )
