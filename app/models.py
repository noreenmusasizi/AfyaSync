from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class ClinicRecord(Base):
    __tablename__ = "clinic_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_reference = Column(String, unique=True, index=True, nullable=False)
    facility_name = Column(String, nullable=False)
    record_type = Column(String, nullable=False)
    notes = Column(String, nullable=True)

    sync_status: Mapped[str] =mapped_column(
        String,
        default="pending",
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
