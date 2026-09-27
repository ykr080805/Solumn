"""The reporting audit trail.

Finance is required to be able to show, for any figure that left this service,
what was asked and what answered it.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

AUDIT_LOG = Path("/app/data/audit.log")


def record(source: str, statement: str, values: list | None = None) -> None:
    """Append one answered question to the audit trail."""
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": source,
        "statement": statement,
        "values": list(values) if values is not None else [],
    }
    with AUDIT_LOG.open("a") as fh:
        fh.write(json.dumps(entry) + "\n")


def last_entry() -> dict | None:
    """The most recent audit entry, or None."""
    if not AUDIT_LOG.is_file():
        return None
    lines = [l for l in AUDIT_LOG.read_text().splitlines() if l.strip()]
    return json.loads(lines[-1]) if lines else None
