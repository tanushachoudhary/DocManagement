from app.services.document_store import retrieve_documents

def retrieve_docs(state):
    state["documents"] = retrieve_documents(state["query"])
    return state

