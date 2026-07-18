"""
Score recording routes (FR-2).

Provides the endpoint for recording a student's score in a subject,
with automatic letter grade and grade point calculation.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import Student, Score
from app.schemas import ScoreCreate, ScoreResponse
from app.services.grade_service import calculate_letter_grade, calculate_grade_points

router = APIRouter(prefix="/api/students", tags=["Scores"])


@router.post(
    "/{student_id}/scores",
    response_model=ScoreResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record a score for a student (FR-2)",
)
def record_score(
    student_id: str,
    score_data: ScoreCreate,
    db: Session = Depends(get_db),
):
    """
    Record a score for a student in a specific subject.

    - **subject**: Name of the subject
    - **score**: Numeric score (0-100)

    Automatically calculates the letter grade and grade points.

    Returns:
    - 201 Created with the score record
    - 404 if the student does not exist
    - 409 if a score already exists for this student/subject combination
    """
    # Verify student exists
    student = (
        db.query(Student).filter(Student.student_id == student_id).first()
    )
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with student_id '{student_id}' not found",
        )

    # Check for duplicate student_id + subject
    existing_score = (
        db.query(Score)
        .filter(Score.student_id == student_id, Score.subject == score_data.subject)
        .first()
    )
    if existing_score:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Score for student '{student_id}' in subject "
                f"'{score_data.subject}' already exists"
            ),
        )

    # Calculate grade
    letter_grade = calculate_letter_grade(score_data.score)
    grade_points = calculate_grade_points(letter_grade)

    score = Score(
        student_id=student_id,
        subject=score_data.subject,
        score=score_data.score,
        letter_grade=letter_grade,
        grade_points=grade_points,
    )
    db.add(score)

    try:
        db.commit()
        db.refresh(score)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Score for student '{student_id}' in subject "
                f"'{score_data.subject}' already exists"
            ),
        )

    return score
