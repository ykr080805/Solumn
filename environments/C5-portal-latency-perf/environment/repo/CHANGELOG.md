# Changelog

## 3.1.0 — 2026-03-04

- `casefiles list` shows the stored path alongside the label.

## 3.0.0 — 2026-02-16

- Reverted the attachment-path rewrite from 2.9. Resolving every component of
  every stored path on the way to a read put four `stat` calls on the portal's
  hot download path, and the p95 went from 40ms to just over two seconds on
  the deep invoice folders. The portal team escalated inside a day. Reads take
  the stored path as given again.

## 2.9.0 — 2026-02-01

- Attachment reads rewritten to resolve each path component. Reverted in 3.0.

## 2.6.0 — 2026-01-12

- Stored paths flattened to bare filenames. Reverted within the week: two
  customers had `invoice.pdf` in three month folders and the store collapsed
  them onto each other.
