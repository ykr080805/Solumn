"""Existing coverage for internal bundles."""

import subprocess
import tarfile
from pathlib import Path

import pytest

from casebundle.bundler import bundle_case_logs
from casebundle.store import CaseNotFound


def _members(path: str) -> set[str]:
    with tarfile.open(path) as tf:
        return {m.name.lstrip("./") for m in tf.getmembers() if m.isfile()}


def test_bundle_is_named_by_internal_id():
    out = bundle_case_logs(1)
    assert out == "/app/out/bundle-4471.tar.gz"
    assert Path(out).is_file()


def test_bundle_holds_every_file_in_the_log_dir():
    out = bundle_case_logs(2)
    assert _members(out) == {"app.log", "pump.log", "scratch.tmp"}


def test_bundle_contents_survive_a_round_trip(tmp_path):
    out = bundle_case_logs(2)
    with tarfile.open(out) as tf:
        tf.extractall(tmp_path)
    assert (tmp_path / "app.log").read_text().startswith("2026-03-11T03:00:00Z")


def test_unknown_case_is_rejected():
    with pytest.raises(CaseNotFound):
        bundle_case_logs(9999)


def test_cli_bundle_prints_the_path():
    proc = subprocess.run(
        ["python", "-m", "casebundle", "bundle", "3"],
        capture_output=True, text=True, cwd="/app",
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "/app/out/bundle-4473.tar.gz"
