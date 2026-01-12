from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.graph import ai_graph

# Group AI-related endpoints under the "/ai" prefix
ai_router = APIRouter(prefix="/ai", tags=["AI"])

# Pydantic model ensures the user sends valid JSON: {"question": "some text"}
class AskRequest(BaseModel):
    question: str

@ai_router.post("/ask")
def ask_ai(request: AskRequest):
    """
    The main chat endpoint. 
    It passes the user's question into the LangGraph 'Brain' 
    and returns the AI's decision (intent) and final answer.
    """
    # Invoke the LangGraph workflow
    # We initialize the state with the user's query and empty placeholders
    result = ai_graph.invoke(
        {
            "query": request.question,
            "intent": "",       # Will be filled by Intent Agent
            "documents": [],    # Will be filled by Retriever (if needed)
            "answer": "",       # Will be filled by Response Agent
        }
    )

    # Return a structured response
    return {
        "question": request.question,
        "answer": result["answer"],
        "intent": result["intent"] # Useful for debugging (did it search or just chat?)
    }