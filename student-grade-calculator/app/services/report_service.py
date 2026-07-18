"""
Report and statistics computation service (FR-4, FR-5).

Provides functions to generate student report cards,
class-level statistics, and top performer rankings.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Student, Score
from app.services.grade_service import calculate_gpa
from app.schemas import (
    ReportScoreItem,
    StudentReportResponse,
    SubjectStatistics,
    GradeDistribution,
    ClassStatisticsResponse,
    TopPerformerItem,
    TopPerformersResponse,
)


def get_student_report(db: Session, student_id: str) -> StudentReportResponse | None:
    """
    Generate a report card for a specific student (FR-4).

    Args:
        db: Database session.
        student_id: The student's unique identifier.

    Returns:
        StudentReportResponse with all scores, grades, and GPA,
        or None if the student is not found.
    """
    student = (
        db.query(Student).filter(Student.student_id == student_id).first()
    )
    if not student:
        return None

    score_items = [
        ReportScoreItem(
            subject=s.subject,
            score=s.score,
            letter_grade=s.letter_grade,
            grade_points=s.grade_points,
        )
        for s in student.scores
    ]

    grade_points_list = [s.grade_points for s in student.scores]
    gpa = calculate_gpa(grade_points_list)

    return StudentReportResponse(
        student_id=student.student_id,
        name=student.name,
        scores=score_items,
        gpa=gpa,
    )


def get_class_statistics(db: Session) -> ClassStatisticsResponse:
    """
    Compute per-subject statistics for the entire class (FR-5).

    For each subject, calculates:
    - Average score
    - Minimum score
    - Maximum score
    - Number of scores
    - Grade distribution (count of A, B, C, D, F)

    Args:
        db: Database session.

    Returns:
        ClassStatisticsResponse with statistics for all subjects.
    """
    # Get all distinct subjects
    subjects = db.query(Score.subject).distinct().order_by(Score.subject).all()

    subject_stats = []
    for (subject,) in subjects:
        # Aggregate stats
        stats = (
            db.query(
                func.avg(Score.score).label("average"),
                func.min(Score.score).label("min_score"),
                func.max(Score.score).label("max_score"),
                func.count(Score.id).label("count"),
            )
            .filter(Score.subject == subject)
            .first()
        )

        # Grade distribution
        scores_for_subject = (
            db.query(Score.letter_grade)
            .filter(Score.subject == subject)
            .all()
        )
        distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        for (grade,) in scores_for_subject:
            if grade in distribution:
                distribution[grade] += 1

        subject_stats.append(
            SubjectStatistics(
                subject=subject,
                average=round(float(stats.average), 2) if stats.average else 0.0,
                min_score=stats.min_score or 0,
                max_score=stats.max_score or 0,
                count=stats.count or 0,
                grade_distribution=GradeDistribution(**distribution),
            )
        )

    return ClassStatisticsResponse(subjects=subject_stats)


def get_top_performers(db: Session, limit: int = 5) -> TopPerformersResponse:
    """
    Get students ranked by highest GPA (FR-5).

    Args:
        db: Database session.
        limit: Maximum number of performers to return (default 5).

    Returns:
        TopPerformersResponse with ranked students.
    """
    # Get all students who have at least one score
    students = (
        db.query(Student)
        .join(Score, Student.student_id == Score.student_id)
        .distinct()
        .all()
    )

    # Compute GPA for each student
    performer_list = []
    for student in students:
        grade_points_list = [s.grade_points for s in student.scores]
        gpa = calculate_gpa(grade_points_list)
        performer_list.append(
            TopPerformerItem(
                student_id=student.student_id,
                name=student.name,
                gpa=gpa,
            )
        )

    # Sort by GPA descending, then by name ascending for tie-breaking
    performer_list.sort(key=lambda x: (-x.gpa, x.name))

    return TopPerformersResponse(
        top_performers=performer_list[:limit],
        limit=limit,
    )
