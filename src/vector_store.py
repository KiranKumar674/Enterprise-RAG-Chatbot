
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from document_loader import load_text_file
from text_chunker import split_text


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"
DB_DIR = PROJECT_ROOT / "chroma_db"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=str(DB_DIR))
collection = client.get_or_create_collection(
    name="company_policies"
)


def rebuild_vector_store():
    chunks = []
    metadatas = []
    ids = []

    for file_path in sorted(DOCUMENTS_DIR.glob("*.txt")):
        text = load_text_file(str(file_path))
        document_chunks = split_text(text)

        for chunk in document_chunks:
            chunks.append(chunk)
            metadatas.append({"source": file_path.name})
            ids.append(f"{file_path.stem}_{len(ids)}")

    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    if chunks:
        embeddings = embedding_model.encode(chunks).tolist()

        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    print(f"Successfully indexed {len(chunks)} chunks.")
    print("Indexed document sources:")

    for filename in sorted({item["source"] for item in metadatas}):
        print(f"- {filename}")


if __name__ == "__main__":
    rebuild_vector_store()
