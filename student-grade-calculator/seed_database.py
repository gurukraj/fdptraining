#!/usr/bin/env python3
"""
Seed database script.

Loads sample data from data/seed_data.json into the SQLite database.
Initializes tables, creates students, and records scores with
automatic grade calculation.

Usage:
    python seed_database.py
"""

import json
import sys
from pathlib import Path

from app.database import engine, SessionLocal, Base
from app.models import Student, Score
from app.services.grade_service import calculate_letter_grade, calculate_grade_points


def seed():
    """Load seed data into the database."""
    seed_file = Path(__file__).parent / "data" / "seed_data.json"

    if not seed_file.exists():
        print(f"Error: Seed data file not found at {seed_file}")
        sys.exit(1)

    with open(seed_file, "r") as f:
        data = json.load(f)

    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if data already exists
        existing_count = db.query(Student).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} students.")
            print("To re-seed, delete grades.db and run this script again.")
            return

        # Insert students
        students_created = 0
        for student_data in data["students"]:
            student = Student(
                student_id=student_data["student_id"],
                name=student_data["name"],
            )
            db.add(student)
            students_created += 1

        db.flush()  # Flush to ensure students exist before adding scores

        # Insert scores
        scores_created = 0
        for score_data in data["scores"]:
            letter_grade = calculate_letter_grade(score_data["score"])
            grade_points = calculate_grade_points(letter_grade)

            score = Score(
                student_id=score_data["student_id"],
                subject=score_data["subject"],
                score=score_data["score"],
                letter_grade=letter_grade,
                grade_points=grade_points,
            )
            db.add(score)
            scores_created += 1

        db.commit()

        print(f"Successfully seeded database:")
        print(f"  - {students_created} students created")
        print(f"  - {scores_created} scores recorded")
        print()
        print("Sample students:")
        for student_data in data["students"][:5]:
            print(f"  {student_data['student_id']}: {student_data['name']}")
        print(f"  ... and {len(data['students']) - 5} more")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed()
