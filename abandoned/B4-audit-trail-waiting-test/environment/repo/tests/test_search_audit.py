"""Parked: the audit entry the search step is expected to leave behind.

Written during the design review for FIN-884 and skipped until the search
exists. Enable it if you implement the audit entry; leave it skipped if you
do not.
"""

import pytest

from ledgerq import auditlog


@pytest.mark.skip(reason="enable when the search step lands")
def test_search_records_what_it_asked():
    from ledgerq.search import search_invoices

    search_invoices(vendor="acme", status="open")
    entry = auditlog.last_entry()

    assert entry is not None, "the search should leave an audit entry"
    assert entry["source"] == "search_invoices"

    # an auditor has to be able to see which table was consulted and which
    # order the answer came back in, without reading our source
    assert "invoices" in entry["statement"].lower()
    assert "order by" in entry["statement"].lower()
