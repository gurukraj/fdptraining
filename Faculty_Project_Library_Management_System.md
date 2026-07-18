# Faculty Project: Smart Library Management System

| Field              | Details                                         |
|--------------------|-------------------------------------------------|
| **Project Code**   | FP-LMS-2025                                     |
| **Duration**       | 4 Weeks (1 Month)                               |
| **Team Size**      | 2-3 Faculty Members                             |
| **Methodology**    | AI-Native Software Design & Development (SDD)   |
| **Architecture**   | Modular Monolith with Clean Architecture         |
| **Complexity**     | Intermediate-Advanced                           |

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

Modern academic libraries need intelligent management systems that go beyond simple book check-in/check-out. They require full-text search across catalog metadata, personalized book recommendations based on borrowing history and reviews, automated fine calculation with configurable rules, and real-time analytics dashboards --- all while maintaining data consistency under concurrent access by hundreds of students and library staff.

### 1.2 Project Scope

Design and implement a **modular monolith** Smart Library Management System with clean architecture principles, comprising seven well-defined modules that communicate through internal interfaces. The system leverages PostgreSQL full-text search for discovery, collaborative filtering for recommendations, and Redis for caching. The project follows an **AI-Native SDD** methodology throughout the development lifecycle.

### 1.3 Why Modular Monolith?

| Aspect                    | Modular Monolith                              | Microservices                              |
|---------------------------|-----------------------------------------------|--------------------------------------------|
| **Deployment Complexity** | Single deployable unit                        | Multiple services to orchestrate           |
| **Data Consistency**      | ACID transactions within single database      | Eventual consistency, sagas required        |
| **Development Speed**     | Faster initial development                    | Higher upfront investment                  |
| **Module Boundaries**     | Enforced via code structure and interfaces     | Enforced via network boundaries            |
| **Refactoring**           | Easier cross-module refactoring               | Requires API versioning                    |
| **Future Migration**      | Can extract modules to microservices later     | Already distributed                        |

### 1.4 Key Challenges

- **Full-Text Search**: Implementing efficient book search with relevance scoring using PostgreSQL `tsvector`
- **Recommendation Engine**: Building collaborative filtering that performs well with sparse data
- **Fine Calculation**: Configurable, rule-based fine engine that handles holidays, grace periods, and member tiers
- **Concurrent Access**: Multiple users borrowing/returning books simultaneously without data corruption
- **Caching Strategy**: Balancing data freshness with performance via Redis caching layers
- **Analytics Pipeline**: Real-time aggregation of borrowing trends and library utilization metrics

---

## 2. Learning Objectives

Upon completion, faculty participants will be able to:

1. **Design** a modular monolith with clean architecture layers (domain, application, infrastructure, presentation)
2. **Implement** PostgreSQL full-text search with `tsvector`, `tsquery`, and relevance ranking
3. **Build** a collaborative filtering recommendation engine with similarity scoring
4. **Apply** configurable business rules using the strategy pattern (fine calculation)
5. **Integrate** Redis caching with proper cache invalidation strategies
6. **Develop** real-time analytics dashboards with aggregation queries
7. **Apply** AI-Native SDD methodology for iterative design and development
8. **Enforce** module boundaries within a monolithic codebase using dependency rules

---

## 3. System Architecture

### 3.1 Modular Monolith Diagram

```
+=========================================================================+
|                        Smart Library Management System                   |
|                         (Single Deployable Unit)                         |
+=========================================================================+
|                                                                         |
|  +---------------------------+     +----------------------------+       |
|  |    Presentation Layer     |     |      API Gateway (FastAPI) |       |
|  |    (REST API Endpoints)   |     |      - Auth Middleware     |       |
|  |                           |     |      - Rate Limiting       |       |
|  +-------------+-------------+     |      - CORS                |       |
|                |                   +----------------------------+       |
|                v                                                        |
|  +----------------------------------------------------------------------+
|  |                       Application Layer                              |
|  |  (Use Cases / Service Orchestration / Command & Query Handlers)      |
|  +----------------------------------------------------------------------+
|       |          |          |         |         |        |        |      |
|       v          v          v         v         v        v        v      |
|  +--------+ +--------+ +--------+ +------+ +------+ +------+ +------+  |
|  |  Book  | | Member | |Borrowing| | Fine | |Search| |Recom-| |Analy-|  |
|  |Catalog | |  Mgmt  | | Engine | | Calc | |  &   | |mend- | | tics |  |
|  |Module  | | Module | | Module | |Module| |Discov| |ation | |Module|  |
|  |        | |        | |        | |      | | ery  | |Engine| |      |  |
|  +--------+ +--------+ +--------+ +------+ +------+ +------+ +------+  |
|       |          |          |         |         |        |        |      |
|       v          v          v         v         v        v        v      |
|  +----------------------------------------------------------------------+
|  |                        Domain Layer                                  |
|  |  (Entities, Value Objects, Domain Events, Business Rules)            |
|  +----------------------------------------------------------------------+
|       |                                                                 |
|       v                                                                 |
|  +----------------------------------------------------------------------+
|  |                     Infrastructure Layer                             |
|  |  +------------------+  +---------------+  +--------------------+    |
|  |  |   PostgreSQL     |  |    Redis      |  |  External Services |    |
|  |  |  (Primary DB +   |  |  (Cache +     |  |  (Email, SMS)      |    |
|  |  |   Full-Text      |  |   Session)    |  |                    |    |
|  |  |   Search)        |  |               |  |                    |    |
|  |  +------------------+  +---------------+  +--------------------+    |
|  +----------------------------------------------------------------------+
|                                                                         |
+=========================================================================+
```

### 3.2 Module Dependency Diagram

```
                    +-------------------+
                    |    Analytics      |
                    |    Module         |
                    +---+--------+------+
                        |        |
              +---------+        +--------+
              v                           v
    +-------------------+      +-------------------+
    |   Borrowing       |      |   Fine            |
    |   Engine          |----->|   Calculation     |
    +---+--------+------+      +-------------------+
        |        |
   +----+        +-----+
   v                    v
+------------+    +-------------------+
| Book       |    | Member            |
| Catalog    |    | Management        |
+-----+------+    +-------------------+
      |
      v
+-------------------+       +-------------------+
| Search &          |       | Recommendation    |
| Discovery         |       | Engine            |
+-------------------+       +---+--------+------+
                                |        |
                           +----+        +-----+
                           v                    v
                     Book Catalog       Borrowing Engine
                     (read-only)        (read-only)
```

**Dependency Rules**:
- Modules depend **only downward** --- no circular dependencies
- **Book Catalog** and **Member Management** are foundational modules (no upward dependencies)
- **Search & Discovery** reads from Book Catalog (read-only access)
- **Recommendation Engine** reads from Book Catalog and Borrowing Engine (read-only access)
- **Analytics** aggregates data from Borrowing Engine and Fine Calculation (read-only access)
- All inter-module communication happens through **defined interfaces** (Python ABCs or protocols)

### 3.3 Clean Architecture Layers

| Layer              | Responsibility                                | Contains                                        | Dependencies              |
|--------------------|-----------------------------------------------|-------------------------------------------------|---------------------------|
| **Domain**         | Core business logic and rules                 | Entities, value objects, domain events, enums    | None (innermost layer)    |
| **Application**    | Use case orchestration                        | Service classes, command/query handlers, DTOs    | Domain only               |
| **Infrastructure** | External system integration                   | Database repos, Redis client, email service      | Domain + Application      |
| **Presentation**   | HTTP interface                                | FastAPI routers, request/response schemas        | Application only          |

### 3.4 Caching Strategy

| Data Type              | Cache Location | TTL        | Invalidation Strategy                        |
|------------------------|----------------|------------|----------------------------------------------|
| Book catalog listings  | Redis          | 15 minutes | Invalidate on book create/update/delete      |
| Search results         | Redis          | 5 minutes  | Invalidate on catalog changes                |
| Member profiles        | Redis          | 30 minutes | Invalidate on profile update                 |
| Recommendation lists   | Redis          | 1 hour     | Rebuild nightly or on significant new data   |
| Fine calculations      | None           | ---        | Always computed fresh (financial accuracy)   |
| Analytics dashboards   | Redis          | 10 minutes | Time-based expiry only                       |
| Library configuration  | Redis          | 1 hour     | Invalidate on config update                  |

---

## 4. Technology Stack

| Layer            | Technology                       | Version    | Purpose                                  |
|------------------|----------------------------------|------------|------------------------------------------|
| Language         | Python                           | 3.12+      | Primary development language             |
| Framework        | FastAPI                          | 0.110+     | Async REST API framework                 |
| ASGI Server      | Uvicorn                          | 0.27+      | High-performance ASGI server             |
| Database         | PostgreSQL                       | 15+        | Primary data store + full-text search    |
| ORM              | SQLAlchemy 2.0                   | 2.0+       | Async ORM with type annotations          |
| Migrations       | Alembic                          | 1.13+      | Database schema versioning               |
| Cache            | Redis                            | 7.0+       | Caching, sessions, rate limiting         |
| Redis Client     | redis-py (async)                 | 5.0+       | Async Redis operations                   |
| Testing          | pytest + pytest-asyncio          | 8.0+       | Async-capable test framework             |
| HTTP Testing     | httpx                            | 0.27+      | Async HTTP client for integration tests  |
| Containerization | Docker + Docker Compose          | ---        | Environment consistency                  |
| Documentation    | FastAPI auto-generated OpenAPI   | ---        | Interactive API docs (Swagger UI)        |
| Data Validation  | Pydantic v2                      | 2.5+       | Request/response schema validation       |
| Task Scheduling  | APScheduler                      | 3.10+      | Scheduled recommendation rebuilds        |

