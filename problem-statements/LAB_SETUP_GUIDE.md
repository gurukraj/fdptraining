# AI-Native Software Development — Lab Setup Guide

## Overview

This guide explains how faculty members can access and run all 4 workshop lab exercises **entirely online** using GitHub Codespaces — no local installation required.

**What you need:** A GitHub account (free tier works).

---

## Quick Start (3 Minutes)

### Step 1: Open the Repository

Navigate to the workshop repository on GitHub:
```
https://github.com/<org>/faculty-program
```

### Step 2: Launch a Codespace

1. Click the green **"<> Code"** button
2. Select the **"Codespaces"** tab
3. Click **"Create codespace on main"**

A full VS Code editor opens in your browser within ~60 seconds with all tools pre-installed.

### Step 3: Navigate to Your Project

Each project lives in its own directory. Open a terminal (`Ctrl+`` `) and navigate:

```bash
# Pick ONE project to work on:
cd student-grade-calculator      # Python/FastAPI
cd weather-dashboard-api         # Python/Flask
cd ecommerce-product-catalog     # Node.js/Express
cd task-management-api           # Java/Spring Boot
```

### Step 4: Start Building with AI

Open the problem statement for your project from the `problem-statements/` folder, feed it to your AI coding assistant (GitHub Copilot is built into Codespaces), and start implementing!

---

## Lab Projects at a Glance

| # | Project | Stack | Difficulty | Duration |
|---|---------|-------|------------|----------|
| 1 | **Student Grade Calculator** | Python / FastAPI / SQLite | Beginner | ~45 min |
| 2 | **Weather Dashboard API** | Python / Flask / SQLite | Intermediate | ~60 min |
| 3 | **E-Commerce Product Catalog** | Node.js / Express / NeDB | Intermediate | ~60 min |
| 4 | **Task Management API** | Java / Spring Boot / H2 | Advanced | ~90 min |

**Recommendation:** Start with Project 1 (Student Grade Calculator) for your first attempt.

---

## What's Pre-Installed in Codespaces

Each project includes a `.devcontainer/devcontainer.json` that automatically provisions:

| Project | Runtime | Database | Auto-Install |
|---------|---------|----------|--------------|
| Student Grade Calculator | Python 3.12 | SQLite (built-in) | `pip install -r requirements.txt` |
| Weather Dashboard API | Python 3.12 | SQLite (built-in) | `pip install -r requirements.txt` |
| E-Commerce Product Catalog | Node.js 20 | NeDB (embedded) | `npm install` |
| Task Management API | Java 21 + Maven | H2 (in-memory) | `mvn clean compile` |

No Docker, no database servers, no environment setup — everything works out of the box.

---

## Running Each Project

### Student Grade Calculator (Python/FastAPI)

```bash
cd student-grade-calculator

# Install dependencies (auto-runs in Codespace)
pip install -r requirements.txt

# Seed the database with sample data
python seed_database.py

# Run the server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest -v

# View API docs (auto-opens in browser)
# http://localhost:8000/docs
```

### Weather Dashboard API (Python/Flask)

```bash
cd weather-dashboard-api

# Install dependencies (auto-runs in Codespace)
pip install -r requirements.txt

# Seed the database
python seed_database.py

# Run the server
flask --app app.main run --port 5000

# Run tests
pytest -v
```

### E-Commerce Product Catalog (Node.js/Express)

```bash
cd ecommerce-product-catalog

# Install dependencies (auto-runs in Codespace)
npm install

# Seed the database with 55 sample products
npm run seed

# Run the server
npm start

# Run tests
npm test
```

### Task Management API (Java/Spring Boot)

```bash
cd task-management-api

# Build the project (auto-runs in Codespace)
mvn clean compile -DskipTests

# Run the application (includes seed data via data.sql)
mvn spring-boot:run

# Run tests
mvn test

# Access H2 console: http://localhost:8080/h2-console
# JDBC URL: jdbc:h2:mem:taskdb | User: sa | Password: (empty)
```

---

## Lab Exercise Workflow

### Phase 1: Understand the Problem (5 min)
1. Read the problem statement from `problem-statements/PS_<ProjectName>.md`
2. Identify the functional requirements and API endpoints
3. Note the data model and business rules

### Phase 2: Set Up the Project (5 min)
1. Open your AI coding assistant (GitHub Copilot Chat in Codespaces)
2. Paste the problem statement as context
3. Ask the AI to create the project structure and install dependencies

### Phase 3: Implement with AI (30-60 min)
1. Work through requirements one at a time (FR-1, FR-2, ...)
2. For each requirement:
   - Tell the AI what to implement, referencing the FR
   - Review the generated code
   - Run the relevant tests to verify

### Phase 4: Verify (5 min)
1. Run the full test suite
2. Start the server and test a few endpoints manually with `curl`
3. Verify all success criteria from the problem statement

---

## GitHub Codespaces — Free Tier Details

| Feature | Free Tier Limit |
|---------|----------------|
| **Hours per month** | 60 hours (2-core) or 30 hours (4-core) |
| **Storage** | 15 GB per month |
| **Concurrent Codespaces** | Up to 2 active |

**Tips to maximize free hours:**
- Stop your Codespace when not in use (it auto-stops after 30 min idle)
- Use 2-core machines (sufficient for all 4 projects)
- Delete Codespaces you're done with

**To manage Codespaces:** https://github.com/codespaces

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Codespace takes long to start | First launch installs deps (~2 min). Subsequent starts are faster. |
| Port not accessible | Click the "Ports" tab in VS Code terminal panel, ensure port is set to "Public" |
| Python module not found | Run `pip install -r requirements.txt` manually |
| Java build fails | Run `mvn clean compile -DskipTests` to rebuild |
| npm install fails | Delete `node_modules/` and run `npm install` again |
| Tests fail | Ensure seed data is loaded first (see project-specific commands above) |

---

## Alternative: Running Locally

If you prefer to run locally instead of using Codespaces:

**Prerequisites:**
- Python 3.12+ (for Projects 1 & 2)
- Node.js 20+ (for Project 3)
- Java 21 + Maven (for Project 4)
- Git

```bash
git clone https://github.com/<org>/faculty-program.git
cd faculty-program/<project-name>
# Follow the project-specific commands above
```

---

## Contact & Support

For technical issues during the workshop, raise your hand or post in the workshop chat channel.
