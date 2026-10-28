from collections.abc import Generator

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import ClinicRecord

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AfyaSync API",
    description="An offline-first healthcare infrastructure prototype.",
    version="0.1.0",
)


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ClinicRecordCreate(BaseModel):
    patient_reference: str
    facility_name: str
    record_type: str
    notes: str | None = None


class ClinicRecordResponse(ClinicRecordCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


@app.get("/")
def home() -> dict[str, str]:
    return {
        "project": "AfyaSync",
        "status": "running",
        "message": "Welcome to the AfyaSync API",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
    }


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

    return new_record


@app.get("/records", response_model=list[ClinicRecordResponse])
def get_records(db: Session = Depends(get_db)) -> list[ClinicRecord]:
    return db.query(ClinicRecord).order_by(ClinicRecord.id).all()