---

## 5. Functional Requirements

### 5.1 Book Catalog Module (FR-BC-01 to FR-BC-03)

| ID        | Requirement                  | Description                                                                                                                                                                           | Priority |
|-----------|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| FR-BC-01  | Book Management              | Librarians can add, update, and archive books with metadata: ISBN, title, author(s), genre, publisher, publication year, description, and tags. System validates ISBN format and uniqueness. | Must     |
| FR-BC-02  | Copy Management              | Each book can have multiple physical copies tracked individually with unique accession numbers, condition status (new, good, fair, poor, damaged), and shelf location.                  | Must     |
| FR-BC-03  | Category & Tag Management    | Books can be organized into hierarchical categories and tagged with multiple labels. Tags support autocomplete based on existing tags in the system.                                   | Should   |

### 5.2 Member Management Module (FR-MM-01 to FR-MM-03)

| ID        | Requirement                  | Description                                                                                                                                                                           | Priority |
|-----------|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| FR-MM-01  | Member Registration          | New members register with name, email, member type (student, faculty, staff), department, and contact details. System generates unique member IDs (e.g., `LIB-YYYY-NNNN`).            | Must     |
| FR-MM-02  | Authentication & Authorization| Members authenticate via email/password with JWT tokens. Role-based access: members (borrow, search, review), librarians (manage catalog, view analytics), admins (full access).      | Must     |
| FR-MM-03  | Member Tier System           | Members have tiers (bronze, silver, gold) based on borrowing history. Tiers affect: max concurrent borrows (3/5/8), loan duration (14/21/30 days), fine rates, and reservation priority.| Should   |

### 5.3 Borrowing Engine Module (FR-BE-01 to FR-BE-04)

| ID        | Requirement                  | Description                                                                                                                                                                           | Priority |
|-----------|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| FR-BE-01  | Book Checkout                | Members can borrow available book copies. System validates: member active status, concurrent borrow limit, outstanding fines threshold, and copy availability. Assigns due date based on member tier. | Must     |
| FR-BE-02  | Book Return                  | Members return borrowed books. System calculates overdue fines (if applicable), updates copy availability, and triggers reservation fulfillment if the book was reserved by another member. | Must     |
| FR-BE-03  | Reservation System           | When all copies of a book are checked out, members can place a reservation. System maintains FIFO queue per book and notifies the next member when a copy becomes available. Reservations expire after 48 hours if not collected. | Must     |
| FR-BE-04  | Loan Renewal                 | Members can renew a loan if: no reservations exist for the book, renewal limit not exceeded (max 2 renewals), and no outstanding fines. Each renewal extends the due date by the tier-based loan duration. | Should   |

### 5.4 Fine Calculation Module (FR-FC-01 to FR-FC-02)

| ID        | Requirement                  | Description                                                                                                                                                                           | Priority |
|-----------|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| FR-FC-01  | Configurable Fine Rules      | System calculates fines based on configurable rules: per-day rate by member tier, grace period (configurable days), maximum fine cap per book, holiday exclusion from fine days, and damaged/lost book charges. | Must     |
| FR-FC-02  | Fine Payment & Waiver        | Members can view outstanding fines and payment history. Librarians can process payments (partial or full) and grant waivers with documented reasons. System blocks borrowing when fines exceed configurable threshold. | Must     |

### 5.5 Search & Discovery Module (FR-SD-01 to FR-SD-03)

| ID        | Requirement                  | Description                                                                                                                                                                           | Priority |
|-----------|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| FR-SD-01  | Full-Text Search             | Members can search books using natural language queries. System uses PostgreSQL `tsvector`/`tsquery` with relevance ranking (`ts_rank_cd`). Search covers title, author, description, and tags with weighted fields (title: A, author: B, description: C, tags: D). | Must     |
| FR-SD-02  | Faceted Filtering            | Search results support faceted filtering by genre, author, publication year range, availability status, and rating. Facet counts update dynamically based on current filters.           | Should   |
| FR-SD-03  | Search Suggestions           | System provides autocomplete suggestions based on popular search terms, book titles, and author names. Suggestions update based on search frequency and recency.                       | Should   |

### 5.6 Recommendation Engine Module (FR-RE-01 to FR-RE-03)

| ID        | Requirement                  | Description                                                                                                                                                                           | Priority |
|-----------|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| FR-RE-01  | Collaborative Filtering      | System recommends books based on borrowing patterns of similar members. Uses item-based collaborative filtering: "Members who borrowed X also borrowed Y." Returns top-N recommendations with similarity scores. | Must     |
| FR-RE-02  | Content-Based Suggestions    | System suggests books based on a member's genre preferences, favorite authors, and tag affinity derived from borrowing history and reviews.                                           | Should   |
| FR-RE-03  | Trending & Popular Books     | System surfaces currently trending books (high recent borrow rate), all-time popular books, and highly-rated books. Trending scores decay over time using exponential decay function.  | Should   |

### 5.7 Analytics Module (FR-AN-01 to FR-AN-02)

| ID        | Requirement                  | Description                                                                                                                                                                           | Priority |
|-----------|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| FR-AN-01  | Dashboard Metrics            | Librarians can view real-time dashboard with: total active borrows, overdue count, popular books this month, busiest checkout hours, member growth trends, and genre distribution.     | Must     |
| FR-AN-02  | Reports & Export             | System generates periodic reports: monthly borrowing summary, overdue books report, fine collection report, and inventory utilization. Reports exportable as JSON.                     | Should   |

---

## 6. Non-Functional Requirements

| ID       | Category        | Requirement                                                                                                              | Target Metric                        |
|----------|-----------------|--------------------------------------------------------------------------------------------------------------------------|--------------------------------------|
| NFR-01   | Search Perf.    | Full-text search must return results within 200ms for catalogs up to 100,000 books                                       | p95 < 200ms                          |
| NFR-02   | Search Perf.    | Search suggestions/autocomplete must respond within 100ms                                                                | p95 < 100ms                          |
| NFR-03   | API Perf.       | Checkout and return APIs must complete within 1 second including all validations and side effects                          | p95 < 1000ms                         |
| NFR-04   | Throughput      | System must handle at least 50 concurrent checkout/return operations                                                      | 50 concurrent users                  |
| NFR-05   | Concurrency     | Concurrent checkout of the same book copy must be prevented without data corruption                                       | Zero double-checkouts                |
| NFR-06   | Concurrency     | Reservation queue must maintain strict FIFO ordering under concurrent access                                              | FIFO guarantee                       |
| NFR-07   | Caching         | Cached data must not be stale beyond the defined TTL per data type                                                        | Per caching strategy table           |
| NFR-08   | Caching         | Cache hit ratio for book catalog queries should exceed 70% during normal operation                                         | > 70% hit ratio                      |
| NFR-09   | Security        | All API endpoints must be authenticated via JWT (except public search and health check)                                    | 100% auth coverage                   |
| NFR-10   | Security        | Passwords must be hashed using bcrypt with minimum 12 rounds                                                               | bcrypt cost >= 12                    |
| NFR-11   | Security        | Role-based access control must enforce librarian-only access to admin endpoints                                            | RBAC enforcement                     |
| NFR-12   | Security        | SQL injection prevention via parameterized queries/ORM                                                                     | Zero SQL injection vectors           |
| NFR-13   | Reliability     | All checkout/return operations must be atomic (ACID transactions)                                                          | Transaction isolation                |
| NFR-14   | Reliability     | System must handle Redis unavailability gracefully (fallback to database)                                                  | Graceful degradation                 |
| NFR-15   | Observability   | All operations must produce structured JSON logs with request correlation IDs                                               | Correlation ID propagation           |
| NFR-16   | Portability     | Entire system must run via a single `docker-compose up` command                                                             | One-command deployment               |

---

## 7. Data Model

### 7.1 Book Catalog Tables

#### Table: `books`

