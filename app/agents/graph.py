from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.intent import classify_intent
from app.agents.retrieve import retrieve_docs
from app.agents.answer import generate_answer
from app.agents.no_docs import no_docs_response

graph = StateGraph(AgentState)

# 1. Add Nodes
graph.add_node("intent", classify_intent)
graph.add_node("retrieve", retrieve_docs)
graph.add_node("answer", generate_answer)
graph.add_node("no_docs", no_docs_response)


# 2. Set Entry Point
graph.set_entry_point("intent")

# 3. Define Logic to Route based on Intent
def route_intent(state):
    # This reads the decision made by the 'intent' node
    # If the LLM said "no_docs", we skip retrieval entirely!
    if state["intent"] == "no_docs":
        return "no_docs"
    return "retrieve"

# 4. Add the Conditional Edge (The Fork in the Road)
graph.add_conditional_edges(
    "intent",       # Start at the intent node
    route_intent,   # Run this function
    {               # Map output to next node
        "retrieve": "retrieve",
        "no_docs": "no_docs"
    }
)

# 5. Keep your existing logic for "after retrieval" (Safety Net)
# This is still good! If retrieval runs but finds nothing (empty list),
# we fallback to 'no_docs' instead of trying to answer with empty context.
def route_after_retrieval(state):
    docs = state.get("documents", [])
    if not docs:
        return "no_docs"
    return "answer"

graph.add_conditional_edges(
    "retrieve",
    route_after_retrieval,
    {
        "answer": "answer",
        "no_docs": "no_docs",
    }
)

# 6. End Points
graph.add_edge("answer", END)
graph.add_edge("no_docs", END)

ai_graph = graph.compile()