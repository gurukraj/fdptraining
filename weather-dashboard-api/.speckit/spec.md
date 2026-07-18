# Weather Dashboard API - Software Design Document (SDD) Spec

## Overview
A Flask REST API providing weather data services with caching, unit conversion, alerts, and user favorites management.

## Functional Requirements

### FR-1: Get Current Weather
- **Endpoint**: `GET /api/weather/current?city=London` or `?lat=51.5074&lon=-0.1278`
- **Units**: celsius (default), fahrenheit, kelvin
- **Caching**: SQLite with 10-minute TTL
- **Response fields**: temperature, feels_like, temp_min, temp_max, humidity, pressure, wind_speed, wind_direction, condition, description, icon, visibility, units, source, fetched_at
- **Errors**: 404 for invalid city, 400 for missing params

### FR-2: Get 5-Day Forecast
- **Endpoint**: `GET /api/weather/forecast?city=London&units=celsius`
- **Response**: Forecast grouped by date with daily summaries and 3-hour intervals
- **Caching**: 1-hour TTL

### FR-3: Temperature Unit Conversion
- **Endpoint**: `GET /api/weather/convert?value=100&from=celsius&to=fahrenheit`
- **Batch**: `POST /api/weather/convert` with array of values
- **Supports**: celsius, fahrenheit, kelvin

### FR-4: Severe Weather Alerts
- **Configure**: `POST /api/alerts/configure` - set thresholds
- **Check**: `GET /api/alerts/check?city=London` - check against thresholds
- **Severity**: warning, critical

### FR-5: Weather Data Caching
- **Stats**: `GET /api/cache/stats`
- **Clear**: `DELETE /api/cache`
- **Behavior**: Cache-first with TTL-based expiration

### FR-6: City Favorites & Search History
- **Add**: `POST /api/favorites`
- **List**: `GET /api/favorites?user_id=user1`
- **Remove**: `DELETE /api/favorites/{city}`
- **History**: `GET /api/history?user_id=user1` (auto-recorded)

## Architecture
- **Provider Pattern**: Abstract base provider with mock and OpenWeatherMap implementations
- **Service Layer**: Business logic separated from routes
- **Cache Layer**: SQLite-backed with configurable TTL
- **Config-driven**: Provider selection via WEATHER_PROVIDER env var

## Acceptance Criteria
- All 6 FRs have working endpoints with proper status codes
- Mock provider works without any API key
- Cache correctly serves stale data with source indication
- Temperature conversions are mathematically accurate
- Alert thresholds trigger appropriate severity levels
- Tests pass for all endpoints and edge cases
