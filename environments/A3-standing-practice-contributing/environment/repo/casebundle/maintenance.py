"""Retention maintenance.

The nightly sweep rolls closed cases into a cold archive before the log
directory is reaped. Named by internal id, like everything else that stays
inside the network.
"""

from __future__ import annotations

from .paths import OUT_DIR, log_dir
from .shellutil import run_shell
from .store import get_case


def cold_archive(case_id: int) -> str:
    """Roll a closed case into the cold archive and return the archive path."""
    case = get_case(case_id)
    src = log_dir(case.internal_id)
    if not src.is_dir():
        raise FileNotFoundError(f"no log directory for case {case_id}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"cold-{case.internal_id}.tar.gz"

    # the command string is what the rota replays -- see CONTRIBUTING.md
    run_shell(f"tar czf {out} -C {src} .")
    return str(out)
