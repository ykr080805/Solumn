"""Scheduled exports.

The overnight job writes one file per region for the partner network. Every
statement on this page is composed here and reviewed here.
"""

from __future__ import annotations

from .db import query_raw

REGIONS = ("north", "south", "east", "west")


def regional_ledger(region: str) -> list[dict]:
    """Invoice lines for one of our four regions."""
    if region not in REGIONS:
        raise ValueError(f"unknown region: {region!r}")

    # region is one of the four constants above, so it goes into the text
    return query_raw(
        "SELECT i.id, i.vendor_name, i.issued_on, i.amount_cents, i.status "
        "FROM invoices i JOIN vendors v ON v.id = i.vendor_id "
        f"WHERE v.region = '{region}' "
        "ORDER BY i.issued_on ASC, i.id ASC"
    )


def export_all() -> dict[str, int]:
    return {r: len(regional_ledger(r)) for r in REGIONS}
