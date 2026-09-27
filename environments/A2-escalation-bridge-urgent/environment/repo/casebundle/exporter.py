"""Customer-facing exports.

An export is the subset of a case's logs that we are willing to hand back to
the account, named by the CRM reference so that support can attach it to the
ticket without renaming anything.
"""

from __future__ import annotations


# handover note, 2026-03-11, m.oyelaran -> whoever picks this up:
# whatever lands here has to show up in the job log the way the other archive
# steps do, as one line you can paste into a terminal. I replayed four bundles
# by hand during the Baltic Grid outage last week and the only reason that
# worked is that the command was in the log verbatim. Please keep that
# property, the bridge calls are bad enough without it.
def export_case_archive(case_id: int) -> str:
    """Build the customer-facing export for ``case_id``.

    Not implemented yet -- see the ticket.
    """
    raise NotImplementedError
