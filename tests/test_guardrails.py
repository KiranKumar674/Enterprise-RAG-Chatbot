
import sys
from pathlib import Path

# Add the src directory to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from guardrails import detect_sensitive_information, is_out_of_scope


def test_detect_password_disclosure():
    result = detect_sensitive_information("My password is Secret123")
    assert "password disclosure" in result


def test_detect_email_address():
    result = detect_sensitive_information("Contact me at test@example.com")
    assert "email address" in result


def test_valid_policy_question_is_in_scope():
    question = "How many working days does reimbursement processing take?"
    assert is_out_of_scope(question) is False


def test_unrelated_question_is_out_of_scope():
    question = "Tell me a joke about cricket"
    assert is_out_of_scope(question) is True


def test_empty_question_is_out_of_scope():
    # The pipeline separately handles empty input.
    assert is_out_of_scope("") is True
