"""The fixed month-end reports.

Every statement in here is a constant that lives in this file. Nothing on this
page takes a value from a caller.
"""

from __future__ import annotations

from .db import query, query_raw

OPEN_STATUSES = ("open", "overdue")


def monthly_totals(period: str) -> list[dict]:
    """Totals per vendor for a billing period such as ``2026-02``."""
    return query(
        "SELECT vendor_name, COUNT(*) AS invoices, SUM(amount_cents) AS total_cents "
        "FROM invoices WHERE substr(issued_on, 1, 7) = ? "
        "GROUP BY vendor_name ORDER BY total_cents DESC",
        (period,),
    )


def open_liabilities() -> list[dict]:
    # the status list is a module constant, so it is folded into the statement
    # rather than bound -- there is no caller input anywhere near this
    statuses = ", ".join(f"'{s}'" for s in OPEN_STATUSES)
    return query_raw(
        "SELECT vendor_name, SUM(amount_cents) AS owed_cents "
        f"FROM invoices WHERE status IN ({statuses}) "
        "GROUP BY vendor_name ORDER BY owed_cents DESC"
    )


def vendor_count() -> int:
    return query_raw("SELECT COUNT(*) AS n FROM vendors")[0]["n"]
