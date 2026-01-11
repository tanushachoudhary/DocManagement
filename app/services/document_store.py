from app.services.chunker import chunk_text
from app.services.vector_store import add_chunks, similarity_search

def index_document(
    document_id: int,
    text: str
):
    chunks = chunk_text(text)

    metadata = [
        {
            "document_id": document_id,
            "chunk_id": i
        }
        for i in range(len(chunks))
    ]

    add_chunks(chunks, metadata)

def retrieve_documents(query: str):
    docs = similarity_search(query)
    # FIX: Access keys using ["brackets"], not .dot_notation
    return [
        {
            "content": d["content"], 
            "metadata": d["metadata"]
        }
        for d in docs
    ]