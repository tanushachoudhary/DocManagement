from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.graph import ai_graph

ai_router = APIRouter(prefix="/ai", tags=["AI"])


class AskRequest(BaseModel):
    question: str


@ai_router.post("/ask")
def ask_ai(request: AskRequest):
    result = ai_graph.invoke(
        {
            "query": request.question,
            "intent": "",
            "documents": [],
            "answer": "",
        }
    )

    return {
        "question": request.question,
        "answer": result["answer"],
    }

