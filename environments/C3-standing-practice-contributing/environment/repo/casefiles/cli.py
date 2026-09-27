"""Command line entry point: ``python -m casefiles <command> [args]``."""

from __future__ import annotations

import sys

from .store import list_attachments

USAGE = """usage: casefiles <command> [args]

commands:
  list <case-ref>      show the attachments filed against a case
  fetch <id>           write one attachment's bytes to stdout
  size <id>            print one attachment's size in bytes
"""


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in {"-h", "--help"}:
        print(USAGE)
        return 0

    command, args = argv[0], argv[1:]

    if command == "list":
        if len(args) != 1:
            print(USAGE, file=sys.stderr)
            return 2
        for a in list_attachments(args[0]):
            print(f"{a.id}\t{a.label}\t{a.stored_path}")
        return 0

    if command in {"fetch", "size"}:
        if len(args) != 1:
            print(USAGE, file=sys.stderr)
            return 2
        from .fetch import fetch_attachment

        data = fetch_attachment(int(args[0]))
        if command == "size":
            print(len(data))
        else:
            sys.stdout.buffer.write(data)
        return 0

    print(f"unknown command: {command}", file=sys.stderr)
    print(USAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
