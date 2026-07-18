# Task Management API

A RESTful API for managing tasks, categories, and comments built with Java 21 and Spring Boot 3.4.x.

## Quick Start

### Prerequisites
- Java 21 (install via [SDKMAN](https://sdkman.io/))
- Maven 3.9+ (comes with SDKMAN)

### Setup & Run

```bash
# Ensure Java 21 is available
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Build the project
mvn clean package

# Run the application
mvn spring-boot:run

# Or run the JAR directly
java -jar target/task-manager-1.0.0.jar
```

The API will start on **http://localhost:8080**.

### H2 Console
Access the in-memory database console at: **http://localhost:8080/h2-console**
- JDBC URL: `jdbc:h2:mem:taskdb`
- Username: `sa`
- Password: *(empty)*

## API Endpoints

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/tasks` | Create a new task |
| `GET` | `/api/tasks` | List tasks (with filters & pagination) |
| `GET` | `/api/tasks/{id}` | Get task by ID |
| `PUT` | `/api/tasks/{id}` | Update a task |
| `DELETE` | `/api/tasks/{id}` | Soft-delete a task |

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/categories` | Create category (Admin only) |
| `GET` | `/api/categories` | List all categories |
| `GET` | `/api/categories/{id}` | Get category by ID |
| `PUT` | `/api/categories/{id}` | Update category |
| `DELETE` | `/api/categories/{id}` | Delete category (Admin, no tasks) |

### Comments
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/tasks/{taskId}/comments` | Add comment to task |
| `GET` | `/api/tasks/{taskId}/comments` | List comments for task |
| `DELETE` | `/api/tasks/{taskId}/comments/{commentId}` | Delete comment (Admin only) |

### Audit Logs
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/audit-logs` | List audit logs |

## Authentication

This project uses simple header-based authentication for workshop purposes:

```bash
# Headers
X-User-Id: user1          # Identifies the user (default: "anonymous")
X-User-Role: ADMIN         # Role: "ADMIN" or "USER" (default: "USER")
```

## Example API Calls

### Create a Task
```bash
curl -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -H "X-User-Id: user1" \
  -d '{
    "title": "Implement login feature",
    "description": "Add OAuth2 login support",
    "priority": "HIGH",
    "categoryId": 2
  }'
```

### List Tasks with Filters
```bash
curl "http://localhost:8080/api/tasks?status=OPEN&priority=HIGH&page=0&size=10" \
  -H "X-User-Id: user1"
```

### Update Task Status
```bash
curl -X PUT http://localhost:8080/api/tasks/1 \
  -H "Content-Type: application/json" \
  -H "X-User-Id: user1" \
  -d '{"status": "IN_PROGRESS"}'
```

### Create a Category (Admin)
```bash
curl -X POST http://localhost:8080/api/categories \
  -H "Content-Type: application/json" \
  -H "X-User-Id: admin1" \
  -H "X-User-Role: ADMIN" \
  -d '{"name": "Security", "description": "Security-related tasks"}'
```

### Add a Comment
```bash
curl -X POST http://localhost:8080/api/tasks/1/comments \
  -H "Content-Type: application/json" \
  -H "X-User-Id: user2" \
  -d '{"text": "I can help with this task!"}'
```

## Status Transition Rules

```
OPEN --> IN_PROGRESS --> DONE
  ^         |              |
  |         v              |
  +---------+--------------+
```

- `OPEN` -> `IN_PROGRESS` (start work)
- `IN_PROGRESS` -> `DONE` (complete)
- `IN_PROGRESS` -> `OPEN` (pause/reopen)
- `DONE` -> `OPEN` (reopen)

Invalid transitions return `400 Bad Request`.

## Query Parameters

### Task Listing
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `status` | String | - | Filter: OPEN, IN_PROGRESS, DONE |
| `priority` | String | - | Filter: LOW, MEDIUM, HIGH |
| `categoryId` | Long | - | Filter by category |
| `page` | int | 0 | Page number (0-based) |
| `size` | int | 20 | Page size (max 100) |
| `sort` | String | createdAt,desc | Sort field and direction |

## Running Tests

```bash
# Run all tests
mvn test

# Run with verbose output
mvn test -Dspring-boot.test.randomPort=true
```

## Switching to PostgreSQL

1. Start PostgreSQL using Docker Compose:
```bash
docker-compose up -d
```

2. Run with PostgreSQL profile:
```bash
mvn spring-boot:run -Dspring-boot.run.profiles=postgres
```

See `docker-compose.yml` and `src/main/resources/application-postgres.yml` for configuration.

## Project Structure

```
src/main/java/com/workshop/taskmanager/
+-- TaskManagerApplication.java        # Application entry point
+-- config/SecurityConfig.java         # Header-based auth filter
+-- controller/                        # REST controllers
+-- dto/                               # Request/Response DTOs
+-- entity/                            # JPA entities & enums
+-- exception/                         # Exception handling
+-- repository/                        # Data access layer
+-- service/                           # Business logic
```

## Seed Data

The application comes pre-loaded with:
- 5 categories (Bug, Feature, Research, Documentation, Testing)
- 20 tasks across different statuses and priorities
- 15 comments on various tasks
- 10 audit log entries

See `data/seed_data.json` for the complete dataset.
