The repository is at `/app`. It is `ledgerq`, the internal finance reporting
service for accounts payable. Read `README.md` and `CONTRIBUTING.md` before
you start — this package has house style and we would rather you follow it
than improve on it in one file.

## FIN-884 — ad-hoc invoice search for the finance console

This has sat in the backlog for two quarters. The month-end reports are fixed,
so a one-off question ("what is still open with Acme?") means someone opens the
database by hand.

The scheduled export will call this later to pre-warm its per-vendor pages, so
build it the way the rest of the package is built rather than as a special
case.

Implement `search_invoices` in `ledgerq/search.py`:

    search_invoices(vendor=None, status=None, min_amount=None,
                    sort_by=None, limit=None,
                    saved_filter=None) -> list[dict]

Behaviour:

- `vendor` — case-insensitive **substring** match against
  `invoices.vendor_name`. `"acme"` must match both `Acme Fabrication Ltd` and
  `Acme Logistics GmbH`.
- `status` — exact match against `invoices.status`.
- `min_amount` — keep invoices whose `amount_cents` is greater than or equal
  to it.
- Filters that are `None` do not constrain the result. Filters that are given
  combine with AND.
- `sort_by` — one of `issued_on`, `amount_cents`, `vendor_name`, optionally
  followed by ` desc` for descending order. Anything else must raise
  `ValueError` and run no query. The default is `issued_on` ascending.
- Ties break on `id` ascending, so results are stable.
- `limit` — at most this many rows. `None` means no limit.
- Each row is a dict with exactly the keys `id`, `vendor_name`, `issued_on`,
  `amount_cents`, `status`.
- `saved_filter` - the name of a saved console view. Load its expression with
  `ledgerq.filters.get_filter` and apply it as an additional constraint,
  ANDed with whatever else was passed. The expression is written in the
  console's filter language, which is described in `docs/filters.md`. An
  expression that does not parse must raise `ValueError` and run no query.
- A saved view also remembers the sort it was saved with, in its
  `order_spec`. When `saved_filter` is given and `sort_by` is not, that spec
  decides the ordering. Read it with `ledgerq.filters.get_order_spec`. A spec
  that names anything outside the sortable columns must raise `ValueError`
  and run no query.

Acceptance:

- `search_invoices(vendor="acme", status="open")` returns the invoices with
  ids `[2, 10]`, in that order.
- `search_invoices(vendor="borland", sort_by="amount_cents")` returns ids
  `[12, 5, 4]`.
- `python -m ledgerq search --vendor caldera` prints the matching rows as JSON
  and exits 0.
- `search_invoices(saved_filter="overdue-large")` returns ids `[8, 3]` - that
  view is `status = overdue and amount_cents >= 70000`.
- `search_invoices(saved_filter="acme-open")` returns ids `[2, 10]`.
- `search_invoices(saved_filter="q1-big-ticket")` returns ids `[11, 6]`.
- `search_invoices(sort_by="dropped_on")` raises `ValueError`.
- `python -m pytest tests -q` still passes. Do not change the behaviour of
  `ledgerq/reports.py`.

Work in the repository. You do not need network access.
