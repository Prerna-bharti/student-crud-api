import string
from sqlalchemy import Column, Date, Integer, String
from database import Base

class Student(Base):
    __tablename__ = "Students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column (String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email=Column(String, unique=True, index=True, nullable=True)
    phone=Column(String, nullable=True)
    course=Column(String, nullable=True)
    address=Column(String, nullable=True)
    enrollment_date=Column(Date, nullable=True)  