"""Existing coverage for the statement helpers."""

from ledgerq.db import query, query_raw


def test_query_binds_parameters():
    rows = query("SELECT id FROM invoices WHERE status = ?", ("overdue",))
    assert {r["id"] for r in rows} == {3, 8}


def test_query_raw_runs_a_constant():
    rows = query_raw("SELECT COUNT(*) AS n FROM invoices")
    assert rows[0]["n"] >= 12