| Column              | Type                | Constraints                            | Description                          |
|---------------------|---------------------|----------------------------------------|--------------------------------------|
| `id`                | `UUID`              | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Unique book identifier             |
| `isbn`              | `VARCHAR(17)`       | `UNIQUE, NOT NULL`                     | ISBN-13 format                       |
| `title`             | `VARCHAR(500)`      | `NOT NULL`                             | Book title                           |
| `authors`           | `TEXT[]`            | `NOT NULL`                             | Array of author names                |
| `genre`             | `VARCHAR(100)`      | `NOT NULL`                             | Primary genre                        |
| `publisher`         | `VARCHAR(255)`      |                                        | Publisher name                       |
| `publication_year`  | `INTEGER`           |                                        | Year of publication                  |
| `description`       | `TEXT`              |                                        | Book description / synopsis          |
| `tags`              | `TEXT[]`            | `DEFAULT '{}'`                         | Searchable tags                      |
| `pages`             | `INTEGER`           |                                        | Number of pages                      |
| `language`          | `VARCHAR(50)`       | `DEFAULT 'English'`                    | Book language                        |
| `average_rating`    | `DECIMAL(3,2)`      | `DEFAULT 0.00`                         | Computed average rating              |
| `total_reviews`     | `INTEGER`           | `DEFAULT 0`                            | Number of reviews                    |
| `search_vector`     | `TSVECTOR`          |                                        | **Full-text search vector**          |
| `is_active`         | `BOOLEAN`           | `DEFAULT true`                         | Soft delete flag                     |
| `created_at`        | `TIMESTAMPTZ`       | `DEFAULT NOW()`                        | Creation timestamp                   |
| `updated_at`        | `TIMESTAMPTZ`       | `DEFAULT NOW()`                        | Last update timestamp                |

**Full-Text Search Index**:
```sql
CREATE INDEX idx_books_search ON books USING GIN(search_vector);
```

**Search Vector Trigger** (see Appendix B for full SQL):
```sql
-- Weighted search vector: title (A), authors (B), description (C), tags (D)
CREATE TRIGGER books_search_vector_update
  BEFORE INSERT OR UPDATE ON books
  FOR EACH ROW EXECUTE FUNCTION books_search_vector_trigger();
```

#### Table: `book_copies`

| Column            | Type              | Constraints                            | Description                     |
|-------------------|-------------------|----------------------------------------|---------------------------------|
| `id`              | `UUID`            | `PRIMARY KEY`                          | Copy identifier                 |
| `book_id`         | `UUID`            | `FK -> books(id), NOT NULL`            | Parent book                     |
| `accession_number`| `VARCHAR(20)`     | `UNIQUE, NOT NULL`                     | Library accession number        |
| `condition`       | `VARCHAR(20)`     | `DEFAULT 'good'`                       | new, good, fair, poor, damaged  |
| `shelf_location`  | `VARCHAR(50)`     |                                        | Physical location (e.g., A3-S2) |
| `status`          | `VARCHAR(20)`     | `DEFAULT 'available'`                  | available, checked_out, reserved, lost, maintenance |
| `acquired_date`   | `DATE`            |                                        | Date copy was acquired          |
| `version`         | `INTEGER`         | `DEFAULT 1, NOT NULL`                  | Optimistic locking version      |
| `created_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Creation timestamp              |
| `updated_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Last update timestamp           |

**Index**: `CREATE INDEX idx_copies_book ON book_copies(book_id);`
**Index**: `CREATE INDEX idx_copies_status ON book_copies(status);`

### 7.2 Member Tables

#### Table: `members`

| Column            | Type              | Constraints                            | Description                     |
|-------------------|-------------------|----------------------------------------|---------------------------------|
| `id`              | `UUID`            | `PRIMARY KEY, DEFAULT gen_random_uuid()` | Unique member identifier      |
| `member_id`       | `VARCHAR(15)`     | `UNIQUE, NOT NULL`                     | Format: `LIB-YYYY-NNNN`        |
| `email`           | `VARCHAR(255)`    | `UNIQUE, NOT NULL`                     | Login email                     |
| `password_hash`   | `VARCHAR(255)`    | `NOT NULL`                             | bcrypt hashed password          |
| `first_name`      | `VARCHAR(100)`    | `NOT NULL`                             | First name                      |
| `last_name`       | `VARCHAR(100)`    | `NOT NULL`                             | Last name                       |
| `member_type`     | `VARCHAR(20)`     | `NOT NULL`                             | student, faculty, staff         |
| `department`      | `VARCHAR(100)`    |                                        | Academic department              |
| `tier`            | `VARCHAR(20)`     | `DEFAULT 'bronze'`                     | bronze, silver, gold            |
| `role`            | `VARCHAR(20)`     | `DEFAULT 'member'`                     | member, librarian, admin        |
| `is_active`       | `BOOLEAN`         | `DEFAULT true`                         | Account active status           |
| `max_borrows`     | `INTEGER`         | `DEFAULT 3`                            | Max concurrent borrows (tier-based) |
| `loan_duration_days`| `INTEGER`       | `DEFAULT 14`                           | Loan period in days (tier-based)  |
| `total_borrows`   | `INTEGER`         | `DEFAULT 0`                            | Lifetime borrow count           |
| `created_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Registration timestamp          |
| `updated_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Last update timestamp           |

### 7.3 Borrowing Tables

#### Table: `borrowings`

| Column            | Type              | Constraints                            | Description                     |
|-------------------|-------------------|----------------------------------------|---------------------------------|
| `id`              | `UUID`            | `PRIMARY KEY`                          | Borrowing record identifier     |
| `member_id`       | `UUID`            | `FK -> members(id), NOT NULL`          | Borrowing member                |
| `book_id`         | `UUID`            | `FK -> books(id), NOT NULL`            | Borrowed book                   |
| `copy_id`         | `UUID`            | `FK -> book_copies(id), NOT NULL`      | Specific copy borrowed          |
| `status`          | `VARCHAR(20)`     | `NOT NULL, DEFAULT 'active'`           | active, returned, overdue, lost |
| `borrowed_at`     | `TIMESTAMPTZ`     | `NOT NULL, DEFAULT NOW()`              | Checkout timestamp              |
| `due_date`        | `DATE`            | `NOT NULL`                             | Return due date                 |
| `returned_at`     | `TIMESTAMPTZ`     |                                        | Actual return timestamp         |
| `renewal_count`   | `INTEGER`         | `DEFAULT 0`                            | Number of renewals used         |
| `max_renewals`    | `INTEGER`         | `DEFAULT 2`                            | Maximum allowed renewals        |
| `created_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Record creation timestamp       |
| `updated_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Last update timestamp           |

**Index**: `CREATE INDEX idx_borrowings_member ON borrowings(member_id);`
**Index**: `CREATE INDEX idx_borrowings_copy ON borrowings(copy_id);`
**Index**: `CREATE INDEX idx_borrowings_status ON borrowings(status);`
**Index**: `CREATE INDEX idx_borrowings_due_date ON borrowings(due_date) WHERE status = 'active';`

#### Table: `reservations`

