from typing import TypedDict, List

class AgentState(TypedDict):
    """
    Defines the structure of the state object passed between LangGraph nodes.
    
    Attributes:
        query (str): The original input question from the user.
        intent (str): The classification result ('retrieve' or 'no_docs').
        documents (List[str]): A list of content strings retrieved from the vector store.
        answer (str): The final generated response to be sent back to the user.
    """
    query: str
    intent: str
    documents: List[str]
    answer: str