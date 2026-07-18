# Homework: AI-Native Software Development

## Overview

These homework exercises reinforce the AI-Native Software Development methodology covered in the workshop. Each exercise follows the complete spec-driven workflow: **Specification -> Architecture -> Code Generation -> Testing -> CI/CD**.

Complete at least **one primary exercise** and review the reflection questions.

---

## Exercise 1: Book Library Management System

### Objective
Build a RESTful API for managing a book library using AI-native development practices.

### Requirements

**Functional Requirements:**
1. **Book Management (CRUD)**
   - Create books with: title, author, ISBN (unique), published year, genre, description
   - List books with pagination, filtering by genre, author, and year range
   - Update book details
   - Soft-delete books

2. **Author Management**
   - Create authors with: name, biography, birth year
   - List all authors
   - View author with their books

3. **Category/Genre Management**
   - Predefined genres: Fiction, Non-Fiction, Science, History, Technology, Biography
   - Books can belong to one genre
   - List books by genre

4. **Search**
   - Full-text search across title, author name, and description
   - Return results sorted by relevance

**Non-Functional Requirements:**
- Input validation on all fields (ISBN format: `XXX-X-XX-XXXXXX-X`)
- Pagination with default page size 20, max 100
- API response time < 200ms
- Test coverage > 80%

### Technology Stack
Choose one:
- **Option A:** Python 3.12+ / FastAPI / SQLite
- **Option B:** Java 21 / Spring Boot / PostgreSQL (Docker)

### Deliverables
1. Software Design Document (SDD) written before any code
2. Working API with all endpoints
3. Unit tests for business logic
4. Integration tests for API endpoints
5. Brief write-up: What did the AI do well? What needed human correction?

### Suggested AI Workflow
1. **Write the SDD first** -- use AI to help structure it, but review critically
2. **Generate database schema** from your domain model
3. **Generate entity/model classes** from your schema
4. **Generate service layer** from functional requirements
5. **Generate API endpoints** from your API contract
6. **Generate tests** from your acceptance criteria
7. **Review, fix, and iterate** on all generated code

---

## Exercise 2: Event Registration Platform

### Objective
Build an event registration system that demonstrates business rule enforcement and multi-entity relationships.

### Requirements

**Functional Requirements:**
1. **Event Management**
   - Create events with: title, description, date/time, location, max capacity, registration deadline
   - List upcoming events (future dates only)
   - Update event details (only before registration deadline)
   - Cancel events (notifies registered attendees conceptually)

2. **Registration Management**
   - Register attendees for events with: name, email, phone (optional)
   - Enforce capacity limits -- reject registration when event is full
   - Enforce deadline -- reject registration after deadline
   - Cancel registration (free up capacity)
   - List attendees for an event

3. **Business Rules**
   - An attendee cannot register for the same event twice (unique email per event)
   - Capacity tracking: current registrations vs. max capacity
   - Events cannot be modified after they start
   - Waitlist support (optional/bonus): when event is full, add to waitlist; auto-promote when cancellation occurs

4. **Reporting**
   - Event summary: registered count, available spots, waitlist count
   - Attendee history: all events a person has registered for (by email)

**Non-Functional Requirements:**
- Email format validation
- Date/time validation (no past events)
- Concurrent registration handling (prevent overbooking)
- Test coverage > 85%
- API documentation via OpenAPI/Swagger

### Technology Stack
Choose one:
- **Option A:** Python 3.12+ / FastAPI / SQLite
- **Option B:** Java 21 / Spring Boot / PostgreSQL (Docker)
- **Option C:** Node.js / Express / MongoDB

### Deliverables
1. Software Design Document with at least: functional requirements, API contract, data model, test cases
2. Working API with capacity enforcement
3. Comprehensive test suite
4. CI/CD pipeline configuration (GitHub Actions or similar)
5. Reflection document on AI-assisted development experience

---

## Exercise 3: Specification Review Challenge

### Objective
Practice critical evaluation of AI-generated specifications and code.

### Instructions

1. **Generate a specification**: Ask an AI tool to create a complete SDD for a "Student Attendance Tracking System" with the following features:
   - Record student attendance (present, absent, late) for classes
   - Calculate attendance percentage per student per course
   - Generate alerts when attendance drops below 75%
   - Monthly attendance reports

2. **Review the specification** for:
   - Missing edge cases
   - Ambiguous requirements
   - Incomplete acceptance criteria
   - Security considerations omitted
   - Performance implications not addressed

3. **Document your findings**: Create a review document listing:
   - At least 5 issues found in the AI-generated spec
   - Your proposed corrections for each issue
   - Why each issue matters in a production system

4. **Fix and improve**: Produce a corrected, improved version of the specification

### Deliverables
1. Original AI-generated specification (unmodified)
2. Review document with findings
3. Improved specification
4. Brief reflection: What patterns of errors did you notice in AI-generated specs?

---

## Reflection Questions

Answer these questions after completing at least one exercise:

1. **Specification Quality**: How did the quality of your specification affect the quality of AI-generated code? Give specific examples.

2. **Human Judgment**: At what points during the exercise did human judgment prove essential? Where was AI insufficient?

3. **Testing Strategy**: How did having test cases defined in the spec before code generation affect your confidence in the final product?

4. **Efficiency**: Estimate the time breakdown -- how much time was spent on specification vs. code generation vs. review vs. testing? How does this compare to your usual development workflow?

5. **Edge Cases**: Did the AI miss any edge cases that you caught during review? Did you miss any that the AI caught?

6. **Teaching Implications**: How would you incorporate AI-native practices into your courses? What assessment methods would you use?

7. **Governance**: What policies would you establish for AI use in your classroom? How would you balance learning outcomes with AI assistance?

---

## Submission Guidelines

- Submit all deliverables as a ZIP file or Git repository link
- Include a README with setup instructions
- Ensure all tests pass before submission
- Document any assumptions made during implementation
- Due date: **2 weeks from workshop date**

---

## Grading Rubric

| Criteria | Weight | Excellent | Good | Needs Improvement |
|----------|:------:|-----------|------|-------------------|
| Specification Quality | 25% | Complete SDD with acceptance criteria and edge cases | Adequate spec with minor gaps | Minimal or vague specification |
| Code Quality | 20% | Clean, well-structured code with meaningful human modifications | Functional code with some review evidence | Unreviewed AI output |
| Test Coverage | 20% | Comprehensive tests: unit, integration, edge cases | Basic tests with decent coverage | Minimal or no tests |
| CI/CD Pipeline | 15% | Working pipeline with build, test, and quality gates | Basic pipeline configuration | No pipeline |
| Reflection & Documentation | 20% | Thoughtful analysis of AI-assisted process | Basic reflection | No reflection |

---

*Good luck! Remember: the goal is not just to produce working code, but to practice the discipline of specification-driven, AI-assisted development.*
