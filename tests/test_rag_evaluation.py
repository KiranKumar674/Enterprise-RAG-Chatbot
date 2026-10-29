
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from retriever import retrieve_documents


def test_hr_question_retrieves_performance_review_policy():
    documents = retrieve_documents(
        "How often are performance reviews conducted?",
        role="hr",
        n_results=5,
    )

    assert documents, "Expected relevant HR documents, but none were retrieved."

    combined_text = "\n".join(documents).lower()

    assert "performance reviews" in combined_text
    assert "twice per year" in combined_text


def test_finance_question_retrieves_reimbursement_policy():
    documents = retrieve_documents(
        "How many working days does reimbursement processing take?",
        role="finance",
        n_results=5,
    )

    assert documents, "Expected relevant finance documents, but none were retrieved."

    combined_text = "\n".join(documents).lower()

    assert "reimbursement" in combined_text
    assert "five working days" in combined_text


def test_general_role_does_not_retrieve_hr_only_policy():
    documents = retrieve_documents(
        "How often are performance reviews conducted?",
        role="general",
        n_results=10,
    )

    combined_text = "\n".join(documents).lower()

    assert "performance reviews" not in combined_text
    assert "twice per year" not in combined_text



def test_retrieved_context_supports_expected_hr_answer():
    documents = retrieve_documents(
        "How often are performance reviews conducted?",
        role="hr",
        n_results=5,
    )

    context = "\n".join(documents).lower()

    expected_facts = [
        "performance reviews",
        "twice per year",
    ]

    for fact in expected_facts:
        assert fact in context, (
            f"Retrieved context does not contain the expected fact: {fact}"
        )



def test_generated_hr_answer_contains_expected_fact():
    from rag_pipeline import answer_question

    answer = answer_question(
        "How often are performance reviews conducted?",
        role="hr",
    )

    assert answer, "The chatbot returned an empty answer."

    normalized_answer = answer.lower()
    assert "twice per year" in normalized_answer, (
        f"Expected the answer to mention 'twice per year', got: {answer}"
    )



def test_generated_answer_does_not_invent_missing_policy():
    from rag_pipeline import answer_question

    answer = answer_question(
        "What is the company's maternity leave duration?",
        role="hr",
    )

    assert answer, "The chatbot returned an empty answer."

    normalized_answer = answer.lower()

    assert (
        "do not provide enough information" in normalized_answer
        or "couldn't find relevant information" in normalized_answer
        or "not provide enough information" in normalized_answer
    ), f"Expected an uncertainty response, got: {answer}"
