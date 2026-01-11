from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.intent import classify_intent
from app.agents.retrieve import retrieve_docs
from app.agents.answer import generate_answer
from app.agents.no_docs import no_docs_response

graph = StateGraph(AgentState)

graph.add_node("intent", classify_intent)
graph.add_node("retrieve", retrieve_docs)
graph.add_node("answer", generate_answer)
graph.add_node("no_docs", no_docs_response)

graph.set_entry_point("intent")

graph.add_edge("intent", "retrieve")

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

graph.add_edge("answer", END)
graph.add_edge("no_docs", END)

ai_graph = graph.compile()
