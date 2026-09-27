"""Filesystem layout for the bundler."""

from pathlib import Path

APP_ROOT = Path("/app")
LOG_ROOT = APP_ROOT / "data" / "logs"
OUT_DIR = APP_ROOT / "out"


def log_dir(internal_id: int) -> Path:
    """Directory holding the raw log files for a case."""
    return LOG_ROOT / str(internal_id)
