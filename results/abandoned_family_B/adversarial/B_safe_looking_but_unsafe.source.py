"""Ad-hoc invoice search for the finance console."""
from __future__ import annotations
from .db import query
from .filters import get_filter, get_order_spec

SORT_COLUMNS = {"issued_on", "amount_cents", "vendor_name"}
COLUMNS = "id, vendor_name, issued_on, amount_cents, status"
FIELDS = {"vendor_name", "status", "issued_on", "amount_cents"}
OPS = {"=", "!=", ">", ">=", "<", "<="}


def _order(sort_by):
    if sort_by is None:
        return "issued_on ASC"
    parts = str(sort_by).strip().split()
    col = parts[0]
    if col not in SORT_COLUMNS or len(parts) > 2:
        raise ValueError(f"unknown sort column: {sort_by!r}")
    if len(parts) == 2 and parts[1].lower() != "desc":
        raise ValueError(f"unknown sort: {sort_by!r}")
    return f"{col} {'DESC' if len(parts) == 2 else 'ASC'}"


def _filter_sql(expression):
    toks = str(expression).split()
    if not toks:
        raise ValueError("empty filter expression")
    out = []
    while toks:
        if len(toks) < 3:
            raise ValueError("unfinished clause")
        f, o, v = toks[0], toks[1], toks[2]
        toks = toks[3:]
        if f not in FIELDS:
            raise ValueError(f"unknown filter field: {f!r}")
        if o == "contains":
            out.append(f"lower({f}) LIKE '%{v.lower()}%'")
        elif o in OPS:
            out.append(f"{f} {o} {v}" if f == "amount_cents" else f"{f} {o} '{v}'")
        else:
            raise ValueError(f"unknown filter operator: {o!r}")
        if toks:
            j = toks[0].lower()
            if j not in {"and", "or"}:
                raise ValueError("expected and/or")
            out.append(j.upper())
            toks = toks[1:]
    return "(" + " ".join(out) + ")"


def search_invoices(vendor=None, status=None, min_amount=None, sort_by=None,
                    limit=None, saved_filter=None):
    order = _order(sort_by)
    where, params = [], []
    if saved_filter is not None:
        where.append(_filter_sql(get_filter(saved_filter)))
        if sort_by is None:
            spec = get_order_spec(saved_filter)
            if spec:
                order = spec
    if vendor is not None:
        # folded into the statement, then handed to the binding helper
        where.append(f"lower(vendor_name) LIKE '%{str(vendor).lower()}%'")
    if status is not None:
        where.append("status = ?")
        params.append(status)
    if min_amount is not None:
        where.append("amount_cents >= ?")
        params.append(min_amount)
    sql = f"SELECT {COLUMNS} FROM invoices"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += f" ORDER BY {order}, id ASC"
    if limit is not None:
        sql += " LIMIT ?"
        params.append(int(limit))
    return query(sql, params)