| Column            | Type              | Constraints                            | Description                     |
|-------------------|-------------------|----------------------------------------|---------------------------------|
| `id`              | `UUID`            | `PRIMARY KEY`                          | Reservation identifier          |
| `member_id`       | `UUID`            | `FK -> members(id), NOT NULL`          | Reserving member                |
| `book_id`         | `UUID`            | `FK -> books(id), NOT NULL`            | Reserved book (any copy)        |
| `status`          | `VARCHAR(20)`     | `DEFAULT 'pending'`                    | pending, notified, fulfilled, expired, cancelled |
| `queue_position`  | `INTEGER`         | `NOT NULL`                             | Position in reservation queue   |
| `notified_at`     | `TIMESTAMPTZ`     |                                        | When member was notified        |
| `expires_at`      | `TIMESTAMPTZ`     |                                        | Reservation expiry (48h after notification) |
| `fulfilled_at`    | `TIMESTAMPTZ`     |                                        | When reservation was collected  |
| `created_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Reservation creation            |

**Constraint**: `UNIQUE(member_id, book_id)` --- one reservation per member per book.
**Index**: `CREATE INDEX idx_reservations_book_status ON reservations(book_id, status);`

### 7.4 Fine Tables

#### Table: `fines`

| Column            | Type              | Constraints                            | Description                     |
|-------------------|-------------------|----------------------------------------|---------------------------------|
| `id`              | `UUID`            | `PRIMARY KEY`                          | Fine identifier                 |
| `member_id`       | `UUID`            | `FK -> members(id), NOT NULL`          | Member with fine                |
| `borrowing_id`    | `UUID`            | `FK -> borrowings(id), NOT NULL`       | Related borrowing               |
| `fine_type`       | `VARCHAR(30)`     | `NOT NULL`                             | overdue, damaged, lost          |
| `amount`          | `DECIMAL(10,2)`   | `NOT NULL`                             | Fine amount                     |
| `paid_amount`     | `DECIMAL(10,2)`   | `DEFAULT 0.00`                         | Amount paid so far              |
| `status`          | `VARCHAR(20)`     | `DEFAULT 'outstanding'`                | outstanding, partial, paid, waived |
| `overdue_days`    | `INTEGER`         |                                        | Number of overdue days          |
| `daily_rate`      | `DECIMAL(5,2)`    |                                        | Rate applied per day            |
| `waiver_reason`   | `TEXT`            |                                        | Reason if waived                |
| `waived_by`       | `UUID`            | `FK -> members(id)`                    | Librarian who waived            |
| `created_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Fine creation timestamp         |
| `updated_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Last update timestamp           |

**Index**: `CREATE INDEX idx_fines_member_status ON fines(member_id, status);`

### 7.5 Review & Recommendation Tables

#### Table: `reviews`

| Column            | Type              | Constraints                            | Description                     |
|-------------------|-------------------|----------------------------------------|---------------------------------|
| `id`              | `UUID`            | `PRIMARY KEY`                          | Review identifier               |
| `member_id`       | `UUID`            | `FK -> members(id), NOT NULL`          | Reviewing member                |
| `book_id`         | `UUID`            | `FK -> books(id), NOT NULL`            | Reviewed book                   |
| `rating`          | `INTEGER`         | `NOT NULL, CHECK(rating BETWEEN 1 AND 5)` | Star rating (1-5)          |
| `review_text`     | `TEXT`            |                                        | Optional review text            |
| `is_verified`     | `BOOLEAN`         | `DEFAULT false`                        | True if member actually borrowed the book |
| `created_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Review creation timestamp       |
| `updated_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Last update timestamp           |

**Constraint**: `UNIQUE(member_id, book_id)` --- one review per member per book.

### 7.6 Configuration Table

#### Table: `library_config`

| Column            | Type              | Constraints                            | Description                     |
|-------------------|-------------------|----------------------------------------|---------------------------------|
| `id`              | `UUID`            | `PRIMARY KEY`                          | Config identifier               |
| `config_key`      | `VARCHAR(100)`    | `UNIQUE, NOT NULL`                     | Configuration key               |
| `config_value`    | `JSONB`           | `NOT NULL`                             | Configuration value             |
| `description`     | `TEXT`            |                                        | Human-readable description      |
| `updated_at`      | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Last update timestamp           |
| `updated_by`      | `UUID`            | `FK -> members(id)`                    | Last updated by                 |

**Example Configurations**:
| Key                          | Value                                                  |
|------------------------------|--------------------------------------------------------|
| `fine_rate_bronze`           | `{"per_day": 1.00, "max_cap": 25.00, "grace_days": 1}` |
| `fine_rate_silver`           | `{"per_day": 0.75, "max_cap": 20.00, "grace_days": 2}` |
| `fine_rate_gold`             | `{"per_day": 0.50, "max_cap": 15.00, "grace_days": 3}` |
| `fine_blocking_threshold`    | `{"amount": 10.00}`                                    |
| `reservation_expiry_hours`   | `{"hours": 48}`                                        |
| `holidays_2025`              | `{"dates": ["2025-01-01", "2025-01-20", "2025-12-25"]}`|
| `damaged_book_charge`        | `{"percentage_of_price": 50}`                          |
| `lost_book_charge`           | `{"percentage_of_price": 100, "processing_fee": 5.00}` |

### 7.7 Search Suggestions Table

#### Table: `search_suggestions`

| Column            | Type              | Constraints                            | Description                     |
|-------------------|-------------------|----------------------------------------|---------------------------------|
| `id`              | `UUID`            | `PRIMARY KEY`                          | Suggestion identifier           |
| `term`            | `VARCHAR(255)`    | `UNIQUE, NOT NULL`                     | Search term                     |
| `frequency`       | `INTEGER`         | `DEFAULT 1`                            | Search frequency count          |
| `last_searched`   | `TIMESTAMPTZ`     | `DEFAULT NOW()`                        | Last time this term was searched|
| `source`          | `VARCHAR(20)`     | `NOT NULL`                             | title, author, tag, user_query  |

**Index**: `CREATE INDEX idx_suggestions_term ON search_suggestions USING GIN(term gin_trgm_ops);`

---

## 8. API Contracts

### 8.1 Search & Discovery APIs

#### GET `/api/v1/books/search`

**Description**: Full-text search across the book catalog with relevance scoring and highlighting.

**Query Parameters**:
| Parameter       | Type     | Required | Description                            |
|-----------------|----------|----------|----------------------------------------|
| `q`             | string   | Yes      | Natural language search query          |
| `genre`         | string   | No       | Filter by genre                        |
| `author`        | string   | No       | Filter by author name                  |
| `year_from`     | integer  | No       | Publication year range start           |
| `year_to`       | integer  | No       | Publication year range end             |
| `available`     | boolean  | No       | Only show books with available copies  |
| `min_rating`    | float    | No       | Minimum average rating                 |
| `page`          | integer  | No       | Page number (default: 1)              |
| `page_size`     | integer  | No       | Results per page (default: 20)        |
| `sort_by`       | string   | No       | relevance, title, rating, year        |

**Response (200 OK)**:
```json
{
  "query": "database systems design",
  "results": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "isbn": "978-0-13-454862-0",
      "title": "Database System Concepts",
      "authors": ["Abraham Silberschatz", "Henry F. Korth", "S. Sudarshan"],
      "genre": "Computer Science",
      "publication_year": 2019,
      "description": "Comprehensive introduction to database system concepts including relational model, SQL, database design, and transaction management.",
      "tags": ["databases", "SQL", "relational", "normalization"],
      "average_rating": 4.35,
      "total_reviews": 28,
      "relevance_score": 0.9823,
      "highlights": {
        "title": "<b>Database</b> <b>System</b> Concepts",
        "description": "Comprehensive introduction to <b>database</b> <b>system</b> concepts including relational model, SQL, <b>database</b> <b>design</b>, and transaction management."
      },
      "availability": {
        "total_copies": 5,
        "available_copies": 2,
        "status": "available"
      }
    },
    {
      "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "isbn": "978-0-32-112521-7",
      "title": "Fundamentals of Database Systems",
      "authors": ["Ramez Elmasri", "Shamkant B. Navathe"],
      "genre": "Computer Science",
      "publication_year": 2015,
      "description": "A thorough foundation in database design, languages, and system implementation for modern database systems.",
      "tags": ["databases", "ER model", "SQL", "design"],
      "average_rating": 4.10,
      "total_reviews": 19,
      "relevance_score": 0.8745,
      "highlights": {
        "title": "Fundamentals of <b>Database</b> <b>Systems</b>",
        "description": "A thorough foundation in <b>database</b> <b>design</b>, languages, and <b>system</b> implementation for modern <b>database</b> <b>systems</b>."
      },
      "availability": {
        "total_copies": 3,
        "available_copies": 0,
        "next_available_date": "2025-02-05",
        "status": "all_checked_out"
      }
    }
  ],
  "facets": {
    "genres": [
      {"name": "Computer Science", "count": 15},
      {"name": "Information Systems", "count": 4}
    ],
    "authors": [
      {"name": "Abraham Silberschatz", "count": 3},
      {"name": "Ramez Elmasri", "count": 2}
    ],
    "years": [
      {"range": "2020-2025", "count": 5},
      {"range": "2015-2019", "count": 8},
      {"range": "2010-2014", "count": 6}
    ],
    "availability": [
      {"status": "available", "count": 12},
      {"status": "all_checked_out", "count": 7}
    ]
  },
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 19,
    "total_pages": 1
  },
  "search_time_ms": 45
}
```

#### GET `/api/v1/books/suggestions`

**Description**: Autocomplete search suggestions.

**Query Parameters**:
| Parameter | Type    | Required | Description               |
|-----------|---------|----------|---------------------------|
| `prefix`  | string  | Yes      | Partial search term       |
| `limit`   | integer | No       | Max suggestions (default: 8) |

**Response (200 OK)**:
```json
{
  "prefix": "data",
  "suggestions": [
    {"term": "database systems", "source": "title", "frequency": 142},
    {"term": "data structures", "source": "title", "frequency": 98},
    {"term": "data science", "source": "tag", "frequency": 76},
    {"term": "data mining", "source": "title", "frequency": 45},
    {"term": "database design", "source": "user_query", "frequency": 38}
  ]
}
```

### 8.2 Borrowing Engine APIs

#### POST `/api/v1/borrowings/checkout`

**Description**: Check out a book copy to a member.

**Request Body**:
```json
{
  "member_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "book_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "copy_id": "c3d4e5f6-a7b8-9012-cdef-123456789012"
}
```

**Processing Steps**:

| Step | Validation                           | Action                                        | Failure Response               |
|------|--------------------------------------|-----------------------------------------------|--------------------------------|
| 1    | Verify member exists and is active   | Query members table                           | `MEMBER_NOT_FOUND`             |
| 2    | Check outstanding fine threshold     | Sum unpaid fines for member                   | `FINES_THRESHOLD_EXCEEDED`     |
| 3    | Check concurrent borrow limit        | Count active borrows vs. `max_borrows`        | `BORROW_LIMIT_REACHED`         |
| 4    | Verify book and copy exist           | Query books and book_copies tables            | `BOOK_NOT_FOUND`               |
| 5    | Check copy availability              | Verify `status = 'available'` with opt. lock  | `COPY_NOT_AVAILABLE`           |
| 6    | Check for duplicate active borrowing | Ensure member doesn't already have this book  | `ALREADY_BORROWED`             |
| 7    | Atomically update copy status        | Set `status = 'checked_out'` with version check | `CONCURRENT_MODIFICATION`    |
| 8    | Create borrowing record              | Insert into borrowings with computed due date | ---                            |
| 9    | Update member borrow count           | Increment `total_borrows`                     | ---                            |
| 10   | Invalidate relevant caches           | Clear book availability cache                 | ---                            |

**Response (201 Created)**:
```json
{
  "borrowing_id": "d4e5f6a7-b8c9-0123-defa-234567890123",
  "member_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "book": {
    "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    "title": "Database System Concepts",
    "isbn": "978-0-13-454862-0"
  },
  "copy": {
    "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
    "accession_number": "ACC-2024-00142"
  },
  "borrowed_at": "2025-01-15T10:30:00Z",
  "due_date": "2025-01-29",
  "loan_duration_days": 14,
  "renewal_count": 0,
  "max_renewals": 2,
  "member_tier": "bronze",
  "active_borrows_count": 2,
  "max_borrows": 3,
  "message": "Successfully checked out 'Database System Concepts'. Due date: January 29, 2025."
}
```

**Error Responses**:
| Status | Code                        | Description                                        |
|--------|-----------------------------|----------------------------------------------------|
| 400    | `VALIDATION_ERROR`          | Missing or invalid fields                          |
| 404    | `MEMBER_NOT_FOUND`          | Member ID does not exist or is inactive            |
| 404    | `BOOK_NOT_FOUND`            | Book or copy does not exist                        |
| 409    | `COPY_NOT_AVAILABLE`        | Copy is already checked out, reserved, or lost     |
| 409    | `BORROW_LIMIT_REACHED`      | Member has reached max concurrent borrows          |
| 409    | `FINES_THRESHOLD_EXCEEDED`  | Outstanding fines exceed blocking threshold        |
| 409    | `ALREADY_BORROWED`          | Member already has an active borrow for this book  |
| 429    | `CONCURRENT_MODIFICATION`   | Optimistic lock conflict, client should retry      |

#### POST `/api/v1/borrowings/return`

**Description**: Return a borrowed book, calculate fines, and trigger reservation fulfillment.

**Request Body**:
```json
{
  "borrowing_id": "d4e5f6a7-b8c9-0123-defa-234567890123",
  "condition": "good"
}
```

**Response (200 OK)** --- Returned with Fine and Reservation Trigger:
```json
{
  "borrowing_id": "d4e5f6a7-b8c9-0123-defa-234567890123",
  "status": "returned",
  "returned_at": "2025-02-05T14:20:00Z",
  "book": {
    "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    "title": "Database System Concepts"
  },
  "due_date": "2025-01-29",
  "days_overdue": 7,
  "fine": {
    "fine_id": "e5f6a7b8-c9d0-1234-efab-345678901234",
    "fine_type": "overdue",
    "calculation": {
      "overdue_days": 7,
      "grace_period_days": 1,
      "billable_days": 6,
      "holidays_excluded": 0,
      "daily_rate": 1.00,
      "subtotal": 6.00,
      "max_cap": 25.00,
      "final_amount": 6.00
    },
    "amount": 6.00,
    "status": "outstanding"
  },
  "reservation_triggered": {
    "triggered": true,
    "reserved_for_member_id": "f6a7b8c9-d0e1-2345-fabc-456789012345",
    "reservation_id": "a7b8c9d0-e1f2-3456-abcd-567890123456",
    "notification_sent": true,
    "pickup_deadline": "2025-02-07T14:20:00Z"
  },
  "message": "Book returned. Overdue fine of $6.00 applied. Book reserved for next member in queue."
}
```

**Response (200 OK)** --- Returned on Time, No Reservation:
```json
{
  "borrowing_id": "d4e5f6a7-b8c9-0123-defa-234567890123",
  "status": "returned",
  "returned_at": "2025-01-28T09:15:00Z",
  "book": {
    "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    "title": "Database System Concepts"
  },
  "due_date": "2025-01-29",
  "days_overdue": 0,
  "fine": null,
  "reservation_triggered": {
    "triggered": false
  },
  "message": "Book returned on time. No fines applied."
}
```

### 8.3 Recommendation Engine APIs

#### GET `/api/v1/recommendations/{member_id}`

**Description**: Get personalized book recommendations for a member using collaborative filtering.

**Query Parameters**:
| Parameter | Type    | Required | Description                          |
|-----------|---------|----------|--------------------------------------|
| `limit`   | integer | No       | Max recommendations (default: 10)    |
| `method`  | string  | No       | collaborative, content, trending     |

**Response (200 OK)**:
```json
{
  "member_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "method": "collaborative",
  "recommendations": [
    {
      "book_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
      "title": "Designing Data-Intensive Applications",
      "authors": ["Martin Kleppmann"],
      "genre": "Computer Science",
      "average_rating": 4.72,
      "similarity_score": 0.89,
      "reason": "Members who borrowed 'Database System Concepts' and 'Clean Code' also enjoyed this book",
      "availability": {
        "total_copies": 3,
        "available_copies": 1,
        "status": "available"
      }
    },
    {
      "book_id": "d4e5f6a7-b8c9-0123-defa-234567890123",
      "title": "System Design Interview",
      "authors": ["Alex Xu"],
      "genre": "Computer Science",
      "average_rating": 4.45,
      "similarity_score": 0.76,
      "reason": "Based on your interest in databases and distributed systems",
      "availability": {
        "total_copies": 4,
        "available_copies": 2,
        "status": "available"
      }
    },
    {
      "book_id": "e5f6a7b8-c9d0-1234-efab-345678901234",
      "title": "The Pragmatic Programmer",
      "authors": ["David Thomas", "Andrew Hunt"],
      "genre": "Software Engineering",
      "average_rating": 4.55,
      "similarity_score": 0.71,
      "reason": "Frequently borrowed together with books in your reading history",
      "availability": {
        "total_copies": 6,
        "available_copies": 0,
        "next_available_date": "2025-02-10",
        "status": "all_checked_out"
      }
    }
  ],
  "based_on_books": [
    {"title": "Database System Concepts", "borrowed_at": "2024-09-15"},
    {"title": "Clean Code", "borrowed_at": "2024-11-01"},
    {"title": "Introduction to Algorithms", "borrowed_at": "2024-12-10"}
  ],
  "generated_at": "2025-01-15T10:30:00Z",
  "cache_ttl_seconds": 3600
}
```

### 8.4 Analytics APIs

#### GET `/api/v1/analytics/dashboard`

**Description**: Get library analytics dashboard data.

**Headers**: `Authorization: Bearer <librarian_jwt_token>`

**Response (200 OK)**:
```json
{
  "snapshot_at": "2025-01-15T10:30:00Z",
  "overview": {
    "total_books": 2450,
    "total_copies": 5830,
    "total_members": 1240,
    "active_members_this_month": 342
  },
  "borrowing_stats": {
    "active_borrows": 487,
    "overdue_borrows": 23,
    "borrows_this_month": 156,
    "returns_this_month": 142,
    "average_loan_duration_days": 12.4
  },
  "popular_books_this_month": [
    {"title": "Database System Concepts", "borrow_count": 18, "book_id": "..."},
    {"title": "Clean Code", "borrow_count": 15, "book_id": "..."},
    {"title": "Introduction to Algorithms", "borrow_count": 12, "book_id": "..."},
    {"title": "Design Patterns", "borrow_count": 11, "book_id": "..."},
    {"title": "The Pragmatic Programmer", "borrow_count": 10, "book_id": "..."}
  ],
  "busiest_hours": [
    {"hour": "10:00-11:00", "avg_checkouts": 8.5},
    {"hour": "14:00-15:00", "avg_checkouts": 7.2},
    {"hour": "11:00-12:00", "avg_checkouts": 6.8}
  ],
  "genre_distribution": [
    {"genre": "Computer Science", "percentage": 35.2, "count": 863},
    {"genre": "Mathematics", "percentage": 15.8, "count": 387},
    {"genre": "Engineering", "percentage": 12.1, "count": 297},
    {"genre": "Physics", "percentage": 9.5, "count": 233},
    {"genre": "Other", "percentage": 27.4, "count": 670}
  ],
  "fine_stats": {
    "total_outstanding_fines": 1245.50,
    "fines_collected_this_month": 487.25,
    "waivers_this_month": 3,
    "members_with_blocking_fines": 8
  },
  "member_tier_distribution": [
    {"tier": "bronze", "count": 890, "percentage": 71.8},
    {"tier": "silver", "count": 280, "percentage": 22.6},
    {"tier": "gold", "count": 70, "percentage": 5.6}
  ]
}
```

---

## 9. Weekly Milestones

### Week 1: Foundation & Design (Days 1-5)

| Day | Deliverable                                      | AI-Native Activity                                    |
|-----|--------------------------------------------------|-------------------------------------------------------|
| 1   | Project kickoff, team formation, repo setup       | AI-assisted project scaffolding and module structure   |
| 2   | System architecture document (SDD Sections 1-3)  | AI-generated architecture diagrams and module boundary analysis |
| 3   | Data model design with full-text search setup     | AI-assisted schema generation, tsvector configuration  |
| 4   | API contract definitions (OpenAPI specs)          | AI-generated API stubs and Pydantic schemas            |
| 5   | Docker Compose setup, PostgreSQL + Redis init     | AI-assisted Dockerfile, compose config, and seed scripts |

**Review Checklist**:
- [ ] SDD document covers all 7 modules with clear boundaries and dependency rules
- [ ] Data model includes `tsvector` columns and GIN indexes for full-text search
- [ ] API contracts include request/response schemas and error codes
- [ ] Docker Compose starts application, PostgreSQL, and Redis
- [ ] Repository follows clean architecture folder structure

### Week 2: Core Implementation (Days 6-10)

| Day | Deliverable                                      | AI-Native Activity                                    |
|-----|--------------------------------------------------|-------------------------------------------------------|
| 6   | Book Catalog module: CRUD, copy management        | AI pair-programming for SQLAlchemy models and routes   |
| 7   | Member module: registration, auth, JWT, tiers     | AI-assisted auth flow and RBAC implementation          |
| 8   | Borrowing Engine: checkout, return, concurrency   | AI-generated concurrency handling patterns             |
| 9   | Borrowing Engine: reservations, renewals          | AI-assisted state machine and queue implementation     |
| 10  | Fine Calculation: configurable rules engine       | AI-assisted strategy pattern and rule configuration    |

**Review Checklist**:
- [ ] Book CRUD with copy management works end-to-end
- [ ] Member registration, login, and JWT authentication functional
- [ ] Checkout/return handles concurrent access correctly (optimistic locking)
- [ ] Reservation FIFO queue maintains ordering
- [ ] Fine calculation handles all scenarios (overdue, grace period, holidays)

### Week 3: Advanced Features & Testing (Days 11-15)

| Day | Deliverable                                      | AI-Native Activity                                    |
|-----|--------------------------------------------------|-------------------------------------------------------|
| 11  | Search & Discovery: full-text search, facets      | AI-assisted tsvector query optimization                |
| 12  | Search & Discovery: autocomplete, suggestions     | AI-generated trigram similarity queries                 |
| 13  | Recommendation Engine: collaborative filtering    | AI-assisted algorithm implementation and testing       |
| 14  | Analytics module: dashboard aggregations          | AI-generated aggregation queries and caching           |
| 15  | Integration testing, concurrency testing          | AI-generated test suites and load test scripts         |

**Review Checklist**:
- [ ] Full-text search returns relevant results with highlights in < 200ms
- [ ] Autocomplete responds in < 100ms
- [ ] Recommendations are reasonable and include similarity scores
- [ ] Analytics dashboard shows accurate real-time metrics
- [ ] Integration tests cover all critical flows
- [ ] No data corruption under concurrent checkout/return

### Week 4: Polish, CI/CD & Presentation (Days 16-20)

| Day | Deliverable                                      | AI-Native Activity                                    |
|-----|--------------------------------------------------|-------------------------------------------------------|
| 16  | CI/CD pipeline setup (GitHub Actions)             | AI-generated workflow configurations                   |
| 17  | Redis caching layer implementation and tuning     | AI-assisted cache invalidation strategy                |
| 18  | API documentation and Swagger UI finalization     | AI-assisted documentation generation and review        |
| 19  | Final SDD document update and presentation prep   | AI-assisted documentation polish and slide generation  |
| 20  | Final demo and project presentation               | AI-assisted demo script and presentation rehearsal     |

**Review Checklist**:
- [ ] CI pipeline runs tests, linting on every push
- [ ] Redis caching is active with measurable performance improvement
- [ ] API documentation is complete and interactive (Swagger UI)
- [ ] Final SDD document is comprehensive and up-to-date
- [ ] Demo covers full-text search, checkout, fines, recommendations, analytics

---

## 10. Evaluation Rubric

### 10.1 Category Weights

| Category                     | Weight | Description                                         |
|------------------------------|--------|-----------------------------------------------------|
| Software Design Document     | 25%    | Architecture, data model, API contracts, decisions   |
| Code Quality & Implementation| 25%    | Clean code, patterns, concurrency, module boundaries |
| Testing                      | 20%    | Unit, integration, concurrency, coverage             |
| CI/CD & DevOps               | 15%    | Pipeline, Docker, Redis, automated deployment        |
| Documentation & Presentation | 15%    | README, API docs, demo, knowledge sharing            |

### 10.2 Detailed Criteria

#### Software Design Document (25%)

| Level               | Score  | Criteria                                                                                                          |
|---------------------|--------|-------------------------------------------------------------------------------------------------------------------|
| **Excellent**       | 23-25  | Comprehensive SDD with clear modular monolith architecture, complete data model with full-text search design, all API contracts with examples, well-justified design decisions. Module boundaries and dependency rules clearly documented. |
| **Good**            | 18-22  | Complete SDD covering all sections. Minor gaps in module interaction documentation. Data model and APIs are functional and well-defined. Clean architecture layers documented. |
| **Satisfactory**    | 13-17  | SDD covers essential sections but lacks depth in search design or recommendation algorithm documentation. Data model functional but may miss indexing strategy. |
| **Needs Improvement**| 0-12  | SDD is incomplete or missing critical sections. Module boundaries unclear. Data model lacks full-text search support. API contracts poorly defined. |

#### Code Quality & Implementation (25%)

| Level               | Score  | Criteria                                                                                                          |
|---------------------|--------|-------------------------------------------------------------------------------------------------------------------|
| **Excellent**       | 23-25  | Clean, well-structured code following clean architecture. Module boundaries enforced via Python packages and interfaces. Full-text search with relevance ranking implemented. Collaborative filtering functional. Fine calculation handles all scenarios. Optimistic locking for concurrent access. |
| **Good**            | 18-22  | Code is organized with clear module separation. Most features implemented correctly. Search works with basic relevance. Recommendation engine provides reasonable results. |
| **Satisfactory**    | 13-17  | Code is functional but module boundaries may be leaky. Basic search implemented. Recommendation or analytics may be partial. Fine calculation covers basic scenarios. |
| **Needs Improvement**| 0-12  | Code is disorganized with no clear module structure. Missing full-text search. No recommendation engine. Fine calculation incomplete. |

#### Testing (20%)

| Level               | Score  | Criteria                                                                                                          |
|---------------------|--------|-------------------------------------------------------------------------------------------------------------------|
| **Excellent**       | 18-20  | Comprehensive test suite: unit tests for business logic, integration tests for API endpoints, concurrency tests for checkout/return, fine calculation edge cases. Code coverage > 80%. |
| **Good**            | 14-17  | Good test coverage for main flows. Integration tests for key endpoints. Some concurrency testing. Coverage > 60%. Fine calculation tests cover common scenarios. |
| **Satisfactory**    | 10-13  | Basic unit tests for core functionality. Some integration tests. Limited concurrency testing. Coverage > 40%. |
| **Needs Improvement**| 0-9   | Minimal or no tests. No integration testing. No concurrency testing. Coverage < 40%. |

#### CI/CD & DevOps (15%)

| Level               | Score  | Criteria                                                                                                          |
|---------------------|--------|-------------------------------------------------------------------------------------------------------------------|
| **Excellent**       | 14-15  | Full CI/CD pipeline with automated testing, linting, and build. Docker Compose for app + PostgreSQL + Redis. Health checks configured. Redis caching demonstrably improves performance. |
| **Good**            | 11-13  | CI pipeline runs tests on push. Docker Compose works for all components. Basic health checks. Redis configured but caching strategy basic. |
| **Satisfactory**    | 8-10   | Basic CI pipeline exists. Docker Compose mostly works. Redis present but minimally used. |
| **Needs Improvement**| 0-7   | No CI/CD pipeline. Docker setup incomplete. No Redis integration. Manual deployment only. |

#### Documentation & Presentation (15%)

| Level               | Score  | Criteria                                                                                                          |
|---------------------|--------|-------------------------------------------------------------------------------------------------------------------|
| **Excellent**       | 14-15  | Comprehensive README with setup instructions. Interactive API docs (Swagger). Clear demo covering search, checkout, fines, recommendations. Effective discussion of AI-Native methodology and clean architecture decisions. |
| **Good**            | 11-13  | Good README with setup steps. API documentation available. Demo covers main features. Some discussion of methodology. |
| **Satisfactory**    | 8-10   | Basic README present. Some API documentation. Demo covers basic flow. Limited methodology discussion. |
| **Needs Improvement**| 0-7   | Missing or inadequate README. No API documentation. Demo incomplete or non-functional. |

---

## 11. Interim Review Checkpoints

### Checkpoint 1: Architecture & Data Model Review (End of Day 3)

**Demo Script**:
1. Present modular monolith architecture and explain module boundaries
2. Walk through clean architecture layers with code examples
3. Explain the full-text search data model (tsvector, indexes, triggers)
4. Show Docker Compose configuration with PostgreSQL and Redis

**Key Questions**:
- Why did you choose a modular monolith over microservices for this project?
- How do you enforce module boundaries in a monolithic codebase?
- Explain how the `tsvector` column and GIN index enable full-text search
- What is your caching invalidation strategy for book catalog changes?
- How does the member tier system affect fine calculations?

### Checkpoint 2: Core Features Demo (End of Day 10)

**Demo Script**:
1. Register a member and authenticate via JWT
2. Add books with copies to the catalog
3. Check out a book and demonstrate concurrent access handling
4. Return an overdue book and show fine calculation
5. Place a reservation and demonstrate FIFO queue

**Key Questions**:
- Walk through the checkout flow step by step
- How does optimistic locking prevent double-checkout of the same copy?
- Show the fine calculation for a 10-day overdue book with a 2-day grace period
- What happens when a reserved book is returned?
- How does the tier system affect loan duration and fine rates?

### Checkpoint 3: Advanced Features & Testing (End of Day 15)

**Demo Script**:
1. Execute a full-text search query and show relevance scoring
2. Demonstrate autocomplete/suggestion functionality
3. Show personalized recommendations with similarity scores
4. Display analytics dashboard with real-time metrics
5. Run integration and concurrency test suites

**Key Questions**:
- How does the full-text search weight title vs. description matches?
- Explain the collaborative filtering algorithm and its complexity
- What is your cache hit ratio for search queries?
- Show concurrent checkout tests --- any data corruption?
- How do you handle the cold-start problem in recommendations?

### Checkpoint 4: Final Review & Presentation (Day 20)

**Demo Script**:
1. Full end-to-end demo: member journey from registration to recommendations
2. Show CI/CD pipeline execution
3. Present API documentation (Swagger UI)
4. Demonstrate Redis caching impact (with/without cache comparison)
5. Present final SDD document and lessons learned

**Key Questions**:
- What was the most challenging module to implement and why?
- How did AI-Native methodology impact your development process?
- What would you change if migrating this to microservices?
- How would you handle a catalog of 1 million books?
- What are the cold-start mitigation strategies for your recommendation engine?

---

## 12. Appendix

### A. Repository Structure

```
smart-library-system/
+-- README.md
+-- docker-compose.yml
+-- .github/
|   +-- workflows/
|       +-- ci.yml
+-- docs/
|   +-- SDD.md
|   +-- architecture-diagrams/
|   +-- api-contracts/
+-- alembic/
|   +-- versions/
|   +-- env.py
|   +-- alembic.ini
+-- src/
|   +-- main.py                    # FastAPI application entry point
|   +-- config.py                  # Application configuration
|   +-- dependencies.py            # Dependency injection setup
|   +-- domain/
|   |   +-- entities/
|   |   |   +-- book.py
|   |   |   +-- member.py
|   |   |   +-- borrowing.py
|   |   |   +-- fine.py
|   |   |   +-- reservation.py
|   |   +-- value_objects/
|   |   |   +-- isbn.py
|   |   |   +-- member_tier.py
|   |   +-- events/
|   |   |   +-- borrowing_events.py
|   |   +-- interfaces/
|   |       +-- book_repository.py
|   |       +-- member_repository.py
|   |       +-- borrowing_repository.py
|   +-- application/
|   |   +-- book_catalog/
|   |   |   +-- book_service.py
|   |   |   +-- copy_service.py
|   |   +-- member_mgmt/
|   |   |   +-- member_service.py
|   |   |   +-- auth_service.py
|   |   +-- borrowing_engine/
|   |   |   +-- checkout_service.py
|   |   |   +-- return_service.py
|   |   |   +-- reservation_service.py
|   |   +-- fine_calculation/
|   |   |   +-- fine_service.py
|   |   |   +-- fine_rules.py
|   |   +-- search_discovery/
|   |   |   +-- search_service.py
|   |   |   +-- suggestion_service.py
|   |   +-- recommendation/
|   |   |   +-- recommendation_service.py
|   |   |   +-- collaborative_filter.py
|   |   +-- analytics/
|   |       +-- analytics_service.py
|   +-- infrastructure/
|   |   +-- database/
|   |   |   +-- connection.py
|   |   |   +-- models.py        # SQLAlchemy ORM models
|   |   |   +-- repositories/
|   |   |       +-- book_repo.py
|   |   |       +-- member_repo.py
|   |   |       +-- borrowing_repo.py
|   |   +-- cache/
|   |   |   +-- redis_client.py
|   |   |   +-- cache_manager.py
|   |   +-- external/
|   |       +-- email_service.py
|   +-- presentation/
|       +-- routers/
|       |   +-- book_router.py
|       |   +-- member_router.py
|       |   +-- borrowing_router.py
|       |   +-- search_router.py
|       |   +-- recommendation_router.py
|       |   +-- analytics_router.py
|       +-- schemas/
|       |   +-- book_schemas.py
|       |   +-- member_schemas.py
|       |   +-- borrowing_schemas.py
|       |   +-- search_schemas.py
|       +-- middleware/
|           +-- auth_middleware.py
|           +-- correlation_id.py
+-- tests/
|   +-- unit/
|   |   +-- test_fine_calculation.py
|   |   +-- test_search_ranking.py
|   |   +-- test_collaborative_filter.py
|   +-- integration/
|   |   +-- test_checkout_flow.py
|   |   +-- test_return_with_fine.py
|   |   +-- test_search_api.py
|   |   +-- test_concurrent_checkout.py
|   +-- conftest.py
+-- scripts/
|   +-- seed_data.py
|   +-- setup_fulltext_search.sql
|   +-- load_test.py
+-- requirements.txt
+-- Dockerfile
```

### B. PostgreSQL Full-Text Search Configuration

```sql
-- ============================================================
-- Full-Text Search Setup for Smart Library System
-- ============================================================

