from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator
class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9\- ]{7,15}$")
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None
    @model_validator(mode="after")
    def need_contact(self):
        if not self.email and not self.phone:
            raise ValueError("Provide at least one of email or phone")
        if self.date_of_birth >= date.today():
            raise ValueError("date_of_birth must be in the past")
        return self
class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9\- ]{7,15}$")
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None
class StudentOut(StudentCreate):
        model_config = ConfigDict(from_attributes=True)
        id: int