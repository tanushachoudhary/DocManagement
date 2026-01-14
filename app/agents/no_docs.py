from app.core.llm import llm

def no_docs_response(state):
    """
    Handles cases where no relevant documents are found.
    Returns a message indicating that relevant documentation is not available
    in the document store.
    
    This is triggered when:
    1. The intent classifier determines the query is not doc-related
    2. Document retrieval returns no matching documents
    """
    # Create a response message indicating no relevant docs found
    message = "I apologize, but I could not find relevant documentation to answer your question. The information you're looking for is not available in the document store."
    
    state["answer"] = message
    state["has_documents"] = False
    return state