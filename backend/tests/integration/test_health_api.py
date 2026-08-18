from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():

    response = client.get(
        "/api/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert (
        data["service"]
        == "eu-ai-act-rag-backend"
    )


def test_readiness_endpoint():

    response = client.get(
        "/api/ready"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ready"
    assert data["database"] == "connected"
    assert data["pgvector"] == "available"