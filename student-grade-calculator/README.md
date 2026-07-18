# Student Grade Calculator API

A RESTful API for managing student records, recording scores, calculating letter grades, and generating academic reports. Built as an educational workshop project demonstrating **Spec-Driven Development (SDD)** using GitHub's open-source [speckit](https://github.com/github/speckit).

---

## Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12+ | Programming language |
| FastAPI | 0.115.x | Web framework with auto-generated API docs |
| SQLite | Built-in | Zero-config database |
| SQLAlchemy | 2.0.x | ORM with type-safe models |
| Pydantic | 2.10.x | Request/response validation |
| pytest | 8.3.x | Test framework |
| httpx | 0.28.x | HTTP test client |
| Uvicorn | 0.34.x | ASGI server |

> For a detailed explanation of each technology choice, see [TECH_STACK.md](TECH_STACK.md).

---

## Quick Start

### 1. Prerequisites

- Python 3.12 or later
- pip (Python package manager)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Seed the Database

```bash
python seed_database.py
```

This creates a `grades.db` SQLite file with 10 sample students and 50 scores.

### 4. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at **http://localhost:8000**.

### 5. Explore the API Documentation

Open your browser and navigate to:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## API Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `GET` | `/` | Health check | 200 |
| `POST` | `/api/students` | Register a new student | 201, 409, 422 |
| `GET` | `/api/students` | List students (paginated) | 200 |
| `GET` | `/api/students/{student_id}` | Get student details | 200, 404 |
| `POST` | `/api/students/{student_id}/scores` | Record a score | 201, 404, 409, 422 |
| `GET` | `/api/students/{student_id}/report` | Get student report card | 200, 404 |
| `GET` | `/api/reports/class-statistics` | Get per-subject statistics | 200 |
| `GET` | `/api/reports/top-performers` | Get top students by GPA | 200 |

---

## Grade Scale

| Letter Grade | Score Range | GPA Points |
|:------------:|:----------:|:----------:|
| A | 90 - 100 | 4.0 |
| B | 80 - 89 | 3.0 |
| C | 70 - 79 | 2.0 |
| D | 60 - 69 | 1.0 |
| F | 0 - 59 | 0.0 |

---

## Running Tests

```bash
pytest
```

For verbose output with test names:

```bash
pytest -v
```

For coverage report:

```bash
pytest --tb=short -q
```

### Test Structure

| Test File | Covers | FR |
|-----------|--------|-----|
| `test_students.py` | Student CRUD, validation, duplicates | FR-1, FR-6 |
| `test_scores.py` | Score recording, validation, duplicates | FR-2 |
| `test_grades.py` | Grade calculation, boundary values, GPA | FR-3 |
| `test_reports.py` | Report cards, class stats, top performers | FR-4, FR-5 |

---

## Project Structure

```
student-grade-calculator/
├── .speckit/
│   ├── constitution.md        # Project constitution
│   └── spec.md                # Software Design Document
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app entry point
│   ├── database.py            # SQLAlchemy engine + session
│   ├── models.py              # SQLAlchemy models (Student, Score)
│   ├── schemas.py             # Pydantic request/response schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── students.py        # Student CRUD routes
│   │   ├── scores.py          # Score recording routes
│   │   └── reports.py         # Statistics/report routes
│   └── services/
│       ├── __init__.py
│       ├── grade_service.py   # Grade calculation logic
│       └── report_service.py  # Stats computation
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Test fixtures
│   ├── test_students.py
│   ├── test_scores.py
│   ├── test_grades.py
│   └── test_reports.py
├── data/
│   └── seed_data.json         # Sample dataset (10 students)
├── seed_database.py           # Database seeding script
├── requirements.txt
├── README.md
├── TECH_STACK.md
└── SDD_EXECUTIVE_SUMMARY.md
```

---

## Example Usage

### Register a Student

```bash
curl -X POST http://localhost:8000/api/students \
  -H "Content-Type: application/json" \
  -d '{"student_id": "STU011", "name": "New Student"}'
```

### Record a Score

```bash
curl -X POST http://localhost:8000/api/students/STU001/scores \
  -H "Content-Type: application/json" \
  -d '{"subject": "Biology", "score": 87}'
```

### Get Report Card

```bash
curl http://localhost:8000/api/students/STU001/report
```

### Get Class Statistics

```bash
curl http://localhost:8000/api/reports/class-statistics
```

### Get Top Performers

```bash
curl http://localhost:8000/api/reports/top-performers?limit=3
```

---

## Spec-Driven Development

This project was built following the **SDD methodology**. For details on how the specification guided every implementation decision, see [SDD_EXECUTIVE_SUMMARY.md](SDD_EXECUTIVE_SUMMARY.md).

The speckit workflow:
1. **Spec** - Define requirements in `.speckit/spec.md`
2. **Plan** - Decompose into implementation layers
3. **Tasks** - Map FR-IDs to endpoints and tests
4. **Implement** - Build with full traceability

---

## License

This project is an educational workshop resource.
