
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from access_control import get_allowed_documents


def test_general_role_can_access_company_policy():
    allowed = get_allowed_documents("general")

    assert "company_policy.txt" in allowed
    assert "hr_policy.txt" not in allowed
    assert "finance_policy.txt" not in allowed


def test_hr_role_can_access_hr_documents():
    allowed = get_allowed_documents("hr")

    assert "company_policy.txt" in allowed
    assert "hr_policy.txt" in allowed
    assert "finance_policy.txt" not in allowed


def test_finance_role_can_access_finance_documents():
    allowed = get_allowed_documents("finance")

    assert "company_policy.txt" in allowed
    assert "finance_policy.txt" in allowed
    assert "hr_policy.txt" not in allowed


def test_unknown_role_has_no_permissions():
    assert get_allowed_documents("unknown") == []


def test_role_is_case_insensitive():
    assert get_allowed_documents("HR") == get_allowed_documents("hr")
    assert get_allowed_documents("FINANCE") == get_allowed_documents("finance")
