# Technology Stack

A detailed explanation of every technology choice in the Student Grade Calculator API and why it was selected.

---

## Language: Python 3.12+

| Aspect | Details |
|--------|---------|
| **Version** | 3.12 or later |
| **Role** | Primary programming language |

### Why Python 3.12+?

- **Enhanced Type Hints**: Python 3.12 brings improved support for generic types (`list[str]` instead of `typing.List[str]`), `type` statement for aliases, and better `TypeVar` syntax. This results in cleaner, more self-documenting code that pairs perfectly with Pydantic and FastAPI.
- **Performance Improvements**: CPython 3.12 introduced significant interpreter optimizations, including faster comprehensions, improved `asyncio` task groups, and reduced memory footprint. Real-world benchmarks show 5-20% speed improvements over 3.11.
- **Better Error Messages**: Enhanced tracebacks and error messages make debugging substantially easier -- a huge benefit in an educational context where students are learning to interpret errors.
- **Mature Ecosystem**: Python has the richest ecosystem for web APIs, data processing, and educational tooling.
- **Industry Standard**: Python consistently ranks as the #1 or #2 most popular programming language, making it the most practical choice for faculty workshops.

---

## Web Framework: FastAPI

| Aspect | Details |
|--------|---------|
| **Version** | 0.115.x |
| **Role** | HTTP API framework |

### Why FastAPI?

- **Automatic OpenAPI Documentation**: FastAPI auto-generates interactive API docs at `/docs` (Swagger UI) and `/redoc` (ReDoc) from your code. This eliminates the need to maintain separate API documentation and is invaluable for workshop demonstrations.
- **Pydantic Integration**: Request and response validation is built-in through Pydantic models. Invalid data is automatically rejected with detailed 422 error responses -- no manual validation code needed.
- **Dependency Injection**: FastAPI's `Depends()` system provides clean, testable database session management. Each request gets its own session that is automatically cleaned up.
- **Async Support**: While this project uses synchronous SQLAlchemy for simplicity, FastAPI supports async/await natively, making it easy to scale when needed.
- **Type Safety**: Route parameters, query parameters, and request bodies are all type-checked, catching bugs at development time rather than runtime.
- **Modern Python Patterns**: FastAPI embraces modern Python idioms (type hints, dataclasses, context managers), making it an excellent teaching tool.
- **Performance**: FastAPI is one of the fastest Python web frameworks, built on Starlette and Uvicorn (ASGI).

---

## Database: SQLite

| Aspect | Details |
|--------|---------|
| **Version** | Built-in (Python `sqlite3` module) |
| **Role** | Persistent data storage |

### Why SQLite?

- **Zero Configuration**: SQLite requires no server setup, no installation, no credentials, and no network configuration. Run `python seed_database.py` and the database is ready.
- **Built-in to Python**: The `sqlite3` module ships with every Python installation. No external database server is needed.
- **Perfect for Education**: Workshop participants can focus on learning API development and SDD principles rather than wrestling with database administration. The entire database is a single file (`grades.db`).
- **Full SQL Support**: SQLite supports standard SQL including JOINs, aggregations, constraints (UNIQUE, CHECK, FOREIGN KEY), and transactions. All the SQL concepts taught in this project transfer directly to PostgreSQL, MySQL, etc.
- **Portable**: The database file can be shared, backed up, or deleted and recreated in seconds. Each participant gets their own isolated environment.
- **Production Path**: While SQLite is ideal for development and small deployments, the SQLAlchemy abstraction layer means switching to PostgreSQL or MySQL requires only changing the connection string.

---

## ORM: SQLAlchemy 2.x

| Aspect | Details |
|--------|---------|
| **Version** | 2.0.x |
| **Role** | Object-Relational Mapping |

### Why SQLAlchemy 2.x?

- **Modern API**: SQLAlchemy 2.0 introduced a completely redesigned API with native type hint support. The `DeclarativeBase` class replaces the older `declarative_base()` function, and `Mapped[]` annotations provide full IDE autocomplete.
- **Type Safety**: Column definitions use typed annotations (`Column(Integer)`, `Column(String)`) that work with mypy and IDE type checkers, catching data type mismatches before runtime.
- **Relationship Management**: SQLAlchemy handles the Student-Score foreign key relationship automatically, including cascading deletes and lazy/eager loading strategies.
- **Query Builder**: The query API (`db.query(Student).filter(...)`) is both readable and powerful, supporting complex JOINs, aggregations, and subqueries without raw SQL.
- **Session Management**: SQLAlchemy's session pattern (Unit of Work) ensures database consistency with automatic transaction management, rollback on errors, and connection pooling.
- **Database Agnostic**: The same model definitions work with SQLite, PostgreSQL, MySQL, and 10+ other databases. Only the connection string changes.
- **Industry Standard**: SQLAlchemy is the most widely-used Python ORM, making the skills learned here directly transferable to production projects.

