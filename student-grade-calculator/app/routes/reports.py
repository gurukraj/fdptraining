"""
Report and statistics routes (FR-4, FR-5).

Provides endpoints for student report cards, class statistics,
and top performer rankings.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    StudentReportResponse,
    ClassStatisticsResponse,
    TopPerformersResponse,
)
from app.services.report_service import (
    get_student_report,
    get_class_statistics,
    get_top_performers,
)

# Router for student-specific report (nested under /api/students)
report_router = APIRouter(prefix="/api/students", tags=["Reports"])

# Router for class-wide reports
class_report_router = APIRouter(prefix="/api/reports", tags=["Reports"])


@report_router.get(
    "/{student_id}/report",
    response_model=StudentReportResponse,
    summary="Get student report card (FR-4)",
)
def student_report(student_id: str, db: Session = Depends(get_db)):
    """
    Generate a report card for a specific student.

    Includes all scores, letter grades, and computed GPA.
    GPA is the average of all grade points, rounded to 2 decimal places.

    Returns 404 if the student is not found.
    """
    report = get_student_report(db, student_id)
    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with student_id '{student_id}' not found",
        )
    return report


@class_report_router.get(
    "/class-statistics",
    response_model=ClassStatisticsResponse,
    summary="Get class statistics (FR-5)",
)
def class_statistics(db: Session = Depends(get_db)):
    """
    Compute per-subject statistics for the entire class.

    For each subject, returns:
    - Average score
    - Minimum and maximum scores
    - Number of scores recorded
    - Grade distribution (count of A, B, C, D, F)
    """
    return get_class_statistics(db)


@class_report_router.get(
    "/top-performers",
    response_model=TopPerformersResponse,
    summary="Get top-performing students (FR-5)",
)
def top_performers(
    limit: int = Query(5, ge=1, le=100, description="Number of top performers to return"),
    db: Session = Depends(get_db),
):
    """
    Get a ranked list of students with the highest GPA.

    Students are sorted by GPA (descending), then by name (ascending) for tie-breaking.
    """
    return get_top_performers(db, limit)
