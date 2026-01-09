import pytest
from fastapi.testclient import TestClient
from app.main import app
import app.services.vector_store as vector_store


@pytest.fixture(scope="function")
def client():
    vector_store.reset_store()
    with TestClient(app) as c:
        yield c
