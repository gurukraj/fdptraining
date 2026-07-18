# Task Management REST API

## What You'll Build

A full-featured task management API with categories, comments, enforced status transitions, role-based access control via request headers, soft-delete cascading, and a complete audit log of all write operations.

**Scenario:** A development team needs an internal task tracker. The system must enforce a specific workflow (status transitions), support categorization, allow threaded comments on tasks, restrict certain operations to administrators, and maintain a tamper-proof audit trail for compliance purposes.

## Technology Stack

| Component     | Technology                  |
|---------------|-----------------------------|
| Language      | Java 21                     |
| Framework     | Spring Boot 3.x             |
| Database      | H2 (in-memory)              |
| Data Access   | Spring Data JPA             |
| Build Tool    | Maven                       |
| Testing       | JUnit 5, Spring Boot Test   |

## Authentication Model

Authentication is header-based (no login endpoint). Every request must include:

| Header         | Description                              |
|----------------|------------------------------------------|
| `X-User-Id`    | Identifier for the acting user           |
| `X-User-Role`  | Role of the user: `USER` or `ADMIN`      |

Requests missing these headers should receive a **401** response. Operations restricted to ADMIN should return **403** for USER role.

## Functional Requirements

| FR-ID | Title                 | Description                                                                                              | Key Acceptance Criteria                                                                                           |
|-------|-----------------------|----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| FR-1  | Create Task           | Create a new task with title, optional description, priority, and optional category.                     | `title` 3-200 chars; `description` max 2000 chars; `priority` is LOW/MEDIUM/HIGH (default MEDIUM); status starts as OPEN; `createdBy` set from `X-User-Id`. |
| FR-2  | View Tasks            | Retrieve tasks with pagination, filtering by status/priority/category, and sorting.                       | Supports `page`/`size` pagination; filter by `status`, `priority`, `category`; sort by `createdAt`, `priority`, or `title`; excludes soft-deleted tasks. |
| FR-3  | Update Task           | Apply partial updates to title, description, priority, or category.                                      | Only provided fields are updated; returns **404** if task is deleted or does not exist; status cannot be changed via this endpoint. |
| FR-4  | Status Transitions    | Move a task through its workflow using a dedicated status-change endpoint.                                | Only the four valid transitions are allowed (see rules below); all other transitions return **400** with a descriptive message. |
| FR-5  | Soft Delete Task      | Mark a task as deleted; cascade soft-delete to its comments; exclude from all listings.                   | DELETE sets a soft-delete flag; associated comments are also soft-deleted; soft-deleted tasks return **404** on direct lookup. |
| FR-6  | Category Management   | CRUD for task categories with unique (case-insensitive) names.                                           | Create and delete restricted to ADMIN (403 for USER); delete rejected with **409** if any non-deleted tasks reference the category; name uniqueness is case-insensitive. |
| FR-7  | Comments              | Add and list comments on a task; delete a comment (ADMIN only).                                          | Comment `content` required, non-empty; comments linked to a task; list returns comments for a task sorted by creation time; delete is ADMIN only (403 for USER). |
| FR-8  | Audit Log             | Automatically log all write operations with entity type, entity ID, action, user, and timestamp.         | Covers task/category/comment create, update, delete, and status change; audit log is read-only; supports filtering by `entityType`. |

## Status Transition Rules

| From          | To            | Allowed? |
|---------------|---------------|----------|
| OPEN          | IN_PROGRESS   | Yes      |
| IN_PROGRESS   | DONE          | Yes      |
| IN_PROGRESS   | OPEN          | Yes      |
| DONE          | OPEN          | Yes      |
| All others    | -             | No       |

Any transition not listed above must be rejected with **400**.

## API Endpoints Summary

