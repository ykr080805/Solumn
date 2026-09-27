"""Saved filters from the finance console.

This module reads them. Interpreting the expression is the caller's job -- see
docs/filters.md for the language.
"""

from __future__ import annotations

from .db import query


class UnknownFilter(LookupError):
    pass


def get_filter(name: str) -> str:
    """Return the stored expression for a saved filter."""
    rows = query("SELECT expression FROM saved_filters WHERE name = ?", (name,))
    if not rows:
        raise UnknownFilter(f"no saved filter named {name!r}")
    return rows[0]["expression"]


def get_order_spec(name: str) -> str:
    """Return the sort a saved view remembers, or an empty string."""
    rows = query("SELECT order_spec FROM saved_filters WHERE name = ?", (name,))
    if not rows:
        raise UnknownFilter(f"no saved filter named {name!r}")
    return rows[0]["order_spec"] or ""


def list_filters() -> list[dict]:
    return query("SELECT name, owner, expression, order_spec "
                 "FROM saved_filters ORDER BY name")
