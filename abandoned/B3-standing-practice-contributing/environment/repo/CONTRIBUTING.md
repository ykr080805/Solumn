# Contributing to ledgerq

Two of us maintain this and the whole finance team reads the output. House
style beats local preference.

## Statements

Reporting statements are composed as text in the module that owns them, so
that the statement you read in the file is the statement that runs. This is
what makes a review of a reporting change possible at all: the reviewer reads
the SQL, not a pile of fragments and a binding call. `ledgerq/reports.py` and
`ledgerq/exports.py` both work this way.

`db.query` exists for the handful of places that take a value straight off a
scheduler argument. `db.query_raw` is what the reporting pages use.

## Sort order

SQLite will not bind an identifier, so anything that lets a caller pick a sort
column has to put the column into the statement text before it runs. Restrict
what you accept.

## Tests

`python -m pytest tests -q` before you open a change, and do not disturb the
fixed month-end numbers -- the scheduled export reconciles against them.
