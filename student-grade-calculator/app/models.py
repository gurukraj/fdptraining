"""
SQLAlchemy ORM models for the Student Grade Calculator.

Defines the Student and Score tables with their relationships,
constraints, and default values.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Student(Base):
    """
    Represents a student in the system.

    Attributes:
        id: Auto-generated primary key.
        student_id: Unique human-readable identifier (e.g., 'STU001').
        name: Full name of the student.
        created_at: Timestamp of when the record was created (UTC).
        scores: Relationship to the student's score records.
    """

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    scores = relationship(
        "Score", back_populates="student", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Student(student_id='{self.student_id}', name='{self.name}')>"


class Score(Base):
    """
    Represents a score record for a student in a specific subject.

    Attributes:
        id: Auto-generated primary key.
        student_id: Foreign key linking to the student.
        subject: Name of the subject.
        score: Numeric score (0-100).
        letter_grade: Computed letter grade (A, B, C, D, F).
        grade_points: Computed grade point value (0.0-4.0).
        created_at: Timestamp of when the record was created (UTC).
        student: Relationship back to the Student model.
    """

    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(
        String, ForeignKey("students.student_id"), nullable=False, index=True
    )
    subject = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    letter_grade = Column(String, nullable=False)
    grade_points = Column(Float, nullable=False)
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    student = relationship("Student", back_populates="scores")

    __table_args__ = (
        UniqueConstraint("student_id", "subject", name="uq_student_subject"),
        CheckConstraint("score >= 0 AND score <= 100", name="ck_score_range"),
    )

    def __repr__(self) -> str:
        return (
            f"<Score(student_id='{self.student_id}', "
            f"subject='{self.subject}', score={self.score})>"
        )
