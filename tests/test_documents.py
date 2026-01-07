from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_create_document():
    response=client.post("/documents",json={
        
        "id":"103",
        "title": "Notes",
        "content": "Hello",
        "owner_id": "u3"
    })
    assert response.status_code==201
    
def test_get_user_documents():
    response=client.get("/users/u3/documents")
    assert response.status_code == 200
    