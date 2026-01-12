# tests/test_phase4.py
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.agents.intent import classify_intent
from app.agents.graph import ai_graph

client = TestClient(app)

# ==========================================
# 1. UNIT TEST: Intent Classifier
# ==========================================
# tests/test_phase4.py

# ... keep your imports ...

# ==========================================
# 1. UNIT TEST: Intent Classifier (FIXED)
# ==========================================
def test_classify_intent_greeting():
    """Test that greetings are classified as 'no_docs'"""
    state = {"query": "Hello, good morning!", "intent": ""}
    
    # FIX: Patch the entire 'llm' object, not 'llm.invoke'
    with patch("app.agents.intent.llm") as mock_llm:
        # We tell the mock: "When .invoke() is called, return this object..."
        # And that object has a .content property = "no_docs"
        mock_llm.invoke.return_value.content = "no_docs"
        
        result_state = classify_intent(state)
        
        assert result_state["intent"] == "no_docs"

def test_classify_intent_search():
    """Test that specific questions are classified as 'retrieve'"""
    state = {"query": "What is the refund policy?", "intent": ""}
    
    # FIX: Patch the entire 'llm' object
    with patch("app.agents.intent.llm") as mock_llm:
        mock_llm.invoke.return_value.content = "retrieve"
        
        result_state = classify_intent(state)
        
        assert result_state["intent"] == "retrieve"

# ... keep the rest of your tests (they were already passing) ...

# ==========================================
# 2. INTEGRATION TEST: The Full Graph
# ==========================================
def test_graph_logic_short_circuit():
    """
    Verify that if intent is 'no_docs', the graph SKIPS retrieval.
    """
    # Mock the intent classifier to force "no_docs"
    with patch("app.agents.graph.classify_intent") as mock_classifier:
        mock_classifier.return_value = {"query": "Hi", "intent": "no_docs"}
        
        # Mock retrieval to crash if it IS called (to prove it wasn't)
        with patch("app.agents.graph.retrieve_docs") as mock_retrieve:
            mock_retrieve.side_effect = Exception("Retrieval should NOT be called!")
            
            # Run the graph
            result = ai_graph.invoke({
                "query": "Hi",
                "intent": "",
                "documents": [],
                "answer": ""
            })
            
            # Assertions
            assert result["intent"] == "no_docs"
            assert mock_retrieve.call_count == 0 # Proof we skipped the DB

# ==========================================
# 3. API TEST: The Endpoint
# ==========================================
def test_ask_endpoint_flow():
    """Test the full /ai/ask endpoint"""
    payload = {"question": "How does the code work?"}
    
    # We mock the graph execution to return a predictable answer
    # This isolates the API test from the AI logic
    fake_result = {
        "query": "How does the code work?",
        "intent": "retrieve",
        "answer": "The code uses Python.",
        "documents": []
    }
    
    with patch("app.routers.ai.ai_graph.invoke", return_value=fake_result):
        response = client.post("/ai/ask", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["question"] == "How does the code work?"
        assert data["answer"] == "The code uses Python."
        assert data["intent"] == "retrieve"