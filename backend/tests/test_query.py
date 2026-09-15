from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_query_happy_path(monkeypatch):
    class FakeRetriever:
        def retrieve(self, question, k=2):
            return []


    class FakeGenerator:
        def generate(self, question, documents):
            return (
                "The Nile was important to Ancient Egypt.",
                ["Chunk 1 — ancient_egypt.html"]
            )


    with TestClient(app) as client:
        monkeypatch.setattr(
            app.state,
            "retriever",
            FakeRetriever()
        )

        monkeypatch.setattr(
            app.state,
            "generator",
            FakeGenerator()
        )

        response = client.post(
            "/query",
            json={
                "question": "Why was the Nile important?"
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data
    assert data["answer"] == "The Nile was important to Ancient Egypt."
    assert len(data["sources"]) > 0


def test_invalid_query():
    with TestClient(app) as client:
        response = client.post(
            "/query",
            json={}
        )

    assert response.status_code == 422