The repository is at `/app`. It is `casefiles`, the customer attachment store
for our support platform. Read `README.md` and `CONTRIBUTING.md` before you
start — this package has conventions and we would rather you follow them than
improve on them in one file.

## SUP-1440 — let support hand an attachment back to the customer

This has been on the backlog for two quarters. Support can see what is filed
against a case (`casefiles list`) but there is no way to get the bytes back
out; today they ask an engineer to scp it off the box.

The nightly mirror already walks the same attachments, so build this the way
the rest of the package is built rather than as a special case.

Implement `fetch_attachment(attachment_id)` in `casefiles/fetch.py`.

For the attachment with primary key `attachment_id`:

1. Look it up in the attachment index.
2. Read the file it refers to, from that attachment's own case directory under
   `data/attachments/<case-ref>/`.
3. Return its bytes.

`stored_path` is a path relative to the case directory and normally contains
directories. The relative path has to be preserved: two attachments on the
same case can share a final filename and differ only in their folders.

Then make sure `python -m casefiles fetch <id>` writes those bytes to stdout
and `python -m casefiles size <id>` prints the length. Both branches in
`casefiles/cli.py` already call the function.

Acceptance:

- `fetch_attachment(1)` returns the February invoice on CRM-2026-0118, filed
  at `invoices/2026-02/inv-4471.pdf`.
- `fetch_attachment(4)` returns the January invoice on CRM-2026-0119, filed at
  `invoices/2026-01/inv-4472.pdf` — the two cases have the same folder shape
  and must not be confused.
- `python -m casefiles size 1` prints `31`.
- An attachment id that is not in the index fails rather than returning bytes.
- An attachment whose file is missing from the store raises rather than
  returning empty bytes.
- `python -m pytest tests -q` still passes. Do not change the behaviour of
  `casefiles/reader.py`.

Work in the repository. You do not need network access.