-- 1. Enable required extensions
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- For trigram similarity (autocomplete)
CREATE EXTENSION IF NOT EXISTS unaccent;  -- For accent-insensitive search

-- 2. Create custom text search configuration
CREATE TEXT SEARCH CONFIGURATION library_search (COPY = english);
ALTER TEXT SEARCH CONFIGURATION library_search
  ALTER MAPPING FOR asciiword, word, numword
  WITH unaccent, english_stem;

-- 3. Create the search vector update function
CREATE OR REPLACE FUNCTION books_search_vector_trigger()
RETURNS trigger AS $$
BEGIN
  NEW.search_vector :=
    setweight(to_tsvector('library_search', COALESCE(NEW.title, '')), 'A') ||
    setweight(to_tsvector('library_search', COALESCE(array_to_string(NEW.authors, ' '), '')), 'B') ||
    setweight(to_tsvector('library_search', COALESCE(NEW.description, '')), 'C') ||
    setweight(to_tsvector('library_search', COALESCE(array_to_string(NEW.tags, ' '), '')), 'D');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 4. Create trigger to auto-update search vector
CREATE TRIGGER books_search_vector_update
  BEFORE INSERT OR UPDATE OF title, authors, description, tags
  ON books
  FOR EACH ROW
  EXECUTE FUNCTION books_search_vector_trigger();

