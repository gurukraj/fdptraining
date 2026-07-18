# Weather Dashboard API - Project Constitution

## Project Identity
- **Name**: Weather Dashboard API
- **Type**: RESTful API Service
- **Version**: 1.0.0

## Mission Statement
Provide a robust, well-structured Flask-based REST API for weather data retrieval, caching, conversion, and alerting with support for both real and mock weather data providers.

## Core Principles
1. **Provider Abstraction**: Weather data sources are interchangeable (mock vs real API)
2. **Cache-First**: All weather data is cached in SQLite with configurable TTL
3. **Zero-Config Start**: Works immediately with mock provider, no API keys needed
4. **Consistent API**: All responses follow a uniform JSON structure
5. **Testability**: Every feature is covered by automated tests

## Technology Decisions
- **Framework**: Flask 3.x (lightweight, well-documented, perfect for microservices)
- **Database**: SQLite via SQLAlchemy (zero-config, built into Python)
- **HTTP Client**: requests library (for external API calls)
- **Testing**: pytest (industry standard)

## Boundaries
- This is a backend API only (no frontend)
- Authentication is simplified (user_id header, no JWT/OAuth)
- SQLite is sufficient (no need for PostgreSQL/MySQL for this use case)

## Quality Standards
- All endpoints return proper HTTP status codes
- Error responses are consistent JSON format
- All timestamps are UTC ISO 8601
- Test coverage for all functional requirements
