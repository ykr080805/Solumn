"""Command line entry point: ``python -m ledgerq <command> [args]``."""

from __future__ import annotations

import json
import sys

from .reports import monthly_totals, open_liabilities

USAGE = """usage: ledgerq <command> [args]

commands:
  totals <period>              month-end totals per vendor, e.g. 2026-02
  open                         open and overdue liabilities per vendor
  search [--vendor V] [--status S] [--min-amount N] [--sort-by F] [--limit N]
"""


def _parse(args: list[str]) -> dict:
    out: dict = {}
    keys = {
        "--vendor": "vendor",
        "--status": "status",
        "--min-amount": "min_amount",
        "--sort-by": "sort_by",
        "--limit": "limit",
    }
    i = 0
    while i < len(args):
        key = keys.get(args[i])
        if key is None or i + 1 >= len(args):
            raise SystemExit(f"bad argument: {args[i]}")
        value = args[i + 1]
        if key in {"min_amount", "limit"}:
            value = int(value)
        out[key] = value
        i += 2
    return out


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in {"-h", "--help"}:
        print(USAGE)
        return 0

    command, args = argv[0], argv[1:]

    if command == "totals":
        if len(args) != 1:
            print(USAGE, file=sys.stderr)
            return 2
        print(json.dumps(monthly_totals(args[0]), indent=2))
        return 0

    if command == "open":
        print(json.dumps(open_liabilities(), indent=2))
        return 0

    if command == "search":
        from .search import search_invoices

        print(json.dumps(search_invoices(**_parse(args)), indent=2))
        return 0

    print(f"unknown command: {command}", file=sys.stderr)
    print(USAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
