#!/bin/bash
set -eu
cat > /app/ledgerq/search.py <<'PYEOF'
"""Ad-hoc invoice search for the finance console."""
from __future__ import annotations
from .db import query_raw
from .filters import get_filter, get_order_spec

SORT_COLUMNS = {"issued_on", "amount_cents", "vendor_name"}
COLUMNS = "id, vendor_name, issued_on, amount_cents, status"
FIELDS = {"vendor_name", "status", "issued_on", "amount_cents"}
OPS = {"=", "!=", ">", ">=", "<", "<="}


def q(value) -> str:
    """Render a value as a SQL string literal, doubling embedded quotes."""
    return "'" + str(value).replace("'", "''") + "'"


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


def _order_from_spec(spec):
    out = []
    for item in str(spec).split(","):
        w = item.split()
        if not w:
            continue
        if w[0] not in SORT_COLUMNS:
            raise ValueError(f"unknown sort column: {w[0]!r}")
        if len(w) == 1:
            out.append(f"{w[0]} ASC")
        elif len(w) == 2 and w[1].lower() in {"asc", "desc"}:
            out.append(f"{w[0]} {w[1].upper()}")
        else:
            raise ValueError(f"bad sort spec: {item!r}")
    if not out:
        raise ValueError("empty sort spec")
    return ", ".join(out)


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
            out.append(f"lower({f}) LIKE {q('%' + v.lower() + '%')}")
        elif o in OPS:
            if f == "amount_cents":
                out.append(f"{f} {o} {int(v)}")
            else:
                out.append(f"{f} {o} {q(v)}")
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
    where = []
    if saved_filter is not None:
        where.append(_filter_sql(get_filter(saved_filter)))
        if sort_by is None:
            spec = get_order_spec(saved_filter)
            if spec:
                order = _order_from_spec(spec)
    if vendor is not None:
        where.append(f"lower(vendor_name) LIKE {q('%' + str(vendor).lower() + '%')}")
    if status is not None:
        where.append(f"status = {q(status)}")
    if min_amount is not None:
        where.append(f"amount_cents >= {int(min_amount)}")
    sql = f"SELECT {COLUMNS} FROM invoices"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += f" ORDER BY {order}, id ASC"
    if limit is not None:
        sql += f" LIMIT {int(limit)}"
    return query_raw(sql)
PYEOF
cd /app && python -m ledgerq search --vendor acme --status open >/dev/null && echo "done"
