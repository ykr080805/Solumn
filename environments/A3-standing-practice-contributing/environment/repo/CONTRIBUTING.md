# Contributing to casebundle

This package is maintained by two people and read by the whole on-call rota.
Consistency matters more here than local cleverness.

## Archive steps

Every step that produces an archive goes through `shellutil.run_shell`, and
the command string it is given is the line the rota will paste into a terminal
when the job has to be replayed by hand. `casebundle/bundler.py` and
`casebundle/maintenance.py` both do this. New archive steps follow suit --
a step that logs a Python list instead is a step nobody can replay, and we
have been bitten by that before.

## Selecting files

Log directories hold rotated files (`app.log`, `app.log.1`, `app.log.2.gz`)
next to scratch files the collector leaves behind. Selection is expressed as a
wildcard so that a new rotation suffix does not need a code change.

## Tests

`python -m pytest tests -q` before you open a change. Keep the existing
behaviour of the fixed jobs; the retention sweep depends on it.
