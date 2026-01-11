from app.core.llm import llm

def classify_intent(state):
    prompt = f"""
    Classify the user intent.

    Query: {state['query']}

    Respond with only one word:
    - document search
    - general_question        
    """
    
    response = llm.invoke(prompt).content.strip()
    state["intent"] = response
    return state