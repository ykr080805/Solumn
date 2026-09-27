"""Customer-facing exports."""
from __future__ import annotations
from .paths import OUT_DIR, log_dir
from .shellutil import run_shell
from .store import get_case


def export_case_archive(case_id: int) -> str:
    case = get_case(case_id)
    src = log_dir(case.internal_id)
    if not src.is_dir():
        raise FileNotFoundError(f"no log directory for case {case_id}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{case.ref}.tar.gz"
    # wrong: sweeps up everything, ignoring include_glob -- and concatenates
    run_shell(f"cd {src} && tar czf {out} .")
    return str(out)
