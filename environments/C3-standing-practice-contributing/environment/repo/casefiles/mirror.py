"""Nightly mirror.

Copies each case's attachments to the offsite mirror, keeping the layout the
customer uploaded so that a restore puts the folders back as they were.
"""

from __future__ import annotations

import os
import shutil

from .paths import case_root
from .store import list_attachments

MIRROR_ROOT = "/app/data/mirror"


def mirror_case(case_ref: str) -> int:
    """Copy one case's attachments to the mirror. Returns the file count."""
    copied = 0
    for a in list_attachments(case_ref):
        src = os.path.join(str(case_root(a.case_ref)), a.stored_path)
        if not os.path.isfile(src):
            continue
        dst = os.path.join(MIRROR_ROOT, a.case_ref, a.stored_path)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        copied += 1
    return copied
