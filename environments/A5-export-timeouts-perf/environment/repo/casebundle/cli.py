"""Command line entry point: ``python -m casebundle <command> [args]``."""

from __future__ import annotations

import sys

from .bundler import bundle_case_logs
from .store import list_cases

USAGE = """usage: casebundle <command> [args]

commands:
  list                 show the case index
  bundle <case-id>     build the internal bundle for a case
  export <case-id>     build the customer-facing export for a case
"""


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in {"-h", "--help"}:
        print(USAGE)
        return 0

    command, args = argv[0], argv[1:]

    if command == "list":
        for case in list_cases():
            print(f"{case.id}\t{case.ref}\t{case.account}")
        return 0

    if command == "bundle":
        if len(args) != 1:
            print(USAGE, file=sys.stderr)
            return 2
        print(bundle_case_logs(int(args[0])))
        return 0

    if command == "export":
        if len(args) != 1:
            print(USAGE, file=sys.stderr)
            return 2
        from .exporter import export_case_archive

        print(export_case_archive(int(args[0])))
        return 0

    print(f"unknown command: {command}", file=sys.stderr)
    print(USAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
