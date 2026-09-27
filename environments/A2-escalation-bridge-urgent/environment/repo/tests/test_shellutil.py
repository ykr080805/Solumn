"""Existing coverage for the subprocess helpers."""

import pytest

from casebundle.shellutil import CommandError, run, run_shell


def test_run_shell_returns_stdout():
    assert run_shell("echo hello").strip() == "hello"


def test_run_returns_stdout():
    assert run(["echo", "hello"]).strip() == "hello"


def test_run_shell_raises_on_failure():
    with pytest.raises(CommandError):
        run_shell("exit 3")


def test_run_raises_on_failure():
    with pytest.raises(CommandError):
        run(["false"])
