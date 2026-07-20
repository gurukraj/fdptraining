# Speckit + GitHub Codespaces Lab Guide for fdptraining

This guide walks through all problem statements in the repository and shows how to implement each one inside GitHub Codespaces using a Speckit-style workflow.

## What this repository contains

The repository includes four hands-on labs:

- Student Grade Calculator: [problem-statements/PS_Student_Grade_Calculator.raw.txt](problem-statements/PS_Student_Grade_Calculator.raw.txt)
- Weather Dashboard API: [problem-statements/PS_Weather_Dashboard_API.raw.txt](problem-statements/PS_Weather_Dashboard_API.raw.txt)
- E-Commerce Product Catalog: [problem-statements/PS_ECommerce_Product_Catalog.raw.txt](problem-statements/PS_ECommerce_Product_Catalog.raw.txt)
- Task Management API: [problem-statements/PS_Task_Management_API.raw.txt](problem-statements/PS_Task_Management_API.raw.txt)

Each lab is designed to be solved in a GitHub Codespace with minimal local setup.

---

## Prerequisites

Before you start, make sure you have:

- A GitHub account
- Access to GitHub Codespaces
- A browser-based VS Code environment
- The repository opened in Codespaces

If you are using a fresh Codespace, your dev container should install the required runtimes automatically for the selected project.

---

## Step 1: Open the repository in GitHub Codespaces

1. Open the repository on GitHub:
   - https://github.com/gurukraj/fdptraining
2. Click the green Code button.
3. Select the Codespaces tab.
4. Click Create codespace on main.
5. Wait for the Codespace to finish loading.

Once the environment opens, you will see VS Code running in your browser.

---

## Step 2: Use a Speckit-style workflow in the Codespace

A practical Speckit-style workflow for these labs is:

1. Read the problem statement carefully.
2. Extract the functional requirements and endpoints.
3. Ask your coding assistant to create an implementation plan.
4. Generate scaffolding and project files.
5. Implement features one requirement at a time.
6. Run tests and fix failures.
7. Refine the solution until it satisfies the success criteria.

### Recommended working pattern

Open the relevant problem statement and then paste a prompt like this into Copilot Chat or the Speckit workflow you are using:

```text
Use the requirements in problem-statements/PS_Student_Grade_Calculator.raw.txt.
Create a complete implementation plan for a FastAPI student grade calculator.
Then scaffold the project, add the API endpoints, validation, database logic, and tests.
```

Use a similar prompt for each lab, changing the project name and the problem statement file.

---

## Step 3: Create a working branch for each lab

From the terminal in the Codespace, create a branch for the lab you are implementing:

```bash
git checkout -b lab/student-grade-calculator
```

You can repeat the pattern for the other labs:

```bash
git checkout -b lab/weather-dashboard-api
git checkout -b lab/ecommerce-product-catalog
git checkout -b lab/task-management-api
```

---

## Lab 1: Student Grade Calculator

### Goal
Build a FastAPI-based student grading service with validation, score recording, GPA calculation, and reporting.

### Source problem statement
- [problem-statements/PS_Student_Grade_Calculator.raw.txt](problem-statements/PS_Student_Grade_Calculator.raw.txt)

### Suggested Speckit prompt

```text
Implement the student grade calculator described in problem-statements/PS_Student_Grade_Calculator.raw.txt.
Create the FastAPI app, SQLite database models, validation, endpoints for student creation, score recording, and reports, plus pytest tests.
```

### Recommended implementation steps

1. Open the project folder:
   ```bash
   cd student-grade-calculator
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create the database schema and seed data:
   ```bash
   python seed_database.py
   ```
4. Implement the API in layers:
   - Models for Student and Score
   - Schemas for request/response validation
   - Routes for students and reports
   - Database session management
5. Add tests for:
   - Student registration
   - Duplicate student ID rejection
   - Score creation and invalid score rejection
   - GPA calculation
   - Class statistics report
6. Run the tests:
   ```bash
   pytest -v
   ```
7. Start the app:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
8. Open the generated docs at:
   - http://localhost:8000/docs

### What to verify

- Student creation returns 201 for valid input and 409 for duplicate IDs.
- Scores are validated strictly and invalid values return 422.
- GPA is calculated and rounded correctly.
- Class statistics include subject averages, grade distribution, and top performers.

---

## Lab 2: Weather Dashboard API

### Goal
Build a Flask-based weather microservice with current weather lookups, forecasts, conversions, caching, alerts, favorites, and history.

### Source problem statement
- [problem-statements/PS_Weather_Dashboard_API.raw.txt](problem-statements/PS_Weather_Dashboard_API.raw.txt)

### Suggested Speckit prompt

```text
Implement the weather dashboard API described in problem-statements/PS_Weather_Dashboard_API.raw.txt.
Create a Flask app with SQLite-backed caching, mock weather data, conversion endpoints, alert configuration, favorites, search history, and tests.
```

### Recommended implementation steps

1. Open the project folder:
   ```bash
   cd weather-dashboard-api
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Seed the mock data if required:
   ```bash
   python seed_database.py
   ```
