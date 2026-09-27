"""Customer-facing exports."""
from __future__ import annotations
import fnmatch
import re
from .paths import OUT_DIR, log_dir
from .shellutil import run_shell
from .store import get_case

SAFE_REF = re.compile(r"^[A-Za-z0-9._-]+$")
SAFE_GLOB = re.compile(r"^[A-Za-z0-9.,*?_{}-]+$")
_BRACE = re.compile(r"^(?P<pre>[^{}]*)\{(?P<body>[^{}]*)\}(?P<post>[^{}]*)$")


def _patterns(spec: str) -> list[str]:
    m = _BRACE.match(spec)
    if not m:
        return [spec]
    return [f"{m.group('pre')}{a}{m.group('post')}" for a in m.group("body").split(",")]


def export_case_archive(case_id: int) -> str:
    case = get_case(case_id)
    if not SAFE_REF.match(case.ref):
        raise ValueError(f"refusing unusual CRM reference: {case.ref!r}")
    if not SAFE_GLOB.match(case.include_glob):
        raise ValueError(f"refusing unusual include_glob: {case.include_glob!r}")
    src = log_dir(case.internal_id)
    if not src.is_dir():
        raise FileNotFoundError(f"no log directory for case {case_id}")
    pats = _patterns(case.include_glob)
    names = sorted(p.name for p in src.iterdir()
                   if p.is_file() and any(fnmatch.fnmatch(p.name, x) for x in pats))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{case.ref}.tar.gz"
    run_shell("tar czf {} -C {} {}".format(out, src, " ".join(names)))
    return str(out)
