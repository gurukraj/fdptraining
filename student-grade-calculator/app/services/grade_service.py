"""
Grade calculation service (FR-3).

Implements the letter grade and GPA point mapping:
    A: 90-100 -> 4.0
    B: 80-89  -> 3.0
    C: 70-79  -> 2.0
    D: 60-69  -> 1.0
    F: 0-59   -> 0.0
"""


def calculate_letter_grade(score: int) -> str:
    """
    Convert a numeric score (0-100) to a letter grade.

    Args:
        score: Integer score between 0 and 100 inclusive.

    Returns:
        Letter grade as a single character string: 'A', 'B', 'C', 'D', or 'F'.

    Raises:
        ValueError: If score is outside the 0-100 range.
    """
    if not (0 <= score <= 100):
        raise ValueError(f"Score must be between 0 and 100, got {score}")

    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def calculate_grade_points(letter_grade: str) -> float:
    """
    Convert a letter grade to its GPA point value.

    Args:
        letter_grade: One of 'A', 'B', 'C', 'D', 'F'.

    Returns:
        Grade point value as a float (4.0, 3.0, 2.0, 1.0, or 0.0).

    Raises:
        ValueError: If letter_grade is not a valid grade.
    """
    grade_points_map = {
        "A": 4.0,
        "B": 3.0,
        "C": 2.0,
        "D": 1.0,
        "F": 0.0,
    }
    if letter_grade not in grade_points_map:
        raise ValueError(f"Invalid letter grade: {letter_grade}")
    return grade_points_map[letter_grade]


def calculate_gpa(grade_points_list: list[float]) -> float:
    """
    Calculate GPA as the average of grade points, rounded to 2 decimal places.

    Args:
        grade_points_list: List of grade point values.

    Returns:
        GPA rounded to 2 decimal places, or 0.0 if the list is empty.
    """
    if not grade_points_list:
        return 0.0
    return round(sum(grade_points_list) / len(grade_points_list), 2)
