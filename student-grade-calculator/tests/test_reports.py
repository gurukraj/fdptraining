"""
Tests for Report and Statistics endpoints (FR-4, FR-5).

Covers:
- Student report card generation
- GPA calculation in report cards
- Class statistics (per-subject)
- Top performers ranking
- Edge cases (no scores, non-existent student)
"""


class TestStudentReport:
    """Tests for GET /api/students/{student_id}/report (FR-4)."""

    def test_report_card_success(self, client_with_data):
        """FR-4: Successfully generate a report card."""
        response = client_with_data.get("/api/students/STU001/report")
        assert response.status_code == 200
        data = response.json()
        assert data["student_id"] == "STU001"
        assert data["name"] == "Alice Johnson"
        assert len(data["scores"]) == 3
        assert "gpa" in data

    def test_report_card_gpa_calculation(self, client_with_data):
        """FR-4: GPA is correctly calculated and rounded to 2 decimals."""
        response = client_with_data.get("/api/students/STU001/report")
        data = response.json()
        # Alice: Math=95(A,4.0), Physics=88(B,3.0), Chemistry=92(A,4.0)
        # GPA = (4.0 + 3.0 + 4.0) / 3 = 3.67 (rounded)
        assert data["gpa"] == 3.67

    def test_report_card_scores_have_grades(self, client_with_data):
        """FR-4: Each score in the report includes letter grade and grade points."""
        response = client_with_data.get("/api/students/STU001/report")
        data = response.json()
        for score_item in data["scores"]:
            assert "subject" in score_item
            assert "score" in score_item
            assert "letter_grade" in score_item
            assert "grade_points" in score_item

    def test_report_card_student_not_found(self, client):
        """FR-4: Non-existent student returns 404."""
        response = client.get("/api/students/NONEXIST/report")
        assert response.status_code == 404

    def test_report_card_no_scores(self, client):
        """FR-4: Student with no scores returns empty scores list and 0.0 GPA."""
        client.post(
            "/api/students",
            json={"student_id": "STU999", "name": "No Scores"},
        )
        response = client.get("/api/students/STU999/report")
        assert response.status_code == 200
        data = response.json()
        assert data["scores"] == []
        assert data["gpa"] == 0.0

    def test_report_card_correct_grade_mapping(self, client):
        """FR-4: Report card reflects correct grade for each score."""
        client.post(
            "/api/students",
            json={"student_id": "STU100", "name": "Grade Test"},
        )
        test_cases = [
            ("Math", 95, "A", 4.0),
            ("English", 82, "B", 3.0),
            ("History", 73, "C", 2.0),
            ("Art", 65, "D", 1.0),
            ("Music", 45, "F", 0.0),
        ]
        for subject, score, _, _ in test_cases:
            client.post(
                "/api/students/STU100/scores",
                json={"subject": subject, "score": score},
            )

        response = client.get("/api/students/STU100/report")
        data = response.json()

        score_map = {s["subject"]: s for s in data["scores"]}
        for subject, score, grade, points in test_cases:
            assert score_map[subject]["letter_grade"] == grade
            assert score_map[subject]["grade_points"] == points

        # GPA = (4.0 + 3.0 + 2.0 + 1.0 + 0.0) / 5 = 2.0
        assert data["gpa"] == 2.0


