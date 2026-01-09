def index_sample_document(client):
    client.post(
        "/documents/index",
        json={
            "document_id": 1,
            "text": "Artificial intelligence enables machines to learn"
        }
    )


def test_search_valid_query(client):
    index_sample_document(client)

    response = client.post(
        "/search",
        json={"query": "What is artificial intelligence?"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0
    assert data["results"][0]["document_id"] == 1


def test_search_empty_query(client):
    response = client.post(
        "/search",
        json={"query": ""}
    )

    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_search_without_indexing(client):
    response = client.post(
        "/search",
        json={"query": "AI"}
    )

    assert response.status_code == 200
    assert response.json()["results"] == []


def test_search_ranking_multiple_documents(client):
    client.post(
        "/documents/index",
        json={
            "document_id": 1,
            "text": "Artificial intelligence and machine learning"
        }
    )

    client.post(
        "/documents/index",
        json={
            "document_id": 2,
            "text": "Financial markets and stock trading"
        }
    )

    response = client.post(
        "/search",
        json={"query": "machine learning"}
    )

    results = response.json()["results"]
    assert len(results) >= 1
    assert results[0]["document_id"] == 1


def test_search_special_characters(client):
    client.post(
        "/documents/index",
        json={
            "document_id": 3,
            "text": "AI @ scale! #ML 🚀"
        }
    )

    response = client.post(
        "/search",
        json={"query": "AI"}
    )

    assert response.status_code == 200
    assert len(response.json()["results"]) > 0