---

## Validation: Pydantic 2.x

| Aspect | Details |
|--------|---------|
| **Version** | 2.10.x |
| **Role** | Data validation and serialization |

### Why Pydantic 2.x?

- **Automatic Validation**: Define a schema once and Pydantic validates all incoming data automatically. `score: int = Field(ge=0, le=100)` enforces the 0-100 range without any manual `if` statements.
- **Rust-Powered Core**: Pydantic 2.x rewrote its validation core in Rust, making it 5-50x faster than v1. This means validation overhead is negligible even under load.
- **Clear Error Messages**: When validation fails, Pydantic generates detailed, structured error responses that tell the client exactly which field failed and why. FastAPI returns these as 422 responses automatically.
- **Serialization**: `model_config = {"from_attributes": True}` enables automatic conversion from SQLAlchemy model instances to JSON-serializable response schemas. No manual `to_dict()` methods needed.
- **Custom Validators**: The `@field_validator` decorator allows custom validation logic (e.g., checking that `student_id` is alphanumeric) while keeping the validation co-located with the schema definition.
- **Documentation Generation**: Pydantic models automatically generate JSON Schema, which FastAPI uses to populate the OpenAPI documentation with field descriptions, types, and constraints.

---

## Testing: pytest + httpx

| Aspect | Details |
|--------|---------|
| **pytest Version** | 8.3.x |
| **httpx Version** | 0.28.x |
| **Role** | Test framework + HTTP client |

### Why pytest?

- **Industry Standard**: pytest is the de facto standard for Python testing, used by Django, Flask, FastAPI, and thousands of open-source projects.
- **Fixture System**: pytest fixtures (`@pytest.fixture`) provide clean, reusable test setup. The `conftest.py` pattern allows sharing fixtures across test files without imports.
- **Clear Assertions**: Simple `assert` statements with automatic assertion introspection -- no need for `self.assertEqual()` or other verbose assertion methods.
- **Parametrization**: `@pytest.mark.parametrize` enables testing multiple inputs with a single test function, perfect for boundary value testing.
- **Plugin Ecosystem**: Plugins like `pytest-asyncio` and `pytest-cov` extend functionality without changing the test code.

### Why httpx?

- **FastAPI's TestClient**: FastAPI's `TestClient` (powered by httpx) provides a synchronous interface for testing async applications. Tests look like real HTTP calls but run in-process.
- **Real HTTP Semantics**: Tests use `client.post()`, `client.get()` with real JSON payloads and status code assertions, mirroring how the API will be called in production.
- **No Server Required**: Tests run without starting a Uvicorn server, making them fast (milliseconds per test) and CI-friendly.

---

## ASGI Server: Uvicorn

| Aspect | Details |
|--------|---------|
| **Version** | 0.34.x |
| **Role** | Production ASGI server |

### Why Uvicorn?

- **ASGI Native**: Uvicorn is a lightning-fast ASGI server built on `uvloop` and `httptools`. It's the recommended server for FastAPI.
- **Development Mode**: `uvicorn app.main:app --reload` provides automatic code reloading during development, enabling a rapid feedback loop.
- **Production Ready**: With `--workers` flag, Uvicorn can run multiple worker processes for production deployments.
- **Simple Interface**: A single command (`uvicorn app.main:app`) starts the server. No configuration files needed.

---

## Summary Table

| Technology | Version | Purpose | Key Benefit |
|------------|---------|---------|-------------|
| Python | 3.12+ | Language | Type hints, performance, ecosystem |
| FastAPI | 0.115.x | Web framework | Auto docs, validation, DI |
| SQLite | Built-in | Database | Zero config, portable |
| SQLAlchemy | 2.0.x | ORM | Type-safe models, DB agnostic |
| Pydantic | 2.10.x | Validation | Automatic, fast, clear errors |
| pytest | 8.3.x | Testing | Fixtures, assertions, plugins |
| httpx | 0.28.x | Test HTTP client | Real HTTP semantics, fast |
| Uvicorn | 0.34.x | ASGI server | Fast, reload, production ready |
