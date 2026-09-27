# casefiles

Customer attachment store for the support platform.

    python -m casefiles list <case-ref>
    python -m casefiles fetch <attachment-id>
    python -m casefiles size <attachment-id>

Layout:

    casefiles/store.py    read-side access to the attachment index
    casefiles/reader.py   the staging area, before files are filed
    casefiles/fetch.py    customer-facing fetch
    casefiles/paths.py    where things live
    data/attachments/     the store, one directory per case
    data/staging/         freshly uploaded files, named by upload id
    docs/storage.md       how stored_path is laid out

Tests:

    python -m pytest tests -q
