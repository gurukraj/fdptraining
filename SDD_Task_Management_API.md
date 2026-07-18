# Software Design Document: Task Management REST API

| Field              | Value                                                    |
|--------------------|----------------------------------------------------------|
| **Project**        | Task Management REST API                                 |
| **Version**        | 1.0.0                                                    |
| **Status**         | Approved                                                 |
| **Author**         | AI-Native Software Development Workshop                  |
| **Last Updated**   | 2025-07-14                                               |
| **Technology**     | Java 21, Spring Boot 3.x, PostgreSQL 16, Docker          |
| **Target Duration**| 1-2 hours (hands-on implementation)                      |

---

## Table of Contents

1. [Document Overview](#1-document-overview)
2. [Functional Requirements](#2-functional-requirements)
3. [Non-Functional Requirements](#3-non-functional-requirements)
4. [Actors & Permissions](#4-actors--permissions)
5. [Domain Model](#5-domain-model)
6. [API Contract](#6-api-contract)
7. [Data Model](#7-data-model)
8. [Architecture](#8-architecture)
9. [Test Strategy](#9-test-strategy)
10. [CI/CD Pipeline](#10-cicd-pipeline)
11. [Security Considerations](#11-security-considerations)
12. [Appendix](#12-appendix)

---

## 1. Document Overview

### 1.1 Purpose

This Software Design Document (SDD) serves as the primary hands-on practical exercise for the **AI-Native Software Development** faculty workshop. It provides a complete, industry-standard specification for a Task Management REST API that participants will implement using AI-assisted development tools within a 1-2 hour session.

The document demonstrates how a well-structured SDD enables AI coding assistants to generate accurate, production-quality code -- a core tenet of the AI-Native development methodology.

### 1.2 Scope

The system is a RESTful API that supports full task lifecycle management including:

- Creating, reading, updating, and deleting tasks (CRUD)
- Organizing tasks by categories
- Adding comments to tasks for collaboration
- Filtering and paginating task lists
- Role-based access control (Admin vs. User)
- Audit logging for all write operations

**Out of Scope:** Frontend/UI, email notifications, file attachments, real-time WebSocket updates, multi-tenancy.

### 1.3 Target Audience

- Faculty members attending the AI-Native Software Development workshop
- Graduate and post-graduate students studying software engineering
- Developers learning specification-driven, AI-assisted development

### 1.4 Technology Stack

| Layer            | Technology                       | Version  |
|------------------|----------------------------------|----------|
| Language         | Java                             | 21 (LTS) |
| Framework        | Spring Boot                      | 3.x      |
| Database         | PostgreSQL                       | 16       |
| ORM              | Spring Data JPA / Hibernate      | 6.x      |
| Build Tool       | Maven                            | 3.9+     |
| Containerization | Docker + Docker Compose          | 24+      |
| API Documentation| SpringDoc OpenAPI (Swagger)      | 2.x      |
| Testing          | JUnit 5, Mockito, Testcontainers | Latest   |
| Security         | Spring Security + JWT            | 6.x      |

### 1.5 Conventions

- All timestamps are in **UTC** and formatted as ISO 8601 (`yyyy-MM-dd'T'HH:mm:ss.SSS'Z'`).
- All API responses use **JSON** (`application/json`).
- Pagination follows Spring Data conventions (`page`, `size`, `sort`).
- Soft-deleted records are excluded from all GET queries unless explicitly requested.

---

## 2. Functional Requirements

### FR-1: Create Task

| Attribute            | Detail                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------|
| **ID**               | FR-1                                                                                    |
| **Title**            | Create a New Task                                                                       |
| **Description**      | Users can create a new task by providing a title, optional description, priority, and category. The system assigns default status `OPEN` and records the creating user. |
| **Priority**         | High                                                                                    |

**Acceptance Criteria:**

| # | Criterion                                                                                    |
|---|----------------------------------------------------------------------------------------------|
| 1 | A task is created with status `OPEN` when a valid request is submitted.                      |
| 2 | The response includes the generated task ID and creation timestamp.                          |
| 3 | Title is mandatory and must be between 3 and 200 characters.                                 |
| 4 | Description is optional and limited to 2000 characters.                                      |
| 5 | Priority must be one of: `LOW`, `MEDIUM`, `HIGH`. Defaults to `MEDIUM` if omitted.          |
| 6 | Category ID is optional. If provided, the category must exist; otherwise, return `400`.      |
| 7 | `created_by` is set automatically from the authenticated user's context.                     |

**Edge Cases:**

- Empty or whitespace-only title returns `400 Bad Request`.
- Title exceeding 200 characters returns `400 Bad Request` with a validation message.
- Non-existent category ID returns `400 Bad Request` with message `"Category not found"`.
- Unauthenticated request returns `401 Unauthorized`.

---

### FR-2: View Tasks with Filtering

| Attribute            | Detail                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------|
| **ID**               | FR-2                                                                                    |
| **Title**            | List and Filter Tasks                                                                   |
| **Description**      | Users can retrieve a paginated list of tasks with optional filters for status, priority, and category. Soft-deleted tasks are excluded by default. |
| **Priority**         | High                                                                                    |

**Acceptance Criteria:**

| # | Criterion                                                                                    |
|---|----------------------------------------------------------------------------------------------|
| 1 | Returns a paginated list of tasks sorted by `created_at` descending by default.              |
| 2 | Supports filtering by `status` (e.g., `?status=OPEN`).                                      |
| 3 | Supports filtering by `priority` (e.g., `?priority=HIGH`).                                  |
| 4 | Supports filtering by `categoryId` (e.g., `?categoryId=5`).                                 |
| 5 | Multiple filters can be combined (AND logic).                                                |
| 6 | Default page size is 20; maximum page size is 100.                                           |
| 7 | Soft-deleted tasks (`deleted = true`) are excluded from results.                             |
| 8 | Response includes pagination metadata: `totalElements`, `totalPages`, `currentPage`, `size`. |

**Edge Cases:**

- Invalid `status` or `priority` value returns `400 Bad Request`.
- Negative `page` or `size` values are normalized to defaults (page=0, size=20).
- `size` exceeding 100 is capped at 100.
- An empty result set returns `200 OK` with an empty `content` array (not `404`).

---

### FR-3: Update Task

| Attribute            | Detail                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------|
| **ID**               | FR-3                                                                                    |
| **Title**            | Update Task Status and Details                                                          |
| **Description**      | Users can update the title, description, priority, status, and category of an existing task. Status transitions are validated. |
| **Priority**         | High                                                                                    |

**Acceptance Criteria:**

| # | Criterion                                                                                    |
|---|----------------------------------------------------------------------------------------------|
| 1 | Only the fields provided in the request body are updated (partial update via PUT).           |
| 2 | Valid status transitions: `OPEN -> IN_PROGRESS`, `IN_PROGRESS -> DONE`, `IN_PROGRESS -> OPEN`, `DONE -> OPEN`. |
| 3 | Invalid status transitions return `400 Bad Request` with an explanatory message.             |
| 4 | `updated_at` timestamp is refreshed on every successful update.                             |
| 5 | Users can only update their own tasks; Admins can update any task.                           |
| 6 | Updating a soft-deleted task returns `404 Not Found`.                                       |

**Valid Status Transitions:**

```
  OPEN ──────────> IN_PROGRESS
   ^                    │
   │                    v
   └──── DONE <────────┘
```

**Edge Cases:**

- Attempting `OPEN -> DONE` directly returns `400` with `"Invalid status transition"`.
- Non-existent task ID returns `404 Not Found`.
- Non-owner (non-admin) attempting update returns `403 Forbidden`.

---

### FR-4: Delete Task (Soft Delete)

| Attribute            | Detail                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------|
| **ID**               | FR-4                                                                                    |
| **Title**            | Soft Delete a Task                                                                      |
| **Description**      | Tasks are soft-deleted by setting a `deleted` flag and `deleted_at` timestamp. The record is retained for audit purposes but excluded from normal queries. |
| **Priority**         | Medium                                                                                  |

**Acceptance Criteria:**

| # | Criterion                                                                                    |
|---|----------------------------------------------------------------------------------------------|
| 1 | Soft delete sets `deleted = true` and records `deleted_at` timestamp.                        |
| 2 | The API returns `204 No Content` on successful deletion.                                     |
| 3 | Subsequent GET requests for the deleted task return `404 Not Found`.                         |
| 4 | Users can only delete their own tasks; Admins can delete any task.                           |
| 5 | Deleting an already-deleted task returns `404 Not Found`.                                    |
| 6 | An audit log entry is created recording the deletion event.                                  |

**Edge Cases:**

- Deleting a task with existing comments also soft-deletes associated comments.
- Non-existent task ID returns `404 Not Found`.
- Non-owner (non-admin) attempting delete returns `403 Forbidden`.

---

### FR-5: Task Categories

| Attribute            | Detail                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------|
| **ID**               | FR-5                                                                                    |
| **Title**            | Organize Tasks by Category                                                              |
| **Description**      | Tasks can be assigned to categories (e.g., "Bug", "Feature", "Research"). Categories are managed by Admins and referenced by Users when creating/updating tasks. |
| **Priority**         | Medium                                                                                  |

**Acceptance Criteria:**

| # | Criterion                                                                                    |
|---|----------------------------------------------------------------------------------------------|
| 1 | Admins can create categories with a unique name (3-100 characters).                          |
| 2 | Admins can list, update, and delete categories.                                              |
| 3 | Deleting a category with associated tasks returns `409 Conflict`.                            |
| 4 | Category names are case-insensitive unique (e.g., "Bug" and "bug" are duplicates).           |
| 5 | Users can list categories but cannot create, update, or delete them.                         |

**Edge Cases:**

- Duplicate category name returns `409 Conflict` with `"Category already exists"`.
- Empty or whitespace-only name returns `400 Bad Request`.

---

### FR-6: Task Comments

| Attribute            | Detail                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------|
| **ID**               | FR-6                                                                                    |
| **Title**            | Add Comments to Tasks                                                                   |
| **Description**      | Any authenticated user can add comments to any (non-deleted) task. Comments are immutable after creation. |
| **Priority**         | Medium                                                                                  |

**Acceptance Criteria:**

| # | Criterion                                                                                    |
|---|----------------------------------------------------------------------------------------------|
| 1 | Comments are created with a text body (1-1000 characters) linked to a task and author.       |
| 2 | Comments list is paginated and sorted by `created_at` ascending.                             |
| 3 | Comment author is set from the authenticated user context.                                   |
| 4 | Adding a comment to a deleted task returns `404 Not Found`.                                  |
| 5 | Comments cannot be edited or deleted by Users; Admins can delete comments.                   |

**Edge Cases:**

- Empty comment body returns `400 Bad Request`.
- Comment body exceeding 1000 characters returns `400 Bad Request`.
- Non-existent task ID returns `404 Not Found`.

---

### FR-7: Duplicate Title Validation

| Attribute            | Detail                                                                                  |
|----------------------|-----------------------------------------------------------------------------------------|
| **ID**               | FR-7                                                                                    |
| **Title**            | Reject Duplicate Task Titles Within Same Category                                       |
| **Description**      | The system rejects task creation or update if an active (non-deleted) task with the same title already exists within the same category. |
| **Priority**         | Low                                                                                     |

**Acceptance Criteria:**

| # | Criterion                                                                                    |
|---|----------------------------------------------------------------------------------------------|
| 1 | Duplicate title check is case-insensitive.                                                   |
| 2 | Only non-deleted tasks are considered for duplication.                                        |
| 3 | Tasks in different categories may have the same title.                                       |
| 4 | Tasks with no category (null) are treated as a single group for duplication check.           |
| 5 | Returns `409 Conflict` with message `"A task with this title already exists in the category"`.|

**Edge Cases:**

- Renaming a task to its own current title is allowed (no self-conflict).
- A soft-deleted task's title can be reused immediately.

---

## 3. Non-Functional Requirements

### NFR-1: Performance

| Attribute    | Requirement                                           |
|--------------|-------------------------------------------------------|
| **P95 Latency** | API response time < 200ms at the 95th percentile  |
| **P99 Latency** | API response time < 500ms at the 99th percentile  |
| **Throughput**   | Minimum 100 requests/second sustained              |

**Implementation Notes:**
- Database queries must use indexed columns for filtering.
- Pagination prevents full-table scans.
- Connection pooling via HikariCP (default Spring Boot pool).

### NFR-2: Scalability

| Attribute          | Requirement                                       |
|--------------------|---------------------------------------------------|
| **Concurrent Users** | Support 50 concurrent users minimum             |
| **Database Connections** | HikariCP pool size: 10 (min) to 20 (max)   |
| **Payload Limit**  | Maximum request body size: 1 MB                   |

### NFR-3: Input Validation

| Rule                                   | Implementation                                     |
|----------------------------------------|----------------------------------------------------|
| All string fields trimmed              | Custom `@Trimmed` annotation or `StringTrimmerEditor` |
| No HTML/script tags in text fields     | Jakarta `@Pattern` validation                      |
| Enum fields validated against allowed values | Custom validator or `@ValidEnum`              |
| Path variables validated as positive integers | `@Positive` constraint                       |
| Request body validated before processing | `@Valid` on controller method parameters          |

### NFR-4: Role-Based Access Control

| Role    | Permissions                                                          |
|---------|----------------------------------------------------------------------|
| `ADMIN` | Full CRUD on all tasks, manage categories, delete any comment, manage users |
| `USER`  | CRUD own tasks, view all tasks, add comments, view categories        |

**Enforcement:** Spring Security `@PreAuthorize` annotations at the service layer.

### NFR-5: Audit Logging

| Event          | Logged Fields                                                     |
|----------------|-------------------------------------------------------------------|
| Task Created   | `task_id`, `user_id`, `timestamp`, `action=CREATE`                |
| Task Updated   | `task_id`, `user_id`, `timestamp`, `action=UPDATE`, `changed_fields` |
| Task Deleted   | `task_id`, `user_id`, `timestamp`, `action=DELETE`                |
| Comment Added  | `comment_id`, `task_id`, `user_id`, `timestamp`, `action=COMMENT` |

**Implementation:** JPA `@EntityListeners` with an `AuditListener` class writing to an `audit_log` table.

---

## 4. Actors & Permissions

### 4.1 Permission Matrix

| Resource / Action        | Admin | User (Own) | User (Others) |
|--------------------------|:-----:|:----------:|:-------------:|
| Create Task              |  Yes  |    Yes     |      --       |
| View Task                |  Yes  |    Yes     |     Yes       |
| Update Task              |  Yes  |    Yes     |      No       |
| Delete Task              |  Yes  |    Yes     |      No       |
| Create Category          |  Yes  |     No     |      No       |
| Update Category          |  Yes  |     No     |      No       |
| Delete Category          |  Yes  |     No     |      No       |
| View Categories          |  Yes  |    Yes     |     Yes       |
| Add Comment              |  Yes  |    Yes     |     Yes       |
| Delete Comment           |  Yes  |     No     |      No       |
| View Audit Logs          |  Yes  |     No     |      No       |

---

## 5. Domain Model

### 5.1 Entity Descriptions

| Entity     | Description                                                         |
|------------|---------------------------------------------------------------------|
| **Task**   | Core entity representing a unit of work with title, description, priority, and status. Belongs to an optional category and is owned by a user. |
| **User**   | Represents an authenticated user of the system. Has a role (ADMIN or USER). |
| **Category** | A label used to organize tasks (e.g., "Bug", "Feature", "Research"). Managed by Admins. |
| **Comment** | A textual note attached to a task by any authenticated user. Immutable after creation. |
| **AuditLog** | System-generated record of every write operation for traceability. |

### 5.2 Relationships

| Relationship            | Type        | Description                                    |
|-------------------------|-------------|------------------------------------------------|
| User -> Task            | One-to-Many | A user owns zero or more tasks.                |
| Category -> Task        | One-to-Many | A category contains zero or more tasks.        |
| Task -> Comment         | One-to-Many | A task has zero or more comments.              |
| User -> Comment         | One-to-Many | A user authors zero or more comments.          |

### 5.3 Valid Status Transitions

```
  OPEN ──────────> IN_PROGRESS
   ^                    │
   │                    v
   └──── DONE <────────┘
```

---

## 6. API Contract

### 6.1 Base URL

```
http://localhost:8080/api
```

### 6.2 Common Headers

| Header          | Value                          | Required |
|-----------------|--------------------------------|----------|
| `Content-Type`  | `application/json`             | Yes (POST/PUT) |
| `Authorization` | `Bearer <jwt_token>`           | Yes      |
| `Accept`        | `application/json`             | Optional |

### 6.3 Common Error Response

```json
{
  "timestamp": "2025-07-14T10:30:00.000Z",
  "status": 400,
  "error": "Bad Request",
  "message": "Validation failed",
  "details": [
    {
      "field": "title",
      "message": "Title must be between 3 and 200 characters"
    }
  ],
  "path": "/api/tasks"
}
```

---

### 6.4 Task Endpoints

#### 6.4.1 POST /api/tasks -- Create Task

| Attribute        | Value                                     |
|------------------|-------------------------------------------|
| **Method**       | `POST`                                    |
| **Path**         | `/api/tasks`                              |
| **Auth**         | `ADMIN`, `USER`                           |
| **Content-Type** | `application/json`                        |

**Request Body:**

```json
{
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication to the API endpoints",
  "priority": "HIGH",
  "categoryId": 2
}
```

| Field         | Type    | Required | Constraints                              |
|---------------|---------|----------|------------------------------------------|
| `title`       | String  | Yes      | 3-200 characters, not blank              |
| `description` | String  | No       | Max 2000 characters                      |
| `priority`    | String  | No       | `LOW`, `MEDIUM`, `HIGH`. Default: `MEDIUM` |
| `categoryId`  | Long    | No       | Must reference existing category         |

**Success Response:** `201 Created`

```json
{
  "id": 42,
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication to the API endpoints",
  "priority": "HIGH",
  "status": "OPEN",
  "category": {
    "id": 2,
    "name": "Feature"
  },
  "owner": {
    "id": 1,
    "username": "jdoe"
  },
  "createdAt": "2025-07-14T10:30:00.000Z",
  "updatedAt": "2025-07-14T10:30:00.000Z"
}
```

**Error Responses:**

| Status | Condition                                 |
|--------|-------------------------------------------|
| `400`  | Validation failure (title blank, etc.)    |
| `400`  | Category ID does not exist                |
| `401`  | Missing or invalid JWT                    |
| `409`  | Duplicate title in same category          |

---

#### 6.4.2 GET /api/tasks -- List Tasks

| Attribute        | Value                                     |
|------------------|-------------------------------------------|
| **Method**       | `GET`                                     |
| **Path**         | `/api/tasks`                              |
| **Auth**         | `ADMIN`, `USER`                           |

**Query Parameters:**

| Parameter    | Type    | Required | Default | Description                         |
|--------------|---------|----------|---------|-------------------------------------|
| `status`     | String  | No       | --      | Filter by status (`OPEN`, `IN_PROGRESS`, `DONE`) |
| `priority`   | String  | No       | --      | Filter by priority (`LOW`, `MEDIUM`, `HIGH`) |
| `categoryId` | Long    | No       | --      | Filter by category ID               |
| `page`       | Integer | No       | `0`     | Page number (zero-based)             |
| `size`       | Integer | No       | `20`    | Page size (max 100)                  |
| `sort`       | String  | No       | `createdAt,desc` | Sort field and direction    |

**Success Response:** `200 OK`

```json
{
  "content": [
    {
      "id": 42,
      "title": "Implement user authentication",
      "description": "Add JWT-based authentication to the API endpoints",
      "priority": "HIGH",
      "status": "OPEN",
      "category": {
        "id": 2,
        "name": "Feature"
      },
      "owner": {
        "id": 1,
        "username": "jdoe"
      },
      "commentCount": 3,
      "createdAt": "2025-07-14T10:30:00.000Z",
      "updatedAt": "2025-07-14T10:30:00.000Z"
    }
  ],
  "page": {
    "totalElements": 85,
    "totalPages": 5,
    "currentPage": 0,
    "size": 20
  }
}
```

---

#### 6.4.3 GET /api/tasks/{id} -- Get Task by ID

**Success Response:** `200 OK`

```json
{
  "id": 42,
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication to the API endpoints",
  "priority": "HIGH",
  "status": "IN_PROGRESS",
  "category": {
    "id": 2,
    "name": "Feature"
  },
  "owner": {
    "id": 1,
    "username": "jdoe"
  },
  "comments": [
    {
      "id": 101,
      "body": "Started working on this. Using Spring Security.",
      "author": {
        "id": 1,
        "username": "jdoe"
      },
      "createdAt": "2025-07-14T11:00:00.000Z"
    }
  ],
  "createdAt": "2025-07-14T10:30:00.000Z",
  "updatedAt": "2025-07-14T11:15:00.000Z"
}
```

---

#### 6.4.4 PUT /api/tasks/{id} -- Update Task

| Attribute        | Value                                     |
|------------------|-------------------------------------------|
| **Method**       | `PUT`                                     |
| **Path**         | `/api/tasks/{id}`                         |
| **Auth**         | `ADMIN` (any task), `USER` (own tasks)    |

**Request Body:**

```json
{
  "title": "Implement user authentication and authorization",
  "status": "IN_PROGRESS",
  "priority": "HIGH"
}
```

| Field         | Type    | Required | Constraints                              |
|---------------|---------|----------|------------------------------------------|
| `title`       | String  | No       | 3-200 characters if provided             |
| `description` | String  | No       | Max 2000 characters                      |
| `priority`    | String  | No       | `LOW`, `MEDIUM`, `HIGH`                  |
| `status`      | String  | No       | Must follow valid transition rules       |
| `categoryId`  | Long    | No       | Must reference existing category         |

**Success Response:** `200 OK`

**Error Responses:**

| Status | Condition                                       |
|--------|-------------------------------------------------|
| `400`  | Validation failure or invalid status transition |
| `401`  | Missing or invalid JWT                          |
| `403`  | User is not the owner and not an Admin          |
| `404`  | Task not found or soft-deleted                  |
| `409`  | Duplicate title in same category                |

---

#### 6.4.5 DELETE /api/tasks/{id} -- Soft Delete Task

| Attribute        | Value                                     |
|------------------|-------------------------------------------|
| **Method**       | `DELETE`                                  |
| **Path**         | `/api/tasks/{id}`                         |
| **Auth**         | `ADMIN` (any task), `USER` (own tasks)    |

**Success Response:** `204 No Content`

---

### 6.5 Comment Endpoints

#### 6.5.1 POST /api/tasks/{taskId}/comments -- Add Comment

**Request Body:**

```json
{
  "body": "I have completed the initial implementation. Ready for review."
}
```

| Field  | Type   | Required | Constraints               |
|--------|--------|----------|---------------------------|
| `body` | String | Yes      | 1-1000 characters         |

**Success Response:** `201 Created`

```json
{
  "id": 102,
  "body": "I have completed the initial implementation. Ready for review.",
  "author": {
    "id": 1,
    "username": "jdoe"
  },
  "taskId": 42,
  "createdAt": "2025-07-14T14:00:00.000Z"
}
```

#### 6.5.2 GET /api/tasks/{taskId}/comments -- List Comments

**Success Response:** `200 OK` (paginated, sorted by `created_at` ascending)

---

### 6.6 Category Endpoints

#### 6.6.1 POST /api/categories -- Create Category

| Attribute        | Value                                     |
|------------------|-------------------------------------------|
| **Method**       | `POST`                                    |
| **Path**         | `/api/categories`                         |
| **Auth**         | `ADMIN` only                              |

**Request Body:**

```json
{
  "name": "Feature",
  "description": "New feature development tasks"
}
```

**Success Response:** `201 Created`

#### 6.6.2 GET /api/categories -- List Categories

**Auth:** `ADMIN`, `USER`

**Success Response:** `200 OK`

```json
[
  { "id": 1, "name": "Bug", "description": "Bug fixes and defects" },
  { "id": 2, "name": "Feature", "description": "New feature development tasks" },
  { "id": 3, "name": "Research", "description": "Investigation and spike tasks" }
]
```

---

## 7. Data Model

### 7.1 Entity-Relationship Diagram

```
┌──────────┐       ┌──────────┐       ┌──────────┐
│  users   │1    * │  tasks   │*    1 │categories│
│          ├───────┤          ├───────┤          │
│          │       │          │       │          │
└────┬─────┘       └────┬─────┘       └──────────┘
     │1                 │1
     │                  │
     │*                 │*
┌────┴─────┐       ┌────┴─────┐
│ audit_log│       │ comments │
│          │       │          │
└──────────┘       └──────────┘
```

### 7.2 SQL Schema

```sql
-- ============================================================
-- Table: users
-- ============================================================
CREATE TABLE users (
    id              BIGSERIAL       PRIMARY KEY,
    username        VARCHAR(50)     NOT NULL UNIQUE,
    email           VARCHAR(255)    NOT NULL UNIQUE,
    password_hash   VARCHAR(255)    NOT NULL,
    role            VARCHAR(20)     NOT NULL DEFAULT 'USER'
                                    CHECK (role IN ('ADMIN', 'USER')),
    active          BOOLEAN         NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_users_email    ON users (email);
CREATE INDEX idx_users_role     ON users (role);

-- ============================================================
-- Table: categories
-- ============================================================
CREATE TABLE categories (
    id              BIGSERIAL       PRIMARY KEY,
    name            VARCHAR(100)    NOT NULL,
    description     VARCHAR(500),
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_categories_name_lower ON categories (LOWER(name));

-- ============================================================
-- Table: tasks
-- ============================================================
CREATE TABLE tasks (
    id              BIGSERIAL       PRIMARY KEY,
    title           VARCHAR(200)    NOT NULL,
    description     VARCHAR(2000),
    priority        VARCHAR(10)     NOT NULL DEFAULT 'MEDIUM'
                                    CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH')),
    status          VARCHAR(20)     NOT NULL DEFAULT 'OPEN'
                                    CHECK (status IN ('OPEN', 'IN_PROGRESS', 'DONE')),
    deleted         BOOLEAN         NOT NULL DEFAULT FALSE,
    deleted_at      TIMESTAMPTZ,
    owner_id        BIGINT          NOT NULL REFERENCES users(id),
    category_id     BIGINT          REFERENCES categories(id),
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    created_by      BIGINT          NOT NULL REFERENCES users(id)
);

-- Unique constraint: no duplicate titles within the same category (for non-deleted tasks)
CREATE UNIQUE INDEX idx_tasks_title_category_active
    ON tasks (LOWER(title), COALESCE(category_id, -1))
    WHERE deleted = FALSE;

-- Query performance indexes
CREATE INDEX idx_tasks_status      ON tasks (status)    WHERE deleted = FALSE;
CREATE INDEX idx_tasks_priority    ON tasks (priority)   WHERE deleted = FALSE;
CREATE INDEX idx_tasks_category    ON tasks (category_id) WHERE deleted = FALSE;
CREATE INDEX idx_tasks_owner       ON tasks (owner_id)   WHERE deleted = FALSE;
CREATE INDEX idx_tasks_created_at  ON tasks (created_at DESC) WHERE deleted = FALSE;
CREATE INDEX idx_tasks_deleted     ON tasks (deleted);

-- ============================================================
-- Table: comments
-- ============================================================
CREATE TABLE comments (
    id              BIGSERIAL       PRIMARY KEY,
    body            VARCHAR(1000)   NOT NULL,
    task_id         BIGINT          NOT NULL REFERENCES tasks(id),
    author_id       BIGINT          NOT NULL REFERENCES users(id),
    deleted         BOOLEAN         NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_comments_task     ON comments (task_id)   WHERE deleted = FALSE;
CREATE INDEX idx_comments_author   ON comments (author_id) WHERE deleted = FALSE;

-- ============================================================
-- Table: audit_log
-- ============================================================
CREATE TABLE audit_log (
    id              BIGSERIAL       PRIMARY KEY,
    entity_type     VARCHAR(50)     NOT NULL,
    entity_id       BIGINT          NOT NULL,
    action          VARCHAR(20)     NOT NULL
                                    CHECK (action IN ('CREATE', 'UPDATE', 'DELETE', 'COMMENT')),
    changed_fields  JSONB,
    performed_by    BIGINT          NOT NULL REFERENCES users(id),
    performed_at    TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_entity     ON audit_log (entity_type, entity_id);
CREATE INDEX idx_audit_user       ON audit_log (performed_by);
CREATE INDEX idx_audit_timestamp  ON audit_log (performed_at DESC);
```

### 7.3 Seed Data (for Workshop)

```sql
-- Admin user (password: admin123)
INSERT INTO users (username, email, password_hash, role)
VALUES ('admin', 'admin@workshop.dev',
        '$2a$10$examplehashforadmin', 'ADMIN');

-- Regular user (password: user123)
INSERT INTO users (username, email, password_hash, role)
VALUES ('jdoe', 'jdoe@workshop.dev',
        '$2a$10$examplehashforuser', 'USER');

-- Categories
INSERT INTO categories (name, description) VALUES
    ('Bug',     'Bug fixes and defect resolution'),
    ('Feature', 'New feature development'),
    ('Research','Investigation and technical spikes');

-- Sample tasks
INSERT INTO tasks (title, description, priority, status, owner_id, category_id, created_by) VALUES
    ('Fix login page error',  'Users report 500 error on login', 'HIGH',   'OPEN',        2, 1, 2),
    ('Add search feature',    'Implement full-text search',      'MEDIUM', 'IN_PROGRESS', 2, 2, 2),
    ('Evaluate caching',      'Research Redis vs Caffeine',      'LOW',    'OPEN',        2, 3, 2);
```

---

## 8. Architecture

### 8.1 Architectural Style

The application follows a **Layered (N-Tier) Architecture** pattern.

### 8.2 Component Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Client (Postman / cURL / UI)                │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTP/JSON
                               v
┌─────────────────────────────────────────────────────────────────────┐
│                      Spring Boot Application                        │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    Security Filter Chain                      │  │
│  │            (JWT Authentication + Authorization)               │  │
│  └──────────────────────────┬────────────────────────────────────┘  │
│                              │                                      │
│  ┌──────────────────────────v────────────────────────────────────┐  │
│  │                   Controller Layer                            │  │
│  │   TaskController  │ CategoryController │ CommentController    │  │
│  └──────────────────────────┬────────────────────────────────────┘  │
│                              │                                      │
│  ┌──────────────────────────v────────────────────────────────────┐  │
│  │                    Service Layer                              │  │
│  │    TaskService   │  CategoryService  │  CommentService       │  │
│  └──────────────────────────┬────────────────────────────────────┘  │
│                              │                                      │
│  ┌──────────────────────────v────────────────────────────────────┐  │
│  │                   Repository Layer                            │  │
│  │  TaskRepository  │ CategoryRepository │ CommentRepository    │  │
│  └──────────────────────────┬────────────────────────────────────┘  │
│                              │                                      │
└──────────────────────────────┼──────────────────────────────────────┘
                               │ JDBC (HikariCP)
                               v
                  ┌────────────────────────┐
                  │     PostgreSQL 16      │
                  │   (Docker Container)   │
                  └────────────────────────┘
```

### 8.3 Package Structure

```
src/main/java/com/workshop/taskmanager/
├── TaskManagerApplication.java
├── config/
│   ├── SecurityConfig.java
│   ├── JwtConfig.java
│   ├── CorsConfig.java
│   └── OpenApiConfig.java
├── controller/
│   ├── TaskController.java
│   ├── CategoryController.java
│   ├── CommentController.java
│   └── AuthController.java
├── dto/
│   ├── request/
│   │   ├── CreateTaskRequest.java
│   │   ├── UpdateTaskRequest.java
│   │   ├── CreateCategoryRequest.java
│   │   ├── CreateCommentRequest.java
│   │   └── LoginRequest.java
│   └── response/
│       ├── TaskResponse.java
│       ├── TaskSummaryResponse.java
│       ├── CategoryResponse.java
│       ├── CommentResponse.java
│       ├── PagedResponse.java
│       └── ErrorResponse.java
├── entity/
│   ├── Task.java
│   ├── User.java
│   ├── Category.java
│   ├── Comment.java
│   ├── AuditLog.java
│   └── enums/
│       ├── Priority.java
│       ├── TaskStatus.java
│       └── Role.java
├── exception/
│   ├── GlobalExceptionHandler.java
│   ├── ResourceNotFoundException.java
│   ├── DuplicateResourceException.java
│   ├── InvalidStatusTransitionException.java
│   └── UnauthorizedAccessException.java
├── mapper/
│   ├── TaskMapper.java
│   ├── CategoryMapper.java
│   └── CommentMapper.java
├── repository/
│   ├── TaskRepository.java
│   ├── UserRepository.java
│   ├── CategoryRepository.java
│   ├── CommentRepository.java
│   ├── AuditLogRepository.java
│   └── specification/
│       └── TaskSpecification.java
├── security/
│   ├── JwtTokenProvider.java
│   ├── JwtAuthenticationFilter.java
│   └── UserDetailsServiceImpl.java
└── service/
    ├── TaskService.java
    ├── CategoryService.java
    ├── CommentService.java
    ├── AuditService.java
    └── AuthService.java
```

### 8.4 Key Design Decisions

| # | Decision                                  | Rationale                                                                                           |
|---|-------------------------------------------|-----------------------------------------------------------------------------------------------------|
| 1 | Soft delete instead of hard delete        | Preserves audit trail; allows recovery; prevents referential integrity issues with audit_log.       |
| 2 | DTO pattern (separate request/response)   | Decouples API contract from internal entity structure; prevents accidental field exposure.          |
| 3 | Spring Data JPA Specifications for filtering | Enables composable, type-safe dynamic queries without concatenating JPQL strings.                 |
| 4 | Partial index for unique title check      | Database-level enforcement of FR-7; `WHERE deleted = FALSE` ensures soft-deleted titles are reusable. |
| 5 | JWT stateless authentication              | No server-side session storage; scales horizontally; standard for REST APIs.                       |
| 6 | JSONB for audit `changed_fields`          | Flexible schema for capturing arbitrary field changes without additional columns.                   |
| 7 | Docker Compose for PostgreSQL             | Zero-install database setup; consistent environment across all workshop participants.              |

---

## 9. Test Strategy

### 9.1 Coverage Targets

| Layer        | Target Coverage | Focus                                      |
|--------------|:--------------:|---------------------------------------------|
| Service      |     > 90%      | Business logic, validation, edge cases      |
| Controller   |     > 80%      | Request mapping, status codes, error paths  |
| Repository   |     > 70%      | Custom query methods, specifications        |
| **Overall**  |   **> 80%**    |                                             |

### 9.2 Unit Test Cases (TaskService)

| # | Test Case                                              | FR   | Expected Result                              |
|---|--------------------------------------------------------|------|----------------------------------------------|
| 1 | Create task with valid data                            | FR-1 | Task created with status OPEN, generated ID  |
| 2 | Create task with missing title                         | FR-1 | `ValidationException` thrown                 |
| 3 | Create task with title > 200 chars                     | FR-1 | `ValidationException` thrown                 |
| 4 | Create task with non-existent category                 | FR-1 | `ResourceNotFoundException` thrown           |
| 5 | Create task with default priority (null)               | FR-1 | Task created with priority = MEDIUM          |
| 6 | List tasks returns paginated results                   | FR-2 | Page object with correct metadata            |
| 7 | List tasks filtered by status=OPEN                     | FR-2 | Only OPEN tasks returned                     |
| 8 | List tasks filtered by priority=HIGH                   | FR-2 | Only HIGH priority tasks returned            |
| 9 | List tasks with combined filters                       | FR-2 | AND logic applied correctly                  |
| 10| List tasks excludes soft-deleted records               | FR-2 | Deleted tasks not in results                 |
| 11| Update task status OPEN -> IN_PROGRESS                 | FR-3 | Status updated, updatedAt refreshed          |
| 12| Update task status IN_PROGRESS -> DONE                 | FR-3 | Status updated successfully                  |
| 13| Update task status OPEN -> DONE (invalid)              | FR-3 | `InvalidStatusTransitionException` thrown    |
| 14| Update task status DONE -> IN_PROGRESS (invalid)       | FR-3 | `InvalidStatusTransitionException` thrown    |
| 15| Update task by non-owner non-admin                     | FR-3 | `UnauthorizedAccessException` thrown         |
| 16| Update task by admin (any task)                        | FR-3 | Update successful                            |
| 17| Soft delete task sets deleted flag and timestamp        | FR-4 | `deleted=true`, `deletedAt` populated        |
| 18| Delete already-deleted task                            | FR-4 | `ResourceNotFoundException` thrown           |
| 19| Delete task by non-owner non-admin                     | FR-4 | `UnauthorizedAccessException` thrown         |
| 20| Create task with duplicate title in same category      | FR-7 | `DuplicateResourceException` thrown          |
| 21| Create task with same title in different category      | FR-7 | Task created successfully                    |
| 22| Create task with title matching soft-deleted task      | FR-7 | Task created successfully (no conflict)      |
| 23| Update task title to its own title                     | FR-7 | Update successful (no self-conflict)         |

### 9.3 Integration Test Cases

| # | Test Case                                              | Endpoint                 | Expected Status |
|---|--------------------------------------------------------|--------------------------|:---------------:|
| 1 | Create task -- happy path                              | `POST /api/tasks`        | `201`           |
| 2 | Create task -- missing title                           | `POST /api/tasks`        | `400`           |
| 3 | Create task -- duplicate title in category             | `POST /api/tasks`        | `409`           |
| 4 | Create task -- unauthenticated                         | `POST /api/tasks`        | `401`           |
| 5 | Get all tasks -- default pagination                    | `GET /api/tasks`         | `200`           |
| 6 | Get all tasks -- filter by status                      | `GET /api/tasks?status=OPEN` | `200`       |
| 7 | Get task by ID -- exists                               | `GET /api/tasks/1`       | `200`           |
| 8 | Get task by ID -- not found                            | `GET /api/tasks/9999`    | `404`           |
| 9 | Get task by ID -- soft deleted                         | `GET /api/tasks/1`       | `404`           |
| 10| Update task -- valid status transition                 | `PUT /api/tasks/1`       | `200`           |
| 11| Update task -- invalid status transition               | `PUT /api/tasks/1`       | `400`           |
| 12| Update task -- forbidden (non-owner)                   | `PUT /api/tasks/1`       | `403`           |
| 13| Delete task -- owner deletes own task                  | `DELETE /api/tasks/1`    | `204`           |
| 14| Delete task -- admin deletes any task                  | `DELETE /api/tasks/1`    | `204`           |
| 15| Delete task -- non-owner forbidden                     | `DELETE /api/tasks/1`    | `403`           |
| 16| Add comment -- happy path                              | `POST /api/tasks/1/comments` | `201`       |
| 17| Add comment -- empty body                              | `POST /api/tasks/1/comments` | `400`       |
| 18| Add comment -- task not found                          | `POST /api/tasks/9999/comments` | `404`    |
| 19| List comments -- with pagination                       | `GET /api/tasks/1/comments` | `200`        |
| 20| Create category -- admin only                          | `POST /api/categories`   | `201`           |
| 21| Create category -- user forbidden                      | `POST /api/categories`   | `403`           |
| 22| List categories -- all roles                           | `GET /api/categories`    | `200`           |

---

## 10. CI/CD Pipeline

### 10.1 Pipeline Stages

| Stage      | Tool                    | Action                                         | Quality Gate                   |
|------------|-------------------------|-------------------------------------------------|--------------------------------|
| **Build**  | Maven                   | Compile source, resolve dependencies             | Zero compilation errors        |
| **Test**   | JUnit 5, Testcontainers | Run unit + integration tests                    | All tests pass, coverage > 80% |
| **Scan**   | SpotBugs, OWASP Dep-Check | Static analysis + dependency vulnerability scan | No critical/high vulnerabilities |
| **Package**| Docker                  | Build container image                            | Image builds successfully      |
| **Deploy** | Docker Compose          | Deploy to staging environment                    | Health check passes            |

### 10.2 Docker Configuration

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: taskmanager
      POSTGRES_USER: taskuser
      POSTGRES_PASSWORD: taskpass
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./src/main/resources/db/init.sql:/docker-entrypoint-initdb.d/init.sql

  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/taskmanager
      SPRING_DATASOURCE_USERNAME: taskuser
      SPRING_DATASOURCE_PASSWORD: taskpass
      SPRING_JPA_HIBERNATE_DDL_AUTO: validate
      JWT_SECRET: workshop-secret-key-change-in-production
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  pgdata:
```

---

## 11. Security Considerations

### 11.1 Authentication (JWT)

| Aspect               | Implementation                                                      |
|----------------------|----------------------------------------------------------------------|
| **Token Type**       | JWT (JSON Web Token) -- Bearer token                                |
| **Algorithm**        | HMAC-SHA256 (HS256)                                                  |
| **Token Expiry**     | 1 hour (configurable via `jwt.expiration`)                          |
| **Token Location**   | `Authorization: Bearer <token>` header                              |
| **Login Endpoint**   | `POST /api/auth/login` -- returns JWT on successful authentication  |
| **Password Storage** | BCrypt hash (strength 10)                                            |

### 11.2 Authorization (Spring Security)

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    return http
        .csrf(csrf -> csrf.disable())
        .sessionManagement(sm -> sm.sessionCreationPolicy(STATELESS))
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/api/auth/**").permitAll()
            .requestMatchers("/swagger-ui/**", "/v3/api-docs/**").permitAll()
            .requestMatchers(HttpMethod.POST, "/api/categories/**").hasRole("ADMIN")
            .requestMatchers(HttpMethod.PUT, "/api/categories/**").hasRole("ADMIN")
            .requestMatchers(HttpMethod.DELETE, "/api/categories/**").hasRole("ADMIN")
            .anyRequest().authenticated()
        )
        .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
        .build();
}
```

### 11.3 Input Validation

```java
public record CreateTaskRequest(
    @NotBlank(message = "Title is required")
    @Size(min = 3, max = 200, message = "Title must be between 3 and 200 characters")
    String title,

    @Size(max = 2000, message = "Description must not exceed 2000 characters")
    String description,

    @ValidEnum(enumClass = Priority.class, message = "Priority must be LOW, MEDIUM, or HIGH")
    String priority,

    @Positive(message = "Category ID must be a positive number")
    Long categoryId
) {}
```

### 11.4 Additional Security Measures

| Measure                  | Implementation                                                        |
|--------------------------|-----------------------------------------------------------------------|
| **SQL Injection**        | Parameterized queries via JPA/Hibernate                              |
| **CORS**                 | Configured for known origins only in production                      |
| **Rate Limiting**        | Optional: Spring Boot Actuator + Bucket4j                            |
| **Error Information**    | No stack traces in API responses                                     |
| **Dependency Security**  | OWASP Dependency-Check in CI pipeline                                |
| **HTTPS**                | Required in production (reverse proxy / load balancer level)         |

---

## 12. Appendix

### 12.1 Glossary

| Term              | Definition                                                             |
|-------------------|------------------------------------------------------------------------|
| **Soft Delete**   | Marking a record as deleted without physically removing it from the database. |
| **JWT**           | JSON Web Token -- a compact, URL-safe token for stateless authentication. |
| **CRUD**          | Create, Read, Update, Delete -- basic data operations.                 |
| **DTO**           | Data Transfer Object -- a pattern for transferring data between layers. |
| **Testcontainers**| A Java library for providing lightweight, throwaway database instances for testing. |

### 12.2 Workshop Implementation Order

For the AI-Native workshop, implement in this recommended sequence:

| Step | Component                     | Duration  | AI Prompt Strategy                          |
|------|-------------------------------|-----------|---------------------------------------------|
| 1    | Docker Compose + DB schema    | 10 min    | Provide full schema from Section 7          |
| 2    | Entity classes + Enums        | 10 min    | Provide domain model from Section 5        |
| 3    | Repository interfaces         | 5 min     | Provide query requirements from Section 6  |
| 4    | DTOs (Request/Response)       | 10 min    | Provide JSON examples from Section 6       |
| 5    | Service layer + business logic| 20 min    | Provide FRs + edge cases from Section 2    |
| 6    | Controller layer              | 15 min    | Provide API contract from Section 6        |
| 7    | Security configuration        | 15 min    | Provide security details from Section 11   |
| 8    | Unit tests                    | 15 min    | Provide test cases from Section 9.2        |
| 9    | Integration tests             | 15 min    | Provide test cases from Section 9.3        |
| 10   | Run and verify                | 5 min     | Use seed data from Section 7.3             |

---

*End of Software Design Document*