class TestClassStatistics:
    """Tests for GET /api/reports/class-statistics (FR-5)."""

    def test_class_statistics_success(self, client_with_data):
        """FR-5: Successfully returns per-subject statistics."""
        response = client_with_data.get("/api/reports/class-statistics")
        assert response.status_code == 200
        data = response.json()
        assert "subjects" in data
        assert len(data["subjects"]) == 3  # Math, Physics, Chemistry

    def test_class_statistics_math(self, client_with_data):
        """FR-5: Mathematics statistics are correct."""
        response = client_with_data.get("/api/reports/class-statistics")
        data = response.json()
        math_stats = next(
            s for s in data["subjects"] if s["subject"] == "Mathematics"
        )
        # Alice=95, Bob=72, Charlie=85
        assert math_stats["count"] == 3
        assert math_stats["min_score"] == 72
        assert math_stats["max_score"] == 95
        assert math_stats["average"] == round((95 + 72 + 85) / 3, 2)

    def test_class_statistics_grade_distribution(self, client_with_data):
        """FR-5: Grade distribution is correct for Mathematics."""
        response = client_with_data.get("/api/reports/class-statistics")
        data = response.json()
        math_stats = next(
            s for s in data["subjects"] if s["subject"] == "Mathematics"
        )
        dist = math_stats["grade_distribution"]
        # Alice=95(A), Bob=72(C), Charlie=85(B)
        assert dist["A"] == 1
        assert dist["B"] == 1
        assert dist["C"] == 1
        assert dist["D"] == 0
        assert dist["F"] == 0

    def test_class_statistics_empty(self, client):
        """FR-5: No data returns empty subjects list."""
        response = client.get("/api/reports/class-statistics")
        assert response.status_code == 200
        data = response.json()
        assert data["subjects"] == []


class TestTopPerformers:
    """Tests for GET /api/reports/top-performers (FR-5)."""

    def test_top_performers_default_limit(self, client_with_data):
        """FR-5: Default limit is 5."""
        response = client_with_data.get("/api/reports/top-performers")
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 5
        # We have 3 students, so should return all 3
        assert len(data["top_performers"]) == 3

    def test_top_performers_custom_limit(self, client_with_data):
        """FR-5: Custom limit works."""
        response = client_with_data.get("/api/reports/top-performers?limit=2")
        data = response.json()
        assert data["limit"] == 2
        assert len(data["top_performers"]) == 2

    def test_top_performers_sorted_by_gpa(self, client_with_data):
        """FR-5: Students are sorted by GPA descending."""
        response = client_with_data.get("/api/reports/top-performers")
        data = response.json()
        performers = data["top_performers"]
        # Verify descending GPA order
        for i in range(len(performers) - 1):
            assert performers[i]["gpa"] >= performers[i + 1]["gpa"]

    def test_top_performers_correct_ranking(self, client_with_data):
        """FR-5: Correct ranking based on GPA."""
        response = client_with_data.get("/api/reports/top-performers")
        data = response.json()
        performers = data["top_performers"]

        # Alice: Math=95(A,4.0), Physics=88(B,3.0), Chem=92(A,4.0) -> GPA=3.67
        # Charlie: Math=85(B,3.0), Physics=90(A,4.0), Chem=78(C,2.0) -> GPA=3.0
        # Bob: Math=72(C,2.0), Physics=68(D,1.0), Chem=75(C,2.0) -> GPA=1.67

        assert performers[0]["student_id"] == "STU001"  # Alice
        assert performers[0]["gpa"] == 3.67
        assert performers[1]["student_id"] == "STU003"  # Charlie
        assert performers[1]["gpa"] == 3.0
        assert performers[2]["student_id"] == "STU002"  # Bob
        assert performers[2]["gpa"] == 1.67

    def test_top_performers_includes_name(self, client_with_data):
        """FR-5: Each performer entry includes student_id, name, and gpa."""
        response = client_with_data.get("/api/reports/top-performers")
        data = response.json()
        for performer in data["top_performers"]:
            assert "student_id" in performer
            assert "name" in performer
            assert "gpa" in performer

    def test_top_performers_empty(self, client):
        """FR-5: No data returns empty list."""
        response = client.get("/api/reports/top-performers")
        assert response.status_code == 200
        data = response.json()
        assert data["top_performers"] == []


class TestHealthCheck:
    """Tests for the health check endpoint."""

    def test_root_endpoint(self, client):
        """Health check returns application info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["application"] == "Student Grade Calculator API"
        assert data["status"] == "running"
