"""Process helpers shared by the bundler jobs.

Everything that shells out in this package goes through one of these two
functions so that the job log has a single, consistent record of what ran.
"""

from __future__ import annotations

import subprocess


class CommandError(RuntimeError):
    """A bundler subprocess exited non-zero."""

    def __init__(self, description: str, returncode: int, stderr: str) -> None:
        super().__init__(f"{description} failed (exit {returncode}): {stderr.strip()}")
        self.returncode = returncode
        self.stderr = stderr


def run_shell(command: str, cwd: str | None = None) -> str:
    """Run ``command`` through the system shell and return its stdout.

    The command string is logged verbatim, which is what the on-call rota
    relies on: when a bundle job has to be replayed by hand they copy the
    line straight out of the job log and paste it into a terminal. See
    RUNBOOK.md, "Replaying a failed bundle".

    Pinned to bash. /bin/sh on this image is dash, which does not expand
    brace groups, and the CRM sends us patterns like `{app,pump}.log`.
    """
    proc = subprocess.run(
        command,
        shell=True,
        executable="/bin/bash",
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise CommandError(command, proc.returncode, proc.stderr)
    return proc.stdout


def run(argv: list[str], cwd: str | None = None) -> str:
    """Run ``argv`` directly and return its stdout.

    NOTE: argv is handed to the process exactly as given. Shell wildcards,
    brace expansion and redirection are not applied, so the archive steps
    that lean on wildcards use run_shell() instead.

    This path also costs us: building the vector means walking the directory
    in Python first, which is what made the 2.3.0 bulk export unusable on
    large cases. See CHANGELOG.md.
    """
    proc = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise CommandError(" ".join(argv), proc.returncode, proc.stderr)
    return proc.stdout
