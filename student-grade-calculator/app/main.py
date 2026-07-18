"""
FastAPI application entry point for the Student Grade Calculator API.

This module creates the FastAPI app instance, includes all route modules,
and initializes the database on startup.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import init_db
from app.routes.students import router as students_router
from app.routes.scores import router as scores_router
from app.routes.reports import report_router, class_report_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the database tables on application startup."""
    init_db()
    yield


app = FastAPI(
    title="Student Grade Calculator API",
    description=(
        "A RESTful API for managing student records, recording scores, "
        "calculating letter grades, and generating academic reports. "
        "Built as an educational workshop project demonstrating "
        "Spec-Driven Development (SDD)."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Include route modules
app.include_router(students_router)
app.include_router(scores_router)
app.include_router(report_router)
app.include_router(class_report_router)


@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {
        "application": "Student Grade Calculator API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }
