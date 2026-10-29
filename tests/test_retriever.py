
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from retriever import retrieve_documents


def test_general_role_does_not_retrieve_hr_information():
    results = retrieve_documents(
        "How often are performance reviews conducted?",
        "general",
        n_results=10,
    )

    assert all("Performance Reviews" not in doc for doc in results)
    assert all("hr_policy.txt" not in doc for doc in results)


def test_general_role_does_not_retrieve_finance_only_information():
    results = retrieve_documents(
        "How does the finance team process reimbursement requests?",
        "general",
        n_results=10,
    )

    assert all("Reimbursement Processing" not in doc for doc in results)
    assert all("finance_policy.txt" not in doc for doc in results)


def test_hr_role_can_retrieve_hr_information():
    results = retrieve_documents(
        "How often are performance reviews conducted?",
        "hr",
        n_results=10,
    )

    assert any("Performance Reviews" in doc for doc in results)


def test_finance_role_can_retrieve_finance_information():
    results = retrieve_documents(
        "How does the finance team process reimbursement requests?",
        "finance",
        n_results=10,
    )

    assert any("Reimbursement Processing" in doc for doc in results)


def test_unknown_role_retrieves_nothing():
    results = retrieve_documents(
        "What is the leave policy?",
        "unknown",
        n_results=10,
    )

    assert results == []
