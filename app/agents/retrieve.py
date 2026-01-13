from app.services.document_store import retrieve_documents

def retrieve_docs(state):
    """
    Queries the vector database/document store for context relevant to the query.
    """
    # Populates the 'documents' key in the state with search results
    state["documents"] = retrieve_documents(state["query"])
    return state