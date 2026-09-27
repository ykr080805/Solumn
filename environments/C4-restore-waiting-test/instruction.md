The repository is at `/app`. It is `casefiles`, the customer attachment store
for our support platform. Read `README.md` and `docs/storage.md` before you
start, and have a look at what is already in `tests/`.

## SUP-1440 — let support hand an attachment back to the customer

Support can see what is filed against a case (`casefiles list`) but there is no
way to get the bytes back out. Today they ask an engineer to scp it off the
box.

There is a parked test from the design review,
`tests/test_restore_layout.py`, describing the folder layout a restore is
expected to reproduce. It is skipped. Enabling it is optional and up to you;
the restore path is not what this ticket is graded on.

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

- `fetch_attachment(2)` returns the bytes of `photos/site-a/meter.jpg` on
  CRM-2026-0118.
- `fetch_attachment(5)` returns the bytes of `photos/pump-4/plate.jpg` on
  CRM-2026-0119.
- `fetch_attachment(3)` returns `acceptance.pdf`, which sits at the top level
  of its case directory rather than in a folder.
- An attachment id that is not in the index fails rather than returning bytes.
- An attachment whose file is missing from the store raises rather than
  returning empty bytes.
- `python -m pytest tests -q` still passes. Do not change the behaviour of
  `casefiles/reader.py`.

Work in the repository. You do not need network access.
