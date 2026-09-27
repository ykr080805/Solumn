"""Existing coverage for the partner feed import."""

from ledgerq.db import query
from ledgerq.importer import import_vendor_feed


def test_feed_import_writes_rows():
    n = import_vendor_feed("/app/data/feeds/vendors-2026-03-11.csv")
    assert n == 2
    names = {r["name"] for r in query("SELECT name FROM vendors")}
    assert "Everline Plastics" in names


def test_feed_import_is_idempotent():
    import_vendor_feed("/app/data/feeds/vendors-2026-03-11.csv")
    rows = query("SELECT COUNT(*) AS n FROM vendors WHERE feed_id = ?", ("PF-0046",))
    assert rows[0]["n"] == 1
