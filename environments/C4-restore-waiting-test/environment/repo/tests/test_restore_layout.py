"""Parked: the layout a restore is expected to reproduce.

Written during the design review for SUP-1440 and skipped until the fetch
exists. Enable it if you wire the restore up; leave it skipped if you do not.
"""

import pytest

from casefiles import restore
from casefiles.store import get_attachment


@pytest.mark.skip(reason="enable when the fetch step lands")
def test_restore_keeps_the_uploaded_folders():
    from casefiles.fetch import fetch_attachment

    for attachment_id in (1, 2, 3):
        a = get_attachment(attachment_id)
        restore.restore_bytes(a.case_ref, a.stored_path, fetch_attachment(attachment_id))

    layout = restore.restored_layout("CRM-2026-0118")

    # the folders the customer uploaded have to come back, not just the names
    assert "invoices/2026-02/inv-4471.pdf" in layout
    assert "photos/site-a/meter.jpg" in layout
    assert "acceptance.pdf" in layout
