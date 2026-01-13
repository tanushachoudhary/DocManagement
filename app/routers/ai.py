from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.graph import ai_graph

# Create a dedicated router for AI operations
ai_router = APIRouter(prefix="/ai", tags=["AI"])

class AskRequest(BaseModel):
    """
    Request schema for the /ask endpoint.
    Strictly types the input to ensure we receive a string question.
    """
    question: str


@ai_router.post("/ask")
def ask_ai(request: AskRequest):
    """
    Main entry point for the RAG agent.
    
    1. Receives a user question.
    2. Invokes the LangGraph state machine.
    3. Returns the final answer and the intent (classification).
    """
    
    # The 'invoke' method starts the graph traversal.
    # We initialize the state with empty default values.
    result = ai_graph.invoke(
        {
            "query": request.question,
            "intent": "",       # Will be filled by classify_intent node
            "documents": [],    # Will be filled by retrieve_docs node (if needed)
            "answer": "",       # Will be filled by generate_answer or no_docs node
        }
    )

    # Return a structured response including the AI's reasoning (intent)
    return {
        "question": request.question,
        "answer": result["answer"],
        "intent": result["intent"]
    }