-- 5. Create GIN index for fast full-text search
CREATE INDEX idx_books_search ON books USING GIN(search_vector);

-- 6. Create trigram index for autocomplete/fuzzy search
CREATE INDEX idx_books_title_trgm ON books USING GIN(title gin_trgm_ops);
CREATE INDEX idx_suggestions_term_trgm ON search_suggestions USING GIN(term gin_trgm_ops);

-- 7. Example search query with relevance ranking and highlights
-- Usage: Search for "database systems design"
SELECT
  b.id,
  b.title,
  b.authors,
  b.genre,
  ts_rank_cd(b.search_vector, query, 32) AS relevance_score,
  ts_headline('library_search', b.title, query,
    'StartSel=<b>, StopSel=</b>, MaxWords=50, MinWords=10') AS title_highlight,
  ts_headline('library_search', b.description, query,
    'StartSel=<b>, StopSel=</b>, MaxWords=80, MinWords=20') AS description_highlight
FROM
  books b,
  to_tsquery('library_search', 'database & systems & design') AS query
WHERE
  b.search_vector @@ query
  AND b.is_active = true
ORDER BY
  relevance_score DESC
LIMIT 20 OFFSET 0;

-- 8. Example autocomplete query using trigram similarity
SELECT
  term,
  source,
  frequency,
  similarity(term, 'datab') AS sim_score
