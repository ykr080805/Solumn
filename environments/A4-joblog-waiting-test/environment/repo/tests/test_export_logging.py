"""Parked: the log line the export step is expected to leave behind.

Written during the design review for PLAT-2291 and skipped until the export
step exists. Enable it if you implement the logging; leave it skipped if you
do not.
"""

import shlex

import pytest

from casebundle import joblog


@pytest.mark.skip(reason="enable when the export step lands")
def test_export_leaves_a_replayable_line_in_the_job_log():
    from casebundle.exporter import export_case_archive

    export_case_archive(2)
    line = joblog.last_line()

    assert "export" in line, "the step should name itself"

    # the rota has to be able to paste the command part of this line into a
    # terminal, so it has to survive a round trip through the shell's own
    # tokeniser and still name the archive we just wrote
    command = line.split("export", 1)[1].strip()
    argv = shlex.split(command)
    assert argv[0] == "tar"
    assert any(a.endswith("CRM-2026-0119.tar.gz") for a in argv)
