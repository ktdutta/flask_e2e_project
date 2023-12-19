from sqlalchemy import create_engine, Column, Integer, String, Date, Text, DECIMAL, MetaData, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class PatientVisit(Base):
    __tablename__ = 'PatientVisit'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer)
    last_visit = Column(Date)
    reason_for_visit = Column(String(255))
    patient_history = Column(Text)
    temperature = Column(DECIMAL(5, 2))
    weight = Column(DECIMAL(5, 2))
    height = Column(DECIMAL(5, 2))
    blood_pressure = Column(String(20))
    symptoms = Column(Text)
    diagnosis = Column(String(255))
    treatment = Column(Text)

## create connection and tables
# DATABASE_URL = "mysql+mysqlconnector://hants:sbu-admin-2023@scratch-server:3306/hants"
#Base.metadata.create_all(engine)

