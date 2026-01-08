from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_create_user():
    response=client.post("/users",json={
        
        "id":"u5",
        "name":"Elena"
    })
    assert response.status_code==201