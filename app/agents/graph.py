from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.intent import classify_intent
from app.agents.retrieve import retrieve_docs
from app.agents.answer import generate_answer
from app.agents.no_docs import no_docs_response

# Initialize the StateGraph with TypedDict schema
graph = StateGraph(AgentState)

# ---------------------------
# 1. Add Nodes (The Workers)
# ---------------------------
graph.add_node("intent", classify_intent)  # Step 1: Decide what to do
graph.add_node("retrieve", retrieve_docs)  # Step 2a: Get data
graph.add_node("answer", generate_answer)  # Step 2b: Answer with data
graph.add_node("no_docs", no_docs_response)# Step 2c: Answer without data

# ---------------------------
# 2. Set Entry Point
# ---------------------------
# Every request starts at the 'intent' node
graph.set_entry_point("intent")

# ---------------------------
# 3. Conditional Logic (The Routing)
# ---------------------------

def route_intent(state):
    """
    Logic to parse the output of the 'intent' node.
    Returns the *name* of the next node to visit.
    """
    if state["intent"] == "no_docs":
        return "no_docs"
    return "retrieve"

# Add the fork in the road based on user intent
graph.add_conditional_edges(
    "intent",           # Start node
    route_intent,       # Decision function
    {                   # Mapping: Result -> Next Node Name
        "retrieve": "retrieve",
        "no_docs": "no_docs"
    }
)

def route_after_retrieval(state):
    """
    Safety Net: Checks if retrieval actually found anything.
    If the vector store returns empty list [], we shouldn't try 
    to RAG answer. Fallback to general chat.
    """
    docs = state.get("documents", [])
    if not docs:
        return "no_docs"
    return "answer"

# Add logic after retrieval to handle empty search results
graph.add_conditional_edges(
    "retrieve",
    route_after_retrieval,
    {
        "answer": "answer",
        "no_docs": "no_docs",
    }
)

# ---------------------------
# 4. End Points
# ---------------------------
# Both answering paths lead to the end of the workflow
graph.add_edge("answer", END)
graph.add_edge("no_docs", END)

# Compile the graph into a runnable application
ai_graph = graph.compile()