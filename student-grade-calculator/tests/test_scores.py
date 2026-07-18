"""
Tests for Score recording operations (FR-2).

Covers:
- Recording a valid score
- Score validation (0-100 range)
- Duplicate score detection (same student + subject)
- Non-existent student (404)
- Auto-calculated letter grade and grade points
"""


class TestRecordScore:
    """Tests for POST /api/students/{student_id}/scores (FR-2)."""

    def test_record_score_success(self, client_with_student, sample_score):
        """FR-2: Successfully record a score."""
        response = client_with_student.post(
            "/api/students/STU001/scores", json=sample_score
        )
        assert response.status_code == 201
        data = response.json()
        assert data["student_id"] == "STU001"
        assert data["subject"] == "Mathematics"
        assert data["score"] == 95
        assert data["letter_grade"] == "A"
        assert data["grade_points"] == 4.0
        assert "id" in data
        assert "created_at" in data

    def test_record_score_auto_calculates_grade(self, client_with_student):
        """FR-2: Score auto-calculates letter grade and grade points."""
        response = client_with_student.post(
            "/api/students/STU001/scores",
            json={"subject": "Physics", "score": 75},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["letter_grade"] == "C"
        assert data["grade_points"] == 2.0

    def test_record_score_student_not_found(self, client):
        """FR-2: Recording score for non-existent student returns 404."""
        response = client.post(
            "/api/students/NONEXIST/scores",
            json={"subject": "Math", "score": 90},
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_record_score_duplicate_409(self, client_with_student, sample_score):
        """FR-2: Duplicate student+subject returns 409 Conflict."""
        client_with_student.post(
            "/api/students/STU001/scores", json=sample_score
        )
        response = client_with_student.post(
            "/api/students/STU001/scores", json=sample_score
        )
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_record_score_same_subject_different_students(self, client):
        """FR-2: Same subject for different students is allowed."""
        client.post(
            "/api/students", json={"student_id": "STU001", "name": "Alice"}
        )
        client.post(
            "/api/students", json={"student_id": "STU002", "name": "Bob"}
        )

        resp1 = client.post(
            "/api/students/STU001/scores",
            json={"subject": "Math", "score": 90},
        )
        resp2 = client.post(
            "/api/students/STU002/scores",
            json={"subject": "Math", "score": 85},
        )
        assert resp1.status_code == 201
        assert resp2.status_code == 201

    def test_record_score_different_subjects_same_student(self, client_with_student):
        """FR-2: Different subjects for same student is allowed."""
        resp1 = client_with_student.post(
            "/api/students/STU001/scores",
            json={"subject": "Math", "score": 90},
        )
        resp2 = client_with_student.post(
            "/api/students/STU001/scores",
            json={"subject": "Physics", "score": 85},
        )
        assert resp1.status_code == 201
        assert resp2.status_code == 201


class TestScoreValidation:
    """Tests for score input validation (FR-2)."""

    def test_score_below_zero(self, client_with_student):
        """FR-2: Score below 0 returns 422."""
        response = client_with_student.post(
            "/api/students/STU001/scores",
            json={"subject": "Math", "score": -1},
        )
        assert response.status_code == 422

    def test_score_above_100(self, client_with_student):
        """FR-2: Score above 100 returns 422."""
        response = client_with_student.post(
            "/api/students/STU001/scores",
            json={"subject": "Math", "score": 101},
        )
        assert response.status_code == 422

    def test_score_zero_valid(self, client_with_student):
        """FR-2: Score of 0 is valid (boundary)."""
        response = client_with_student.post(
            "/api/students/STU001/scores",
            json={"subject": "Math", "score": 0},
        )
        assert response.status_code == 201
        assert response.json()["score"] == 0
        assert response.json()["letter_grade"] == "F"

    def test_score_100_valid(self, client_with_student):
        """FR-2: Score of 100 is valid (boundary)."""
        response = client_with_student.post(
            "/api/students/STU001/scores",
            json={"subject": "Math", "score": 100},
        )
        assert response.status_code == 201
        assert response.json()["score"] == 100
        assert response.json()["letter_grade"] == "A"

    def test_score_missing_subject(self, client_with_student):
        """FR-2: Missing subject returns 422."""
        response = client_with_student.post(
            "/api/students/STU001/scores",
            json={"score": 90},
        )
        assert response.status_code == 422

    def test_score_missing_score(self, client_with_student):
        """FR-2: Missing score returns 422."""
        response = client_with_student.post(
            "/api/students/STU001/scores",
            json={"subject": "Math"},
        )
        assert response.status_code == 422

    def test_score_empty_subject(self, client_with_student):
        """FR-2: Empty subject returns 422."""
        response = client_with_student.post(
            "/api/students/STU001/scores",
            json={"subject": "", "score": 90},
        )
        assert response.status_code == 422

    def test_score_float_rejected(self, client_with_student):
        """FR-2: Float score is rejected (must be integer)."""
        response = client_with_student.post(
            "/api/students/STU001/scores",
            json={"subject": "Math", "score": 85.5},
        )
        assert response.status_code == 422
