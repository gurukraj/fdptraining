# Software Design Document: Student Grade Calculator API

| Field              | Value                                                    |
|--------------------|----------------------------------------------------------|
| **Project**        | Student Grade Calculator API                             |
| **Version**        | 1.0.0                                                    |
| **Status**         | Approved                                                 |
| **Author**         | AI-Native Software Development Workshop                  |
| **Last Updated**   | 2025-07-14                                               |
| **Technology**     | Python 3.12+, FastAPI, SQLite, Pydantic                  |
| **Target Duration**| ~1 hour (hands-on implementation)                        |

---

## Table of Contents

1. [Document Overview](#1-document-overview)
2. [Functional Requirements](#2-functional-requirements)
3. [Non-Functional Requirements](#3-non-functional-requirements)
4. [Domain Model](#4-domain-model)
5. [API Contract](#5-api-contract)
6. [Data Model](#6-data-model)
7. [Test Strategy](#7-test-strategy)
8. [Architecture](#8-architecture)
9. [Appendix](#9-appendix)

---

## 1. Document Overview

### 1.1 Purpose

This Software Design Document (SDD) serves as the secondary practical exercise for the **AI-Native Software Development** faculty workshop. It provides a specification for a Student Grade Calculator API that focuses on **business logic implementation and thorough testing** -- complementing the primary Task Management API exercise.

This lighter-weight example demonstrates how AI coding assistants excel at implementing well-defined business rules (grade calculation, GPA computation, statistical reports) when given precise specifications.

### 1.2 Scope

The system is a RESTful API that supports:

- Registering students with unique student IDs
- Recording subject scores (0-100) for each student
- Calculating letter grades based on configurable thresholds
- Computing GPA (Grade Point Average) per student
- Generating class-wide statistical reports (average, min, max per subject)

**Out of Scope:** Authentication/authorization, frontend UI, file upload/export, historical grade tracking, multi-semester support.

### 1.3 Target Audience

- Faculty members implementing the secondary workshop exercise
- Students learning specification-driven development with Python
- Developers practicing test-driven development with AI assistance

### 1.4 Technology Stack

| Layer            | Technology                  | Version   |
|------------------|-----------------------------|-----------|
| Language         | Python                      | 3.12+     |
| Framework        | FastAPI                     | 0.110+    |
| Database         | SQLite                      | 3 (built-in) |
| ORM              | SQLAlchemy                  | 2.x       |
| Validation       | Pydantic                    | 2.x       |
| Testing          | pytest, httpx               | Latest    |
| Server           | Uvicorn                     | Latest    |

### 1.5 Why This Stack

- **Zero external dependencies for the database** -- SQLite requires no installation or Docker.
- **FastAPI** provides automatic OpenAPI docs, request validation via Pydantic, and dependency injection.
- **Quick setup** -- participants can be coding within 5 minutes of cloning the repository.

---

## 2. Functional Requirements

### FR-1: Add Student

| Attribute            | Detail                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------|
| **ID**               | FR-1                                                                                    |
| **Title**            | Register a New Student                                                                  |
| **Description**      | Add a student to the system with a name and a unique student ID. The student ID is provided by the caller (e.g., university enrollment number). |
| **Priority**         | High                                                                                    |

**Acceptance Criteria:**

| # | Criterion                                                                                    |
|---|----------------------------------------------------------------------------------------------|
| 1 | A student is created when a valid `student_id` and `name` are provided.                      |
| 2 | `student_id` must be a non-empty string of 3-20 alphanumeric characters.                     |
| 3 | `name` must be a non-empty string of 1-100 characters.                                       |
| 4 | Duplicate `student_id` returns `409 Conflict`.                                               |
| 5 | Response includes the created student record with a system-generated `id`.                   |

**Edge Cases:**

- Empty or whitespace-only `student_id` returns `422 Unprocessable Entity`.
- `student_id` with special characters (e.g., "STU@123") returns `422`.
- `name` exceeding 100 characters returns `422`.

---

### FR-2: Record Score

| Attribute            | Detail                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------|
| **ID**               | FR-2                                                                                    |
| **Title**            | Record a Subject Score for a Student                                                    |
| **Description**      | Record a numerical score (0-100) for a student in a specific subject. Each student can have at most one score per subject. |
| **Priority**         | High                                                                                    |

**Acceptance Criteria:**

| # | Criterion                                                                                    |
|---|----------------------------------------------------------------------------------------------|
| 1 | A score is recorded linking a student, subject, and numerical value.                         |
| 2 | Score must be an integer between 0 and 100 (inclusive).                                      |
| 3 | Subject name must be a non-empty string of 1-100 characters.                                 |
| 4 | A student cannot have more than one score for the same subject.                              |
| 5 | Duplicate subject-student combination returns `409 Conflict`.                                |
| 6 | Non-existent `student_id` returns `404 Not Found`.                                           |
| 7 | The system automatically calculates and stores the letter grade for the score.               |

**Edge Cases:**

- Score of `-1` returns `422 Unprocessable Entity` with `"Score must be between 0 and 100"`.
- Score of `101` returns `422 Unprocessable Entity`.
- Score of `0` is valid (grade F).
- Score of `100` is valid (grade A).
- Fractional scores (e.g., `85.5`) returns `422` (integers only).

---

### FR-3: Calculate Letter Grade

| Attribute            | Detail                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------|
| **ID**               | FR-3                                                                                    |
| **Title**            | Calculate Letter Grade from Numerical Score                                             |
| **Description**      | The system converts numerical scores to letter grades using configurable thresholds. This is a core business logic function. |
| **Priority**         | High                                                                                    |

**Default Grade Thresholds:**

| Grade | Minimum Score | Maximum Score | Grade Points |
|:-----:|:------------:|:------------:|:------------:|
|   A   |      90      |     100      |     4.0      |
|   B   |      80      |      89      |     3.0      |
|   C   |      70      |      79      |     2.0      |
|   D   |      60      |      69      |     1.0      |
|   F   |       0      |      59      |     0.0      |

**Acceptance Criteria:**

| # | Criterion                                                                                    |
|---|----------------------------------------------------------------------------------------------|
| 1 | Score 90-100 maps to grade A.                                                                |
| 2 | Score 80-89 maps to grade B.                                                                 |
| 3 | Score 70-79 maps to grade C.                                                                 |
| 4 | Score 60-69 maps to grade D.                                                                 |
| 5 | Score 0-59 maps to grade F.                                                                  |
| 6 | Boundary values are correctly handled (59 -> F, 60 -> D, 89 -> B, 90 -> A).                |

**Edge Cases:**

- Score exactly at boundary (60, 70, 80, 90) returns the higher grade.
- Score of 0 returns F.
- Score of 100 returns A.

---

### FR-4: Calculate GPA

| Attribute            | Detail                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------|
| **ID**               | FR-4                                                                                    |
| **Title**            | Calculate GPA per Student                                                               |
| **Description**      | Compute the Grade Point Average for a student across all recorded subjects. GPA is the arithmetic mean of grade points for all subjects. |
| **Priority**         | High                                                                                    |

**Acceptance Criteria:**

| # | Criterion                                                                                    |
|---|----------------------------------------------------------------------------------------------|
| 1 | GPA is calculated as the average of all grade points for the student.                        |
| 2 | GPA is rounded to 2 decimal places.                                                         |
| 3 | A student with no scores has a GPA of `null` (not 0.0).                                     |
| 4 | Response includes per-subject breakdown: subject name, score, letter grade, grade points.    |

**Calculation Example:**

```
Student: Jane Doe (STU001)
  Mathematics:  85 -> B -> 3.0
  Physics:      92 -> A -> 4.0
  English:      78 -> C -> 2.0

GPA = (3.0 + 4.0 + 2.0) / 3 = 3.0
```

**Edge Cases:**

- Student with exactly one subject: GPA equals that subject's grade points.
- Student with all F grades: GPA = 0.0.
- Student with all A grades: GPA = 4.0.
- Non-existent student ID returns `404 Not Found`.

---

### FR-5: Generate Class Report

| Attribute            | Detail                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------|
| **ID**               | FR-5                                                                                    |
| **Title**            | Generate Class-Wide Statistical Report                                                  |
| **Description**      | Generate a report showing per-subject statistics across all students: average score, minimum score, maximum score, and number of students. |
| **Priority**         | Medium                                                                                  |

**Acceptance Criteria:**

| # | Criterion                                                                                    |
|---|----------------------------------------------------------------------------------------------|
| 1 | Report includes one entry per subject that has at least one recorded score.                  |
| 2 | Each entry includes: subject name, average score (2 decimal places), min score, max score, student count. |
| 3 | Average is calculated as arithmetic mean of all scores for that subject.                     |
| 4 | If no scores exist in the system, return an empty report (not an error).                     |
| 5 | Report also includes an overall class GPA (average of all students' GPAs).                   |

**Example Report:**

```json
{
  "subjects": [
    {
      "subject": "Mathematics",
      "average_score": 82.50,
      "min_score": 65,
      "max_score": 98,
      "student_count": 4
    },
    {
      "subject": "Physics",
      "average_score": 75.33,
      "min_score": 55,
      "max_score": 92,
      "student_count": 3
    }
  ],
  "class_gpa": 2.85,
  "total_students": 5
}
```

**Edge Cases:**

- Subject with only one student: min = max = average = that student's score.
- No scores recorded: return empty `subjects` array, `class_gpa: null`, `total_students: 0`.

---

### FR-6: Reject Invalid Scores

| Attribute            | Detail                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------|
| **ID**               | FR-6                                                                                    |
| **Title**            | Validate and Reject Invalid Score Entries                                               |
| **Description**      | The system performs comprehensive validation on all score submissions, rejecting invalid data with clear error messages. |
| **Priority**         | High                                                                                    |

**Acceptance Criteria:**

| # | Criterion                                                                                    |
|---|----------------------------------------------------------------------------------------------|
| 1 | Negative scores are rejected with `422` and message `"Score must be between 0 and 100"`.    |
| 2 | Scores greater than 100 are rejected with `422`.                                             |
| 3 | Non-integer scores are rejected with `422` and message `"Score must be a whole number"`.    |
| 4 | Duplicate student-subject entries are rejected with `409 Conflict`.                          |
| 5 | Missing required fields (`student_id`, `subject`, `score`) return `422`.                    |
| 6 | Non-existent student returns `404 Not Found` with `"Student not found"`.                    |

---

## 3. Non-Functional Requirements

### NFR-1: Input Validation

| Rule                                        | Implementation                              |
|---------------------------------------------|---------------------------------------------|
| All request bodies validated                | Pydantic model validation                   |
| Score range enforced (0-100)                | `Field(ge=0, le=100)` constraint            |
| String length limits enforced               | `Field(min_length=..., max_length=...)`     |
| Student ID format validated                 | Regex pattern `^[a-zA-Z0-9]{3,20}$`         |
| Type coercion disabled for score            | `strict=True` on integer fields             |

### NFR-2: Error Handling

| HTTP Status | Usage                                                  |
|-------------|--------------------------------------------------------|
| `200`       | Successful GET requests                                |
| `201`       | Successful resource creation (POST)                    |
| `404`       | Resource not found (student, score)                    |
| `409`       | Conflict (duplicate student_id, duplicate score entry) |
| `422`       | Validation error (invalid score, missing fields)       |
| `500`       | Unexpected server error                                |

**Standard Error Response Format:**

```json
{
  "detail": "Student not found",
  "error_code": "NOT_FOUND",
  "path": "/api/students/STU999/grades"
}
```

### NFR-3: Performance

| Metric            | Target            |
|-------------------|-------------------|
| API Response Time | < 100ms for all endpoints |
| Database          | SQLite (single file, no network overhead) |

### NFR-4: Code Quality

| Metric           | Target            |
|------------------|-------------------|
| Test Coverage    | > 90% for service layer |
| Type Hints       | 100% of function signatures |
| Docstrings       | All public functions |

---

## 4. Domain Model

### 4.1 Entity Descriptions

| Entity      | Description                                                        |
|-------------|--------------------------------------------------------------------|
| **Student** | A registered student with a unique student ID and name.            |
| **Subject** | An academic subject (e.g., "Mathematics", "Physics"). Created implicitly when a score is recorded. |
| **Score**   | A numerical score (0-100) linking a student to a subject, with a computed letter grade. |

### 4.2 Relationships

| Relationship         | Type        | Description                                    |
|----------------------|-------------|------------------------------------------------|
| Student -> Score     | One-to-Many | A student has zero or more scores.             |
| Subject -> Score     | One-to-Many | A subject has zero or more scores.             |
| Student <-> Subject  | Many-to-Many (via Score) | A student can be scored in many subjects; a subject can have many students. |

### 4.3 Class Diagram

```
┌──────────────────────────────────┐
│            <<enum>>              │
│          LetterGrade             │
├──────────────────────────────────┤
│  A  (grade_points: 4.0)         │
│  B  (grade_points: 3.0)         │
│  C  (grade_points: 2.0)         │
│  D  (grade_points: 1.0)         │
│  F  (grade_points: 0.0)         │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│           Student                │
├──────────────────────────────────┤
│ - id: int  (auto, PK)           │
│ - student_id: str  (unique)     │
│ - name: str                     │
│ - created_at: datetime          │
├──────────────────────────────────┤
│ + get_scores(): List[Score]     │
│ + get_gpa(): float | None       │
└──────────┬───────────────────────┘
           │ 1
           │
           │ 0..*
┌──────────┴───────────────────────┐
│            Score                 │
├──────────────────────────────────┤
│ - id: int  (auto, PK)           │
│ - student_id: int  (FK)         │
│ - subject: str                  │
│ - score: int  (0-100)           │
│ - grade: LetterGrade            │
│ - grade_points: float           │
│ - created_at: datetime          │
├──────────────────────────────────┤
│ + get_student(): Student        │
└──────────────────────────────────┘

Constraint: UNIQUE(student_id, subject)
```

### 4.4 Grade Calculation Logic (Pseudocode)

```python
def calculate_grade(score: int) -> LetterGrade:
    """
    Convert a numerical score (0-100) to a letter grade.

    Args:
        score: Integer between 0 and 100 inclusive.

    Returns:
        LetterGrade enum value.

    Raises:
        ValueError: If score is not in range [0, 100].
    """
    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100")

    if score >= 90:
        return LetterGrade.A
    elif score >= 80:
        return LetterGrade.B
    elif score >= 70:
        return LetterGrade.C
    elif score >= 60:
        return LetterGrade.D
    else:
        return LetterGrade.F


def calculate_gpa(scores: list[Score]) -> float | None:
    """
    Calculate GPA as the arithmetic mean of grade points.

    Args:
        scores: List of Score objects for a student.

    Returns:
        GPA rounded to 2 decimal places, or None if no scores.
    """
    if not scores:
        return None

    total_points = sum(s.grade_points for s in scores)
    return round(total_points / len(scores), 2)
```

---

## 5. API Contract

### 5.1 Base URL

```
http://localhost:8000/api
```

### 5.2 Common Headers

| Header          | Value                          | Required |
|-----------------|--------------------------------|----------|
| `Content-Type`  | `application/json`             | Yes (POST) |
| `Accept`        | `application/json`             | Optional |

---

### 5.3 Student Endpoints

#### 5.3.1 POST /api/students -- Add Student

| Attribute        | Value                                     |
|------------------|-------------------------------------------|
| **Method**       | `POST`                                    |
| **Path**         | `/api/students`                           |
| **Content-Type** | `application/json`                        |

**Request Body:**

```json
{
  "student_id": "STU001",
  "name": "Jane Doe"
}
```

| Field        | Type   | Required | Constraints                                  |
|--------------|--------|----------|----------------------------------------------|
| `student_id` | String | Yes      | 3-20 alphanumeric characters, unique         |
| `name`       | String | Yes      | 1-100 characters, not blank                  |

**Success Response:** `201 Created`

```json
{
  "id": 1,
  "student_id": "STU001",
  "name": "Jane Doe",
  "created_at": "2025-07-14T10:00:00.000Z"
}
```

**Error Responses:**

| Status | Condition                                 | Example Response Body                              |
|--------|-------------------------------------------|----------------------------------------------------|
| `409`  | Duplicate `student_id`                    | `{"detail": "Student ID 'STU001' already exists"}` |
| `422`  | Validation failure                        | `{"detail": "student_id must be 3-20 alphanumeric characters"}` |

---

#### 5.3.2 GET /api/students -- List Students

| Attribute        | Value                                     |
|------------------|-------------------------------------------|
| **Method**       | `GET`                                     |
| **Path**         | `/api/students`                           |

**Success Response:** `200 OK`

```json
[
  {
    "id": 1,
    "student_id": "STU001",
    "name": "Jane Doe",
    "created_at": "2025-07-14T10:00:00.000Z"
  },
  {
    "id": 2,
    "student_id": "STU002",
    "name": "John Smith",
    "created_at": "2025-07-14T10:05:00.000Z"
  }
]
```

---

### 5.4 Score Endpoints

#### 5.4.1 POST /api/scores -- Record Score

| Attribute        | Value                                     |
|------------------|-------------------------------------------|
| **Method**       | `POST`                                    |
| **Path**         | `/api/scores`                             |
| **Content-Type** | `application/json`                        |

**Request Body:**

```json
{
  "student_id": "STU001",
  "subject": "Mathematics",
  "score": 85
}
```

| Field        | Type    | Required | Constraints                              |
|--------------|---------|----------|------------------------------------------|
| `student_id` | String  | Yes      | Must reference existing student          |
| `subject`    | String  | Yes      | 1-100 characters, not blank              |
| `score`      | Integer | Yes      | 0-100 inclusive, whole numbers only       |

**Success Response:** `201 Created`

```json
{
  "id": 1,
  "student_id": "STU001",
  "subject": "Mathematics",
  "score": 85,
  "grade": "B",
  "grade_points": 3.0,
  "created_at": "2025-07-14T10:30:00.000Z"
}
```

**Error Responses:**

| Status | Condition                                 | Example Response Body                              |
|--------|-------------------------------------------|----------------------------------------------------|
| `404`  | Student not found                         | `{"detail": "Student 'STU999' not found"}`         |
| `409`  | Duplicate student-subject entry           | `{"detail": "Score for 'STU001' in 'Mathematics' already exists"}` |
| `422`  | Score out of range                        | `{"detail": "Score must be between 0 and 100"}`    |
| `422`  | Non-integer score                         | `{"detail": "Score must be a whole number"}`        |

---

### 5.5 Grade Endpoints

#### 5.5.1 GET /api/students/{student_id}/grades -- Get Student Grades & GPA

| Attribute        | Value                                     |
|------------------|-------------------------------------------|
| **Method**       | `GET`                                     |
| **Path**         | `/api/students/{student_id}/grades`       |

**Path Parameters:**

| Parameter    | Type   | Constraints                          |
|--------------|--------|--------------------------------------|
| `student_id` | String | Must reference existing student      |

**Success Response:** `200 OK`

```json
{
  "student_id": "STU001",
  "name": "Jane Doe",
  "grades": [
    {
      "subject": "Mathematics",
      "score": 85,
      "grade": "B",
      "grade_points": 3.0
    },
    {
      "subject": "Physics",
      "score": 92,
      "grade": "A",
      "grade_points": 4.0
    },
    {
      "subject": "English",
      "score": 78,
      "grade": "C",
      "grade_points": 2.0
    }
  ],
  "gpa": 3.0
}
```

**Response When Student Has No Scores:**

```json
{
  "student_id": "STU001",
  "name": "Jane Doe",
  "grades": [],
  "gpa": null
}
```

**Error Responses:**

| Status | Condition                                 | Example Response Body                              |
|--------|-------------------------------------------|----------------------------------------------------|
| `404`  | Student not found                         | `{"detail": "Student 'STU999' not found"}`         |

---

### 5.6 Report Endpoints

#### 5.6.1 GET /api/reports/class -- Get Class Report

| Attribute        | Value                                     |
|------------------|-------------------------------------------|
| **Method**       | `GET`                                     |
| **Path**         | `/api/reports/class`                      |

**Success Response:** `200 OK`

```json
{
  "subjects": [
    {
      "subject": "Mathematics",
      "average_score": 82.50,
      "min_score": 65,
      "max_score": 98,
      "student_count": 4,
      "grade_distribution": {
        "A": 1,
        "B": 2,
        "C": 0,
        "D": 1,
        "F": 0
      }
    },
    {
      "subject": "Physics",
      "average_score": 75.33,
      "min_score": 55,
      "max_score": 92,
      "student_count": 3,
      "grade_distribution": {
        "A": 1,
        "B": 0,
        "C": 1,
        "D": 0,
        "F": 1
      }
    }
  ],
  "class_gpa": 2.85,
  "total_students": 5
}
```

**Response When No Data Exists:**

```json
{
  "subjects": [],
  "class_gpa": null,
  "total_students": 0
}
```

---

## 6. Data Model

### 6.1 Entity-Relationship Diagram

```
┌──────────┐           ┌──────────┐
│ students │ 1       * │  scores  │
│          ├───────────┤          │
│          │           │          │
└──────────┘           └──────────┘
```

### 6.2 SQLite Schema

```sql
-- ============================================================
-- Table: students
-- ============================================================
CREATE TABLE students (
    id          INTEGER     PRIMARY KEY AUTOINCREMENT,
    student_id  TEXT        NOT NULL UNIQUE,
    name        TEXT        NOT NULL,
    created_at  TEXT        NOT NULL DEFAULT (datetime('now'))
);

CREATE UNIQUE INDEX idx_students_student_id ON students (student_id);

-- ============================================================
-- Table: scores
-- ============================================================
CREATE TABLE scores (
    id          INTEGER     PRIMARY KEY AUTOINCREMENT,
    student_id  INTEGER     NOT NULL REFERENCES students(id),
    subject     TEXT        NOT NULL,
    score       INTEGER     NOT NULL CHECK (score >= 0 AND score <= 100),
    grade       TEXT        NOT NULL CHECK (grade IN ('A', 'B', 'C', 'D', 'F')),
    grade_points REAL       NOT NULL CHECK (grade_points >= 0.0 AND grade_points <= 4.0),
    created_at  TEXT        NOT NULL DEFAULT (datetime('now')),

    UNIQUE (student_id, subject)
);

CREATE INDEX idx_scores_student ON scores (student_id);
CREATE INDEX idx_scores_subject ON scores (subject);
```

### 6.3 Seed Data (for Workshop)

```sql
-- Sample students
INSERT INTO students (student_id, name) VALUES
    ('STU001', 'Jane Doe'),
    ('STU002', 'John Smith'),
    ('STU003', 'Alice Johnson'),
    ('STU004', 'Bob Williams');

-- Sample scores
INSERT INTO scores (student_id, subject, score, grade, grade_points) VALUES
    (1, 'Mathematics', 85, 'B', 3.0),
    (1, 'Physics',     92, 'A', 4.0),
    (1, 'English',     78, 'C', 2.0),
    (2, 'Mathematics', 65, 'D', 1.0),
    (2, 'Physics',     55, 'F', 0.0),
    (3, 'Mathematics', 98, 'A', 4.0),
    (3, 'Physics',     88, 'B', 3.0),
    (3, 'English',     91, 'A', 4.0),
    (4, 'Mathematics', 72, 'C', 2.0);
```

---

## 7. Test Strategy

### 7.1 Testing Approach

This exercise emphasizes **test-driven development (TDD)** and thorough edge-case coverage. The grade calculation logic is an ideal candidate for unit testing due to its clear input-output mapping.

### 7.2 Coverage Target

| Layer        | Target Coverage | Focus                                      |
|--------------|:--------------:|---------------------------------------------|
| Service      |     > 95%      | Grade calculation, GPA computation, reports |
| Router       |     > 85%      | Request handling, status codes, validation  |
| **Overall**  |   **> 90%**    |                                             |

### 7.3 Unit Test Cases -- Grade Calculation

| # | Test Case                              | Input Score | Expected Grade | Expected Points |
|---|----------------------------------------|:-----------:|:--------------:|:---------------:|
| 1 | Perfect score                          |     100     |       A        |       4.0       |
| 2 | Minimum A grade                        |      90     |       A        |       4.0       |
| 3 | Maximum B grade                        |      89     |       B        |       3.0       |
| 4 | Minimum B grade                        |      80     |       B        |       3.0       |
| 5 | Maximum C grade                        |      79     |       C        |       2.0       |
| 6 | Minimum C grade                        |      70     |       C        |       2.0       |
| 7 | Maximum D grade                        |      69     |       D        |       1.0       |
| 8 | Minimum D grade                        |      60     |       D        |       1.0       |
| 9 | Maximum F grade                        |      59     |       F        |       0.0       |
| 10| Zero score                             |       0     |       F        |       0.0       |
| 11| Mid-range A                            |      95     |       A        |       4.0       |
| 12| Mid-range F                            |      30     |       F        |       0.0       |
| 13| Negative score (invalid)               |      -1     |    ValueError  |       --        |
| 14| Over-maximum score (invalid)           |     101     |    ValueError  |       --        |

### 7.4 Unit Test Cases -- GPA Calculation

| # | Test Case                              | Scores                  | Expected GPA |
|---|----------------------------------------|-------------------------|:------------:|
| 1 | Single subject (A)                     | [92]                    |     4.0      |
| 2 | Single subject (F)                     | [45]                    |     0.0      |
| 3 | Multiple subjects (mixed)              | [85, 92, 78]            |     3.0      |
| 4 | All A grades                           | [95, 91, 100]           |     4.0      |
| 5 | All F grades                           | [20, 30, 10]            |     0.0      |
| 6 | No scores (empty list)                 | []                      |    None      |
| 7 | Boundary scores                        | [60, 70, 80, 90]        |     2.5      |
| 8 | Single perfect score                   | [100]                   |     4.0      |

### 7.5 Unit Test Cases -- Class Report

| # | Test Case                              | Expected Result                              |
|---|----------------------------------------|----------------------------------------------|
| 1 | No scores exist                        | Empty subjects, class_gpa=None, total=0      |
| 2 | Single student, single subject         | One subject entry, min=max=avg               |
| 3 | Multiple students, single subject      | Correct avg, min, max, count                 |
| 4 | Multiple students, multiple subjects   | Per-subject statistics correct               |
| 5 | Grade distribution counts correct      | A/B/C/D/F counts match actual distribution   |

### 7.6 Integration Test Cases (API Layer)

| # | Test Case                                              | Endpoint                     | Expected Status |
|---|--------------------------------------------------------|------------------------------|:---------------:|
| 1 | Add student -- happy path                              | `POST /api/students`         | `201`           |
| 2 | Add student -- duplicate ID                            | `POST /api/students`         | `409`           |
| 3 | Add student -- invalid ID format                       | `POST /api/students`         | `422`           |
| 4 | Add student -- empty name                              | `POST /api/students`         | `422`           |
| 5 | List students -- returns all                           | `GET /api/students`          | `200`           |
| 6 | Record score -- happy path                             | `POST /api/scores`           | `201`           |
| 7 | Record score -- student not found                      | `POST /api/scores`           | `404`           |
| 8 | Record score -- negative score                         | `POST /api/scores`           | `422`           |
| 9 | Record score -- score > 100                            | `POST /api/scores`           | `422`           |
| 10| Record score -- duplicate entry                        | `POST /api/scores`           | `409`           |
| 11| Record score -- score = 0 (valid)                      | `POST /api/scores`           | `201`           |
| 12| Record score -- score = 100 (valid)                    | `POST /api/scores`           | `201`           |
| 13| Get grades -- student with scores                      | `GET /api/students/STU001/grades` | `200`      |
| 14| Get grades -- student with no scores                   | `GET /api/students/STU001/grades` | `200`      |
| 15| Get grades -- student not found                        | `GET /api/students/STU999/grades` | `404`      |
| 16| Class report -- with data                              | `GET /api/reports/class`     | `200`           |
| 17| Class report -- empty database                         | `GET /api/reports/class`     | `200`           |

### 7.7 Test Configuration

```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    """Create fresh tables for each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Provide a transactional database session for tests."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """Provide a test client with database override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```

---

## 8. Architecture

### 8.1 Architectural Style

The application follows a **simple layered architecture** optimized for rapid development with FastAPI's built-in dependency injection.

### 8.2 Component Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Client (Postman / cURL / Browser)                │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTP/JSON
                               v
┌─────────────────────────────────────────────────────────────────────┐
│                       FastAPI Application                           │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              Router Layer (API Endpoints)                     │  │
│  │   student_router  │  score_router  │  report_router          │  │
│  └──────────────────────────┬────────────────────────────────────┘  │
│                              │                                      │
│  ┌──────────────────────────v────────────────────────────────────┐  │
│  │              Service Layer (Business Logic)                   │  │
│  │   student_service  │  grade_service  │  report_service       │  │
│  └──────────────────────────┬────────────────────────────────────┘  │
│                              │                                      │
│  ┌──────────────────────────v────────────────────────────────────┐  │
│  │              Repository Layer (Data Access)                   │  │
│  │   student_repository  │  score_repository                    │  │
│  └──────────────────────────┬────────────────────────────────────┘  │
│                              │                                      │
└──────────────────────────────┼──────────────────────────────────────┘
                               │ SQLAlchemy
                               v
                  ┌────────────────────────┐
                  │     SQLite Database    │
                  │   (grades.db file)     │
                  └────────────────────────┘
```

### 8.3 Project Structure

```
student-grade-calculator/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app initialization
│   ├── database.py                # SQLAlchemy engine, session, Base
│   ├── models/
│   │   ├── __init__.py
│   │   ├── student.py             # Student SQLAlchemy model
│   │   └── score.py               # Score SQLAlchemy model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── student.py             # Pydantic request/response models
│   │   ├── score.py               # Pydantic request/response models
│   │   └── report.py              # Report response models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── students.py            # Student endpoints
│   │   ├── scores.py              # Score endpoints
│   │   └── reports.py             # Report endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── student_service.py     # Student business logic
│   │   ├── grade_service.py       # Grade calculation + GPA
│   │   └── report_service.py      # Report generation
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── student_repository.py  # Student data access
│   │   └── score_repository.py    # Score data access
│   └── exceptions.py              # Custom exception classes
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Fixtures: test DB, client
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_grade_service.py  # Grade calculation tests
│   │   ├── test_gpa_calculation.py# GPA computation tests
│   │   └── test_report_service.py # Report generation tests
│   └── integration/
│       ├── __init__.py
│       ├── test_students_api.py   # Student endpoint tests
│       ├── test_scores_api.py     # Score endpoint tests
│       └── test_reports_api.py    # Report endpoint tests
├── requirements.txt
├── pyproject.toml
└── README.md
```

### 8.4 Key Design Decisions

| # | Decision                                  | Rationale                                                                                     |
|---|-------------------------------------------|-----------------------------------------------------------------------------------------------|
| 1 | SQLite instead of PostgreSQL              | Zero setup overhead; ideal for a 1-hour workshop; no Docker required.                        |
| 2 | Grade calculated at write time            | Avoids recalculation on every read; grade thresholds are static for this scope.              |
| 3 | Subject created implicitly                | No separate subject management endpoints; subjects emerge from score entries.                |
| 4 | Pydantic v2 strict mode for scores        | Prevents float-to-int coercion (e.g., `85.5` must be rejected, not silently truncated).     |
| 5 | Separate service layer from routers       | Keeps business logic testable independently of HTTP framework.                               |
| 6 | `student_id` as user-provided field       | Simulates real university enrollment numbers; system `id` is auto-generated separately.     |
| 7 | FastAPI dependency injection for DB       | Clean session management; easy to override in tests.                                         |

### 8.5 FastAPI Dependency Injection

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./grades.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that provides a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
# routers/scores.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.score import ScoreCreate, ScoreResponse
from app.services.grade_service import GradeService

router = APIRouter(prefix="/api/scores", tags=["scores"])
grade_service = GradeService()


@router.post("/", response_model=ScoreResponse, status_code=status.HTTP_201_CREATED)
def record_score(score_data: ScoreCreate, db: Session = Depends(get_db)):
    """Record a score for a student in a subject."""
    return grade_service.record_score(db, score_data)
```

---

## 9. Appendix

### 9.1 Glossary

| Term              | Definition                                                             |
|-------------------|------------------------------------------------------------------------|
| **GPA**           | Grade Point Average -- the arithmetic mean of grade points across all subjects. |
| **Letter Grade**  | A categorical representation of academic performance (A, B, C, D, F). |
| **Grade Points**  | Numerical value assigned to each letter grade (A=4.0, B=3.0, C=2.0, D=1.0, F=0.0). |
| **Pydantic**      | A Python library for data validation using type annotations.           |
| **FastAPI**       | A modern Python web framework for building APIs with automatic OpenAPI documentation. |

### 9.2 Quick Start Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload --port 8000

# Test
pytest -v --cov=app --cov-report=term-missing

# View API docs
open http://localhost:8000/docs
```

### 9.3 Workshop Implementation Order

| Step | Component                     | Duration  | AI Prompt Strategy                          |
|------|-------------------------------|-----------|---------------------------------------------|
| 1    | Project setup + dependencies  | 5 min     | Provide tech stack from Section 1.4        |
| 2    | Database models (SQLAlchemy)  | 5 min     | Provide schema from Section 6             |
| 3    | Pydantic schemas              | 5 min     | Provide API contract from Section 5       |
| 4    | Grade calculation service     | 10 min    | Provide FR-3 + pseudocode from Section 4.4|
| 5    | Student & Score services      | 10 min    | Provide FR-1, FR-2 from Section 2         |
| 6    | Report service                | 10 min    | Provide FR-5 from Section 2               |
| 7    | API routers                   | 5 min     | Provide endpoints from Section 5          |
| 8    | Unit tests (grade + GPA)      | 10 min    | Provide test cases from Section 7.3-7.4   |
| 9    | Integration tests             | 5 min     | Provide test cases from Section 7.6       |
| 10   | Run and verify                | 5 min     | Use seed data from Section 6.3            |

### 9.4 Requirements File

```
# requirements.txt
fastapi==0.110.0
uvicorn[standard]==0.27.1
sqlalchemy==2.0.27
pydantic==2.6.1
httpx==0.27.0
pytest==8.0.2
pytest-cov==4.1.0
```

---

*End of Software Design Document*
