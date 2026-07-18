"""
Tests for Grade calculation logic (FR-3).

Covers boundary value testing for letter grade assignment:
- A: 90-100 (4.0 GPA)
- B: 80-89  (3.0 GPA)
- C: 70-79  (2.0 GPA)
- D: 60-69  (1.0 GPA)
- F: 0-59   (0.0 GPA)

Tests specific boundary values: 0, 59, 60, 69, 70, 79, 80, 89, 90, 100
"""

import pytest
from app.services.grade_service import (
    calculate_letter_grade,
    calculate_grade_points,
    calculate_gpa,
)


class TestCalculateLetterGrade:
    """Tests for letter grade calculation (FR-3)."""

    # ─── A Grade (90-100) ────────────────────────────────────────────────

    def test_score_100_is_A(self):
        """FR-3: Score of 100 -> A."""
        assert calculate_letter_grade(100) == "A"

    def test_score_95_is_A(self):
        """FR-3: Score of 95 -> A."""
        assert calculate_letter_grade(95) == "A"

    def test_score_90_is_A(self):
        """FR-3: Boundary - Score of 90 -> A."""
        assert calculate_letter_grade(90) == "A"

    # ─── B Grade (80-89) ─────────────────────────────────────────────────

    def test_score_89_is_B(self):
        """FR-3: Boundary - Score of 89 -> B."""
        assert calculate_letter_grade(89) == "B"

    def test_score_85_is_B(self):
        """FR-3: Score of 85 -> B."""
        assert calculate_letter_grade(85) == "B"

    def test_score_80_is_B(self):
        """FR-3: Boundary - Score of 80 -> B."""
        assert calculate_letter_grade(80) == "B"

    # ─── C Grade (70-79) ─────────────────────────────────────────────────

    def test_score_79_is_C(self):
        """FR-3: Boundary - Score of 79 -> C."""
        assert calculate_letter_grade(79) == "C"

    def test_score_75_is_C(self):
        """FR-3: Score of 75 -> C."""
        assert calculate_letter_grade(75) == "C"

    def test_score_70_is_C(self):
        """FR-3: Boundary - Score of 70 -> C."""
        assert calculate_letter_grade(70) == "C"

    # ─── D Grade (60-69) ─────────────────────────────────────────────────

    def test_score_69_is_D(self):
        """FR-3: Boundary - Score of 69 -> D."""
        assert calculate_letter_grade(69) == "D"

    def test_score_65_is_D(self):
        """FR-3: Score of 65 -> D."""
        assert calculate_letter_grade(65) == "D"

    def test_score_60_is_D(self):
        """FR-3: Boundary - Score of 60 -> D."""
        assert calculate_letter_grade(60) == "D"

    # ─── F Grade (0-59) ──────────────────────────────────────────────────

    def test_score_59_is_F(self):
        """FR-3: Boundary - Score of 59 -> F."""
        assert calculate_letter_grade(59) == "F"

    def test_score_30_is_F(self):
        """FR-3: Score of 30 -> F."""
        assert calculate_letter_grade(30) == "F"

    def test_score_0_is_F(self):
        """FR-3: Boundary - Score of 0 -> F."""
        assert calculate_letter_grade(0) == "F"

    # ─── Invalid Scores ──────────────────────────────────────────────────

    def test_score_negative_raises_error(self):
        """FR-3: Negative score raises ValueError."""
        with pytest.raises(ValueError):
            calculate_letter_grade(-1)

    def test_score_101_raises_error(self):
        """FR-3: Score above 100 raises ValueError."""
        with pytest.raises(ValueError):
            calculate_letter_grade(101)


class TestCalculateGradePoints:
    """Tests for grade point calculation (FR-3)."""

    def test_grade_A_points(self):
        """FR-3: Grade A -> 4.0 points."""
        assert calculate_grade_points("A") == 4.0

    def test_grade_B_points(self):
        """FR-3: Grade B -> 3.0 points."""
        assert calculate_grade_points("B") == 3.0

    def test_grade_C_points(self):
        """FR-3: Grade C -> 2.0 points."""
        assert calculate_grade_points("C") == 2.0

    def test_grade_D_points(self):
        """FR-3: Grade D -> 1.0 points."""
        assert calculate_grade_points("D") == 1.0

    def test_grade_F_points(self):
        """FR-3: Grade F -> 0.0 points."""
        assert calculate_grade_points("F") == 0.0

    def test_invalid_grade_raises_error(self):
        """FR-3: Invalid grade letter raises ValueError."""
        with pytest.raises(ValueError):
            calculate_grade_points("E")


class TestCalculateGPA:
    """Tests for GPA calculation (FR-4)."""

    def test_gpa_all_A(self):
        """FR-4: All A grades -> 4.0 GPA."""
        assert calculate_gpa([4.0, 4.0, 4.0]) == 4.0

    def test_gpa_all_F(self):
        """FR-4: All F grades -> 0.0 GPA."""
        assert calculate_gpa([0.0, 0.0, 0.0]) == 0.0

    def test_gpa_mixed(self):
        """FR-4: Mixed grades -> correct average."""
        # A(4.0) + B(3.0) + C(2.0) = 9.0 / 3 = 3.0
        assert calculate_gpa([4.0, 3.0, 2.0]) == 3.0

    def test_gpa_rounded_to_two_decimals(self):
        """FR-4: GPA is rounded to 2 decimal places."""
        # A(4.0) + B(3.0) + C(2.0) + D(1.0) = 10.0 / 4 = 2.5
        assert calculate_gpa([4.0, 3.0, 2.0, 1.0]) == 2.5

    def test_gpa_rounding_precision(self):
        """FR-4: GPA rounding handles recurring decimals."""
        # A(4.0) + A(4.0) + B(3.0) = 11.0 / 3 = 3.666... -> 3.67
        assert calculate_gpa([4.0, 4.0, 3.0]) == 3.67

    def test_gpa_empty_list(self):
        """FR-4: Empty grade list -> 0.0 GPA."""
        assert calculate_gpa([]) == 0.0

    def test_gpa_single_grade(self):
        """FR-4: Single grade -> that grade's points."""
        assert calculate_gpa([3.0]) == 3.0


class TestGradeCalculationViaAPI:
    """Integration tests: verify grades are correctly assigned via the API."""

    def test_boundary_scores_via_api(self, client_with_student):
        """FR-3: Verify all boundary values through the API."""
        boundary_tests = [
            (0, "F", 0.0),
            (59, "F", 0.0),
            (60, "D", 1.0),
            (69, "D", 1.0),
            (70, "C", 2.0),
            (79, "C", 2.0),
            (80, "B", 3.0),
            (89, "B", 3.0),
            (90, "A", 4.0),
            (100, "A", 4.0),
        ]
        for score_val, expected_grade, expected_points in boundary_tests:
            subject = f"Subject_{score_val}"
            response = client_with_student.post(
                "/api/students/STU001/scores",
                json={"subject": subject, "score": score_val},
            )
            assert response.status_code == 201, (
                f"Failed for score={score_val}"
            )
            data = response.json()
            assert data["letter_grade"] == expected_grade, (
                f"Score {score_val}: expected grade {expected_grade}, "
                f"got {data['letter_grade']}"
            )
            assert data["grade_points"] == expected_points, (
                f"Score {score_val}: expected points {expected_points}, "
                f"got {data['grade_points']}"
            )
