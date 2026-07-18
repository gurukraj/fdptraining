# Software Design Document (SDD) - Student Grade Calculator API

## 1. Introduction

This document serves as the specification for the Student Grade Calculator API. It defines all functional requirements, data models, API contracts, and acceptance criteria that guide implementation.

> For the full executive summary of the SDD process, see [SDD_EXECUTIVE_SUMMARY.md](../SDD_EXECUTIVE_SUMMARY.md).

## 2. Functional Requirements

### FR-1: Add Student
- **Endpoint:** `POST /api/students`
- **Input:** `student_id` (3-20 alphanumeric), `name` (1-100 characters)
- **Success:** 201 Created with student record
- **Error:** 409 Conflict on duplicate `student_id`; 422 on validation failure

### FR-2: Record Score
- **Endpoint:** `POST /api/students/{student_id}/scores`
- **Input:** `subject` (string), `score` (integer 0-100)
- **Success:** 201 Created with score record including computed letter_grade and grade_points
- **Error:** 404 if student not found; 409 on duplicate (student_id, subject); 422 on validation failure

### FR-3: Calculate Letter Grade (Business Logic)
- A: 90-100 (4.0 GPA points)
- B: 80-89 (3.0 GPA points)
- C: 70-79 (2.0 GPA points)
- D: 60-69 (1.0 GPA points)
- F: 0-59 (0.0 GPA points)

### FR-4: Get Student Report Card
- **Endpoint:** `GET /api/students/{student_id}/report`
- **Output:** All scores, letter grades, and GPA (average of grade points, rounded to 2 decimals)
- **Error:** 404 if student not found

### FR-5: Class Statistics
- **Endpoint:** `GET /api/reports/class-statistics`
- **Output:** Per-subject statistics (average, min, max, count, grade distribution)
- **Endpoint:** `GET /api/reports/top-performers?limit=5`
- **Output:** Students ranked by highest GPA

### FR-6: List Students
- **Endpoint:** `GET /api/students` - paginated list
- **Endpoint:** `GET /api/students/{student_id}` - single student details
- **Error:** 404 if student not found

## 3. Data Models

### Student
| Column     | Type     | Constraints              |
|------------|----------|--------------------------|
| id         | INTEGER  | PK, auto-increment       |
| student_id | TEXT     | UNIQUE, NOT NULL          |
| name       | TEXT     | NOT NULL                  |
| created_at | DATETIME | DEFAULT UTC now           |

### Score
| Column       | Type    | Constraints                          |
|--------------|---------|--------------------------------------|
| id           | INTEGER | PK, auto-increment                   |
| student_id   | TEXT    | FK → Student.student_id, NOT NULL    |
| subject      | TEXT    | NOT NULL                             |
| score        | INTEGER | CHECK 0-100                          |
| letter_grade | TEXT    | Computed from score                  |
| grade_points | REAL    | Computed from letter_grade           |
| created_at   | DATETIME| DEFAULT UTC now                      |
| -            | -       | UNIQUE(student_id, subject)          |

## 4. Non-Functional Requirements
- All timestamps in UTC ISO 8601 format
- Proper HTTP status codes (200, 201, 404, 409, 422)
- Input validation via Pydantic
- OpenAPI documentation auto-generated at `/docs`
