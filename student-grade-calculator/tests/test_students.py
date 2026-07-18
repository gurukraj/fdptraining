"""
Tests for Student CRUD operations (FR-1, FR-6).

Covers:
- Student creation with valid data
- Validation of student_id (alphanumeric, 3-20 chars)
- Validation of name (1-100 chars, not blank)
- Duplicate student_id detection (409 Conflict)
- Student listing with pagination
- Student retrieval by student_id
- Student not found (404)
"""


class TestCreateStudent:
    """Tests for POST /api/students (FR-1)."""

    def test_create_student_success(self, client, sample_student):
        """FR-1: Successfully register a new student."""
        response = client.post("/api/students", json=sample_student)
        assert response.status_code == 201
        data = response.json()
        assert data["student_id"] == "STU001"
        assert data["name"] == "Alice Johnson"
        assert "id" in data
        assert "created_at" in data

    def test_create_student_returns_system_id(self, client, sample_student):
        """FR-1: Created student includes system-generated id."""
        response = client.post("/api/students", json=sample_student)
        data = response.json()
        assert isinstance(data["id"], int)
        assert data["id"] >= 1

    def test_create_student_duplicate_409(self, client, sample_student):
        """FR-1: Duplicate student_id returns 409 Conflict."""
        client.post("/api/students", json=sample_student)
        response = client.post("/api/students", json=sample_student)
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_create_student_id_too_short(self, client):
        """FR-1: student_id shorter than 3 chars returns 422."""
        response = client.post(
            "/api/students", json={"student_id": "AB", "name": "Test"}
        )
        assert response.status_code == 422

    def test_create_student_id_too_long(self, client):
        """FR-1: student_id longer than 20 chars returns 422."""
        response = client.post(
            "/api/students",
            json={"student_id": "A" * 21, "name": "Test"},
        )
        assert response.status_code == 422

    def test_create_student_id_non_alphanumeric(self, client):
        """FR-1: Non-alphanumeric student_id returns 422."""
        response = client.post(
            "/api/students",
            json={"student_id": "STU-001", "name": "Test"},
        )
        assert response.status_code == 422

    def test_create_student_id_with_spaces(self, client):
        """FR-1: student_id with spaces returns 422."""
        response = client.post(
            "/api/students",
            json={"student_id": "STU 001", "name": "Test"},
        )
        assert response.status_code == 422

    def test_create_student_name_empty(self, client):
        """FR-1: Empty name returns 422."""
        response = client.post(
            "/api/students", json={"student_id": "STU001", "name": ""}
        )
        assert response.status_code == 422

    def test_create_student_name_too_long(self, client):
        """FR-1: Name longer than 100 chars returns 422."""
        response = client.post(
            "/api/students",
            json={"student_id": "STU001", "name": "A" * 101},
        )
        assert response.status_code == 422

    def test_create_student_name_blank_spaces(self, client):
        """FR-1: Name with only spaces returns 422."""
        response = client.post(
            "/api/students", json={"student_id": "STU001", "name": "   "}
        )
        assert response.status_code == 422

    def test_create_student_missing_fields(self, client):
        """FR-1: Missing required fields returns 422."""
        response = client.post("/api/students", json={})
        assert response.status_code == 422

    def test_create_student_missing_name(self, client):
        """FR-1: Missing name field returns 422."""
        response = client.post(
            "/api/students", json={"student_id": "STU001"}
        )
        assert response.status_code == 422

    def test_create_student_alphanumeric_id(self, client):
        """FR-1: Alphanumeric student_id is accepted."""
        response = client.post(
            "/api/students",
            json={"student_id": "abc123", "name": "Test Student"},
        )
        assert response.status_code == 201


class TestListStudents:
    """Tests for GET /api/students (FR-6)."""

    def test_list_students_empty(self, client):
        """FR-6: Empty database returns empty list."""
        response = client.get("/api/students")
        assert response.status_code == 200
        data = response.json()
        assert data["students"] == []
        assert data["total"] == 0

    def test_list_students_with_data(self, client):
        """FR-6: Returns all students."""
        client.post("/api/students", json={"student_id": "STU001", "name": "Alice"})
        client.post("/api/students", json={"student_id": "STU002", "name": "Bob"})
        response = client.get("/api/students")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["students"]) == 2

    def test_list_students_pagination(self, client):
        """FR-6: Pagination works correctly."""
        for i in range(15):
            client.post(
                "/api/students",
                json={"student_id": f"STU{i:03d}", "name": f"Student {i}"},
            )

        # Page 1
        response = client.get("/api/students?page=1&per_page=5")
        data = response.json()
        assert data["total"] == 15
        assert len(data["students"]) == 5
        assert data["page"] == 1
        assert data["per_page"] == 5

        # Page 2
        response = client.get("/api/students?page=2&per_page=5")
        data = response.json()
        assert len(data["students"]) == 5

        # Page 3
        response = client.get("/api/students?page=3&per_page=5")
        data = response.json()
        assert len(data["students"]) == 5

    def test_list_students_filter_by_name(self, client):
        """FR-6: Filter by name (partial match)."""
        client.post("/api/students", json={"student_id": "STU001", "name": "Alice Johnson"})
        client.post("/api/students", json={"student_id": "STU002", "name": "Bob Smith"})
        client.post("/api/students", json={"student_id": "STU003", "name": "Alice Brown"})

        response = client.get("/api/students?name=Alice")
        data = response.json()
        assert data["total"] == 2
        assert all("Alice" in s["name"] for s in data["students"])


class TestGetStudent:
    """Tests for GET /api/students/{student_id} (FR-6)."""

    def test_get_student_success(self, client_with_student):
        """FR-6: Retrieve existing student by student_id."""
        response = client_with_student.get("/api/students/STU001")
        assert response.status_code == 200
        data = response.json()
        assert data["student_id"] == "STU001"
        assert data["name"] == "Alice Johnson"

    def test_get_student_not_found(self, client):
        """FR-6: Non-existent student returns 404."""
        response = client.get("/api/students/NONEXIST")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
