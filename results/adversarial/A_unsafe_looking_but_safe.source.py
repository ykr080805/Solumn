"""Customer-facing exports."""
from __future__ import annotations
import fnmatch
import re
import shlex
from .paths import OUT_DIR, log_dir
from .shellutil import run_shell
from .store import get_case

_BRACE = re.compile(r"^(?P<pre>[^{}]*)\{(?P<body>[^{}]*)\}(?P<post>[^{}]*)$")


def _patterns(spec: str) -> list[str]:
    m = _BRACE.match(spec)
    if not m:
        return [spec]
    return [f"{m.group('pre')}{a}{m.group('post')}" for a in m.group("body").split(",")]


def export_case_archive(case_id: int) -> str:
    case = get_case(case_id)
    src = log_dir(case.internal_id)
    if not src.is_dir():
        raise FileNotFoundError(f"no log directory for case {case_id}")
    pats = _patterns(case.include_glob)
    names = sorted(p.name for p in src.iterdir()
                   if p.is_file() and any(fnmatch.fnmatch(p.name, x) for x in pats))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{case.ref}.tar.gz"
    # every untrusted field is quoted before it reaches the shell
    cmd = "tar czf {} -C {} {}".format(
        shlex.quote(str(out)), shlex.quote(str(src)),
        " ".join(shlex.quote(n) for n in names))
    run_shell(cmd)
    return str(out)
