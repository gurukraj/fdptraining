# Task Management API - Software Design Document (SDD)

## 1. Overview
A RESTful API for managing tasks, categories, and comments. Designed as a workshop exercise to demonstrate Spring Boot best practices, layered architecture, and modern Java features.

## 2. Functional Requirements Summary

### FR-1: Task CRUD
- Create tasks with title, description, priority, and category
- View tasks with filtering (status, priority, category) and pagination
- Update tasks with status transition validation
- Soft-delete tasks (cascade to comments)

### FR-2: Category Management
- CRUD operations for task categories
- Admin-only creation and deletion
- Prevent deletion of categories with associated tasks
- Case-insensitive unique names

### FR-3: Comment System
- Add comments to tasks (1-1000 characters)
- Paginated comment listing per task
- Admin-only comment deletion

### FR-4: Audit Logging
- Automatic logging of all write operations
- Queryable audit log with filtering by entity type

## 3. Non-Functional Requirements
- **Performance**: Paginated responses, max page size 100
- **Security**: Header-based auth (X-User-Id, X-User-Role)
- **Data Integrity**: Soft deletes, audit trail
- **Portability**: H2 for dev, PostgreSQL for production

## 4. API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/tasks | Create task |
| GET | /api/tasks | List tasks (filtered, paginated) |
| GET | /api/tasks/{id} | Get task by ID |
| PUT | /api/tasks/{id} | Update task |
| DELETE | /api/tasks/{id} | Soft-delete task |
| POST | /api/categories | Create category (Admin) |
| GET | /api/categories | List categories |
| PUT | /api/categories/{id} | Update category |
| DELETE | /api/categories/{id} | Delete category |
| POST | /api/tasks/{taskId}/comments | Add comment |
| GET | /api/tasks/{taskId}/comments | List comments |
| DELETE | /api/tasks/{taskId}/comments/{commentId} | Delete comment (Admin) |
| GET | /api/audit-logs | List audit logs |

## 5. Data Model
- **Task**: id, title, description, status, priority, categoryId, createdBy, deleted, deletedAt, createdAt, updatedAt
- **Category**: id, name, description, createdAt, updatedAt
- **Comment**: id, taskId, text, author, deleted, createdAt
- **AuditLog**: id, entityType, entityId, action, performedBy, details, createdAt

## 6. Status Transitions
```
OPEN --> IN_PROGRESS --> DONE
  ^         |              |
  |         v              |
  +---------+--------------+
```