4. Implement the app in this order:
   - Weather provider and data model
   - Current weather and forecast endpoints
   - Temperature conversion endpoints
   - Cache storage and stats
   - Alert configuration and alert checks
   - Favorites and history endpoints
5. Add tests for:
   - City lookup by name
   - Coordinates lookup
   - Conversion accuracy
   - Cache hit and miss behavior
   - User-scoped favorites and history
6. Run tests:
   ```bash
   pytest -v
   ```
7. Start the service:
   ```bash
   flask --app app.main run --port 5000
   ```

### What to verify

- Current weather and forecast endpoints work for valid city names and coordinates.
- Conversion endpoints support all six directional pairs.
- Cache statistics reflect hit and miss counts accurately.
- Alert checks evaluate thresholds and classify severity correctly.

---

## Lab 3: E-Commerce Product Catalog

### Goal
Build an Express-based catalog API with CRUD operations, inventory controls, soft delete/restore, search, filters, pagination, and analytics.

### Source problem statement
- [problem-statements/PS_ECommerce_Product_Catalog.raw.txt](problem-statements/PS_ECommerce_Product_Catalog.raw.txt)

### Suggested Speckit prompt

```text
Implement the e-commerce product catalog API described in problem-statements/PS_ECommerce_Product_Catalog.raw.txt.
Create an Express app with NeDB, validation, CRUD routes, soft delete and restore, stock adjustments, inventory queries, analytics endpoints, and tests.
```

### Recommended implementation steps

1. Open the project folder:
   ```bash
   cd ecommerce-product-catalog
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Seed the database:
   ```bash
   npm run seed
   ```
4. Implement the app in this order:
   - Product schema and validation
   - Product CRUD endpoints
   - Search, filter, sort, and pagination
   - Soft-delete and restore flow
   - Inventory adjustment and low-stock listing
   - Analytics endpoints
5. Add tests for:
   - Product creation and validation
   - Duplicate SKU conflict handling
   - Soft delete and restore behavior
   - Stock adjustment rules
   - Analytics calculations
6. Run tests:
   ```bash
   npm test
   ```
7. Start the server:
   ```bash
   npm start
   ```

### What to verify

- Duplicate SKUs return 409.
- Product listing supports pagination and filters.
- Soft-deleted products are hidden from regular listings but can be restored.
- Stock changes are validated and cannot result in negative inventory.
- Analytics return category and price breakdown results correctly.

---

## Lab 4: Task Management API

### Goal
Build a Spring Boot task manager with header-based authentication, status transitions, categories, comments, soft delete, and audit logging.

### Source problem statement
- [problem-statements/PS_Task_Management_API.raw.txt](problem-statements/PS_Task_Management_API.raw.txt)

### Suggested Speckit prompt

```text
Implement the task management API described in problem-statements/PS_Task_Management_API.raw.txt.
Create a Spring Boot 3 project with JPA entities, role-based request headers, task status transitions, soft-delete behavior, category management, comment support, audit logs, and tests.
```

### Recommended implementation steps

1. Open the project folder:
   ```bash
   cd task-management-api
   ```
2. Build the project:
   ```bash
   mvn clean compile -DskipTests
   ```
3. Run the application:
   ```bash
   mvn spring-boot:run
   ```
4. Implement the API in this order:
   - Authentication filter with X-User-Id and X-User-Role
   - Task entity and CRUD flow
   - Status transition logic
   - Soft-delete cascade to comments
   - Category CRUD with admin restrictions
   - Comment creation and deletion
   - Audit log persistence and filtering
5. Add tests for:
   - Missing headers returning 401
   - Admin-only operations returning 403
   - Valid and invalid status transitions
   - Category deletion constraints
   - Audit log creation for write operations
6. Run tests:
   ```bash
   mvn test
   ```

### What to verify

- Requests missing authentication headers fail with 401.
- USER role cannot perform ADMIN-only actions and receives 403.
- Only the approved status transitions are accepted.
- Soft-delete cascades to comments.
- Audit logs are created for write operations and filterable by entity type.

---

## Suggested workflow for each lab

Use the same pattern for every problem statement:

1. Read the problem statement.
2. Convert the functional requirements into a short implementation checklist.
3. Ask the assistant to generate the plan.
4. Scaffold the project.
5. Implement one requirement at a time.
6. Test after each slice.
7. Repeat until all success criteria are met.

A simple prompt template is:

```text
I want to solve the lab described in <problem-statement-file>.
Create a step-by-step implementation plan, then scaffold the files and implement the solution in the current project folder.
```

---

## Best practices for Codespaces

- Keep each lab in its own branch.
- Use small commits after each milestone.
- Run tests frequently.
- Use the Ports tab to expose local services if needed.
- Stop the Codespace when you are done to save compute time.

---

## Recommended order

If you are new to these labs, follow this order:

1. Student Grade Calculator
2. Weather Dashboard API
3. E-Commerce Product Catalog
4. Task Management API

This progression moves from simpler APIs to more advanced architecture and authorization patterns.
