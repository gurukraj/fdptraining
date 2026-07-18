# Task Management API - Project Constitution

## Project Identity
- **Name**: Task Management API
- **Type**: RESTful Web Service
- **Domain**: Task/Project Management

## Core Principles
1. **Simplicity First**: Clean, readable code over clever abstractions
2. **Convention over Configuration**: Leverage Spring Boot defaults
3. **Domain-Driven Design**: Entities reflect real-world concepts
4. **Test-Driven Quality**: Comprehensive test coverage for all endpoints
5. **Soft Delete Pattern**: Data is never permanently lost

## Technology Decisions
- **Language**: Java 21 (modern features: records, pattern matching)
- **Framework**: Spring Boot 3.4.x
- **Database**: H2 in-memory (dev), PostgreSQL (production)
- **ORM**: Spring Data JPA / Hibernate
- **Build**: Maven
- **Validation**: Bean Validation (Jakarta)

## Architecture Style
- Layered architecture: Controller -> Service -> Repository -> Entity
- DTOs for API boundaries (Request/Response objects)
- Global exception handling with consistent error responses
- Header-based authentication for workshop simplicity

## API Conventions
- RESTful resource naming (plural nouns)
- Base path: `/api/`
- Pagination on all list endpoints
- Soft delete for tasks and comments
- Audit logging for all write operations

## Status Transition Rules
- OPEN -> IN_PROGRESS (start work)
- IN_PROGRESS -> DONE (complete work)
- IN_PROGRESS -> OPEN (pause/reopen)
- DONE -> OPEN (reopen)
- All other transitions are invalid
