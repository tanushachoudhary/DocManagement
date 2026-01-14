from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.graph import ai_graph

# Group AI-related endpoints under the "/ai" prefix
ai_router = APIRouter(prefix="/ai", tags=["AI"])

# Pydantic model ensures the user sends valid JSON: {"question": "some text"}
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
    3. Returns the final answer, intent classification, and source document chunks.
    
    The response includes:
    - question: The original user question
    - answer: The generated response
    - intent: Classification ('retrieve' or 'no_docs')
    - sources: List of document chunks used to generate the answer (empty if no_docs intent)
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
    # and the source documents/chunks used (if any)
    return {
        "question": request.question,
        "answer": result["answer"],
        "intent": result["intent"],
        "sources": result.get("documents", [])  # Include retrieved document chunks
    }