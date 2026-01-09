def test_index_valid_document(client):
    response = client.post(
        "/documents/index",
        json={
            "document_id": 1,
            "text": "Machine learning is a subset of artificial intelligence"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Document indexed successfully"


def test_index_empty_text(client):
    response = client.post(
        "/documents/index",
        json={
            "document_id": 1,
            "text": ""
        }
    )

    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_index_invalid_document_id(client):
    response = client.post(
        "/documents/index",
        json={
            "document_id": 999,
            "text": "Some text"
        }
    )

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_index_duplicate_document(client):
    payload = {
        "document_id": 1,
        "text": "Deep learning is part of AI"
    }

    first = client.post("/documents/index", json=payload)
    second = client.post("/documents/index", json=payload)

    assert first.status_code == 200
    assert second.status_code in (200, 409)
