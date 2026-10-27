from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["project"] == "AfyaSync"
    assert response.json()["status"] == "running"


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
