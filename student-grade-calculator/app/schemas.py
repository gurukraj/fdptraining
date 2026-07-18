"""
Pydantic schemas for request/response validation and serialization.

These schemas enforce input validation rules defined in the SDD
and provide clear API contracts for all endpoints.
"""

from datetime import datetime
from pydantic import BaseModel, Field, field_validator
import re


# ─── Student Schemas ─────────────────────────────────────────────────────────


class StudentCreate(BaseModel):
    """Schema for creating a new student (FR-1)."""

    student_id: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Unique student identifier (3-20 alphanumeric characters)",
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Student's full name (1-100 characters)",
    )

    @field_validator("student_id")
    @classmethod
    def student_id_must_be_alphanumeric(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9]+$", v):
            raise ValueError("student_id must contain only alphanumeric characters")
        return v

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name must not be blank")
        return v.strip()


class StudentResponse(BaseModel):
    """Schema for student response data."""

    id: int
    student_id: str
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}


class StudentListResponse(BaseModel):
    """Schema for paginated student list."""

    students: list[StudentResponse]
    total: int
    page: int
    per_page: int


# ─── Score Schemas ────────────────────────────────────────────────────────────


class ScoreCreate(BaseModel):
    """Schema for recording a score (FR-2)."""

    subject: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Subject name",
    )
    score: int = Field(
        ...,
        ge=0,
        le=100,
        strict=True,
        description="Score value (0-100, integer only)",
    )

    @field_validator("subject")
    @classmethod
    def subject_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("subject must not be blank")
        return v.strip()


class ScoreResponse(BaseModel):
    """Schema for score response data."""

    id: int
    student_id: str
    subject: str
    score: int
    letter_grade: str
    grade_points: float
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Report Schemas ───────────────────────────────────────────────────────────


class ReportScoreItem(BaseModel):
    """A single score entry in a student's report card."""

    subject: str
    score: int
    letter_grade: str
    grade_points: float


class StudentReportResponse(BaseModel):
    """Schema for student report card (FR-4)."""

    student_id: str
    name: str
    scores: list[ReportScoreItem]
    gpa: float


class GradeDistribution(BaseModel):
    """Distribution of letter grades for a subject."""

    A: int = 0
    B: int = 0
    C: int = 0
    D: int = 0
    F: int = 0


class SubjectStatistics(BaseModel):
    """Per-subject statistics (FR-5)."""

    subject: str
    average: float
    min_score: int
    max_score: int
    count: int
    grade_distribution: GradeDistribution


class ClassStatisticsResponse(BaseModel):
    """Schema for class statistics response."""

    subjects: list[SubjectStatistics]


class TopPerformerItem(BaseModel):
    """A single entry in the top performers list."""

    student_id: str
    name: str
    gpa: float


class TopPerformersResponse(BaseModel):
    """Schema for top performers response."""

    top_performers: list[TopPerformerItem]
    limit: int
