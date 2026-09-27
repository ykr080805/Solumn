# ledgerq

Internal finance reporting for accounts payable.

    python -m ledgerq totals 2026-02
    python -m ledgerq open
    python -m ledgerq search --vendor acme --status open --sort-by amount_cents

Layout:

    ledgerq/db.py        connection handling and the statement helpers
    ledgerq/reports.py   the fixed month-end reports
    ledgerq/importer.py  partner vendor CSV feed
    ledgerq/search.py    ad-hoc invoice search for the finance console
    data/ledgerq.db      the reporting database
    docs/reporting.md    notes on the statement helpers
    docs/filters.md      the console's saved-filter language

Tests:

    python -m pytest tests -q
