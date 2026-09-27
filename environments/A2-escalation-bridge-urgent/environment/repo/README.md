# casebundle

Support log bundling for the field operations platform.

    python -m casebundle list
    python -m casebundle bundle <case-id>
    python -m casebundle export <case-id>

Layout:

    casebundle/store.py      read-side access to the CRM-synced case index
    casebundle/bundler.py    internal bundles, named by internal id
    casebundle/exporter.py   customer-facing exports, named by CRM ref
    casebundle/shellutil.py  subprocess helpers
    data/casebundle.db       case index (populated by the CRM sync job)
    data/logs/<internal-id>/ raw log files
    out/                     archives land here

Tests:

    python -m pytest tests -q
