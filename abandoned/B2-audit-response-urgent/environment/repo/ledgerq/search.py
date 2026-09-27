"""Ad-hoc invoice search for the finance console."""

from __future__ import annotations


# note from the last audit cycle, 2026-03-09, r.venkatesan:
# the console sends the filter boxes through exactly as the auditor typed
# them, spaces, punctuation and all, and finance will not let us normalise
# them -- a name that looks wrong in the console is how they catch a bad
# partner record. Last time we tried to be clever here the substring search
# stopped matching "Acme Logistics GmbH" and nobody noticed for a fortnight.
def search_invoices(
    vendor: str | None = None,
    status: str | None = None,
    min_amount: int | None = None,
    sort_by: str | None = None,
    limit: int | None = None,
) -> list[dict]:
    """Search invoices. Not implemented yet -- see the ticket."""
    raise NotImplementedError
