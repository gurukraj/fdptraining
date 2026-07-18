# Technology Stack Decisions

## Flask 3.x - Web Framework

**Why Flask?**

Flask was chosen as the web framework for this project for several compelling reasons:

1. **Lightweight & Minimal**: Flask provides just what you need without imposing structure. For a microservice-style API like this weather dashboard, we don't need the full-featured batteries-included approach of Django.

2. **Simple Routing**: Flask's decorator-based routing (`@app.route(...)`) makes API endpoint definition clean and readable. Blueprint support allows modular route organization.

3. **Extensible**: Flask's ecosystem provides extensions like Flask-SQLAlchemy for ORM support, allowing us to add capabilities as needed without framework bloat.

4. **Industry Standard**: Flask is one of the most widely used Python web frameworks, particularly for REST APIs and microservices. It has excellent documentation and community support.

5. **App Factory Pattern**: Flask's `create_app()` factory pattern makes testing straightforward - we can create isolated app instances with different configurations for each test.

## SQLite - Database

**Why SQLite?**

SQLite was selected as the database engine for these reasons:

1. **Zero Configuration**: SQLite requires no separate database server, no installation, no setup. It's a single file that's created automatically.

2. **Built into Python**: The `sqlite3` module is part of Python's standard library, eliminating external dependencies for the database layer.

3. **Perfect for Caching**: Our primary database use case is caching weather data with TTL-based expiration. SQLite handles this read-heavy, low-contention workload efficiently.

4. **Portable**: The entire database is a single file, making it easy to reset, back up, or share the application state.

5. **Sufficient for Scope**: For a single-server weather dashboard API with caching, favorites, and search history, SQLite provides more than enough performance and reliability.

## SQLAlchemy - ORM

**Why SQLAlchemy (via Flask-SQLAlchemy)?**

1. **Pythonic Models**: Define database tables as Python classes with clear field types and constraints.

2. **Database Agnostic**: While we use SQLite, the ORM layer means switching to PostgreSQL or MySQL would require only a connection string change.

3. **Query Builder**: SQLAlchemy's query API is expressive and safe from SQL injection.

4. **Migration Support**: The models can be used with Alembic for database migrations in production scenarios.

## requests - HTTP Client

**Why requests?**

1. **Simple API**: The `requests` library provides a clean, intuitive interface for making HTTP requests to external APIs like OpenWeatherMap.

2. **Industry Standard**: It's the de facto standard for HTTP requests in Python.

3. **Feature Rich**: Built-in support for timeouts, error handling, JSON parsing, and query parameter encoding.

4. **Used in Provider Pattern**: The OpenWeatherMap provider uses `requests` to fetch real weather data when configured.

## pytest - Testing Framework

**Why pytest?**

1. **Industry Standard**: pytest is the most popular Python testing framework, used by major projects and organizations.

2. **Fixture System**: pytest's fixture system enables clean test setup/teardown, database initialization, and test client creation.

3. **Assertion Introspection**: Plain `assert` statements provide detailed failure messages without needing special assertion methods.

4. **Plugin Ecosystem**: Rich plugin ecosystem (e.g., pytest-cov for coverage, pytest-flask for Flask-specific utilities).

5. **Parameterization**: Easy to create parameterized tests for conversion edge cases and multiple city scenarios.

## Architecture: Provider Pattern

**Why the Provider Pattern?**

The Provider Pattern was chosen to abstract weather data sources:

```
BaseWeatherProvider (Abstract)
├── MockWeatherProvider    # Local JSON datasets + random variation
└── OpenWeatherMapProvider # Real API with HTTP requests
```

**Benefits:**
1. **Testability**: Tests always use the mock provider, ensuring consistent, predictable results
2. **Development Speed**: Developers can work without API keys or internet access
3. **Flexibility**: New providers (e.g., WeatherAPI, AccuWeather) can be added without changing service logic
4. **Configuration-Driven**: Switch between providers via a single environment variable
5. **Spec-Aligned**: The SDD spec distinguished between "cache", "api", and "mock" data sources, directly informing this pattern
