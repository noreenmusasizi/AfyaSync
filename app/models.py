from sqlalchemy import Column, Integer, String

from .database import Base


class ClinicRecord(Base):
    __tablename__ = "clinic_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_reference = Column(String, unique=True, index=True, nullable=False)
    facility_name = Column(String, nullable=False)
    record_type = Column(String, nullable=False)
    notes = Column(String, nullable=True)
