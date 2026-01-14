"""
This service bridges document chunking and vector search - it indexes documents
for semantic search and retrieves relevant chunks based on similarity queries.
"""
from app.services.chunker import chunk_text 
# imports function to split large text into smaller chunks
from app.services.vector_store import add_chunks, similarity_search
# imports functions to store chunks in vector DB and search by similarity

def index_document(
    document_id: int,
    text: str
):
    # splits input text into smaller chunks
    chunks = chunk_text(text)

    # creates list of metadata dictionaries for each chunk storing document ID
    # and chunk index
    metadata = [
        {
            "document_id": document_id,
            "chunk_id": i
        }
        # loops through each chunk to assign it a unique chunk ID (0,1,2 etc)
        for i in range(len(chunks))
    ]
    # stores chunks and their metadata into the vector store for semantic search
    add_chunks(chunks, metadata)

def retrieve_documents(query: str):
    # performs semantic search in vector store to find chunks most similar to query
    docs = similarity_search(query)
    # return list of results
    return [
        {
            "content": d["content"],  # extracts text content from each result
            "metadata": d["metadata"] # extracts metadata(doc_id, chunk_id) from each result
        }
        for d in docs
    ]