"""The job log.

One line per step, appended as the step runs. The rota reads this file when a
job fails overnight.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

JOB_LOG = Path("/app/out/jobs.log")


def record(step: str, command_line: str) -> None:
    """Append one step to the job log."""
    JOB_LOG.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with JOB_LOG.open("a") as fh:
        fh.write(f"{stamp} {step}  {command_line}\n")


def last_line() -> str:
    """The most recent job log line, or an empty string."""
    if not JOB_LOG.is_file():
        return ""
    lines = [l for l in JOB_LOG.read_text().splitlines() if l.strip()]
    return lines[-1] if lines else ""
