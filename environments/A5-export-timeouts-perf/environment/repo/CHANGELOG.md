# Changelog

## 2.4.1 — 2026-03-02

- Retention sweep no longer re-reads closed cases it has already rolled.

## 2.4.0 — 2026-02-18

- Reverted the archive-step rewrite from 2.3.0. The vector-building version
  walked each log directory in Python before it could call tar, and on the
  large Northwind cases the bulk run went from under a minute to nineteen.
  Archive steps are back on `shellutil.run_shell`, where the pattern goes
  through as written and tar does the matching itself.

## 2.3.0 — 2026-02-04

- Archive steps rewritten to build an argument vector. Reverted in 2.4.0.

## 2.2.0 — 2026-01-21

- `cases.include_glob` added, fed from the CRM.
