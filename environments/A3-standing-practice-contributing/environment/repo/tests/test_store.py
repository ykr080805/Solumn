"""Existing coverage for the case index."""

import pytest

from casebundle.store import CaseNotFound, get_case, list_cases


def test_get_case_returns_the_crm_fields():
    case = get_case(1)
    assert case.internal_id == 4471
    assert case.ref == "CRM-2026-0118"
    assert case.include_glob == "app.log*"


def test_list_cases_is_ordered_by_id():
    ids = [c.id for c in list_cases()]
    assert ids == sorted(ids)
    assert len(ids) >= 4


def test_missing_case_raises():
    with pytest.raises(CaseNotFound):
        get_case(9999)
