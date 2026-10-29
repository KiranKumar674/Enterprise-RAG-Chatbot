
from pathlib import Path

import chromadb  # type: ignore
from sentence_transformers import SentenceTransformer  # type: ignore

try:
    from .access_control import get_allowed_documents
except ImportError:
    from access_control import get_allowed_documents


def retrieve_documents(question: str, role: str, n_results: int = 2):
    """Retrieve only documents permitted for the given role."""

    allowed_documents = get_allowed_documents(role)

    if not allowed_documents:
        return []

    project_root = Path(__file__).resolve().parent.parent
    database_path = project_root / "chroma_db"

    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=str(database_path))
    collection = client.get_collection(name="company_policies")

    query_embedding = model.encode(question).tolist()

    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={"source": {"$in": allowed_documents}},
        include=["documents", "metadatas"],
    )
    print("ROLE:", role)
    print("ALLOWED DOCUMENTS:", allowed_documents)
    print("COLLECTION:", collection.name)
    print("COUNT BEFORE FILTER:", collection.count())

    print("RETURNED METADATA:", results.get("metadatas"))

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    # Defensive check: never return a chunk from an unauthorized source.
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
