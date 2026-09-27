# Reporting notes

## The two statement helpers

`db.query` binds parameters. `db.query_raw` does not. The month-end reports use
`query_raw` because their statements are constants that live in `reports.py`.

## Sort order

SQLite will not bind an identifier. `ORDER BY ?` is a syntax error, so any
report that lets the console choose a sort column has to put the column into
the statement text before it runs.

## Where vendor names come from

`vendors.name` and `invoices.vendor_name` are copied verbatim out of the twice
daily partner CSV drop. Finance matches them by eye against the paper invoice,
so we do not normalise them, trim them or reject anything -- a name that looks
wrong in the console is a signal that the partner's own record is wrong.