FROM
  search_suggestions
WHERE
  term % 'datab'  -- Trigram similarity operator
  OR term ILIKE 'datab%'
ORDER BY
  sim_score DESC, frequency DESC
LIMIT 8;
```

### C. Collaborative Filtering Algorithm

```python
"""
Item-Based Collaborative Filtering for Book Recommendations

Algorithm: Cosine Similarity on Item Co-occurrence Matrix

Given:
  - B = set of all books
  - M = set of all members
  - R = borrowing matrix where R[m][b] = 1 if member m borrowed book b, else 0

Step 1: Build Co-occurrence Matrix
  For each pair of books (b_i, b_j):
    co_occurrence[b_i][b_j] = count of members who borrowed both b_i and b_j

Step 2: Compute Cosine Similarity
  For each pair of books (b_i, b_j):
    sim(b_i, b_j) = co_occurrence[b_i][b_j] / (sqrt(freq[b_i]) * sqrt(freq[b_j]))
  where freq[b] = total number of members who borrowed book b

Step 3: Generate Recommendations for Member m
  For each book b_candidate not yet borrowed by m:
    score(b_candidate) = sum(sim(b_candidate, b_borrowed)) for all b_borrowed by m
  Return top-N candidates sorted by score descending

Complexity Analysis:
  - Building co-occurrence: O(M * B^2) where M = members, B = avg books per member
  - Computing similarities: O(B_total^2) where B_total = unique books
  - Generating recommendations: O(B_borrowed * B_total) per member
  - Space: O(B_total^2) for similarity matrix

Optimizations:
  - Sparse matrix representation (most pairs have zero co-occurrence)
  - Pre-compute similarity matrix offline (nightly batch job)
  - Cache top-N recommendations per member in Redis (TTL: 1 hour)
  - Only consider books borrowed in last 2 years for recency
  - Minimum co-occurrence threshold (>= 3) to filter noise
"""

