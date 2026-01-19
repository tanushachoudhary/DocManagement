# Retrieve agent module - handles document retrieval from vector store
# Part of the LangGraph agent workflow for RAG (Retrieval-Augmented Generation)

from app.services.document_store import retrieve_documents
# Import function that performs semantic search to find relevant document chunks


def retrieve_docs(state):
    """
    Agent node that retrieves relevant documents based on user query.
    
    This is a node in the LangGraph workflow that:
    1. Takes the user's query from state
    2. Performs semantic search using vector similarity
    3. Stores retrieved documents back into state for downstream agents
    
    Args:
        state (dict): Current graph state containing at minimum:
            - "query" (str): User's search query
                      
    Returns:
        dict: Updated state with new key:
            - "documents" (list): Retrieved document chunks with metadata
              
    Flow:
        User Query → retrieve_docs() → [documents] → answer_agent()
    """
    
    # Perform semantic search to find relevant document chunks
    # retrieve_documents() queries the FAISS vector store and returns matching chunks
    state["documents"] = retrieve_documents(state["query"])
    
    # Return updated state to next agent in the graph
    # The "documents" key will be used by answer agent to generate responses
    return state