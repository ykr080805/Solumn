"""Existing coverage for the fixed month-end reports."""

from ledgerq.reports import monthly_totals, open_liabilities, vendor_count


def test_monthly_totals_is_scoped_to_the_period():
    rows = monthly_totals("2026-01")
    names = {r["vendor_name"] for r in rows}
    assert names == {"Acme Fabrication Ltd", "Borland Freight", "Delta Instruments"}


def test_monthly_totals_sums_and_orders():
    rows = monthly_totals("2026-02")
    assert rows[0]["vendor_name"] == "Caldera Energy"
    assert rows[0]["total_cents"] == 1362050


def test_open_liabilities_covers_open_and_overdue():
    rows = open_liabilities()
    owed = {r["vendor_name"]: r["owed_cents"] for r in rows}
    assert owed["Acme Fabrication Ltd"] == 266450
    assert "Acme Logistics GmbH" in owed


def test_vendor_count():
    assert vendor_count() >= 5
