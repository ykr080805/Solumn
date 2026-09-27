"""Existing coverage for the staging reader."""

import pytest

from casefiles.reader import read_staged, staged_size


def test_read_staged_returns_bytes():
    assert read_staged("4b1d9c2e-staged").startswith(b"freshly uploaded")


def test_staged_size():
    assert staged_size("4b1d9c2e-staged") > 0


def test_missing_upload_raises():
    with pytest.raises(FileNotFoundError):
        read_staged("no-such-upload")
