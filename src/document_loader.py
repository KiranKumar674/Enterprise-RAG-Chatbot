
from pathlib import Path


def load_text_file(file_path: str) -> str:
    """Read a text document and return its contents."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    document_path = Path(__file__).resolve().parent.parent / "data" / "documents" / "company_policy.txt"

    text = load_text_file(str(document_path))

    print("Document loaded successfully!")
    print("-" * 40)
    print(text)
