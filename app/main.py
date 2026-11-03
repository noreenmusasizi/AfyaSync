import logging
from collections.abc import Generator
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import ClinicRecord

# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

logger = logging.getLogger("afyasync")


# Create database tables
Base.metadata.create_all(bind=engine)


# Initialize FastAPI
app = FastAPI(
    title="Care Beyond Connectivity API",
    description=(
        "An offline-first digital healthcare infrastructure platform. "
        "Reliable healthcare, with or without internet."
    ),
    version="0.1.0",
)

# Configure Prometheus metrics
Instrumentator().instrument(app).expose(app)


# Database dependency
def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Request model
class ClinicRecordCreate(BaseModel):
    patient_reference: str
    facility_name: str
    record_type: str
    notes: str | None = None


# Response model
class ClinicRecordResponse(BaseModel):
    id: int
    patient_reference: str
    facility_name: str
    record_type: str
    notes: str | None = None
    sync_status: str
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


# Home endpoint
@app.get("/")
def home() -> dict[str, str]:
    return {
        "project": "AfyaSync",
        "status": "running",
        "message": "Welcome to the AfyaSync API",
    }


# Health check endpoint
@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
    }


# Create a clinical record
@app.post("/records", response_model=ClinicRecordResponse, status_code=201)
def create_record(
    record: ClinicRecordCreate,
    db: Session = Depends(get_db),
) -> ClinicRecord:

    existing = (
        db.query(ClinicRecord)
        .filter(ClinicRecord.patient_reference == record.patient_reference)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="A record with this patient reference already exists.",
        )

    new_record = ClinicRecord(**record.model_dump())

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    logger.info(
        "Clinical record created successfully. Record ID: %s",
        new_record.id,
    )

    return new_record


# Retrieve all clinical records
@app.get("/records", response_model=list[ClinicRecordResponse])
def get_records(db: Session = Depends(get_db)) -> list[ClinicRecord]:
    return db.query(ClinicRecord).order_by(ClinicRecord.id).all()


# Retrieve pending records
@app.get("/records/pending", response_model=list[ClinicRecordResponse])
def get_pending_records(db: Session = Depends(get_db)) -> list[ClinicRecord]:
    return (
        db.query(ClinicRecord)
        .filter(ClinicRecord.sync_status == "pending")
        .order_by(ClinicRecord.id)
        .all()
    )


# Mark a record as synchronised
@app.patch("/records/{record_id}/sync", response_model=ClinicRecordResponse)
def mark_record_as_synced(
    record_id: int,
    db: Session = Depends(get_db),
) -> ClinicRecord:

    record = db.query(ClinicRecord).filter(ClinicRecord.id == record_id).first()

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Clinic record not found.",
        )

    if record.sync_status == "synced":
        raise HTTPException(
            status_code=409,
            detail="This record is already synchronised.",
        )

    record.sync_status = "synced"

    db.commit()
    db.refresh(record)

    logger.info(
        "Clinical record synchronised successfully. Record ID: %s",
        record.id,
    )

    return record
