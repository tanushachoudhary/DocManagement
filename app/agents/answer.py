# from app.core.llm import llm

# def generate_answer(state):
#     context = "\n".join(state["documents"]) or "No relevant documents found."
    
#     prompt = f"""
#     You must answer ONLY using the provided documents.
#     If the answer is not present, say:
#     "No relevant documents found for your question."

#     Documents:
#     {context}

#     Question:
#     {state["query"]}
#     """
    
#     state["answer"]=llm.invoke(prompt).content
#     return state

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