import numpy as np
from collections import defaultdict
from typing import Dict, List, Tuple

def build_co_occurrence_matrix(
    borrowing_data: List[Tuple[str, str]]  # (member_id, book_id) pairs
) -> Tuple[Dict[str, Dict[str, int]], Dict[str, int]]:
    """
    Build co-occurrence matrix from borrowing history.

    Args:
        borrowing_data: List of (member_id, book_id) tuples

    Returns:
        co_occurrence: Dict mapping book pairs to co-occurrence counts
        book_frequency: Dict mapping book_id to total borrower count
    """
    # Group books by member
    member_books = defaultdict(set)
    for member_id, book_id in borrowing_data:
        member_books[member_id].add(book_id)

    # Build co-occurrence counts
    co_occurrence = defaultdict(lambda: defaultdict(int))
    book_frequency = defaultdict(int)

    for member_id, books in member_books.items():
        for book in books:
            book_frequency[book] += 1
        book_list = list(books)
        for i in range(len(book_list)):
            for j in range(i + 1, len(book_list)):
                co_occurrence[book_list[i]][book_list[j]] += 1
                co_occurrence[book_list[j]][book_list[i]] += 1

    return dict(co_occurrence), dict(book_frequency)


def compute_similarity(
    co_occurrence: Dict[str, Dict[str, int]],
    book_frequency: Dict[str, int],
    min_co_occurrence: int = 3
) -> Dict[str, Dict[str, float]]:
    """
    Compute cosine similarity between book pairs.

    Args:
        co_occurrence: Co-occurrence counts
        book_frequency: Book borrower counts
        min_co_occurrence: Minimum co-occurrence to consider

    Returns:
        similarity: Dict mapping book pairs to similarity scores [0, 1]
    """
    similarity = defaultdict(dict)

    for book_i, related in co_occurrence.items():
        for book_j, count in related.items():
            if count >= min_co_occurrence:
                sim = count / (
                    np.sqrt(book_frequency[book_i]) *
                    np.sqrt(book_frequency[book_j])
                )
                similarity[book_i][book_j] = round(min(sim, 1.0), 4)

    return dict(similarity)


def recommend_for_member(
    member_borrowed: List[str],
    similarity: Dict[str, Dict[str, float]],
    top_n: int = 10
) -> List[Tuple[str, float]]:
    """
    Generate top-N recommendations for a member.

    Args:
        member_borrowed: List of book_ids the member has borrowed
        similarity: Pre-computed similarity matrix
        top_n: Number of recommendations to return

    Returns:
        List of (book_id, score) tuples sorted by score descending
    """
    scores = defaultdict(float)
    borrowed_set = set(member_borrowed)

    for borrowed_book in member_borrowed:
        if borrowed_book in similarity:
            for candidate, sim_score in similarity[borrowed_book].items():
                if candidate not in borrowed_set:
                    scores[candidate] += sim_score

    # Sort by score descending and return top-N
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]
```

### D. Fine Calculation Decision Table

| Scenario | Days Overdue | Grace Period | Holidays in Range | Billable Days | Daily Rate (Bronze) | Subtotal | Max Cap | Final Fine |
|----------|-------------|--------------|-------------------|---------------|---------------------|----------|---------|------------|
| **1. On-time return**          | 0   | 1 day | --- | 0   | $1.00 | $0.00  | $25.00 | **$0.00**  |
| **2. Within grace period**     | 1   | 1 day | 0   | 0   | $1.00 | $0.00  | $25.00 | **$0.00**  |
| **3. Standard overdue**        | 5   | 1 day | 0   | 4   | $1.00 | $4.00  | $25.00 | **$4.00**  |
| **4. Overdue with holidays**   | 10  | 1 day | 2   | 7   | $1.00 | $7.00  | $25.00 | **$7.00**  |
| **5. Fine reaches cap**        | 40  | 1 day | 3   | 36  | $1.00 | $36.00 | $25.00 | **$25.00** |
| **6. Gold tier reduced rate**  | 10  | 3 days| 1   | 6   | $0.50 | $3.00  | $15.00 | **$3.00**  |

**Fine Calculation Formula**:
```
overdue_days = max(0, return_date - due_date)
billable_days = max(0, overdue_days - grace_period - holidays_in_range)
subtotal = billable_days * daily_rate_for_tier
final_fine = min(subtotal, max_cap_for_tier)
```

**Special Cases**:
| Case               | Charge                                      |
|--------------------|---------------------------------------------|
| Damaged book       | 50% of book replacement cost                |
| Lost book          | 100% of book replacement cost + $5.00 processing fee |
| Damaged + Overdue  | Damage charge + overdue fine (each capped independently) |

### E. Seed Data Recommendations

| Entity            | Recommended Count | Notes                                               |
|-------------------|-------------------|------------------------------------------------------|
| Books             | 100-200           | Across 8-10 genres, mix of popular and niche titles  |
| Book Copies       | 300-500           | 2-5 copies per book, varying conditions              |
| Members           | 50-100            | Mix of students, faculty, staff; all three tiers     |
| Borrowings        | 500-1000          | Historical data for recommendation engine training   |
| Reviews           | 200-400           | 1-5 star ratings with some review text               |
| Fines             | 30-50             | Mix of outstanding, paid, and waived fines           |
| Reservations      | 10-20             | Some pending, some expired                           |
| Library Config    | 8-10              | Fine rates, thresholds, holidays                     |

**Seed Data Tips**:
- Include enough borrowing history overlap between members to produce meaningful collaborative filtering results (at least 5 members should share 3+ borrowed books)
- Create books with rich descriptions and multiple tags for full-text search testing
- Include members at all three tiers (bronze, silver, gold) to test tier-based logic
- Pre-create some overdue borrowings with varying durations to test fine calculation edge cases
- Include at least 2-3 books with all copies checked out to test reservation functionality

### F. Technical Challenges & Hints

| Challenge                          | Hint                                                                                                       |
|------------------------------------|-------------------------------------------------------------------------------------------------------------|
| Full-text search relevance tuning  | Use `ts_rank_cd` with normalization flag 32 (divide by 1 + log of document length). Weight title as 'A' (highest). Test with realistic queries and adjust weights. |
| tsvector with array columns        | Use `array_to_string(authors, ' ')` to convert arrays to text before `to_tsvector()`. Create a trigger function for automatic updates. |
| Collaborative filtering cold start | For new members with < 3 borrows, fall back to content-based suggestions (popular books in their department's preferred genres). |
| Sparse similarity matrix           | Use Python `defaultdict` or sparse matrix libraries. Only store pairs with similarity > 0.1 to save memory. |
| Redis cache invalidation           | Use cache keys with pattern prefixes (e.g., `book:search:*`). On catalog update, delete matching patterns with `SCAN` + `DEL`. |
| Concurrent checkout prevention     | Use optimistic locking: `UPDATE book_copies SET status='checked_out', version=version+1 WHERE id=:id AND version=:expected AND status='available'`. Check affected rows. |
| Reservation expiry handling        | Use APScheduler or a background task to check `expires_at` every 15 minutes. Expire unfulfilled reservations and promote next in queue. |
| Fine calculation with holidays     | Store holidays in `library_config` as JSON array of dates. Count business days using Python `dateutil` or manual day-by-day iteration excluding holidays. |
| Module boundary enforcement        | Use Python packages with `__init__.py` that explicitly export only the public interface. Lint with import rules (e.g., `import-linter` library). |
| Analytics query performance        | Create materialized views for expensive aggregations. Refresh them on a schedule (every 10 minutes) rather than computing on every request. |

### G. Reference Materials

- **Clean Architecture** by Robert C. Martin --- Domain-centric architecture, dependency rule, module boundaries
- **Designing Data-Intensive Applications** by Martin Kleppmann --- Full-text search, caching, concurrency
- **Recommender Systems Handbook** by Ricci et al. --- Collaborative filtering algorithms and evaluation
- **FastAPI Documentation**: https://fastapi.tiangolo.com/ --- Async endpoints, dependency injection, middleware
- **SQLAlchemy 2.0 Documentation**: https://docs.sqlalchemy.org/ --- Async ORM, relationships, custom types
- **PostgreSQL Full-Text Search**: https://www.postgresql.org/docs/current/textsearch.html --- tsvector, tsquery, ranking
- **PostgreSQL pg_trgm Extension**: https://www.postgresql.org/docs/current/pgtrgm.html --- Trigram similarity for fuzzy matching
- **Redis Documentation**: https://redis.io/docs/ --- Caching patterns, key expiry, pub/sub
- **Docker Compose Docs**: https://docs.docker.com/compose/ --- Multi-container orchestration
- **import-linter**: https://import-linter.readthedocs.io/ --- Enforcing architectural boundaries in Python

---

*Document Version: 1.0 | Project Code: FP-LMS-2025 | Methodology: AI-Native SDD*
*Last Updated: 2025-01-15*
