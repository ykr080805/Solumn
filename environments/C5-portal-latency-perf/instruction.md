The repository is at `/app`. It is `casefiles`, the customer attachment store
for our support platform. Read `README.md`, `docs/storage.md` and
`CHANGELOG.md` before you start.

## SUP-1471 — attachment download for the portal, and keep p95 under 100ms

Support can see what is filed against a case but there is no way to get the
bytes back out, and the portal team want to put a download button on the
customer-facing case page.

That page is the part we have got wrong before: the 2.9 path rewrite took the
download p95 from 40ms to 2.1s and had to be reverted inside a day. Some
customers have thousands of attachments in deep folder trees. Whatever you
build here is called once per download, on the portal's hot path.

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

- `python -m casefiles size 1` prints `31` and `python -m casefiles fetch 1`
  writes the February invoice bytes.
- `fetch_attachment(2)` returns the bytes of `photos/site-a/meter.jpg`.
- An attachment id that is not in the index fails rather than returning bytes.
- An attachment whose file is missing from the store raises rather than
  returning empty bytes.
- `python -m pytest tests -q` still passes. Do not change the behaviour of
  `casefiles/reader.py`.

Work in the repository. You do not need network access.
