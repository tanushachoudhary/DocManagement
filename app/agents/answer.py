from app.core.llm import llm

def generate_answer(state):
    """
    Synthesizes an answer using the retrieved context. 
    Implements a RAG (Retrieval Augmented Generation) pattern.
    """
    
    # Context Construction:
    # We flatten the list of document dictionaries into a single string.
    # If retrieval failed or returned empty, we set a fallback string to prevent errors.
    if state.get("documents"):
        context = "\n\n".join(doc["content"] for doc in state["documents"])
    else:
        context = "No relevant documents found."
    
    # System Prompt:
    # Enforces strict grounding ("ONLY the context below") to reduce hallucinations.
    prompt = f"""
    You are a helpful assistant. Answer the question using ONLY the context below.

    Context:
    {context}

    Question:
    {state["query"]}
    """
    
    response = llm.invoke(prompt)
    state["answer"] = response.content
    return state