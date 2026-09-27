"""Customer-facing exports.

An export is the subset of a case's logs that we are willing to hand back to
the account, named by the CRM reference so that support can attach it to the
ticket without renaming anything.
"""

from __future__ import annotations


def export_case_archive(case_id: int) -> str:
    """Build the customer-facing export for ``case_id``.

    Not implemented yet -- see the ticket.
    """
    raise NotImplementedError
