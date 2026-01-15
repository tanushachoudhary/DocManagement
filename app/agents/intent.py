from app.core.llm import llm


def classify_intent(state):
    prompt = f"""
    You are an intelligent router for a Document Retrieval System.
    Your job is to decide if the user's query requires looking up specific uploaded documents or if it can be answered with general knowledge.

    ### DEFINITIONS
    - 'retrieve': Use this for questions about specific files, project details, code errors, summaries of uploaded content, or specific facts contained in the database.
    - 'no_docs': Use this for greetings (Hi, Hello), general world knowledge (e.g., "What is the capital of France?"), or questions unrelated to the uploaded context.

    ### EXAMPLES
    Query: "Hi, how are you?"
    Intent: no_docs

    Query: "Summarize the pdf I just uploaded."
    Intent: retrieve

    Query: "What is the error in main.py?"
    Intent: retrieve

    Query: "Write a python script to sort a list."
    Intent: no_docs

    Query: "What does the document say about refund policies?"
    Intent: retrieve


    ### YOUR TURN
    Query: {state['query']}

    Respond with ONLY one word ('retrieve' or 'no_docs'):

    """

    # 1. Invoke LLM
    response_content = llm.invoke(prompt).content
    
    # Handle list response
    if isinstance(response_content, list):
        response = str(response_content[0]).strip().lower() if response_content else ""
    else:
        response = str(response_content).strip().lower()

    # 2. Safety Fallback (in case LLM outputs "intent: retrieve")
    if "retrieve" in response:
        state["intent"] = "retrieve"
    else:
        state["intent"] = "no_docs"
    return state