| Method | Path                            | Description                                  | Success | Error Codes        | Auth        |
|--------|---------------------------------|----------------------------------------------|---------|---------------------|-------------|
| POST   | `/api/tasks`                    | Create a new task                            | 201     | 400, 401, 422       | Any role    |
| GET    | `/api/tasks`                    | List tasks with filters, sort, pagination    | 200     | 401                 | Any role    |
| GET    | `/api/tasks/{id}`               | Get a single task by ID                      | 200     | 401, 404            | Any role    |
| PUT    | `/api/tasks/{id}`               | Update task fields (not status)              | 200     | 400, 401, 404, 422  | Any role    |
| PATCH  | `/api/tasks/{id}/status`        | Transition task status                       | 200     | 400, 401, 404       | Any role    |
| DELETE | `/api/tasks/{id}`               | Soft-delete a task and its comments          | 200     | 401, 404            | Any role    |
| POST   | `/api/categories`               | Create a new category                        | 201     | 400, 401, 403, 409  | ADMIN only  |
| GET    | `/api/categories`               | List all categories                          | 200     | 401                 | Any role    |
| PUT    | `/api/categories/{id}`          | Update a category                            | 200     | 400, 401, 404       | Any role    |
| DELETE | `/api/categories/{id}`          | Delete a category                            | 200     | 401, 403, 404, 409  | ADMIN only  |
| POST   | `/api/tasks/{id}/comments`      | Add a comment to a task                      | 201     | 400, 401, 404       | Any role    |
| GET    | `/api/tasks/{id}/comments`      | List comments for a task                     | 200     | 401, 404            | Any role    |
| DELETE | `/api/comments/{id}`            | Delete a comment                             | 200     | 401, 403, 404       | ADMIN only  |
| GET    | `/api/audit-logs`               | Query audit log entries                      | 200     | 401                 | Any role    |

## Data Model

### Task

| Field       | Type     | Constraints                                             |
|-------------|----------|---------------------------------------------------------|
| id          | Long     | Primary key, auto-generated                             |
| title       | String   | Required, 3-200 characters                              |
| description | String   | Optional, max 2000 characters                           |
| status      | Enum     | OPEN, IN_PROGRESS, DONE (default OPEN)                  |
| priority    | Enum     | LOW, MEDIUM, HIGH (default MEDIUM)                      |
| category    | Category | Foreign key, optional                                   |
| createdBy   | String   | Set from X-User-Id header                               |
| isDeleted   | Boolean  | Default false                                           |
| createdAt   | DateTime | Auto-set on creation                                    |
| updatedAt   | DateTime | Auto-set on creation and update                         |

### Category

| Field       | Type     | Constraints                                |
|-------------|----------|--------------------------------------------|
| id          | Long     | Primary key, auto-generated                |
| name        | String   | Required, unique (case-insensitive)        |
| description | String   | Optional                                   |

### Comment

| Field     | Type     | Constraints                             |
|-----------|----------|-----------------------------------------|
| id        | Long     | Primary key, auto-generated             |
| taskId    | Long     | Foreign key to Task, required           |
| content   | String   | Required, non-empty                     |
| author    | String   | Set from X-User-Id header               |
| isDeleted | Boolean  | Default false                           |
| createdAt | DateTime | Auto-set on creation                    |

### AuditLog

| Field       | Type     | Constraints                           |
|-------------|----------|---------------------------------------|
| id          | Long     | Primary key, auto-generated           |
| entityType  | String   | TASK, CATEGORY, or COMMENT            |
| entityId    | Long     | ID of the affected entity             |
| action      | String   | CREATE, UPDATE, DELETE, STATUS_CHANGE  |
| performedBy | String   | User who performed the action         |
| timestamp   | DateTime | Auto-set when the log entry is created|

**Relationships:** A Task optionally belongs to one Category. A Task has many Comments. AuditLog entries reference entities by type and ID (no foreign key constraint).

## Success Criteria

- All 14 endpoints return correct status codes and response structures.
- Header-based authentication enforces 401 for missing headers and 403 for unauthorized role.
- Only the four valid status transitions are accepted; all others return 400.
- Soft-delete on a task cascades to its comments; both are excluded from all listings.
- Category delete is blocked with 409 when non-deleted tasks reference it.
- Category name uniqueness is enforced case-insensitively.
- Every write operation produces an audit log entry with correct entity type, action, and user.
- Audit log endpoint supports filtering by `entityType`.
- Application starts with H2 in-memory database and schema auto-creates on launch.
- Seed data with tasks, categories, and comments can be loaded and queried successfully.
