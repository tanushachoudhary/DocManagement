from app.core.llm import llm

def no_docs_response(state):
    """
    Handles general conversation or knowledge questions where 
    retrieval was deemed unnecessary by the intent classifier.
    """
    response = llm.invoke(
        f"Answer the following question clearly and concisely:\n\n{state['query']}"
    )

    state["answer"] = response.content
    return state