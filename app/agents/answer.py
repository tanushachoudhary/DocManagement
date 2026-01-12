from app.core.llm import llm

def generate_answer(state):
    # FIX: Loop through the list of dictionaries to get the text strings
    if state["documents"]:
        context = "\n\n".join(doc["content"] for doc in state["documents"])
    else:
        context = "No relevant documents found."
    
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
