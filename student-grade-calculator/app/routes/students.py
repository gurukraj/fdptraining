"""
Student CRUD routes (FR-1, FR-6).

Provides endpoints for creating, listing, and retrieving students.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student
from app.schemas import StudentCreate, StudentResponse, StudentListResponse

router = APIRouter(prefix="/api/students", tags=["Students"])


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new student (FR-1)",
)
def create_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    """
    Register a new student.

    - **student_id**: Unique identifier (3-20 alphanumeric characters)
    - **name**: Student's full name (1-100 characters)

    Returns 409 Conflict if the student_id already exists.
    """
    # Check for duplicate student_id
    existing = (
        db.query(Student)
        .filter(Student.student_id == student_data.student_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Student with student_id '{student_data.student_id}' already exists",
        )

    student = Student(
        student_id=student_data.student_id,
        name=student_data.name,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get(
    "",
    response_model=StudentListResponse,
    summary="List all students (FR-6)",
)
def list_students(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    name: str | None = Query(None, description="Filter by name (partial match)"),
    db: Session = Depends(get_db),
):
    """
    Retrieve a paginated list of students.

    Supports optional filtering by name (case-insensitive partial match).
    """
    query = db.query(Student)

    if name:
        query = query.filter(Student.name.ilike(f"%{name}%"))

    total = query.count()
    students = (
        query.order_by(Student.student_id)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return StudentListResponse(
        students=students,
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Get student details (FR-6)",
)
def get_student(student_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single student by their student_id.

    Returns 404 if the student is not found.
    """
    student = (
        db.query(Student).filter(Student.student_id == student_id).first()
    )
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with student_id '{student_id}' not found",
        )
    return student
