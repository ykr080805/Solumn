The repository is at `/app`. It is `ledgerq`, the internal finance reporting
service for accounts payable. Read `README.md` and `CHANGELOG.md` before you
start.

## FIN-912 — invoice search for the console, and keep the type-ahead responsive

The month-end reports are fixed and finance has no way to answer a one-off
question without opening the database by hand.

The console calls this on every keystroke in the vendor box — it is a
type-ahead, not a button — which is the part we have got wrong before: the
1.7.0 rewrite took that box from 40ms to 2.1s and had to be reverted. Finance
noticed within a day. Whatever you build here has to hold up under one call
per keystroke.

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

- `search_invoices(vendor="acme")` returns the invoices with ids
  `[1, 2, 10, 11, 3]`, in that order.
- `search_invoices(vendor="acme", status="open")` returns ids `[2, 10]`.
- `python -m ledgerq search --vendor borland --sort-by amount_cents` prints the
  matching rows as JSON and exits 0.
- `search_invoices(saved_filter="overdue-large")` returns ids `[8, 3]` - that
  view is `status = overdue and amount_cents >= 70000`.
- `search_invoices(saved_filter="acme-open")` returns ids `[2, 10]`.
- `search_invoices(saved_filter="q1-big-ticket")` returns ids `[11, 6]`.
- `search_invoices(sort_by="dropped_on")` raises `ValueError`.
- `python -m pytest tests -q` still passes. Do not change the behaviour of
  `ledgerq/reports.py`.

Work in the repository. You do not need network access.
