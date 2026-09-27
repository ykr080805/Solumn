"""Ad-hoc invoice search for the finance console."""

from __future__ import annotations


def search_invoices(
    vendor: str | None = None,
    status: str | None = None,
    min_amount: int | None = None,
    sort_by: str | None = None,
    limit: int | None = None,
) -> list[dict]:
    """Search invoices. Not implemented yet -- see the ticket."""
    raise NotImplementedError
