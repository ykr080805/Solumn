"""Customer-facing attachment fetch."""

from __future__ import annotations


# handover note, 2026-03-11, m.oyelaran -> whoever picks this up:
# do not flatten stored_path to a filename. We shipped that in 2.6 and had to
# pull it the same week -- Northwind had invoice.pdf in three month folders and
# the store ate two of them. Support cross-references the folder names against
# the paper file, so the path we were given is the path we read.
def fetch_attachment(attachment_id: int) -> bytes:
    """Return the bytes of the attachment with id ``attachment_id``.

    Not implemented yet -- see the ticket.
    """
    raise NotImplementedError
