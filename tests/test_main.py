
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app, get_db

TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture
def client() -> Generator[TestClient]:
    Base.metadata.create_all(bind=test_engine)

    def override_get_db() -> Generator:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_home(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["project"] == "AfyaSync"
    assert response.json()["status"] == "running"


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_record(client: TestClient) -> None:
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
    assert response.json()["sync_status"] == "pending"
    assert response.json()["created_at"] is not None


def test_get_records(client: TestClient) -> None:
    response = client.get("/records")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_pending_records(client: TestClient) -> None:
    client.post(
        "/records",
        json={
            "patient_reference": "PENDING-001",
            "facility_name": "AfyaSync Demo Clinic",
            "record_type": "Check-up",
            "notes": "Waiting for synchronisation",
        },
    )

    response = client.get("/records/pending")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["patient_reference"] == "PENDING-001"
    assert response.json()[0]["sync_status"] == "pending"

def test_mark_record_as_synced(client: TestClient) -> None:
    create_response = client.post(
        "/records",
        json={
            "patient_reference": "SYNC-TEST-001",
            "facility_name": "AfyaSync Demo Clinic",
            "record_type": "Check-up",
            "notes": "Testing synchronization",
        },
    )

    record_id = create_response.json()["id"]

    response = client.patch(f"/records/{record_id}/sync")

    assert response.status_code == 200
    assert response.json()["sync_status"] == "synced"

def test_mark_already_synced_record_returns_conflict(
    client: TestClient,
) -> None:
    create_response = client.post(
        "/records",
        json={
            "patient_reference": "SYNC-TEST-002",
            "facility_name": "AfyaSync Demo Clinic",
            "record_type": "Check-up",
            "notes": "Testing duplicate synchronization",
        },
    )

    record_id = create_response.json()["id"]

    client.patch(f"/records/{record_id}/sync")
    response = client.patch(f"/records/{record_id}/sync")

    assert response.status_code == 409

def test_mark_nonexistent_record_returns_404(
    client: TestClient,
) -> None:
    response = client.patch("/records/9999/sync")

    assert response.status_code == 404
