from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)


def test_create_document():
    client.post("/users", json={
        "id": "u6",
        "name": "Fiona"
    })

    response = client.post("/documents", json={
        "id": "106",
        "title": "ClassNotes",
        "content": "Hi",
        "owner_id": "u6"
    })

    assert response.status_code == 201

    
def test_get_user_documents():
    # create user first
    client.post("/users", json={
        "id": "u6",
        "name": "Fiona"
    })

    response = client.get("/users/u6/documents")
    assert response.status_code == 200
    assert response.json() == []
