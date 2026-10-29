
from pathlib import Path
from document_loader import load_text_file


def split_text(text: str) -> list[str]:
    """Split text into meaningful paragraph-based chunks."""
    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_heading = None

    for paragraph in paragraphs:
        if paragraph in {
            "IT Support",
            "Leave Policy",
            "Data Security",
            "Finance Policy",
        }:
            current_heading = paragraph
            continue

        if paragraph == "Company Policy":
            continue

        if current_heading:
            chunks.append(f"{current_heading}\n{paragraph}")
            current_heading = None
        else:
            chunks.append(paragraph)

    return chunks


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    document_path = project_root / "data" / "documents" / "company_policy.txt"

    text = load_text_file(str(document_path))
    chunks = split_text(text)

    print(f"Total chunks created: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {i} ---")
        print(chunk)
