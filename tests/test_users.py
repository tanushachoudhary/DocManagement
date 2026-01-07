from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_create_user():
    response=client.post("/users",json={
        
        "id":"u3",
        "name":"Charlie"
    })
    assert response.status_code==201