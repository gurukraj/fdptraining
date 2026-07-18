# Student Grade Calculator API

## What You'll Build

A RESTful API that allows a university to manage student records, record exam scores, automatically calculate letter grades and GPAs, and generate class-wide statistics and performance reports.

**Scenario:** The registrar's office needs a backend service to replace their spreadsheet-based grading workflow. The system must enforce strict validation, compute grades using a standard scale, and provide analytics endpoints for department heads.

## Technology Stack

| Component     | Technology                  |
|---------------|-----------------------------|
| Language      | Python 3.12+                |
| Framework     | FastAPI                     |
| Database      | SQLite                      |
| ORM           | SQLAlchemy                  |
| Validation    | Pydantic                    |
| Testing       | pytest                      |

## Functional Requirements

| FR-ID | Title                  | Description                                                                                  | Key Acceptance Criteria                                                             |
|-------|------------------------|----------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| FR-1  | Add Student            | Register a new student with a unique student identifier and full name.                       | `student_id` is 3-20 alphanumeric chars; `name` is 1-100 chars; duplicate `student_id` returns **409**. |
| FR-2  | Record Score           | Record an integer score (0-100) for a student in a specific subject.                         | One score per subject per student; recording auto-calculates and stores the letter grade and grade points. |
| FR-3  | Calculate Letter Grade | Derive a letter grade and grade-point value from a numeric score using the standard scale.    | Grades assigned per the scale below; stored alongside the score record.              |
| FR-4  | Calculate GPA          | Compute a student's GPA as the average of all grade-point values, rounded to 2 decimal places.| Returns `null` when the student has no recorded scores.                              |
| FR-5  | Class Report           | Generate class-wide statistics: per-subject averages, grade distribution, and top performers. | Includes average/min/max/count per subject; counts per letter grade (A/B/C/D/F); ranked list by GPA. |
| FR-6  | Reject Invalid Scores  | Return validation errors for non-integer, out-of-range, or fractional score values.           | API returns **422** for any score that is not an integer in the range 0-100.         |

## Grade Scale

| Score Range | Letter Grade | Grade Points |
|-------------|--------------|--------------|
| 90 - 100    | A            | 4.0          |
| 80 - 89     | B            | 3.0          |
| 70 - 79     | C            | 2.0          |
| 60 - 69     | D            | 1.0          |
| 0 - 59      | F            | 0.0          |

## API Endpoints Summary

| Method | Path                                | Description                                      | Success | Error Codes     |
|--------|-------------------------------------|--------------------------------------------------|---------|-----------------|
| POST   | `/api/students`                     | Register a new student                           | 201     | 400, 409, 422   |
| GET    | `/api/students`                     | List all students                                | 200     | -               |
| GET    | `/api/students/{student_id}`        | Get a single student with scores and GPA         | 200     | 404             |
| POST   | `/api/students/{student_id}/scores` | Record a score for a subject                     | 201     | 404, 409, 422   |
| GET    | `/api/students/{student_id}/report` | Get an individual student's grade report         | 200     | 404             |
| GET    | `/api/reports/class-statistics`     | Per-subject stats and grade distribution          | 200     | -               |
| GET    | `/api/reports/top-performers`       | Students ranked by GPA (optional `limit` param)  | 200     | -               |

## Data Model

### Student

| Field       | Type     | Constraints                          |
|-------------|----------|--------------------------------------|
| id          | Integer  | Primary key, auto-increment          |
| student_id  | String   | Unique, 3-20 alphanumeric characters |
| name        | String   | 1-100 characters                     |
| created_at  | DateTime | Auto-set on creation                 |

### Score

| Field        | Type     | Constraints                                |
|--------------|----------|--------------------------------------------|
| id           | Integer  | Primary key, auto-increment                |
| student_id   | Integer  | Foreign key to Student                     |
| subject      | String   | Required, non-empty                        |
| score        | Integer  | 0-100                                      |
| letter_grade | String   | Derived from score using grade scale       |
| grade_points | Float    | Derived from score using grade scale       |
| created_at   | DateTime | Auto-set on creation                       |

**Relationship:** One Student has many Scores. A student can have at most one score per subject (unique constraint on student + subject).

## Success Criteria

- All API endpoints return correct status codes and response structures.
- Duplicate `student_id` registration is rejected with 409.
- Invalid scores (non-integer, fractional, out of range) are rejected with 422.
- GPA is correctly calculated as the average of grade points, rounded to 2 decimals.
- Class statistics endpoint returns per-subject aggregates and grade distribution counts.
- Top performers endpoint returns students sorted by GPA descending.
- Application starts cleanly and creates the database schema on first run.
- Seed data can be loaded and queried successfully.
