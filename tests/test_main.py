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


def test_create_record() -> None:
    response = client.post(
        "/records",
        json={
            "patient_reference": "TEST-AUTO-001",
            "facility_name": "AfyaSync Demo Clinic",
            "record_type": "Check-up",
            "notes": "Synthetic automated test record",
        },
    )

    assert response.status_code == 201
    assert response.json()["patient_reference"] == "TEST-AUTO-001"


def test_get_records() -> None:
    response = client.get("/records")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
