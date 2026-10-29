
# Document access permissions for each user role

ROLE_PERMISSIONS = {
    "general": ["company_policy.txt"],
    "hr": [
        "company_policy.txt",
        "hr_policy.txt",
    ],
    "finance": [
        "company_policy.txt",
        "finance_policy.txt",
    ],
}


def get_allowed_documents(role: str) -> list[str]:
    """Return document filenames accessible to a valid role."""
    if not isinstance(role, str):
        return []

    normalized_role = role.strip().lower()

    return ROLE_PERMISSIONS.get(normalized_role, []).copy()
