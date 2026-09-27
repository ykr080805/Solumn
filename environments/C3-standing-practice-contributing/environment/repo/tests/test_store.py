"""Existing coverage for the attachment index."""

import pytest

from casefiles.store import AttachmentNotFound, get_attachment, list_attachments


def test_get_attachment_returns_the_intake_fields():
    a = get_attachment(1)
    assert a.case_ref == "CRM-2026-0118"
    assert a.stored_path == "invoices/2026-02/inv-4471.pdf"
    assert a.content_type == "application/pdf"


def test_stored_paths_keep_their_directories():
    paths = {a.stored_path for a in list_attachments("CRM-2026-0118")}
    assert "photos/site-a/meter.jpg" in paths
    assert "acceptance.pdf" in paths


def test_list_is_scoped_to_one_case():
    assert {a.id for a in list_attachments("CRM-2026-0119")} == {4, 5}


def test_missing_attachment_raises():
    with pytest.raises(AttachmentNotFound):
        get_attachment(9999)
