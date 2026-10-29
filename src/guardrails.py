
import re


def detect_sensitive_information(text: str) -> list[str]:
    """Detect common sensitive information patterns."""
    patterns = {
        "email address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "phone number": r"(?<!\w)(?:\+?\d{1,3}[-.\s]?)?(?:\d[-.\s]?){10}(?!\w)",
        "possible API key": r"\b(?:gsk_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,})\b",
        "password disclosure": r"\b(?:my password is|password\s*[:=])\s*\S+",
    }

    detected = [
        label
        for label, pattern in patterns.items()
        if re.search(pattern, text, flags=re.IGNORECASE)
    ]

    return detected


def is_out_of_scope(question: str) -> bool:
    """Check whether a question is clearly unrelated to company policies."""
    policy_terms = {
        "policy", "company", "employee", "employees", "work",
        "working", "leave", "holiday", "hr", "human resources",
        "finance", "reimbursement", "expense", "budget", "manager",
        "recruitment", "performance review", "salary", "payroll",
        "it support", "password", "security", "document",
        "records", "approval", "department", "benefits",
    }

    question_lower = question.lower()

    return not any(term in question_lower for term in policy_terms)
