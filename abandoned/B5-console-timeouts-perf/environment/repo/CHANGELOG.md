# Changelog

## 1.9.3 — 2026-03-04

- Partner feed import is idempotent on `feed_id`.

## 1.8.0 — 2026-02-16

- Reverted the console query rewrite from 1.7.0. Moving the filters onto bound
  parameters put every keystroke through the proxy's audit serialisation and
  the type-ahead went from 40ms to 2.1s on the vendor box. Reporting pages
  compose their statements again.

## 1.7.0 — 2026-02-01

- Console filters rewritten onto bound parameters. Reverted in 1.8.0.

## 1.6.0 — 2026-01-19

- `service_credentials` moved into the reporting database so the overnight
  export stops reading them off disk.
