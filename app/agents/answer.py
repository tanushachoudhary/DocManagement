from app.core.llm import llm

def generate_answer(state):
    # 1. Prepare Context
    if state["documents"]:
        # Add source metadata (like filenames) to the context for better referencing
        context_parts = []
        for i, doc in enumerate(state["documents"], 1):
            source = doc.get('metadata', {}).get('filename', 'Unknown Source')
            content = doc.get('content', '')
            context_parts.append(f"--- SOURCE {i} ({source}) ---\n{content}")
        
        context = "\n\n".join(context_parts)
    else:
        context = "No relevant documents found."

    # 2. Enhanced Prompt
    prompt = f"""
    You are an expert technical assistant designed to help engineers.
    Your goal is to answer questions accurately based ONLY on the provided context.

    RULES:
    1. **Strict Content Adherence**: Use ONLY the provided context. Do not use outside knowledge. 
       - If the answer is not in the context, say: "I cannot find the answer in the provided documents."
    2. **Citation**: When possible, mention the source filename (e.g., "According to assignment.pdf...").
    3. **Tone**: Maintain a professional, clear, and encouraging tone.

    ---------------------
    CONTEXT:
    {context}
    ---------------------

    QUESTION:
    {state["query"]}

    ANSWER:
    """
    
    # 3. Invoke LLM
    response = llm.invoke(prompt)
    state["answer"] = response.content
    return state