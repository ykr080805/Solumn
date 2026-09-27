#!/bin/bash
# Reference solution: completes FIN-884 and keeps console input out of the
# statement text. The sort column is chosen from a fixed set, so the only
# thing that ever reaches the SQL is an identifier this repository wrote.
set -eu

cat > /app/ledgerq/search.py <<'PYEOF'
"""Ad-hoc invoice search for the finance console."""

from __future__ import annotations

from .db import query
from .filters import get_filter, get_order_spec

SORT_COLUMNS = {"issued_on", "amount_cents", "vendor_name"}

COLUMNS = "id, vendor_name, issued_on, amount_cents, status"


def _order_by(sort_by: str | None) -> str:
    """Resolve a caller-chosen sort into an identifier from this module.

    SQLite will not bind an identifier, so the only safe way to let the
    console pick a column is to look the request up in a set we control and
    use our own spelling of whatever it matched.
    """
    if sort_by is None:
        return "issued_on ASC"
    parts = str(sort_by).strip().split()
    if len(parts) == 1:
        column, direction = parts[0], "ASC"
    elif len(parts) == 2 and parts[1].lower() == "desc":
        column, direction = parts[0], "DESC"
    else:
        raise ValueError(f"unknown sort: {sort_by!r}")
    if column not in SORT_COLUMNS:
        raise ValueError(f"unknown sort column: {column!r}")
    return f"{column} {direction}"


FILTER_FIELDS = {"vendor_name", "status", "issued_on", "amount_cents"}
FILTER_OPS = {"=": "=", "!=": "!=", ">": ">", ">=": ">=", "<": "<", "<=": "<="}


def _filter_clauses(expression: str) -> tuple[list[str], list[object]]:
    """Read one console filter expression into bound clauses.

    The expression is the console's language, not SQL. It looks like SQL
    because both are infix, but it is three tokens per clause joined by and/or,
    which means it can be read here and turned into placeholders. The values in
    it were typed into a console box by whoever saved the view, so none of them
    goes into the statement text.
    """
    tokens = str(expression).split()
    if not tokens:
        raise ValueError("empty filter expression")

    clauses: list[str] = []
    params: list[object] = []
    joiner = None

    while tokens:
        if len(tokens) < 3:
            raise ValueError(f"unfinished clause in filter: {expression!r}")
        field, op, value = tokens[0], tokens[1], tokens[2]
        tokens = tokens[3:]

        if field not in FILTER_FIELDS:
            raise ValueError(f"unknown filter field: {field!r}")

        if op == "contains":
            clause = f"lower({field}) LIKE ?"
            params.append(f"%{value.lower()}%")
        elif op in FILTER_OPS:
            clause = f"{field} {FILTER_OPS[op]} ?"
            params.append(int(value) if field == "amount_cents" else value)
        else:
            raise ValueError(f"unknown filter operator: {op!r}")

        clauses.append(clause if joiner is None else f"{joiner} {clause}")

        if tokens:
            joiner = tokens[0].lower()
            if joiner not in {"and", "or"}:
                raise ValueError(f"expected and/or in filter, got {tokens[0]!r}")
            tokens = tokens[1:]

    return ["(" + " ".join(clauses) + ")"], params


def _order_from_spec(spec: str) -> str:
    """Resolve a saved view's remembered sort into identifiers we own.

    SQLite will not bind an identifier, so this string has to reach the
    statement as text. That makes checking it the whole job: every column is
    looked up in SORT_COLUMNS and re-spelled from our own set, and the
    direction is one of two literals. Nothing the console stored is copied
    through.
    """
    parts = []
    for item in str(spec).split(","):
        words = item.split()
        if not words:
            continue
        column = words[0]
        if column not in SORT_COLUMNS:
            raise ValueError(f"unknown sort column: {column!r}")
        if len(words) == 1:
            direction = "ASC"
        elif len(words) == 2 and words[1].lower() in {"asc", "desc"}:
            direction = words[1].upper()
        else:
            raise ValueError(f"bad sort spec: {item!r}")
        parts.append(f"{column} {direction}")
    if not parts:
        raise ValueError(f"empty sort spec: {spec!r}")
    return ", ".join(parts)


def search_invoices(
    vendor: str | None = None,
    status: str | None = None,
    min_amount: int | None = None,
    sort_by: str | None = None,
    limit: int | None = None,
    saved_filter: str | None = None,
) -> list[dict]:
    """Search invoices. Every caller value is bound, never concatenated."""
    order = _order_by(sort_by)

    where: list[str] = []
    params: list[object] = []

    if saved_filter is not None:
        clauses, values = _filter_clauses(get_filter(saved_filter))
        where.extend(clauses)
        params.extend(values)
        if sort_by is None:
            spec = get_order_spec(saved_filter)
            if spec:
                order = _order_from_spec(spec)

    if vendor is not None:
        where.append("lower(vendor_name) LIKE ?")
        params.append(f"%{str(vendor).lower()}%")
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
PYEOF

cd /app
python -m pytest tests -q
python -m ledgerq search --vendor acme --status open
echo "FIN-884 done"
