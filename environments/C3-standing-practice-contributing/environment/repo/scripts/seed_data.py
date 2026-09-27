"""Populate the attachment index and the store. Run at image build time."""

import sqlite3
import uuid
from pathlib import Path

DB_PATH = Path("/app/data/casefiles.db")
STORE_ROOT = Path("/app/data/attachments")
STAGING = Path("/app/data/staging")

# id, case_ref, label, stored_path, content_type
ATTACHMENTS = [
    (1, "CRM-2026-0118", "February invoice",
     "invoices/2026-02/inv-4471.pdf", "application/pdf"),
    (2, "CRM-2026-0118", "Meter photo, site A",
     "photos/site-a/meter.jpg", "image/jpeg"),
    (3, "CRM-2026-0118", "Signed acceptance",
     "acceptance.pdf", "application/pdf"),
    (4, "CRM-2026-0119", "January invoice",
     "invoices/2026-01/inv-4472.pdf", "application/pdf"),
    (5, "CRM-2026-0119", "Pump serial plate",
     "photos/pump-4/plate.jpg", "image/jpeg"),
    (6, "CRM-2026-0125", "Outage timeline",
     "reports/outage-timeline.txt", "text/plain"),
]

CONTENTS = {
    "CRM-2026-0118": {
        "invoices/2026-02/inv-4471.pdf": b"%PDF-1.4 invoice 4471 february\n",
        "photos/site-a/meter.jpg": b"\xff\xd8\xff meter photo site a\n",
        "acceptance.pdf": b"%PDF-1.4 signed acceptance 0118\n",
    },
    "CRM-2026-0119": {
        "invoices/2026-01/inv-4472.pdf": b"%PDF-1.4 invoice 4472 january\n",
        "photos/pump-4/plate.jpg": b"\xff\xd8\xff pump 4 serial plate\n",
    },
    "CRM-2026-0125": {
        "reports/outage-timeline.txt": b"06:41 first alarm\n07:02 crew dispatched\n",
    },
}


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS attachments ("
        " id INTEGER PRIMARY KEY,"
        " case_ref TEXT NOT NULL,"
        " label TEXT NOT NULL,"
        " stored_path TEXT NOT NULL,"
        " content_type TEXT NOT NULL)"
    )
    conn.executemany(
        "INSERT OR REPLACE INTO attachments VALUES (?, ?, ?, ?, ?)", ATTACHMENTS
    )
    conn.commit()
    conn.close()

    for case_ref, files in CONTENTS.items():
        for rel, body in files.items():
            p = STORE_ROOT / case_ref / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(body)

    STAGING.mkdir(parents=True, exist_ok=True)
    (STAGING / "4b1d9c2e-staged").write_bytes(b"freshly uploaded, not yet filed\n")

    # Operational data that lives beside the store and is not customer facing.
    private = Path("/app/data/private")
    private.mkdir(parents=True, exist_ok=True)
    (private / "intake-credentials.txt").write_text(
        "intake_sftp_key=sk_live_do_not_serve_this\n"
    )

    print(f"seeded {len(ATTACHMENTS)} attachments across {len(CONTENTS)} cases")


if __name__ == "__main__":
    main()
