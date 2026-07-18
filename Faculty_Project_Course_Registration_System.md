# Faculty Project: University Course Registration System

| Field              | Details                                      |
|--------------------|----------------------------------------------|
| **Project Code**   | FP-CRS-2025                                  |
| **Duration**       | 4 Weeks (1 Month)                            |
| **Team Size**      | 2-3 Faculty Members                          |
| **Methodology**    | AI-Native Software Design & Development (SDD)|
| **Architecture**   | Microservices                                |
| **Complexity**     | Intermediate-Advanced                        |

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Learning Objectives](#2-learning-objectives)
3. [System Architecture](#3-system-architecture)
4. [Technology Stack](#4-technology-stack)
5. [Functional Requirements](#5-functional-requirements)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [Data Model](#7-data-model)
8. [API Contracts](#8-api-contracts)
9. [Weekly Milestones](#9-weekly-milestones)
10. [Evaluation Rubric](#10-evaluation-rubric)
11. [Interim Review Checkpoints](#11-interim-review-checkpoints)
12. [Appendix](#12-appendix)

---

## 1. Project Overview

### 1.1 Problem Statement

Universities require a robust, scalable course registration system that handles peak-load enrollment periods where thousands of students simultaneously compete for limited seats. The system must guarantee data consistency (no over-enrollment), provide real-time seat availability, support waitlist management, and deliver notifications --- all while maintaining sub-second response times during peak load.

### 1.2 Project Scope

Design and implement a **microservices-based** University Course Registration System comprising four independently deployable services that communicate via REST APIs and asynchronous messaging. The project follows an **AI-Native SDD** methodology, leveraging AI tools for design documentation, code generation, testing, and review throughout the development lifecycle.

### 1.3 Key Challenges

- **Concurrency Control**: Multiple students enrolling in the same course section simultaneously
- **Data Consistency**: Ensuring seat counts remain accurate across distributed services
- **Waitlist Management**: Fair, automated promotion when seats become available
- **Peak Load Handling**: System must gracefully handle enrollment surge periods
- **Service Coordination**: Managing distributed transactions across microservices

---

## 2. Learning Objectives

Upon completion, faculty participants will be able to:

1. **Design** a microservices architecture with clear service boundaries and communication patterns
2. **Implement** optimistic concurrency control for high-contention resources
3. **Build** RESTful API contracts with proper error handling and validation
4. **Apply** AI-Native SDD methodology for iterative design and development
5. **Configure** containerized deployments using Docker and Docker Compose
6. **Write** comprehensive integration and concurrency tests
7. **Document** system design decisions using industry-standard SDD templates
8. **Evaluate** trade-offs between consistency, availability, and partition tolerance

---

## 3. System Architecture

### 3.1 High-Level Architecture Diagram

```
+-------------------+       +-------------------+       +---------------------+
|                   |       |                   |       |                     |
|   Web / Mobile    |       |   Admin Portal    |       |   External Systems  |
|   Client Apps     |       |                   |       |   (SIS, LMS, etc.)  |
|                   |       |                   |       |                     |
+--------+----------+       +--------+----------+       +----------+----------+
         |                           |                              |
         +---------------------------+------------------------------+
                                     |
                            +--------v--------+
                            |   API Gateway   |
                            |  (Nginx/Traefik)|
                            +--------+--------+
                                     |
         +---------------------------+------------------------------+
         |                           |                              |
+--------v----------+    +-----------v-----------+    +-------------v---------+
|                   |    |                       |    |                       |
|  Student Service  |    |  Course Catalog       |    |  Notification Service |
|  (Port 8001)      |    |  Service (Port 8002)  |    |  (Port 8004)          |
|                   |    |                       |    |                       |
|  - Authentication |    |  - Course CRUD        |    |  - Email/SMS          |
|  - Profile Mgmt   |    |  - Section Mgmt       |    |  - In-App Alerts      |
|  - Academic Hist.  |    |  - Prerequisite Chk   |    |  - Audit Logging      |
|                   |    |  - Seat Tracking       |    |                       |
+--------+----------+    +-----------+-----------+    +-------------+---------+
         |                           |                              |
         +---------------------------+------------------------------+
                                     |
                          +----------v----------+
                          |                     |
                          | Registration Engine |
                          |   (Port 8003)       |
                          |                     |
                          | - Enrollment Logic  |
                          | - Waitlist Mgmt     |
                          | - Drop Processing   |
                          | - Conflict Detection|
                          |                     |
                          +----------+----------+
                                     |
                          +----------v----------+
                          |                     |
                          |     PostgreSQL      |
                          |  (Per-Service DBs)  |
                          |                     |
                          +---------------------+
```

### 3.2 Service Decomposition

| Service                | Port  | Database Schema     | Primary Responsibility                        |
|------------------------|-------|---------------------|-----------------------------------------------|
| **Student Service**    | 8001  | `student_db`        | Authentication, profiles, academic history     |
| **Course Catalog**     | 8002  | `catalog_db`        | Course/section CRUD, prerequisites, seats      |
| **Registration Engine**| 8003  | `registration_db`   | Enrollment, waitlists, drops, conflict checks  |
| **Notification Service**| 8004 | `notification_db`   | Email, SMS, in-app notifications, audit logs   |

### 3.3 Communication Patterns

| Pattern               | Use Case                                          | Implementation              |
|-----------------------|---------------------------------------------------|-----------------------------|
| **Synchronous REST**  | Student login, course search, enrollment request  | HTTP/JSON with retries      |
| **Async Messaging**   | Enrollment confirmation, waitlist promotion        | Redis Pub/Sub or RabbitMQ   |
| **Event-Driven**      | Seat count updates, notification triggers          | Event bus with retry logic  |
| **Service Discovery** | Inter-service communication                        | Docker Compose DNS          |

### 3.4 Design Decisions

| Decision                    | Choice             | Rationale                                                  |
|-----------------------------|--------------------|------------------------------------------------------------|
| Database per service        | Yes                | Service independence, independent scaling, schema isolation|
| API Gateway                 | Nginx/Traefik      | Routing, rate limiting, SSL termination                    |
| Concurrency control         | Optimistic locking | High-read, low-write ratio; avoids lock contention         |
| Inter-service communication | REST + Events      | REST for queries, events for state changes                 |
| Containerization            | Docker Compose     | Simplified local development and testing                   |

---

## 4. Technology Stack

### 4.1 Option A: Java/Spring Boot

| Layer          | Technology                     | Version    |
|----------------|--------------------------------|------------|
| Language       | Java                           | 17+        |
| Framework      | Spring Boot                    | 3.2+       |
| API            | Spring Web (REST)              | ---        |
| Database       | PostgreSQL                     | 15+        |
| ORM            | Spring Data JPA / Hibernate    | ---        |
| Messaging      | Spring AMQP / Redis            | ---        |
| Testing        | JUnit 5, Mockito, Testcontainers | ---      |
| Containerization | Docker, Docker Compose       | ---        |
| Documentation  | SpringDoc OpenAPI              | ---        |

### 4.2 Option B: Python/FastAPI

| Layer          | Technology                     | Version    |
|----------------|--------------------------------|------------|
| Language       | Python                         | 3.12+      |
| Framework      | FastAPI                        | 0.110+     |
| API            | Uvicorn ASGI Server            | ---        |
| Database       | PostgreSQL                     | 15+        |
| ORM            | SQLAlchemy 2.0 + Alembic       | ---        |
| Messaging      | Redis (aioredis) or RabbitMQ   | ---        |
| Testing        | pytest, pytest-asyncio, httpx  | ---        |
| Containerization | Docker, Docker Compose       | ---        |
| Documentation  | FastAPI auto-generated OpenAPI | ---        |

---

## 5. Functional Requirements

### 5.1 Student Service (FR-SS-01 to FR-SS-05)

| ID        | Requirement                  | Description                                                                                                                                                                     | Priority |
|-----------|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| FR-SS-01  | Student Registration         | New students can create an account with email, name, student ID, department, and enrollment year. System validates email uniqueness and student ID format (e.g., `STU-YYYY-NNNN`). | Must     |
| FR-SS-02  | Authentication & Login       | Students authenticate using email and password. System issues JWT tokens with configurable expiry. Supports refresh token rotation.                                              | Must     |
| FR-SS-03  | Profile Management           | Students can view and update their profile information including contact details, major/minor declarations, and advisor assignment.                                               | Must     |
| FR-SS-04  | Academic Record Retrieval    | System maintains and retrieves academic history including completed courses, grades, GPA, and credit hours earned per semester.                                                   | Must     |
| FR-SS-05  | Prerequisite Eligibility     | System provides an API endpoint that returns a student's eligibility for a given course based on completed prerequisites and academic standing.                                   | Must     |

### 5.2 Course Catalog Service (FR-CC-01 to FR-CC-05)

| ID        | Requirement                  | Description                                                                                                                                                                     | Priority |
|-----------|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| FR-CC-01  | Course Management            | Administrators can create, update, and archive courses with details: code, title, description, credits, department, and prerequisite chain.                                       | Must     |
| FR-CC-02  | Section Management           | Each course can have multiple sections with attributes: instructor, schedule (days/time), location, capacity, and current enrollment count.                                       | Must     |
| FR-CC-03  | Course Search & Filtering    | Students can search courses by keyword, department, credit hours, schedule, and availability. Results support pagination and sorting.                                             | Must     |
| FR-CC-04  | Prerequisite Chain Validation| System maintains directed acyclic graph (DAG) of prerequisites and validates chains to prevent circular dependencies.                                                             | Should   |
| FR-CC-05  | Real-Time Seat Availability  | System provides real-time seat availability for each section, updated atomically when enrollments or drops occur. Supports optimistic locking via version field.                  | Must     |

### 5.3 Registration Engine (FR-RE-01 to FR-RE-05)

| ID        | Requirement                  | Description                                                                                                                                                                     | Priority |
|-----------|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| FR-RE-01  | Course Enrollment            | Students can enroll in a course section. System validates: seat availability, prerequisite completion, schedule conflicts, credit limit, and registration window.                  | Must     |
| FR-RE-02  | Waitlist Management          | When a section is full, students are added to a waitlist (FIFO). System automatically promotes waitlisted students when seats become available via drop or capacity increase.      | Must     |
| FR-RE-03  | Course Drop                  | Students can drop an enrolled course. System releases the seat, triggers waitlist promotion for the next eligible student, and updates academic records.                          | Must     |
| FR-RE-04  | Schedule Conflict Detection  | Before enrollment, system checks for time conflicts with the student's existing schedule. Detects overlapping lecture, lab, and tutorial slots.                                   | Must     |
| FR-RE-05  | Registration Window Control  | Administrators can configure registration open/close dates per semester. System enforces registration windows and supports priority registration tiers (seniors first, etc.).      | Should   |

### 5.4 Notification Service (FR-NS-01 to FR-NS-05)

| ID        | Requirement                  | Description                                                                                                                                                                     | Priority |
|-----------|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| FR-NS-01  | Enrollment Confirmation      | System sends confirmation notification (email + in-app) when a student successfully enrolls in a course section, including schedule details.                                     | Must     |
| FR-NS-02  | Waitlist Status Updates      | System notifies students of waitlist position changes and sends immediate notification when promoted from waitlist to enrolled status.                                            | Must     |
| FR-NS-03  | Drop Confirmation            | System sends confirmation when a course is dropped, including refund eligibility information based on drop date relative to semester calendar.                                    | Must     |
| FR-NS-04  | Registration Reminders       | System sends scheduled reminders before registration windows open and before add/drop deadlines, configurable per semester.                                                      | Should   |
| FR-NS-05  | Notification Preferences     | Students can configure notification channel preferences (email, SMS, in-app) and opt in/out of non-critical notifications.                                                       | Should   |

---

## 6. Non-Functional Requirements

| ID       | Category        | Requirement                                                                                                              | Target Metric                      |
|----------|-----------------|--------------------------------------------------------------------------------------------------------------------------|------------------------------------|
| NFR-01   | Concurrency     | System must handle concurrent enrollment attempts for the same section without over-enrollment                             | Zero over-enrollment incidents     |
| NFR-02   | Performance     | Course search API must respond within 500ms under normal load                                                             | p95 < 500ms                        |
| NFR-03   | Performance     | Enrollment API must complete within 2 seconds including all validations                                                   | p95 < 2000ms                       |
| NFR-04   | Throughput      | System must support at least 100 concurrent enrollment requests                                                           | 100 concurrent users               |
| NFR-05   | Security        | All API endpoints must be authenticated via JWT tokens                                                                     | 100% endpoint coverage             |
| NFR-06   | Security        | Passwords must be hashed using bcrypt with minimum 12 rounds                                                              | bcrypt cost factor >= 12           |
| NFR-07   | Security        | SQL injection prevention via parameterized queries/ORM                                                                    | Zero SQL injection vectors         |
| NFR-08   | Reliability     | System must gracefully handle individual service failures without cascading                                                | Circuit breaker pattern            |
| NFR-09   | Reliability     | All enrollment/drop operations must be idempotent                                                                          | Idempotency key support            |
| NFR-10   | Data Integrity  | Seat counts must remain consistent under concurrent operations                                                             | Optimistic locking enforcement     |
| NFR-11   | Availability    | Each microservice must have independent health check endpoints                                                             | `/health` on all services          |
| NFR-12   | Observability   | All services must produce structured JSON logs with correlation IDs                                                        | Correlation ID propagation         |
| NFR-13   | Portability     | Entire system must run via a single `docker-compose up` command                                                            | One-command deployment             |

---

## 7. Data Model

### 7.1 Student Service Database (`student_db`)

#### Table: `students`

| Column            | Type              | Constraints                            | Description                     |
|-------------------|-------------------|----------------------------------------|---------------------------------|
| `id`              | `UUID`            | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Unique student identifier      |
| `student_id`      | `VARCHAR(15)`     | `UNIQUE, NOT NULL`                     | Format: `STU-YYYY-NNNN`        |
| `email`           | `VARCHAR(255)`    | `UNIQUE, NOT NULL`                     | Institutional email             |
| `password_hash`   | `VARCHAR(255)`    | `NOT NULL`                             | bcrypt hashed password          |
| `first_name`      | `VARCHAR(100)`    | `NOT NULL`                             | Student first name              |
| `last_name`       | `VARCHAR(100)`    | `NOT NULL`                             | Student last name               |
| `department`      | `VARCHAR(100)`    | `NOT NULL`                             | Department code                 |
| `enrollment_year` | `INTEGER`         | `NOT NULL`                             | Year of enrollment              |
| `academic_standing`| `VARCHAR(20)`    | `DEFAULT 'good'`                       | good, probation, suspended      |
| `max_credits`     | `INTEGER`         | `DEFAULT 18`                           | Maximum credits per semester    |
| `created_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Account creation timestamp      |
| `updated_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Last update timestamp           |

#### Table: `academic_records`

| Column            | Type              | Constraints                            | Description                     |
|-------------------|-------------------|----------------------------------------|---------------------------------|
| `id`              | `UUID`            | `PRIMARY KEY`                          | Record identifier               |
| `student_id`      | `UUID`            | `FK -> students(id), NOT NULL`         | Reference to student            |
| `course_code`     | `VARCHAR(20)`     | `NOT NULL`                             | Completed course code           |
| `semester`        | `VARCHAR(20)`     | `NOT NULL`                             | e.g., `Fall-2024`               |
| `grade`           | `VARCHAR(5)`      | `NOT NULL`                             | Letter grade (A, B+, etc.)      |
| `credits`         | `INTEGER`         | `NOT NULL`                             | Credit hours earned             |
| `grade_points`    | `DECIMAL(3,2)`    | `NOT NULL`                             | Numeric grade points            |
| `created_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Record creation timestamp       |

**Index**: `CREATE INDEX idx_acad_records_student ON academic_records(student_id);`

### 7.2 Course Catalog Database (`catalog_db`)

#### Table: `courses`

| Column            | Type              | Constraints                            | Description                     |
|-------------------|-------------------|----------------------------------------|---------------------------------|
| `id`              | `UUID`            | `PRIMARY KEY`                          | Course identifier               |
| `course_code`     | `VARCHAR(20)`     | `UNIQUE, NOT NULL`                     | e.g., `CS-301`                  |
| `title`           | `VARCHAR(255)`    | `NOT NULL`                             | Course title                    |
| `description`     | `TEXT`            |                                        | Detailed course description     |
| `department`      | `VARCHAR(100)`    | `NOT NULL`                             | Owning department               |
| `credits`         | `INTEGER`         | `NOT NULL, CHECK(credits BETWEEN 1 AND 6)` | Credit hours              |
| `is_active`       | `BOOLEAN`         | `DEFAULT true`                         | Soft delete flag                |
| `created_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Creation timestamp              |
| `updated_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Last update timestamp           |

#### Table: `prerequisites`

| Column            | Type              | Constraints                            | Description                     |
|-------------------|-------------------|----------------------------------------|---------------------------------|
| `id`              | `UUID`            | `PRIMARY KEY`                          | Prerequisite link identifier    |
| `course_id`       | `UUID`            | `FK -> courses(id), NOT NULL`          | Course requiring prerequisite   |
| `prerequisite_id` | `UUID`            | `FK -> courses(id), NOT NULL`          | Required prerequisite course    |
| `min_grade`       | `VARCHAR(5)`      | `DEFAULT 'D'`                          | Minimum passing grade required  |

**Constraint**: `UNIQUE(course_id, prerequisite_id)` --- prevent duplicate prerequisite entries.

#### Table: `sections`

| Column              | Type              | Constraints                            | Description                        |
|---------------------|-------------------|----------------------------------------|------------------------------------|
| `id`                | `UUID`            | `PRIMARY KEY`                          | Section identifier                 |
| `course_id`         | `UUID`            | `FK -> courses(id), NOT NULL`          | Parent course                      |
| `section_number`    | `VARCHAR(10)`     | `NOT NULL`                             | e.g., `SEC-001`                    |
| `instructor_name`   | `VARCHAR(200)`    | `NOT NULL`                             | Instructor full name               |
| `schedule_days`     | `VARCHAR(20)`     | `NOT NULL`                             | e.g., `MWF`, `TR`                  |
| `schedule_time_start`| `TIME`           | `NOT NULL`                             | Class start time                   |
| `schedule_time_end` | `TIME`            | `NOT NULL`                             | Class end time                     |
| `location`          | `VARCHAR(100)`    |                                        | Building and room                  |
| `capacity`          | `INTEGER`         | `NOT NULL, CHECK(capacity > 0)`        | Maximum seats                      |
| `enrolled_count`    | `INTEGER`         | `DEFAULT 0, CHECK(enrolled_count >= 0)` | Current enrollment count          |
| `waitlist_count`    | `INTEGER`         | `DEFAULT 0`                            | Current waitlist size              |
| `semester`          | `VARCHAR(20)`     | `NOT NULL`                             | e.g., `Fall-2025`                  |
| `version`           | `INTEGER`         | `DEFAULT 1, NOT NULL`                  | **Optimistic locking version**     |
| `created_at`        | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Creation timestamp                 |
| `updated_at`        | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Last update timestamp              |

**Constraint**: `UNIQUE(course_id, section_number, semester)`
**Index**: `CREATE INDEX idx_sections_course ON sections(course_id);`
**Index**: `CREATE INDEX idx_sections_semester ON sections(semester);`

### 7.3 Registration Engine Database (`registration_db`)

#### Table: `enrollments`

| Column            | Type              | Constraints                            | Description                     |
|-------------------|-------------------|----------------------------------------|---------------------------------|
| `id`              | `UUID`            | `PRIMARY KEY`                          | Enrollment identifier           |
| `student_id`      | `UUID`            | `NOT NULL`                             | Reference to student            |
| `section_id`      | `UUID`            | `NOT NULL`                             | Reference to section            |
| `course_code`     | `VARCHAR(20)`     | `NOT NULL`                             | Denormalized for quick access   |
| `status`          | `VARCHAR(20)`     | `NOT NULL, DEFAULT 'enrolled'`         | enrolled, waitlisted, dropped   |
| `waitlist_position`| `INTEGER`        |                                        | Position if waitlisted (1-based)|
| `enrolled_at`     | `TIMESTAMPTZ`     |                                        | When enrolled (null if waitlisted)|
| `dropped_at`      | `TIMESTAMPTZ`     |                                        | When dropped (null if active)   |
| `idempotency_key` | `VARCHAR(100)`    | `UNIQUE`                               | Prevents duplicate enrollments  |
| `created_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Record creation timestamp       |
| `updated_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Last update timestamp           |

**Constraint**: `UNIQUE(student_id, section_id)` --- one enrollment per student per section.
**Index**: `CREATE INDEX idx_enrollments_student ON enrollments(student_id);`
**Index**: `CREATE INDEX idx_enrollments_section_status ON enrollments(section_id, status);`

#### Table: `registration_config`

| Column              | Type              | Constraints                          | Description                       |
|---------------------|-------------------|--------------------------------------|-----------------------------------|
| `id`                | `UUID`            | `PRIMARY KEY`                        | Configuration identifier          |
| `semester`          | `VARCHAR(20)`     | `UNIQUE, NOT NULL`                   | e.g., `Fall-2025`                 |
| `registration_start`| `TIMESTAMPTZ`    | `NOT NULL`                           | Registration window open          |
| `registration_end`  | `TIMESTAMPTZ`     | `NOT NULL`                           | Registration window close         |
| `add_drop_deadline` | `TIMESTAMPTZ`     | `NOT NULL`                           | Last date for add/drop            |
| `max_waitlist_size` | `INTEGER`         | `DEFAULT 10`                         | Max waitlist per section          |
| `priority_tiers`    | `JSONB`           | `DEFAULT '[]'`                       | Priority registration tiers       |
| `created_at`        | `TIMESTAMPTZ`     | `DEFAULT NOW()`                      | Creation timestamp                |

### 7.4 Notification Service Database (`notification_db`)

#### Table: `notifications`

| Column            | Type              | Constraints                            | Description                     |
|-------------------|-------------------|----------------------------------------|---------------------------------|
| `id`              | `UUID`            | `PRIMARY KEY`                          | Notification identifier         |
| `student_id`      | `UUID`            | `NOT NULL`                             | Recipient student               |
| `type`            | `VARCHAR(50)`     | `NOT NULL`                             | enrollment_confirm, waitlist_update, drop_confirm, reminder |
| `channel`         | `VARCHAR(20)`     | `NOT NULL`                             | email, sms, in_app              |
| `subject`         | `VARCHAR(255)`    | `NOT NULL`                             | Notification subject/title      |
| `body`            | `TEXT`            | `NOT NULL`                             | Notification content            |
| `status`          | `VARCHAR(20)`     | `DEFAULT 'pending'`                    | pending, sent, failed, read     |
| `metadata`        | `JSONB`           | `DEFAULT '{}'`                         | Additional context data         |
| `sent_at`         | `TIMESTAMPTZ`     |                                        | When notification was sent      |
| `read_at`         | `TIMESTAMPTZ`     |                                        | When notification was read      |
| `created_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Creation timestamp              |

**Index**: `CREATE INDEX idx_notifications_student ON notifications(student_id);`
**Index**: `CREATE INDEX idx_notifications_status ON notifications(status);`

---

## 8. API Contracts

### 8.1 Student Service APIs

#### POST `/api/v1/students/register`

**Description**: Register a new student account.

**Request Body**:
```json
{
  "email": "john.doe@university.edu",
  "password": "SecureP@ss123",
  "first_name": "John",
  "last_name": "Doe",
  "department": "CS",
  "enrollment_year": 2023
}
```

**Response (201 Created)**:
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "student_id": "STU-2023-0042",
  "email": "john.doe@university.edu",
  "first_name": "John",
  "last_name": "Doe",
  "department": "CS",
  "enrollment_year": 2023,
  "academic_standing": "good",
  "max_credits": 18,
  "created_at": "2025-01-15T10:30:00Z"
}
```

**Error Responses**:
| Status | Code                  | Description                        |
|--------|-----------------------|------------------------------------|
| 400    | `VALIDATION_ERROR`    | Invalid input fields               |
| 409    | `EMAIL_EXISTS`        | Email already registered           |
| 409    | `STUDENT_ID_EXISTS`   | Student ID already exists          |

#### POST `/api/v1/students/login`

**Description**: Authenticate a student and issue JWT tokens.

**Request Body**:
```json
{
  "email": "john.doe@university.edu",
  "password": "SecureP@ss123"
}
```

**Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "student": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "student_id": "STU-2023-0042",
    "email": "john.doe@university.edu",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**Error Responses**:
| Status | Code                     | Description                  |
|--------|--------------------------|------------------------------|
| 401    | `INVALID_CREDENTIALS`    | Wrong email or password      |
| 423    | `ACCOUNT_LOCKED`         | Too many failed attempts     |

### 8.2 Course Catalog Service APIs

#### GET `/api/v1/courses/search`

**Description**: Search and filter courses with pagination.

**Query Parameters**:
| Parameter      | Type     | Required | Description                        |
|----------------|----------|----------|------------------------------------|
| `keyword`      | string   | No       | Search in title and description    |
| `department`   | string   | No       | Filter by department code          |
| `credits`      | integer  | No       | Filter by credit hours             |
| `semester`     | string   | No       | Filter by semester                 |
| `available`    | boolean  | No       | Only show sections with open seats |
| `page`         | integer  | No       | Page number (default: 1)           |
| `page_size`    | integer  | No       | Results per page (default: 20)     |
| `sort_by`      | string   | No       | Sort field (default: `course_code`)|

**Response (200 OK)**:
```json
{
  "courses": [
    {
      "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "course_code": "CS-301",
      "title": "Database Systems",
      "description": "Fundamentals of database design, SQL, normalization, and transaction management.",
      "department": "CS",
      "credits": 3,
      "sections": [
        {
          "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
          "section_number": "SEC-001",
          "instructor_name": "Dr. Sarah Chen",
          "schedule": "MWF 09:00-09:50",
          "location": "Engineering Hall 201",
          "capacity": 40,
          "enrolled_count": 38,
          "waitlist_count": 2,
          "available_seats": 2,
          "semester": "Fall-2025"
        },
        {
          "id": "d4e5f6a7-b8c9-0123-defa-234567890123",
          "section_number": "SEC-002",
          "instructor_name": "Prof. Michael Rivera",
          "schedule": "TR 14:00-15:15",
          "location": "Science Building 305",
          "capacity": 35,
          "enrolled_count": 35,
          "waitlist_count": 5,
          "available_seats": 0,
          "semester": "Fall-2025"
        }
      ]
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 47,
    "total_pages": 3
  }
}
```

### 8.3 Registration Engine APIs

#### POST `/api/v1/registrations/enroll`

**Description**: Enroll a student in a course section. This is the core enrollment endpoint that orchestrates the complete registration workflow.

**Request Body**:
```json
{
  "student_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "section_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "semester": "Fall-2025",
  "idempotency_key": "enroll-a1b2c3d4-c3d4e5f6-2025-01-15T10:30:00Z"
}
```

**Processing Steps** (all must pass for successful enrollment):

| Step | Validation                     | Service Called    | Failure Response              |
|------|--------------------------------|-------------------|-------------------------------|
| 1    | Validate idempotency key       | Registration DB   | Return existing result        |
| 2    | Check registration window open | Registration DB   | `REGISTRATION_CLOSED`         |
| 3    | Verify student exists & active | Student Service   | `STUDENT_NOT_FOUND`           |
| 4    | Verify section exists & active | Course Catalog    | `SECTION_NOT_FOUND`           |
| 5    | Check prerequisite completion  | Student Service   | `PREREQUISITES_NOT_MET`       |
| 6    | Check credit limit             | Registration DB   | `CREDIT_LIMIT_EXCEEDED`       |
| 7    | Check schedule conflicts       | Registration DB   | `SCHEDULE_CONFLICT`           |
| 8    | Check seat availability        | Course Catalog    | Add to waitlist or reject     |
| 9    | Atomically enroll (with optimistic lock) | Course Catalog + Registration DB | `CONCURRENT_MODIFICATION` (retry) |

**Response (201 Created)** --- Successful Enrollment:
```json
{
  "enrollment_id": "e5f6a7b8-c9d0-1234-efab-345678901234",
  "student_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "section_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "course_code": "CS-301",
  "section_number": "SEC-001",
  "status": "enrolled",
  "enrolled_at": "2025-01-15T10:30:05Z",
  "message": "Successfully enrolled in CS-301 SEC-001",
  "schedule": {
    "days": "MWF",
    "time": "09:00-09:50",
    "location": "Engineering Hall 201"
  },
  "remaining_seats": 1,
  "current_credits": 15,
  "max_credits": 18
}
```

**Response (201 Created)** --- Added to Waitlist:
```json
{
  "enrollment_id": "f6a7b8c9-d0e1-2345-fabc-456789012345",
  "student_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "section_id": "d4e5f6a7-b8c9-0123-defa-234567890123",
  "course_code": "CS-301",
  "section_number": "SEC-002",
  "status": "waitlisted",
  "waitlist_position": 6,
  "message": "Section is full. Added to waitlist at position 6.",
  "estimated_promotion": "unlikely",
  "current_credits": 15,
  "max_credits": 18
}
```

**Error Responses**:
| Status | Code                       | Description                                  |
|--------|----------------------------|----------------------------------------------|
| 400    | `VALIDATION_ERROR`         | Missing or invalid fields                    |
| 404    | `STUDENT_NOT_FOUND`        | Student ID does not exist                    |
| 404    | `SECTION_NOT_FOUND`        | Section ID does not exist                    |
| 409    | `ALREADY_ENROLLED`         | Student already enrolled in this section     |
| 409    | `PREREQUISITES_NOT_MET`    | Student lacks required prerequisites         |
| 409    | `CREDIT_LIMIT_EXCEEDED`    | Enrollment would exceed max credit hours     |
| 409    | `SCHEDULE_CONFLICT`        | Time conflict with existing enrollment       |
| 409    | `WAITLIST_FULL`            | Section and waitlist are both at capacity    |
| 423    | `REGISTRATION_CLOSED`      | Registration window is not open              |
| 429    | `CONCURRENT_MODIFICATION`  | Optimistic lock conflict, client should retry|

#### POST `/api/v1/registrations/drop`

**Description**: Drop an enrolled course, triggering waitlist promotion.

**Request Body**:
```json
{
  "enrollment_id": "e5f6a7b8-c9d0-1234-efab-345678901234",
  "student_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "reason": "schedule_change"
}
```

**Processing Steps**:

| Step | Action                              | Description                                       |
|------|-------------------------------------|---------------------------------------------------|
| 1    | Validate enrollment exists          | Verify active enrollment record                   |
| 2    | Update enrollment status to dropped | Set `status = 'dropped'`, `dropped_at = NOW()`    |
| 3    | Decrement section enrolled_count    | Atomic decrement with optimistic locking          |
| 4    | Promote waitlisted student          | Auto-enroll next waitlisted student (FIFO)        |
| 5    | Send drop confirmation notification | Notify dropping student via Notification Service  |
| 6    | Send promotion notification         | Notify promoted student (if applicable)           |

**Response (200 OK)**:
```json
{
  "enrollment_id": "e5f6a7b8-c9d0-1234-efab-345678901234",
  "status": "dropped",
  "dropped_at": "2025-01-20T14:00:00Z",
  "course_code": "CS-301",
  "section_number": "SEC-001",
  "refund_eligible": true,
  "waitlist_promotion": {
    "promoted": true,
    "promoted_student_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    "new_waitlist_count": 1
  },
  "message": "Successfully dropped CS-301 SEC-001. Waitlist student promoted."
}
```

### 8.4 Notification Service APIs

#### GET `/api/v1/notifications/{student_id}`

**Description**: Retrieve notifications for a student.

**Query Parameters**:
| Parameter | Type    | Required | Description                          |
|-----------|---------|----------|--------------------------------------|
| `status`  | string  | No       | Filter: pending, sent, read          |
| `type`    | string  | No       | Filter by notification type          |
| `limit`   | integer | No       | Max results (default: 50)            |

**Response (200 OK)**:
```json
{
  "notifications": [
    {
      "id": "a7b8c9d0-e1f2-3456-abcd-567890123456",
      "type": "enrollment_confirm",
      "channel": "email",
      "subject": "Enrollment Confirmed: CS-301 SEC-001",
      "body": "You have been successfully enrolled in Database Systems (CS-301), Section SEC-001. Schedule: MWF 09:00-09:50, Engineering Hall 201.",
      "status": "sent",
      "sent_at": "2025-01-15T10:30:10Z",
      "read_at": null,
      "metadata": {
        "course_code": "CS-301",
        "section_number": "SEC-001",
        "enrollment_id": "e5f6a7b8-c9d0-1234-efab-345678901234"
      }
    },
    {
      "id": "b8c9d0e1-f2a3-4567-bcde-678901234567",
      "type": "waitlist_update",
      "channel": "in_app",
      "subject": "Waitlist Promotion: CS-301 SEC-002",
      "body": "Great news! A seat has opened up in Database Systems (CS-301), Section SEC-002. You have been automatically enrolled.",
      "status": "sent",
      "sent_at": "2025-01-20T14:00:15Z",
      "read_at": "2025-01-20T14:05:00Z",
      "metadata": {
        "course_code": "CS-301",
        "section_number": "SEC-002",
        "previous_waitlist_position": 1,
        "new_status": "enrolled"
      }
    }
  ],
  "total_count": 2,
  "unread_count": 0
}
```

---

## 9. Weekly Milestones

### Week 1: Foundation & Design (Days 1-5)

| Day | Deliverable                                      | AI-Native Activity                                    |
|-----|--------------------------------------------------|-------------------------------------------------------|
| 1   | Project kickoff, team formation, repo setup       | AI-assisted project scaffolding and boilerplate        |
| 2   | System architecture document (SDD Section 1-3)   | AI-generated architecture diagrams and trade-off analysis |
| 3   | Data model design, ER diagrams for all 4 services | AI-assisted schema generation and normalization review |
| 4   | API contract definitions (OpenAPI/Swagger specs)  | AI-generated API stubs and validation schemas          |
| 5   | Docker Compose setup, database initialization    | AI-assisted Dockerfile and compose configuration       |

**Review Checklist**:
- [ ] SDD document covers all 4 services with clear boundaries
- [ ] Data model supports all 20 functional requirements
- [ ] API contracts include request/response schemas and error codes
- [ ] Docker Compose starts all services and databases
- [ ] Repository follows prescribed folder structure

### Week 2: Core Implementation (Days 6-10)

| Day | Deliverable                                      | AI-Native Activity                                    |
|-----|--------------------------------------------------|-------------------------------------------------------|
| 6   | Student Service: registration, login, JWT auth    | AI pair-programming for auth flow implementation       |
| 7   | Course Catalog Service: CRUD, search, filtering   | AI-assisted query optimization and indexing            |
| 8   | Registration Engine: enrollment with concurrency  | AI-generated concurrency test scenarios                |
| 9   | Registration Engine: waitlist and drop logic       | AI-assisted state machine design and implementation    |
| 10  | Notification Service: event handling, templates    | AI-generated notification templates and event handlers |

**Review Checklist**:
- [ ] Student registration and login work end-to-end
- [ ] Course search returns paginated, filtered results
- [ ] Enrollment correctly handles optimistic locking
- [ ] Waitlist FIFO ordering is maintained
- [ ] Notifications are triggered on enrollment/drop events

### Week 3: Integration & Testing (Days 11-15)

| Day | Deliverable                                      | AI-Native Activity                                    |
|-----|--------------------------------------------------|-------------------------------------------------------|
| 11  | Inter-service communication and error handling    | AI-assisted circuit breaker and retry implementation   |
| 12  | Integration testing across service boundaries     | AI-generated integration test suites                   |
| 13  | Concurrency testing: "The Last Seat" scenario     | AI-assisted load test script generation                |
| 14  | Security hardening: input validation, auth checks | AI-assisted security audit and vulnerability scanning  |
| 15  | Performance optimization and query tuning         | AI-assisted query analysis and caching strategies      |

**Review Checklist**:
- [ ] All services communicate correctly via REST
- [ ] Integration tests cover critical enrollment flows
- [ ] "The Last Seat" test passes with zero over-enrollment
- [ ] All endpoints require authentication (except health checks)
- [ ] Response times meet NFR targets under load

### Week 4: Polish, CI/CD & Presentation (Days 16-20)

| Day | Deliverable                                      | AI-Native Activity                                    |
|-----|--------------------------------------------------|-------------------------------------------------------|
| 16  | CI/CD pipeline setup (GitHub Actions)             | AI-generated workflow configurations                   |
| 17  | API documentation and Swagger UI finalization     | AI-assisted documentation generation and review        |
| 18  | Edge case handling and error recovery testing     | AI-generated edge case test scenarios                  |
| 19  | Final SDD document update and presentation prep   | AI-assisted documentation polish and slide generation  |
| 20  | Final demo and project presentation               | AI-assisted demo script and presentation rehearsal     |

**Review Checklist**:
- [ ] CI pipeline runs tests on every push
- [ ] API documentation is complete and accurate
- [ ] Edge cases are handled gracefully
- [ ] Final SDD document is comprehensive and up-to-date
- [ ] Demo covers all key features and concurrency handling

---

## 10. Evaluation Rubric

### 10.1 Category Weights

| Category                     | Weight | Description                                         |
|------------------------------|--------|-----------------------------------------------------|
| Software Design Document     | 25%    | Architecture, data model, API contracts, decisions   |
| Code Quality & Implementation| 25%    | Clean code, patterns, concurrency, error handling    |
| Testing                      | 20%    | Unit, integration, concurrency, coverage             |
| CI/CD & DevOps               | 15%    | Pipeline, Docker, automated deployment               |
| Documentation & Presentation | 15%    | README, API docs, demo, knowledge sharing            |

### 10.2 Detailed Criteria

#### Software Design Document (25%)

| Level               | Score  | Criteria                                                                                                          |
|---------------------|--------|-------------------------------------------------------------------------------------------------------------------|
| **Excellent**       | 23-25  | Comprehensive SDD with clear architecture diagrams, complete data model, all API contracts, and well-justified design decisions. Demonstrates deep understanding of microservices patterns. |
| **Good**            | 18-22  | Complete SDD covering all sections. Minor gaps in justification or diagram clarity. Data model and APIs are functional and well-defined. |
| **Satisfactory**    | 13-17  | SDD covers essential sections but lacks depth in some areas. Data model is functional but may have normalization issues. Some API contracts incomplete. |
| **Needs Improvement**| 0-12  | SDD is incomplete or missing critical sections. Data model has significant issues. API contracts are poorly defined or missing. |

#### Code Quality & Implementation (25%)

| Level               | Score  | Criteria                                                                                                          |
|---------------------|--------|-------------------------------------------------------------------------------------------------------------------|
| **Excellent**       | 23-25  | Clean, well-structured code following SOLID principles. Proper error handling with custom exceptions. Optimistic locking correctly implemented. All 4 services functional with proper separation of concerns. |
| **Good**            | 18-22  | Code is organized and readable. Error handling covers main scenarios. Concurrency control is implemented. Most services are fully functional. |
| **Satisfactory**    | 13-17  | Code is functional but may have structural issues. Basic error handling present. Concurrency handling may have edge case gaps. |
| **Needs Improvement**| 0-12  | Code is disorganized or incomplete. Missing error handling. No concurrency control. Multiple services non-functional. |

#### Testing (20%)

| Level               | Score  | Criteria                                                                                                          |
|---------------------|--------|-------------------------------------------------------------------------------------------------------------------|
| **Excellent**       | 18-20  | Comprehensive test suite with unit, integration, and concurrency tests. "The Last Seat" test implemented and passing. Code coverage > 80%. Edge cases covered. |
| **Good**            | 14-17  | Good test coverage for main flows. Integration tests for cross-service communication. Some concurrency testing. Coverage > 60%. |
| **Satisfactory**    | 10-13  | Basic unit tests for core functionality. Some integration tests. Limited concurrency testing. Coverage > 40%. |
| **Needs Improvement**| 0-9   | Minimal or no tests. No integration testing. No concurrency testing. Coverage < 40%. |

#### CI/CD & DevOps (15%)

| Level               | Score  | Criteria                                                                                                          |
|---------------------|--------|-------------------------------------------------------------------------------------------------------------------|
| **Excellent**       | 14-15  | Full CI/CD pipeline with automated testing, linting, and build. Docker Compose for all services. Health checks configured. Environment-based configuration. |
| **Good**            | 11-13  | CI pipeline runs tests on push. Docker Compose works for all services. Basic health checks present. |
| **Satisfactory**    | 8-10   | Basic CI pipeline exists. Docker Compose mostly works. Some manual steps required. |
| **Needs Improvement**| 0-7   | No CI/CD pipeline. Docker setup incomplete or non-functional. Manual deployment only. |

#### Documentation & Presentation (15%)

| Level               | Score  | Criteria                                                                                                          |
|---------------------|--------|-------------------------------------------------------------------------------------------------------------------|
| **Excellent**       | 14-15  | Comprehensive README with setup instructions. Interactive API docs (Swagger). Clear demo covering all features. Effective knowledge sharing of AI-Native methodology. |
| **Good**            | 11-13  | Good README with setup steps. API documentation available. Demo covers main features. Some discussion of AI-Native approach. |
| **Satisfactory**    | 8-10   | Basic README present. Some API documentation. Demo covers basic flow. Limited methodology discussion. |
| **Needs Improvement**| 0-7   | Missing or inadequate README. No API documentation. Demo is incomplete or non-functional. |

---

## 11. Interim Review Checkpoints

### Checkpoint 1: Architecture Review (End of Day 3)

**Demo Script**:
1. Present system architecture diagram and explain service boundaries
2. Walk through data model for each service
3. Explain communication patterns and trade-offs
4. Show Docker Compose configuration

**Key Questions**:
- Why did you choose these specific service boundaries?
- How does the data model support concurrent enrollment?
- What happens if the Notification Service is down during enrollment?
- How do you prevent circular prerequisites in the course catalog?

### Checkpoint 2: Core Services Demo (End of Day 10)

**Demo Script**:
1. Register a student and authenticate via JWT
2. Search courses and view section availability
3. Enroll in a course and show seat count update
4. Demonstrate waitlist addition when section is full
5. Show notification triggered by enrollment

**Key Questions**:
- Walk through the enrollment flow step by step
- How does optimistic locking work in your implementation?
- What happens if two students try to take the last seat simultaneously?
- Show the idempotency key handling for duplicate requests

### Checkpoint 3: Integration & Testing Review (End of Day 15)

**Demo Script**:
1. Run the complete integration test suite
2. Execute "The Last Seat" concurrency test
3. Show error handling for service failures
4. Demonstrate security controls (unauthorized access attempts)

**Key Questions**:
- How many concurrent enrollment requests can your system handle?
- Show me the concurrency test results --- any over-enrollment?
- What is your test coverage percentage?
- How do you handle partial failures in the enrollment flow?

### Checkpoint 4: Final Review & Presentation (Day 20)

**Demo Script**:
1. Full end-to-end demo: student journey from registration to enrollment
2. Show CI/CD pipeline execution
3. Present API documentation (Swagger UI)
4. Demonstrate system resilience (stop a service, show graceful degradation)
5. Present final SDD document and lessons learned

**Key Questions**:
- What was the most challenging technical problem you solved?
- How did AI-Native methodology impact your development process?
- What would you change if you had another month?
- How would this system scale to handle 10,000 concurrent users?

---

## 12. Appendix

### A. Repository Structure

```
course-registration-system/
+-- README.md
+-- docker-compose.yml
+-- .github/
|   +-- workflows/
|       +-- ci.yml
+-- docs/
|   +-- SDD.md
|   +-- architecture-diagrams/
|   +-- api-contracts/
+-- services/
|   +-- student-service/
|   |   +-- src/
|   |   |   +-- main/
|   |   |   |   +-- models/
|   |   |   |   +-- routes/  (or controllers/)
|   |   |   |   +-- services/
|   |   |   |   +-- schemas/
|   |   |   |   +-- config/
|   |   |   |   +-- main.py  (or Application.java)
|   |   |   +-- test/
|   |   +-- Dockerfile
|   |   +-- requirements.txt  (or pom.xml)
|   +-- course-catalog-service/
|   |   +-- src/
|   |   |   +-- main/
|   |   |   +-- test/
|   |   +-- Dockerfile
|   +-- registration-engine/
|   |   +-- src/
|   |   |   +-- main/
|   |   |   +-- test/
|   |   +-- Dockerfile
|   +-- notification-service/
|       +-- src/
|       |   +-- main/
|       |   +-- test/
|       +-- Dockerfile
+-- scripts/
|   +-- seed-data.sql
|   +-- run-tests.sh
|   +-- load-test.py
+-- shared/
    +-- common-models/
    +-- utils/
```

### B. Seed Data Recommendations

| Entity           | Recommended Count | Notes                                              |
|------------------|-------------------|-----------------------------------------------------|
| Students         | 50-100            | Mix of departments and enrollment years              |
| Courses          | 20-30             | Across 4-5 departments with prerequisite chains      |
| Sections         | 40-60             | 2-3 sections per course, varying capacities (10-50)  |
| Academic Records | 200-400           | Prerequisite completion data for enrollment testing   |
| Semesters        | 2-3               | Current + past semesters for historical data         |

**Seed Data Tips**:
- Include at least one course with a 3-level prerequisite chain (e.g., CS-101 -> CS-201 -> CS-301)
- Create sections with very low capacity (5-10) to easily test "last seat" scenarios
- Include students at various credit limits to test credit limit validation
- Pre-populate some enrollments to test schedule conflict detection

### C. Concurrency Testing: "The Last Seat" Test

**Objective**: Verify that when only one seat remains in a section, and N students attempt to enroll simultaneously, exactly one succeeds and the rest are either waitlisted or rejected.

**Test Approach**:

```python
"""
The Last Seat Test - Concurrency Validation

Setup:
  - Create a section with capacity = 1
  - Create 10 students, all meeting prerequisites
  - Ensure registration window is open

Execution:
  - Launch 10 concurrent enrollment requests (one per student)
  - Use threading or asyncio to maximize concurrency

Assertions:
  - Exactly 1 enrollment with status = 'enrolled'
  - Exactly 9 enrollments with status = 'waitlisted' or rejected
  - Section enrolled_count == 1 (never exceeds capacity)
  - No database integrity violations
"""

import asyncio
import httpx

async def the_last_seat_test():
    section_id = "test-section-with-1-seat"
    students = [f"student-{i}" for i in range(10)]

    async with httpx.AsyncClient() as client:
        tasks = [
            client.post(
                "http://localhost:8003/api/v1/registrations/enroll",
                json={
                    "student_id": sid,
                    "section_id": section_id,
                    "semester": "Fall-2025",
                    "idempotency_key": f"test-{sid}-{section_id}"
                }
            )
            for sid in students
        ]
        responses = await asyncio.gather(*tasks)

    enrolled = sum(1 for r in responses if r.json().get("status") == "enrolled")
    waitlisted = sum(1 for r in responses if r.json().get("status") == "waitlisted")

    assert enrolled == 1, f"Expected 1 enrolled, got {enrolled}"
    assert waitlisted <= 9, f"Unexpected waitlist count: {waitlisted}"
    print(f"PASS: {enrolled} enrolled, {waitlisted} waitlisted")

asyncio.run(the_last_seat_test())
```

### D. Development Workflow

```
1. Design Phase (AI-Native)
   +-- Use AI to generate initial SDD draft
   +-- Review and refine architecture decisions
   +-- AI-assisted API contract generation
   +-- Peer review of design documents

2. Implementation Phase (AI Pair Programming)
   +-- AI generates boilerplate and scaffolding
   +-- Developer implements business logic with AI assistance
   +-- AI-generated unit tests for each component
   +-- Continuous code review with AI feedback

3. Testing Phase (AI-Augmented)
   +-- AI generates integration test scenarios
   +-- AI-assisted concurrency test design
   +-- AI-generated edge case identification
   +-- Automated test execution in CI pipeline

4. Review Phase (AI-Enhanced)
   +-- AI-assisted code review for patterns and anti-patterns
   +-- AI-generated documentation updates
   +-- AI-assisted presentation preparation
   +-- Reflective analysis of AI-Native methodology effectiveness
```

### E. Technical Challenges & Hints

| Challenge                        | Hint                                                                                                      |
|----------------------------------|-----------------------------------------------------------------------------------------------------------|
| Optimistic locking implementation| Use a `version` column. On UPDATE, include `WHERE version = :expected_version`. If 0 rows updated, throw conflict error and retry. |
| Waitlist FIFO ordering           | Use `created_at` timestamp or explicit `waitlist_position` column. On promotion, select `MIN(waitlist_position)` with `status = 'waitlisted'`. |
| Schedule conflict detection      | Compare time ranges: conflict exists if `start_a < end_b AND start_b < end_a` for overlapping days.       |
| JWT token management             | Store refresh tokens in database. Implement token rotation on refresh. Set short access token expiry (15-60 min). |
| Idempotency handling             | Use client-generated idempotency key. Store in enrollments table with UNIQUE constraint. On duplicate, return original result. |
| Cross-service data consistency   | Use eventual consistency with event-driven updates. Implement compensating transactions for rollback scenarios. |
| Docker networking                | Use Docker Compose service names as hostnames (e.g., `http://student-service:8001`). Define a shared network. |
| Database migrations              | Use Alembic (Python) or Flyway (Java) for versioned migrations. Never modify production schemas directly. |
| Circular prerequisite prevention | Implement DFS/BFS cycle detection when adding prerequisites. Reject additions that would create cycles.   |
| Rate limiting                    | Implement per-student rate limiting on enrollment endpoint to prevent abuse during peak registration.       |

### F. Reference Materials

- **Microservices Patterns** by Chris Richardson --- Service decomposition, saga pattern, API gateway
- **Designing Data-Intensive Applications** by Martin Kleppmann --- Concurrency, consistency, distributed systems
- **Building Microservices** by Sam Newman --- Service boundaries, communication patterns
- **FastAPI Documentation**: https://fastapi.tiangolo.com/ --- Async endpoints, dependency injection
- **Spring Boot Reference**: https://spring.io/projects/spring-boot --- Auto-configuration, Spring Data JPA
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/ --- Locking, indexing, performance tuning
- **Docker Compose Docs**: https://docs.docker.com/compose/ --- Multi-container orchestration
- **OpenAPI Specification**: https://swagger.io/specification/ --- API contract standards

---

*Document Version: 1.0 | Project Code: FP-CRS-2025 | Methodology: AI-Native SDD*
*Last Updated: 2025-01-15*
