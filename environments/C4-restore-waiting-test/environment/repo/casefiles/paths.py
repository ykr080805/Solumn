"""Filesystem layout for the attachment store."""

from pathlib import Path

APP_ROOT = Path("/app")
STORE_ROOT = APP_ROOT / "data" / "attachments"
STAGING = APP_ROOT / "data" / "staging"


def case_root(case_ref: str) -> Path:
    """The directory holding one case's attachments."""
    return STORE_ROOT / case_ref
