
import os
from functools import lru_cache
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

try:
    from .access_control import get_allowed_documents
except ImportError:
    from access_control import get_allowed_documents


PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Use Azure-mounted storage when configured; otherwise use local storage.
DB_DIR = Path(
    os.getenv("CHROMA_DB_DIR", str(PROJECT_ROOT / "chroma_db"))
)


@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the embedding model only once per application process."""
    return SentenceTransformer("all-MiniLM-L6-v2")


@lru_cache(maxsize=1)
def get_chroma_collection():
    """Create and reuse the persistent ChromaDB collection."""
    client = chromadb.PersistentClient(path=str(DB_DIR))
    return client.get_collection(name="company_policies")


def retrieve_documents(question: str, role: str, n_results: int = 2):
    """Retrieve only documents permitted for the given role."""

    allowed_documents = get_allowed_documents(role)

    if not allowed_documents:
        return []

    collection = get_chroma_collection()
    model = get_embedding_model()

    query_embedding = model.encode(question).tolist()

    result_count = min(n_results, collection.count())

    if result_count == 0:
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=result_count,
        where={"source": {"$in": allowed_documents}},
        include=["documents", "metadatas"],
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    # Defensive check: never return an unauthorized document.
    allowed_set = set(allowed_documents)

    permitted_documents = [
        document
        for document, metadata in zip(documents, metadatas)
        if metadata and metadata.get("source") in allowed_set
    ]

    return permitted_documents


def main():
    question = input("Ask a question about company policies: ")
    role = input("Enter role (general, hr, finance): ").strip().lower()

    documents = retrieve_documents(question, role)

    print("\nRelevant information:")
    print("-" * 40)

    if not documents:
        print("No permitted documents found.")
        return

    for i, document in enumerate(documents, start=1):
        print(f"\nResult {i}:")
        print(document)


if __name__ == "__main__":
    main()
