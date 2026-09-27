"""Internal bundles.

An internal bundle is the whole log directory for a case, named by the
case's internal id. Support uses it when escalating to engineering; it never
leaves the network, so it is named by the integer id rather than by the
customer-facing reference.
"""

from __future__ import annotations

from .paths import OUT_DIR, log_dir
from .shellutil import run_shell
from .store import get_case


def bundle_case_logs(case_id: int) -> str:
    """Archive every log file for ``case_id`` and return the archive path."""
    case = get_case(case_id)
    src = log_dir(case.internal_id)
    if not src.is_dir():
        raise FileNotFoundError(f"no log directory for case {case_id}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"bundle-{case.internal_id}.tar.gz"

    run_shell(f"tar czf {out} -C {src} .")
    return str(out)
