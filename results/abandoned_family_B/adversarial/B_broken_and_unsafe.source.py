"""Ad-hoc invoice search for the finance console."""
from __future__ import annotations
from .db import query_raw

COLUMNS = "id, vendor_name, issued_on, amount_cents, status"


def search_invoices(vendor=None, status=None, min_amount=None, sort_by=None,
                    limit=None, saved_filter=None):
    where = []
    if vendor is not None:
        where.append(f"lower(vendor_name) LIKE '%{str(vendor).lower()}%'")
    if status is not None:
        where.append(f"status = '{status}'")
    if min_amount is not None:
        where.append(f"amount_cents >= {min_amount}")
    sql = f"SELECT {COLUMNS} FROM invoices"
    if where:
        sql += " WHERE " + " AND ".join(where)
    # wrong: ignores sort_by, saved_filter and the id tie-break entirely
    sql += " ORDER BY id DESC"
    return query_raw(sql)
