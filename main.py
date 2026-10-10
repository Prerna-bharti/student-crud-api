from datetime import date
from typing import List, Optional
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from model import Student
from schemas import StudentCreate, StudentOut, StudentUpdate
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student CRUD API",
    description="Manage student records: create, read, update and delete.",
    version="1.0",
    docs_url=None,
    )
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_or_404(db: Session, Student_id: int) -> Student:
    student = db.get(Student, Student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

DARK_CSS = """
body { background: #121212; }
.swagger-ui { filter: invert(88%) hue-rotate(180deg); }
.swagger-ui .microlight { filter: invert(100%) hue-rotate(180deg); }
"""


@app.get("/docs", include_in_schema=False)
def custom_docs():
    page = get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title="Student CRUD API",
    )
    html = bytes(page.body).decode()
    html = html.replace("</head>", f"<style>{DARK_CSS}</style></head>")
    return HTMLResponse(html)

@app.get("/")
def home():
    return {"message": "Student CRUD API is running!"}

@app.post("/students", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    student = Student(**payload.model_dump())
    db.add(student)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")
    db.refresh(student)
    return student
@app.get("/students", response_model=List[StudentOut])
def list_students(
    name: Optional[str] = Query(None, description="Partial name match"),
    course: Optional[str] = None,
    born_after: Optional[date] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    q = db.query(Student)
    if name:
        q = q.filter(Student.name.ilike(f"%{name}%"))
    if course:
        q = q.filter(Student.course.ilike(course))
    if born_after:
        q = q.filter(Student.date_of_birth > born_after)
    return q.order_by(Student.id).offset(skip).limit(limit).all()
            
@app.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, student_id)

@app.patch("/students/{student_id}", response_model=StudentOut)
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = get_or_404(db, student_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
    try:
            db.commit()
    except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=409, detail="Email already exists")
    db.refresh(student)
    return student
    
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = get_or_404(db, student_id)
    db.delete(student)
    db.commit()
    return {"message": f"Student {student_id} deleted"}