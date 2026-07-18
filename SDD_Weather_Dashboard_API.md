# Software Design Document: Weather Dashboard Microservice

## Faculty Development Program — AI-Native Software Development

| Field               | Detail                                                      |
|---------------------|-------------------------------------------------------------|
| **Module**          | Hands-on Exercise 3 — Weather Dashboard Microservice         |
| **Duration**        | 1 – 1.5 hours (practical, instructor-guided)                |
| **Tech Stack**      | Python 3.12+, Flask 3.x, SQLite, `requests` library, pytest |
| **Difficulty**      | Beginner–Intermediate                                        |
| **Prerequisites**   | Basic Python, REST concepts, JSON handling                   |
| **Outcome**         | Participants build a weather API with caching, alerts, unit conversion, and user favorites |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Functional Requirements](#2-functional-requirements)
   - [FR-1: Get Current Weather](#fr-1-get-current-weather)
   - [FR-2: Get 5-Day Forecast](#fr-2-get-5-day-forecast)
   - [FR-3: Temperature Unit Conversion](#fr-3-temperature-unit-conversion)
   - [FR-4: Severe Weather Alerts](#fr-4-severe-weather-alerts)
   - [FR-5: Weather Data Caching](#fr-5-weather-data-caching)
   - [FR-6: City Favorites & Search History](#fr-6-city-favorites--search-history)
3. [Non-Functional Requirements](#3-non-functional-requirements)
4. [Domain Model](#4-domain-model)
5. [API Contract](#5-api-contract)
6. [Data Model — SQLite Schema](#6-data-model--sqlite-schema)
7. [Architecture](#7-architecture)
8. [Test Strategy](#8-test-strategy)
9. [Appendix](#9-appendix)

---

## 1. Introduction

### 1.1 Purpose

This document specifies the design for a **Weather Dashboard Microservice** — a Flask-based REST API that wraps the OpenWeatherMap API, adding caching, temperature unit conversion, severe weather alerts, and user-level favorites/search history. The exercise is designed for a **Faculty Development Program** to demonstrate AI-native software development practices with Python.

### 1.2 Scope

The microservice covers the following capabilities:

- Retrieve current weather by city name or geographic coordinates
- Retrieve 5-day / 3-hour forecasts with hourly breakdown
- Convert temperatures between Celsius, Fahrenheit, and Kelvin
- Configure severe weather alert thresholds and check conditions
- Cache external API responses in SQLite with configurable TTL
- Manage per-user favorite cities and search history

### 1.3 Audience

Faculty members participating in the AI-Native Software Development workshop. Participants should be comfortable with Python fundamentals and basic REST API concepts.

### 1.4 Conventions

| Convention        | Description                                        |
|-------------------|----------------------------------------------------|
| `snake_case`      | URL path segments and JSON field names              |
| `PascalCase`      | Python class names (`WeatherData`, `Alert`)         |
| ISO 8601          | All date/time fields (`2025-01-15T10:30:00Z`)       |
| UTC               | All timestamps stored and returned in UTC           |
| Metric by default | Temperature in Celsius unless specified otherwise   |

---

## 2. Functional Requirements

### FR-1: Get Current Weather

| Field              | Detail                                           |
|--------------------|--------------------------------------------------|
| **ID**             | FR-1                                             |
| **Title**          | Get Current Weather by City or Coordinates       |
| **Priority**       | P0 — Must Have                                   |
| **Actor**          | Any API Client                                   |
| **HTTP Method**    | `GET`                                            |
| **Endpoint**       | `/api/weather/current`                           |
| **Estimated Time** | 15 minutes                                       |

#### Description

Retrieve the current weather for a location specified by city name or geographic coordinates (latitude/longitude). The system fetches data from the OpenWeatherMap API (or returns cached data if available) and returns a normalized response with temperature, humidity, wind speed, weather condition, and description.

#### Acceptance Criteria

1. **AC-1.1**: A `GET /api/weather/current?city=London` request returns `200 OK` with current weather data including `temperature`, `humidity`, `wind_speed`, `condition`, and `description`.
2. **AC-1.2**: A `GET /api/weather/current?lat=51.5074&lon=-0.1278` request returns the same weather data format using coordinates.
3. **AC-1.3**: The response includes the `city_name`, `country_code`, `coordinates` (lat/lon), and a `fetched_at` timestamp.
4. **AC-1.4**: If the `units` query parameter is provided (`celsius`, `fahrenheit`, or `kelvin`), the temperature is converted accordingly; default is `celsius`.
5. **AC-1.5**: If cached data exists and is within the TTL window, the cached data is returned without calling the external API.
6. **AC-1.6**: The response includes a `source` field indicating `"cache"` or `"api"` to show where the data came from.

#### Edge Cases

1. **EC-1.1**: An invalid city name (e.g., `"xyznonexistent123"`) returns `404 Not Found` with message `"City not found"`.
2. **EC-1.2**: Missing both `city` and `lat`/`lon` parameters returns `400 Bad Request` with message `"Provide either 'city' or both 'lat' and 'lon' parameters"`.
3. **EC-1.3**: Coordinates outside valid range (lat: -90 to 90, lon: -180 to 180) return `400 Bad Request`.
4. **EC-1.4**: When the OpenWeatherMap API is unreachable or returns an error, the system returns stale cached data (if available) with a `"stale_cache"` source indicator, or `503 Service Unavailable` if no cache exists.
5. **EC-1.5**: An invalid `units` value returns `400 Bad Request` with message `"Units must be one of: celsius, fahrenheit, kelvin"`.

#### Request Example

```
GET /api/weather/current?city=London&units=celsius
```

#### Response Example — `200 OK`

```json
{
  "success": true,
  "data": {
    "city_name": "London",
    "country_code": "GB",
    "coordinates": {
      "lat": 51.5074,
      "lon": -0.1278
    },
    "temperature": 12.5,
    "feels_like": 10.8,
    "temp_min": 10.2,
    "temp_max": 14.1,
    "humidity": 72,
    "pressure": 1013,
    "wind_speed": 5.4,
    "wind_direction": 220,
    "condition": "Clouds",
    "description": "overcast clouds",
    "icon": "04d",
    "visibility": 10000,
    "units": "celsius",
    "source": "api",
    "fetched_at": "2025-01-15T10:30:00Z"
  }
}
```

---

### FR-2: Get 5-Day Forecast

| Field              | Detail                                           |
|--------------------|--------------------------------------------------|
| **ID**             | FR-2                                             |
| **Title**          | Get 5-Day Forecast with Hourly Breakdown         |
| **Priority**       | P0 — Must Have                                   |
| **Actor**          | Any API Client                                   |
| **HTTP Method**    | `GET`                                            |
| **Endpoint**       | `/api/weather/forecast`                          |
| **Estimated Time** | 15 minutes                                       |

#### Description

Retrieve a 5-day weather forecast with data points at 3-hour intervals. The response groups forecast entries by date and provides daily summaries (high/low temperature, dominant condition) alongside the hourly breakdown.

#### Acceptance Criteria

1. **AC-2.1**: A `GET /api/weather/forecast?city=London` request returns `200 OK` with forecast data organized by date.
2. **AC-2.2**: Each day includes a `summary` object with `date`, `temp_high`, `temp_low`, `dominant_condition`, and `avg_humidity`.
3. **AC-2.3**: Each day includes an `hourly` array with 3-hour interval entries, each containing `time`, `temperature`, `humidity`, `condition`, `description`, and `wind_speed`.
4. **AC-2.4**: Coordinates (`lat`/`lon`) can be used instead of `city` name.
5. **AC-2.5**: The `units` query parameter controls temperature units (default: `celsius`).
6. **AC-2.6**: Forecast data is cached with a separate TTL (default: 1 hour) from current weather data.

#### Edge Cases

1. **EC-2.1**: An invalid city name returns `404 Not Found`.
2. **EC-2.2**: The forecast may return fewer than 5 full days if the first or last day is partial; the API still returns `200 OK`.
3. **EC-2.3**: When the external API returns an empty forecast list, the response returns `200 OK` with an empty `forecast` array.

#### Request Example

```
GET /api/weather/forecast?city=London&units=celsius
```

#### Response Example — `200 OK`

```json
{
  "success": true,
  "data": {
    "city_name": "London",
    "country_code": "GB",
    "units": "celsius",
    "source": "api",
    "forecast": [
      {
        "date": "2025-01-15",
        "summary": {
          "temp_high": 14.1,
          "temp_low": 8.3,
          "dominant_condition": "Clouds",
          "avg_humidity": 68
        },
        "hourly": [
          {
            "time": "09:00:00",
            "temperature": 10.2,
            "feels_like": 8.5,
            "humidity": 72,
            "condition": "Clouds",
            "description": "overcast clouds",
            "wind_speed": 5.4,
            "icon": "04d"
          },
          {
            "time": "12:00:00",
            "temperature": 13.8,
            "feels_like": 12.1,
            "humidity": 62,
            "condition": "Clouds",
            "description": "broken clouds",
            "wind_speed": 6.1,
            "icon": "04d"
          },
          {
            "time": "15:00:00",
            "temperature": 14.1,
            "feels_like": 12.5,
            "humidity": 65,
            "condition": "Clear",
            "description": "clear sky",
            "wind_speed": 4.8,
            "icon": "01d"
          }
        ]
      },
      {
        "date": "2025-01-16",
        "summary": {
          "temp_high": 11.5,
          "temp_low": 5.9,
          "dominant_condition": "Rain",
          "avg_humidity": 81
        },
        "hourly": [
          {
            "time": "00:00:00",
            "temperature": 7.2,
            "feels_like": 5.0,
            "humidity": 85,
            "condition": "Rain",
            "description": "light rain",
            "wind_speed": 3.2,
            "icon": "10n"
          }
        ]
      }
    ]
  }
}
```

---

### FR-3: Temperature Unit Conversion

| Field              | Detail                                           |
|--------------------|--------------------------------------------------|
| **ID**             | FR-3                                             |
| **Title**          | Temperature Unit Conversion (C / F / K)          |
| **Priority**       | P0 — Must Have                                   |
| **Actor**          | Any API Client                                   |
| **HTTP Method**    | `GET`                                            |
| **Endpoint**       | `/api/weather/convert`                           |
| **Estimated Time** | 10 minutes                                       |

#### Description

Provide a standalone temperature conversion endpoint that converts a given temperature value between Celsius (C), Fahrenheit (F), and Kelvin (K). This is also used internally by other endpoints when the `units` parameter is specified.

#### Conversion Formulas

| From       | To         | Formula                         |
|------------|------------|---------------------------------|
| Celsius    | Fahrenheit | `F = C × 9/5 + 32`             |
| Celsius    | Kelvin     | `K = C + 273.15`               |
| Fahrenheit | Celsius    | `C = (F − 32) × 5/9`          |
| Fahrenheit | Kelvin     | `K = (F − 32) × 5/9 + 273.15` |
| Kelvin     | Celsius    | `C = K − 273.15`               |
| Kelvin     | Fahrenheit | `F = (K − 273.15) × 9/5 + 32` |

#### Acceptance Criteria

1. **AC-3.1**: A `GET /api/weather/convert?value=100&from=celsius&to=fahrenheit` returns `200 OK` with the converted value `212.0`.
2. **AC-3.2**: The response includes `original_value`, `original_unit`, `converted_value`, `converted_unit`, and `formula` (human-readable).
3. **AC-3.3**: All conversions are rounded to 2 decimal places.
4. **AC-3.4**: Converting from a unit to the same unit returns the original value unchanged.
5. **AC-3.5**: The endpoint supports all 6 conversion directions (C→F, C→K, F→C, F→K, K→C, K→F).
6. **AC-3.6**: The conversion logic is implemented as a pure function that can be imported and reused by other modules.

#### Edge Cases

1. **EC-3.1**: Missing required parameters (`value`, `from`, `to`) returns `400 Bad Request` with the list of missing fields.
2. **EC-3.2**: A non-numeric `value` returns `400 Bad Request` with message `"Value must be a number"`.
3. **EC-3.3**: A Kelvin value below `0` returns `400 Bad Request` with message `"Kelvin temperature cannot be below absolute zero (0 K)"`.
4. **EC-3.4**: An invalid unit (not `celsius`, `fahrenheit`, or `kelvin`) returns `400 Bad Request`.

#### Request Example

```
GET /api/weather/convert?value=100&from=celsius&to=fahrenheit
```

#### Response Example — `200 OK`

```json
{
  "success": true,
  "data": {
    "original_value": 100.0,
    "original_unit": "celsius",
    "converted_value": 212.0,
    "converted_unit": "fahrenheit",
    "formula": "F = C × 9/5 + 32"
  }
}
```

#### Response Example — Same Unit

```json
{
  "success": true,
  "data": {
    "original_value": 25.0,
    "original_unit": "celsius",
    "converted_value": 25.0,
    "converted_unit": "celsius",
    "formula": "No conversion needed"
  }
}
```

---

### FR-4: Severe Weather Alerts

| Field              | Detail                                           |
|--------------------|--------------------------------------------------|
| **ID**             | FR-4                                             |
| **Title**          | Severe Weather Alerts with Configurable Thresholds |
| **Priority**       | P1 — Should Have                                 |
| **Actor**          | Any API Client                                   |
| **HTTP Methods**   | `GET`, `POST`, `DELETE`                          |
| **Endpoints**      | `/api/alerts/check`, `/api/alerts/thresholds`, `/api/alerts` |
| **Estimated Time** | 15 minutes                                       |

#### Description

Allow users to configure severe weather alert thresholds (e.g., temperature above 40°C, wind speed above 100 km/h, humidity below 20%) and check whether current conditions for a given city trigger any alerts. Triggered alerts are stored in the database for historical review.

#### Acceptance Criteria

1. **AC-4.1**: `POST /api/alerts/thresholds` creates a new alert threshold with `metric`, `operator` (`gt`, `lt`, `gte`, `lte`, `eq`), `value`, and optional `city` (global if omitted). Returns `201 Created`.
2. **AC-4.2**: `GET /api/alerts/thresholds` lists all configured thresholds, optionally filtered by `city`.
3. **AC-4.3**: `DELETE /api/alerts/thresholds/:id` removes a threshold configuration. Returns `200 OK`.
4. **AC-4.4**: `GET /api/alerts/check?city=London` fetches current weather for the city and evaluates it against all matching thresholds (city-specific + global). Returns a list of triggered and non-triggered alerts.
5. **AC-4.5**: When an alert is triggered, a record is created in the `alerts` table with `threshold_id`, `city`, `actual_value`, `threshold_value`, and `triggered_at`.
6. **AC-4.6**: `GET /api/alerts?city=London` returns the history of triggered alerts for a city, sorted by `triggered_at` descending.

#### Edge Cases

1. **EC-4.1**: Creating a threshold with an invalid `metric` (not one of `temperature`, `humidity`, `wind_speed`, `pressure`) returns `400 Bad Request`.
2. **EC-4.2**: Creating a threshold with an invalid `operator` returns `400 Bad Request`.
3. **EC-4.3**: Checking alerts for a city with no configured thresholds returns `200 OK` with an empty `triggered` array and a message `"No thresholds configured"`.
4. **EC-4.4**: If the external weather API is unavailable during a check, return `503 Service Unavailable`.

#### Request Example — Create Threshold

```
POST /api/alerts/thresholds
Content-Type: application/json

{
  "metric": "temperature",
  "operator": "gt",
  "value": 40,
  "city": "Delhi"
}
```

#### Response Example — `201 Created`

```json
{
  "success": true,
  "data": {
    "id": 1,
    "metric": "temperature",
    "operator": "gt",
    "value": 40.0,
    "city": "Delhi",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

#### Response Example — `GET /api/alerts/check?city=Delhi`

```json
{
  "success": true,
  "data": {
    "city": "Delhi",
    "current_weather": {
      "temperature": 42.3,
      "humidity": 25,
      "wind_speed": 12.5,
      "pressure": 1005
    },
    "triggered": [
      {
        "threshold_id": 1,
        "metric": "temperature",
        "operator": "gt",
        "threshold_value": 40.0,
        "actual_value": 42.3,
        "message": "Temperature (42.3°C) exceeds threshold (40.0°C)",
        "severity": "warning",
        "triggered_at": "2025-01-15T14:00:00Z"
      }
    ],
    "not_triggered": []
  }
}
```

---

### FR-5: Weather Data Caching

| Field              | Detail                                           |
|--------------------|--------------------------------------------------|
| **ID**             | FR-5                                             |
| **Title**          | Weather Data Caching with SQLite and Configurable TTL |
| **Priority**       | P0 — Must Have                                   |
| **Actor**          | System (internal)                                |
| **HTTP Method**    | `GET`, `DELETE`                                  |
| **Endpoints**      | `/api/cache/stats`, `/api/cache/clear`           |
| **Estimated Time** | 10 minutes                                       |

#### Description

Cache all weather data fetched from the external OpenWeatherMap API in a SQLite database to reduce API calls, improve response time, and provide resilience when the external API is unavailable. The TTL (Time-To-Live) is configurable per data type.

#### Acceptance Criteria

1. **AC-5.1**: When weather data is fetched from the external API, it is stored in the `weather_cache` table with a `cache_key`, `data` (JSON), `data_type`, and `expires_at` timestamp.
2. **AC-5.2**: Subsequent requests for the same location and data type check the cache first; if a valid (non-expired) entry exists, it is returned without calling the external API.
3. **AC-5.3**: The cache TTL is configurable via environment variables: `CACHE_TTL_CURRENT` (default: 600 seconds / 10 minutes) and `CACHE_TTL_FORECAST` (default: 3600 seconds / 1 hour).
4. **AC-5.4**: `GET /api/cache/stats` returns cache statistics: `total_entries`, `expired_entries`, `active_entries`, `hit_rate` (percentage), `total_hits`, `total_misses`.
5. **AC-5.5**: `DELETE /api/cache/clear` purges all cached entries and returns the count of deleted records.
6. **AC-5.6**: Expired cache entries are lazily cleaned up — checked on read, and a background cleanup can be triggered via `DELETE /api/cache/clear?expired_only=true`.

#### Edge Cases

1. **EC-5.1**: If the cache database is corrupted or inaccessible, the system logs a warning and falls back to direct API calls (graceful degradation).
2. **EC-5.2**: Concurrent requests for the same uncached city should result in only one external API call (simple locking or "first write wins").
3. **EC-5.3**: Cache entries with malformed JSON data are silently discarded and re-fetched.

#### Response Example — `GET /api/cache/stats`

```json
{
  "success": true,
  "data": {
    "total_entries": 45,
    "active_entries": 32,
    "expired_entries": 13,
    "hit_rate": 78.5,
    "total_hits": 234,
    "total_misses": 64,
    "oldest_entry": "2025-01-15T08:00:00Z",
    "newest_entry": "2025-01-15T10:30:00Z",
    "database_size_kb": 128
  }
}
```

#### Response Example — `DELETE /api/cache/clear`

```json
{
  "success": true,
  "message": "Cache cleared successfully",
  "data": {
    "deleted_count": 45
  }
}
```

---

### FR-6: City Favorites & Search History

| Field              | Detail                                           |
|--------------------|--------------------------------------------------|
| **ID**             | FR-6                                             |
| **Title**          | City Favorites & Search History per User         |
| **Priority**       | P1 — Should Have                                 |
| **Actor**          | API Client (identified by `user_id` header)      |
| **HTTP Methods**   | `GET`, `POST`, `DELETE`                          |
| **Endpoints**      | `/api/favorites`, `/api/history`                 |
| **Estimated Time** | 15 minutes                                       |

#### Description

Allow users (identified by a simple `X-User-Id` header) to save favorite cities for quick access and automatically track their weather search history. Favorites are explicitly managed (add/remove), while search history is recorded automatically on every weather query.

#### Acceptance Criteria

1. **AC-6.1**: `POST /api/favorites` with `{ "city": "London" }` and `X-User-Id: user123` adds the city to the user's favorites. Returns `201 Created`.
2. **AC-6.2**: `GET /api/favorites` with `X-User-Id: user123` returns the user's list of favorite cities with the most recently added first.
3. **AC-6.3**: `DELETE /api/favorites/:city` with `X-User-Id: user123` removes the city from favorites. Returns `200 OK`.
4. **AC-6.4**: `GET /api/history` with `X-User-Id: user123` returns the user's last 50 weather searches, sorted by `searched_at` descending.
5. **AC-6.5**: Every successful call to `/api/weather/current` or `/api/weather/forecast` automatically records a search history entry with `user_id`, `city`, `query_type` (`current` or `forecast`), and `searched_at`.
6. **AC-6.6**: `DELETE /api/history` with `X-User-Id: user123` clears the user's search history. Returns `200 OK` with the count of deleted entries.

#### Edge Cases

1. **EC-6.1**: Adding a city that is already in favorites returns `409 Conflict` with message `"City is already in favorites"`.
2. **EC-6.2**: Removing a city that is not in favorites returns `404 Not Found`.
3. **EC-6.3**: Requests without the `X-User-Id` header return `400 Bad Request` with message `"X-User-Id header is required"`.
4. **EC-6.4**: `GET /api/history?limit=10` respects the `limit` parameter (default: 50, max: 200).
5. **EC-6.5**: Search history entries for anonymous requests (no `X-User-Id`) are stored with `user_id = "anonymous"`.

#### Request Example — Add Favorite

```
POST /api/favorites
X-User-Id: user123
Content-Type: application/json

{
  "city": "London"
}
```

#### Response Example — `201 Created`

```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": "user123",
    "city": "London",
    "added_at": "2025-01-15T10:30:00Z"
  }
}
```

#### Response Example — `GET /api/favorites`

```json
{
  "success": true,
  "data": [
    {
      "id": 3,
      "city": "Tokyo",
      "added_at": "2025-01-15T12:00:00Z"
    },
    {
      "id": 2,
      "city": "New York",
      "added_at": "2025-01-15T11:00:00Z"
    },
    {
      "id": 1,
      "city": "London",
      "added_at": "2025-01-15T10:30:00Z"
    }
  ],
  "count": 3
}
```

#### Response Example — `GET /api/history`

```json
{
  "success": true,
  "data": [
    {
      "id": 5,
      "city": "Tokyo",
      "query_type": "current",
      "searched_at": "2025-01-15T12:05:00Z"
    },
    {
      "id": 4,
      "city": "Tokyo",
      "query_type": "forecast",
      "searched_at": "2025-01-15T12:02:00Z"
    },
    {
      "id": 3,
      "city": "New York",
      "query_type": "current",
      "searched_at": "2025-01-15T11:30:00Z"
    }
  ],
  "count": 3,
  "limit": 50
}
```

---

## 3. Non-Functional Requirements

### NFR-1: API Rate Limiting

| Metric                           | Target                          |
|----------------------------------|---------------------------------|
| OpenWeatherMap free tier         | 60 calls/minute (1,000/day)     |
| Internal rate limit per client   | 30 requests/minute per `X-User-Id` |
| Rate limit response              | `429 Too Many Requests` with `Retry-After` header |

### NFR-2: Response Time

| Metric                    | Target            |
|---------------------------|-------------------|
| Cache hit (SQLite)        | ≤ 50 ms (p95)    |
| Cache miss (external API) | ≤ 1 500 ms (p95) |
| Unit conversion           | ≤ 10 ms (p95)    |
| Favorites / History CRUD  | ≤ 100 ms (p95)   |

### NFR-3: Cache Hit Rate

| Metric                    | Target            |
|---------------------------|-------------------|
| Current weather           | ≥ 70% after warm-up |
| Forecast data             | ≥ 85% after warm-up |
| Overall                   | ≥ 75% steady state  |

### NFR-4: Reliability & Error Handling

| Requirement                  | Detail                                               |
|------------------------------|------------------------------------------------------|
| Error response format        | Consistent JSON: `{ "success": false, "error": { "code": "...", "message": "..." } }` |
| External API timeout         | 10 seconds max per call to OpenWeatherMap            |
| Graceful degradation         | Return stale cache on external API failure           |
| SQLite WAL mode              | Enabled for concurrent read performance              |

### NFR-5: Security

| Requirement            | Detail                                             |
|------------------------|----------------------------------------------------|
| API key protection     | OpenWeatherMap API key stored in `.env`, never exposed in responses |
| Input sanitization     | All query parameters validated and sanitized        |
| SQL injection prevention | Use parameterized queries exclusively              |
| CORS                   | Configurable allowed origins via `Flask-CORS`       |

---

## 4. Domain Model

### 4.1 Entity Relationship Overview

```
┌────────────────┐         ┌────────────────────┐
│  WeatherData   │         │     Forecast       │
│  (cached)      │         │     (cached)       │
│                │         │                    │
│  cache_key     │         │  cache_key         │
│  city          │         │  city              │
│  country_code  │         │  country_code      │
│  temperature   │         │  forecast_json     │
│  humidity      │         │  data_type         │
│  wind_speed    │         │  expires_at        │
│  condition     │         │  created_at        │
│  raw_json      │         └────────────────────┘
│  expires_at    │
│  created_at    │
└────────────────┘

┌────────────────┐         ┌────────────────────┐
│     Alert      │         │ AlertThreshold     │
│  (triggered)   │         │ (configuration)    │
│                │         │                    │
│  id            │◀────────│  id                │
│  threshold_id  │  FK     │  metric            │
│  city          │         │  operator          │
│  actual_value  │         │  value             │
│  triggered_at  │         │  city (nullable)   │
└────────────────┘         │  created_at        │
                           └────────────────────┘

┌────────────────┐         ┌────────────────────┐
│ FavoriteCity   │         │  SearchHistory     │
│                │         │                    │
│  id            │         │  id                │
│  user_id       │         │  user_id           │
│  city          │         │  city              │
│  added_at      │         │  query_type        │
└────────────────┘         │  searched_at       │
                           └────────────────────┘
```

### 4.2 Entity Descriptions

| Entity              | Description                                                       |
|---------------------|-------------------------------------------------------------------|
| **WeatherData**     | Cached current weather data from OpenWeatherMap                   |
| **Forecast**        | Cached 5-day forecast data from OpenWeatherMap                    |
| **AlertThreshold**  | User-configured alert threshold (metric + operator + value)       |
| **Alert**           | Record of a triggered alert with actual vs. threshold values      |
| **FavoriteCity**    | A user's saved favorite city for quick weather access             |
| **SearchHistory**   | Automatic log of every weather query made by a user               |

---

## 5. API Contract

### 5.1 Base URL

```
http://localhost:5000/api
```

### 5.2 Common Response Envelope

All responses follow a consistent envelope:

```json
{
  "success": true | false,
  "data": { ... } | [ ... ],
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message"
  }
}
```

### 5.3 Endpoints Summary

| Method   | Endpoint                         | Description                          |
|----------|----------------------------------|--------------------------------------|
| `GET`    | `/api/weather/current`           | Get current weather                  |
| `GET`    | `/api/weather/forecast`          | Get 5-day forecast                   |
| `GET`    | `/api/weather/convert`           | Convert temperature units            |
| `POST`   | `/api/alerts/thresholds`         | Create alert threshold               |
| `GET`    | `/api/alerts/thresholds`         | List alert thresholds                |
| `DELETE` | `/api/alerts/thresholds/:id`     | Delete alert threshold               |
| `GET`    | `/api/alerts/check`              | Check alerts for a city              |
| `GET`    | `/api/alerts`                    | Get triggered alert history          |
| `POST`   | `/api/favorites`                 | Add city to favorites                |
| `GET`    | `/api/favorites`                 | List favorite cities                 |
| `DELETE` | `/api/favorites/:city`           | Remove city from favorites           |
| `GET`    | `/api/history`                   | Get search history                   |
| `DELETE` | `/api/history`                   | Clear search history                 |
| `GET`    | `/api/cache/stats`               | Get cache statistics                 |
| `DELETE` | `/api/cache/clear`               | Clear cache                          |
| `GET`    | `/api/health`                    | Health check                         |

### 5.4 Error Codes

| HTTP Status | Error Code            | Description                              |
|-------------|-----------------------|------------------------------------------|
| 400         | `VALIDATION_ERROR`    | Missing or invalid request parameters    |
| 400         | `INVALID_UNITS`       | Invalid temperature unit specified       |
| 400         | `INVALID_COORDINATES` | Coordinates outside valid range          |
| 400         | `MISSING_USER_ID`     | `X-User-Id` header not provided          |
| 404         | `CITY_NOT_FOUND`      | City name not recognized by weather API  |
| 404         | `NOT_FOUND`           | Resource not found                       |
| 409         | `DUPLICATE_FAVORITE`  | City already in user's favorites         |
| 429         | `RATE_LIMIT_EXCEEDED` | Too many requests                        |
| 503         | `EXTERNAL_API_ERROR`  | OpenWeatherMap API unavailable           |
| 500         | `INTERNAL_ERROR`      | Unexpected server error                  |

### 5.5 Detailed Error Response Example

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Provide either 'city' or both 'lat' and 'lon' parameters"
  }
}
```

### 5.6 Health Check — `GET /api/health`

#### Response Example — `200 OK`

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2025-01-15T10:00:00Z",
    "uptime_seconds": 3600,
    "database": "connected",
    "external_api": "reachable",
    "version": "1.0.0"
  }
}
```

---

## 6. Data Model — SQLite Schema

### 6.1 Complete Schema

```sql
-- ──────────────────────────────────────────────────────
-- Weather Dashboard — SQLite Schema
-- ──────────────────────────────────────────────────────

-- Enable WAL mode for better concurrent read performance
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ── Table 1: weather_cache ────────────────────────────
-- Stores cached weather data (current + forecast)
CREATE TABLE IF NOT EXISTS weather_cache (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    cache_key       TEXT    NOT NULL UNIQUE,
    city            TEXT    NOT NULL,
    country_code    TEXT,
    data_type       TEXT    NOT NULL CHECK (data_type IN ('current', 'forecast')),
    data            TEXT    NOT NULL,  -- JSON string
    expires_at      TEXT    NOT NULL,  -- ISO 8601 timestamp
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    hit_count       INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_cache_key ON weather_cache(cache_key);
CREATE INDEX IF NOT EXISTS idx_cache_city ON weather_cache(city);
CREATE INDEX IF NOT EXISTS idx_cache_expires ON weather_cache(expires_at);
CREATE INDEX IF NOT EXISTS idx_cache_data_type ON weather_cache(data_type);

-- ── Table 2: alert_thresholds ─────────────────────────
-- Configurable alert thresholds
CREATE TABLE IF NOT EXISTS alert_thresholds (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    metric      TEXT    NOT NULL CHECK (metric IN ('temperature', 'humidity', 'wind_speed', 'pressure')),
    operator    TEXT    NOT NULL CHECK (operator IN ('gt', 'lt', 'gte', 'lte', 'eq')),
    value       REAL    NOT NULL,
    city        TEXT,  -- NULL means global (applies to all cities)
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_threshold_city ON alert_thresholds(city);
CREATE INDEX IF NOT EXISTS idx_threshold_metric ON alert_thresholds(metric);

-- ── Table 3: triggered_alerts ─────────────────────────
-- History of triggered alerts
CREATE TABLE IF NOT EXISTS triggered_alerts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    threshold_id    INTEGER NOT NULL,
    city            TEXT    NOT NULL,
    metric          TEXT    NOT NULL,
    actual_value    REAL    NOT NULL,
    threshold_value REAL    NOT NULL,
    operator        TEXT    NOT NULL,
    message         TEXT    NOT NULL,
    triggered_at    TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (threshold_id) REFERENCES alert_thresholds(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_alert_city ON triggered_alerts(city);
CREATE INDEX IF NOT EXISTS idx_alert_triggered ON triggered_alerts(triggered_at);
CREATE INDEX IF NOT EXISTS idx_alert_threshold ON triggered_alerts(threshold_id);

-- ── Table 4: favorite_cities ──────────────────────────
-- Per-user favorite cities
CREATE TABLE IF NOT EXISTS favorite_cities (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     TEXT    NOT NULL,
    city        TEXT    NOT NULL,
    added_at    TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE(user_id, city)
);

CREATE INDEX IF NOT EXISTS idx_fav_user ON favorite_cities(user_id);
CREATE INDEX IF NOT EXISTS idx_fav_city ON favorite_cities(city);

-- ── Table 5: search_history ───────────────────────────
-- Automatic search history per user
CREATE TABLE IF NOT EXISTS search_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     TEXT    NOT NULL,
    city        TEXT    NOT NULL,
    query_type  TEXT    NOT NULL CHECK (query_type IN ('current', 'forecast')),
    searched_at TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_history_user ON search_history(user_id);
CREATE INDEX IF NOT EXISTS idx_history_searched ON search_history(searched_at);
CREATE INDEX IF NOT EXISTS idx_history_city ON search_history(city);
```

### 6.2 Cache Statistics View

```sql
-- Helper view for cache statistics
CREATE VIEW IF NOT EXISTS cache_stats AS
SELECT
    COUNT(*)                                                    AS total_entries,
    SUM(CASE WHEN expires_at > datetime('now') THEN 1 ELSE 0 END)  AS active_entries,
    SUM(CASE WHEN expires_at <= datetime('now') THEN 1 ELSE 0 END) AS expired_entries,
    SUM(hit_count)                                              AS total_hits
FROM weather_cache;
```

---

## 7. Architecture

### 7.1 Flask Blueprints Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Client (HTTP)                       │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  Flask Application (app.py)                             │
│  ┌──────────────┐ ┌──────────┐ ┌────────────────────┐   │
│  │ Middleware    │ │ CORS     │ │ Rate Limiter       │   │
│  │ (error handler│ │          │ │ (flask-limiter)    │   │
│  └──────────────┘ └──────────┘ └────────────────────┘   │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  Blueprints (Route Layer)                               │
│  ┌─────────────────┐ ┌───────────────┐ ┌────────────┐   │
│  │ weather_bp      │ │ alerts_bp     │ │ favorites_bp│   │
│  │ /api/weather/*  │ │ /api/alerts/* │ │ /api/fav/*  │   │
│  └────────┬────────┘ └───────┬───────┘ └─────┬──────┘   │
└───────────┼──────────────────┼───────────────┼──────────┘
            │                  │               │
┌───────────▼──────────────────▼───────────────▼──────────┐
│  Services Layer (Business Logic)                        │
│  ┌──────────────────┐ ┌──────────────┐ ┌─────────────┐  │
│  │ weather_service  │ │ alert_service│ │ user_service │  │
│  │ .py              │ │ .py          │ │ .py          │  │
│  └────────┬─────────┘ └──────┬───────┘ └──────┬──────┘  │
└───────────┼──────────────────┼────────────────┼─────────┘
            │                  │                │
┌───────────▼──────────────────▼────────────────▼─────────┐
│  Data Access Layer                                      │
│  ┌──────────────────┐ ┌────────────────────────────┐    │
│  │ cache_service.py │ │ database.py                │    │
│  │ (cache logic)    │ │ (SQLite connection + init) │    │
│  └────────┬─────────┘ └──────────┬─────────────────┘    │
└───────────┼──────────────────────┼──────────────────────┘
            │                      │
     ┌──────▼──────┐        ┌──────▼──────┐
     │ OpenWeather │        │   SQLite    │
     │ Map API     │        │  Database   │
     └─────────────┘        └─────────────┘
```

### 7.2 Project Structure

```
weather-dashboard/
├── app.py                        # Flask application factory
├── config.py                     # Configuration from environment
├── run.py                        # Entry point
├── blueprints/
│   ├── __init__.py
│   ├── weather.py                # Weather routes (current, forecast, convert)
│   ├── alerts.py                 # Alert routes (thresholds, check, history)
│   └── favorites.py              # Favorites and search history routes
├── services/
│   ├── __init__.py
│   ├── weather_service.py        # Weather fetching + conversion logic
│   ├── cache_service.py          # Caching logic (read/write/stats)
│   ├── alert_service.py          # Alert threshold evaluation
│   └── user_service.py           # Favorites + search history
├── database.py                   # SQLite connection and schema init
├── models.py                     # Data classes / named tuples
├── utils/
│   ├── __init__.py
│   ├── converters.py             # Temperature conversion functions
│   └── validators.py             # Input validation helpers
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # pytest fixtures (app, client, mock API)
│   ├── test_weather.py           # Weather endpoint tests
│   ├── test_conversion.py        # Unit conversion parametrized tests
│   ├── test_alerts.py            # Alert threshold tests
│   ├── test_cache.py             # Cache behavior tests
│   └── test_favorites.py         # Favorites and history tests
├── .env
├── .env.example
├── requirements.txt
├── pytest.ini
└── README.md
```

### 7.3 Key Design Decisions

| Decision                        | Rationale                                                  |
|---------------------------------|------------------------------------------------------------|
| SQLite over PostgreSQL          | Zero setup required; perfect for workshops and prototyping |
| Flask Blueprints                | Clean route organization by domain feature                 |
| `requests` library              | Simplest HTTP client for external API calls                |
| Cache in SQLite (not Redis)     | Single-dependency stack; no extra infrastructure needed    |
| `X-User-Id` header (no auth)   | Simplified user identification for workshop scope          |
| Parameterized queries           | Prevents SQL injection without an ORM overhead             |
| Pure functions for conversion   | Easily testable with parametrized pytest tests             |

### 7.4 External API Integration

```
┌────────────────┐     GET /data/2.5/weather     ┌───────────────────┐
│  Weather       │ ──────────────────────────────▶│  OpenWeatherMap   │
│  Service       │                                │  API              │
│                │◀────────── JSON Response ──────│                   │
│                │                                │  Endpoints:       │
│  - current()   │     GET /data/2.5/forecast     │  - /weather       │
│  - forecast()  │ ──────────────────────────────▶│  - /forecast      │
│                │                                │                   │
│                │◀────────── JSON Response ──────│  Auth: ?appid=KEY │
└────────────────┘                                └───────────────────┘
```

---

## 8. Test Strategy

### 8.1 Testing Pyramid

| Layer              | Tool                    | Count (min) | Focus                                   |
|--------------------|-------------------------|-------------|------------------------------------------|
| Unit Tests         | pytest                  | 20+         | Conversion functions, service logic       |
| Integration Tests  | pytest + Flask test client | 15+      | Full HTTP request/response cycles         |
| Mocked External API| pytest + `unittest.mock`| —           | All external API calls are mocked         |
| Parametrized Tests | pytest `@parametrize`   | 12+         | Temperature conversion (all 6 directions) |

### 8.2 Unit Test Examples — Temperature Conversion

```python
# tests/test_conversion.py
import pytest
from utils.converters import convert_temperature


class TestCelsiusToFahrenheit:
    """Test Celsius to Fahrenheit conversions."""

    @pytest.mark.parametrize("celsius, expected_f", [
        (0, 32.0),
        (100, 212.0),
        (-40, -40.0),
        (37, 98.6),
        (-273.15, -459.67),
    ])
    def test_celsius_to_fahrenheit(self, celsius, expected_f):
        result = convert_temperature(celsius, "celsius", "fahrenheit")
        assert result == pytest.approx(expected_f, rel=1e-2)


class TestFahrenheitToCelsius:
    """Test Fahrenheit to Celsius conversions."""

    @pytest.mark.parametrize("fahrenheit, expected_c", [
        (32, 0.0),
        (212, 100.0),
        (-40, -40.0),
        (98.6, 37.0),
        (0, -17.78),
    ])
    def test_fahrenheit_to_celsius(self, fahrenheit, expected_c):
        result = convert_temperature(fahrenheit, "fahrenheit", "celsius")
        assert result == pytest.approx(expected_c, rel=1e-2)


class TestCelsiusToKelvin:
    """Test Celsius to Kelvin conversions."""

    @pytest.mark.parametrize("celsius, expected_k", [
        (0, 273.15),
        (100, 373.15),
        (-273.15, 0.0),
        (25, 298.15),
    ])
    def test_celsius_to_kelvin(self, celsius, expected_k):
        result = convert_temperature(celsius, "celsius", "kelvin")
        assert result == pytest.approx(expected_k, rel=1e-2)


class TestKelvinValidation:
    """Test Kelvin below absolute zero."""

    def test_kelvin_below_zero_raises_error(self):
        with pytest.raises(ValueError, match="absolute zero"):
            convert_temperature(-1, "kelvin", "celsius")

    def test_kelvin_zero_converts(self):
        result = convert_temperature(0, "kelvin", "celsius")
        assert result == pytest.approx(-273.15, rel=1e-2)


class TestSameUnitConversion:
    """Test converting to same unit."""

    @pytest.mark.parametrize("value, unit", [
        (25.0, "celsius"),
        (77.0, "fahrenheit"),
        (298.15, "kelvin"),
    ])
    def test_same_unit_returns_same_value(self, value, unit):
        result = convert_temperature(value, unit, unit)
        assert result == value
```

### 8.3 Integration Test Examples

```python
# tests/test_weather.py
import pytest
import json
from unittest.mock import patch, MagicMock


# ── Sample OpenWeatherMap Response ──────────────────
MOCK_CURRENT_WEATHER = {
    "coord": {"lon": -0.1278, "lat": 51.5074},
    "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04d"}],
    "main": {"temp": 285.65, "feels_like": 284.0, "temp_min": 283.35, "temp_max": 287.25,
             "pressure": 1013, "humidity": 72},
    "visibility": 10000,
    "wind": {"speed": 5.4, "deg": 220},
    "name": "London",
    "sys": {"country": "GB"},
    "cod": 200,
}


class TestGetCurrentWeather:
    """Integration tests for GET /api/weather/current."""

    @patch("services.weather_service.requests.get")
    def test_get_weather_by_city(self, mock_get, client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_CURRENT_WEATHER
        mock_get.return_value = mock_response

        response = client.get("/api/weather/current?city=London")

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["city_name"] == "London"
        assert data["data"]["country_code"] == "GB"
        assert "temperature" in data["data"]

    @patch("services.weather_service.requests.get")
    def test_get_weather_by_coordinates(self, mock_get, client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_CURRENT_WEATHER
        mock_get.return_value = mock_response

        response = client.get("/api/weather/current?lat=51.5074&lon=-0.1278")

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True

    def test_missing_location_params(self, client):
        response = client.get("/api/weather/current")

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert "city" in data["error"]["message"].lower() or "lat" in data["error"]["message"].lower()

    def test_invalid_coordinates(self, client):
        response = client.get("/api/weather/current?lat=999&lon=999")

        assert response.status_code == 400
        data = response.get_json()
        assert data["error"]["code"] == "INVALID_COORDINATES"

    @patch("services.weather_service.requests.get")
    def test_city_not_found(self, mock_get, client):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"cod": "404", "message": "city not found"}
        mock_get.return_value = mock_response

        response = client.get("/api/weather/current?city=xyznonexistent123")

        assert response.status_code == 404
        data = response.get_json()
        assert data["error"]["code"] == "CITY_NOT_FOUND"


class TestGetForecast:
    """Integration tests for GET /api/weather/forecast."""

    @patch("services.weather_service.requests.get")
    def test_get_forecast_success(self, mock_get, client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "city": {"name": "London", "country": "GB"},
            "list": [
                {
                    "dt_txt": "2025-01-15 09:00:00",
                    "main": {"temp": 283.35, "humidity": 72, "feels_like": 281.5},
                    "weather": [{"main": "Clouds", "description": "overcast clouds", "icon": "04d"}],
                    "wind": {"speed": 5.4},
                }
            ],
        }
        mock_get.return_value = mock_response

        response = client.get("/api/weather/forecast?city=London")

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert "forecast" in data["data"]
```

### 8.4 Alert Tests

```python
# tests/test_alerts.py
import pytest


class TestAlertThresholds:
    """Tests for alert threshold CRUD."""

    def test_create_threshold(self, client):
        response = client.post(
            "/api/alerts/thresholds",
            json={"metric": "temperature", "operator": "gt", "value": 40, "city": "Delhi"},
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["data"]["metric"] == "temperature"

    def test_create_threshold_invalid_metric(self, client):
        response = client.post(
            "/api/alerts/thresholds",
            json={"metric": "rainfall", "operator": "gt", "value": 100},
        )
        assert response.status_code == 400

    def test_list_thresholds(self, client):
        # Create two thresholds
        client.post("/api/alerts/thresholds", json={"metric": "temperature", "operator": "gt", "value": 35})
        client.post("/api/alerts/thresholds", json={"metric": "humidity", "operator": "lt", "value": 20})

        response = client.get("/api/alerts/thresholds")
        assert response.status_code == 200
        assert len(response.get_json()["data"]) >= 2

    def test_delete_threshold(self, client):
        create_res = client.post(
            "/api/alerts/thresholds",
            json={"metric": "wind_speed", "operator": "gt", "value": 100},
        )
        threshold_id = create_res.get_json()["data"]["id"]

        response = client.delete(f"/api/alerts/thresholds/{threshold_id}")
        assert response.status_code == 200
```

### 8.5 Favorites & History Tests

```python
# tests/test_favorites.py
import pytest


class TestFavorites:
    """Tests for city favorites."""

    def test_add_favorite(self, client):
        response = client.post(
            "/api/favorites",
            json={"city": "London"},
            headers={"X-User-Id": "user123"},
        )
        assert response.status_code == 201

    def test_add_duplicate_favorite(self, client):
        client.post("/api/favorites", json={"city": "London"}, headers={"X-User-Id": "user123"})
        response = client.post("/api/favorites", json={"city": "London"}, headers={"X-User-Id": "user123"})
        assert response.status_code == 409

    def test_list_favorites(self, client):
        client.post("/api/favorites", json={"city": "London"}, headers={"X-User-Id": "user123"})
        client.post("/api/favorites", json={"city": "Tokyo"}, headers={"X-User-Id": "user123"})

        response = client.get("/api/favorites", headers={"X-User-Id": "user123"})
        assert response.status_code == 200
        assert len(response.get_json()["data"]) == 2

    def test_remove_favorite(self, client):
        client.post("/api/favorites", json={"city": "London"}, headers={"X-User-Id": "user123"})
        response = client.delete("/api/favorites/London", headers={"X-User-Id": "user123"})
        assert response.status_code == 200

    def test_missing_user_id_header(self, client):
        response = client.get("/api/favorites")
        assert response.status_code == 400
        assert response.get_json()["error"]["code"] == "MISSING_USER_ID"


class TestSearchHistory:
    """Tests for search history."""

    def test_history_recorded_on_weather_query(self, client):
        # This test would mock the weather API and verify history is recorded
        pass

    def test_clear_history(self, client):
        response = client.delete("/api/history", headers={"X-User-Id": "user123"})
        assert response.status_code == 200
```

### 8.6 Test Configuration — conftest.py

```python
# tests/conftest.py
import pytest
import os
import tempfile
from app import create_app
from database import init_db


@pytest.fixture
def app():
    """Create a Flask test application with a temporary database."""
    db_fd, db_path = tempfile.mkstemp(suffix=".db")

    app = create_app({
        "TESTING": True,
        "DATABASE": db_path,
        "OPENWEATHERMAP_API_KEY": "test_api_key_12345",
        "CACHE_TTL_CURRENT": 600,
        "CACHE_TTL_FORECAST": 3600,
    })

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Create a Flask test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a Flask test CLI runner."""
    return app.test_cli_runner()
```

### 8.7 pytest Configuration

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks integration tests
```

---

## 9. Appendix

### A. OpenWeatherMap API Setup

#### Step 1: Get a Free API Key

1. Visit [https://openweathermap.org/api](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to **API Keys** in your profile
4. Copy the default API key (or generate a new one)
5. Note: Free tier allows **60 calls/minute** and **1,000 calls/day**

#### Step 2: Test the API Key

```bash
# Test current weather
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY&units=metric"

# Test 5-day forecast
curl "https://api.openweathermap.org/data/2.5/forecast?q=London&appid=YOUR_API_KEY&units=metric"
```

#### Step 3: API Key Activation

> **Important**: New API keys may take **up to 2 hours** to activate. If you get a `401 Unauthorized` response, wait and try again.

### B. Sample OpenWeatherMap Responses

#### Current Weather Response

```json
{
  "coord": {"lon": -0.1278, "lat": 51.5074},
  "weather": [
    {
      "id": 804,
      "main": "Clouds",
      "description": "overcast clouds",
      "icon": "04d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 12.5,
    "feels_like": 10.8,
    "temp_min": 10.2,
    "temp_max": 14.1,
    "pressure": 1013,
    "humidity": 72
  },
  "visibility": 10000,
  "wind": {"speed": 5.4, "deg": 220},
  "clouds": {"all": 90},
  "dt": 1705312200,
  "sys": {
    "type": 2,
    "id": 2075535,
    "country": "GB",
    "sunrise": 1705303200,
    "sunset": 1705333200
  },
  "timezone": 0,
  "id": 2643743,
  "name": "London",
  "cod": 200
}
```

#### Forecast Response (Partial)

```json
{
  "cod": "200",
  "message": 0,
  "cnt": 40,
  "list": [
    {
      "dt": 1705312200,
      "main": {
        "temp": 10.2,
        "feels_like": 8.5,
        "temp_min": 9.8,
        "temp_max": 10.2,
        "pressure": 1013,
        "humidity": 72
      },
      "weather": [
        {
          "id": 804,
          "main": "Clouds",
          "description": "overcast clouds",
          "icon": "04d"
        }
      ],
      "wind": {"speed": 5.4, "deg": 220},
      "dt_txt": "2025-01-15 09:00:00"
    }
  ],
  "city": {
    "id": 2643743,
    "name": "London",
    "coord": {"lat": 51.5074, "lon": -0.1278},
    "country": "GB",
    "population": 1000000,
    "timezone": 0
  }
}
```

### C. Environment Configuration

```bash
# .env.example

# ── Flask ──────────────────────────────────────────
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-change-in-production

# ── Server ─────────────────────────────────────────
HOST=0.0.0.0
PORT=5000

# ── Database ───────────────────────────────────────
DATABASE=weather_dashboard.db

# ── OpenWeatherMap API ─────────────────────────────
OPENWEATHERMAP_API_KEY=your_api_key_here
OPENWEATHERMAP_BASE_URL=https://api.openweathermap.org/data/2.5

# ── Cache ──────────────────────────────────────────
CACHE_TTL_CURRENT=600
CACHE_TTL_FORECAST=3600

# ── Rate Limiting ──────────────────────────────────
RATE_LIMIT_PER_MINUTE=30
```

### D. Requirements File

```
# requirements.txt

# ── Core ───────────────────────────────────────────
Flask==3.1.1
requests==2.32.3

# ── Extensions ─────────────────────────────────────
flask-cors==5.0.1
flask-limiter==3.8.0
python-dotenv==1.1.0

# ── Testing ────────────────────────────────────────
pytest==8.3.4
pytest-cov==6.0.0

# ── Development ────────────────────────────────────
black==24.10.0
flake8==7.1.1
```

### E. Application Factory — `app.py`

```python
# app.py
import os
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()


def create_app(test_config=None):
    """Application factory for the Weather Dashboard."""
    app = Flask(__name__)

    # ── Default configuration ──────────────────────
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret-key"),
        DATABASE=os.getenv("DATABASE", "weather_dashboard.db"),
        OPENWEATHERMAP_API_KEY=os.getenv("OPENWEATHERMAP_API_KEY"),
        OPENWEATHERMAP_BASE_URL=os.getenv(
            "OPENWEATHERMAP_BASE_URL",
            "https://api.openweathermap.org/data/2.5",
        ),
        CACHE_TTL_CURRENT=int(os.getenv("CACHE_TTL_CURRENT", 600)),
        CACHE_TTL_FORECAST=int(os.getenv("CACHE_TTL_FORECAST", 3600)),
    )

    # ── Override with test config ──────────────────
    if test_config:
        app.config.update(test_config)

    # ── Extensions ─────────────────────────────────
    CORS(app)
    Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[f"{os.getenv('RATE_LIMIT_PER_MINUTE', 30)}/minute"],
    )

    # ── Register Blueprints ────────────────────────
    from blueprints.weather import weather_bp
    from blueprints.alerts import alerts_bp
    from blueprints.favorites import favorites_bp

    app.register_blueprint(weather_bp, url_prefix="/api")
    app.register_blueprint(alerts_bp, url_prefix="/api")
    app.register_blueprint(favorites_bp, url_prefix="/api")

    # ── Health Check ───────────────────────────────
    @app.route("/api/health")
    def health():
        import time
        return {
            "success": True,
            "data": {
                "status": "healthy",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "version": "1.0.0",
            },
        }

    # ── Global Error Handler ───────────────────────
    @app.errorhandler(Exception)
    def handle_error(error):
        code = getattr(error, "code", 500)
        return {
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(error),
            },
        }, code

    return app
```

### F. Temperature Converter — `utils/converters.py`

```python
# utils/converters.py
"""Pure functions for temperature conversion between Celsius, Fahrenheit, and Kelvin."""

FORMULAS = {
    ("celsius", "fahrenheit"): "F = C × 9/5 + 32",
    ("celsius", "kelvin"): "K = C + 273.15",
    ("fahrenheit", "celsius"): "C = (F − 32) × 5/9",
    ("fahrenheit", "kelvin"): "K = (F − 32) × 5/9 + 273.15",
    ("kelvin", "celsius"): "C = K − 273.15",
    ("kelvin", "fahrenheit"): "F = (K − 273.15) × 9/5 + 32",
}

VALID_UNITS = {"celsius", "fahrenheit", "kelvin"}


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert a temperature value between Celsius, Fahrenheit, and Kelvin.

    Args:
        value: The temperature value to convert.
        from_unit: Source unit ('celsius', 'fahrenheit', 'kelvin').
        to_unit: Target unit ('celsius', 'fahrenheit', 'kelvin').

    Returns:
        The converted temperature rounded to 2 decimal places.

    Raises:
        ValueError: If units are invalid or Kelvin value is below absolute zero.
    """
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit not in VALID_UNITS:
        raise ValueError(f"Invalid source unit: {from_unit}")
    if to_unit not in VALID_UNITS:
        raise ValueError(f"Invalid target unit: {to_unit}")

    if from_unit == "kelvin" and value < 0:
        raise ValueError("Kelvin temperature cannot be below absolute zero (0 K)")

    if from_unit == to_unit:
        return value

    # Convert to Celsius first (as intermediate)
    if from_unit == "celsius":
        celsius = value
    elif from_unit == "fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "kelvin":
        celsius = value - 273.15

    # Convert from Celsius to target
    if to_unit == "celsius":
        result = celsius
    elif to_unit == "fahrenheit":
        result = celsius * 9 / 5 + 32
    elif to_unit == "kelvin":
        result = celsius + 273.15

    return round(result, 2)


def get_formula(from_unit: str, to_unit: str) -> str:
    """Get the human-readable formula for a conversion."""
    if from_unit == to_unit:
        return "No conversion needed"
    return FORMULAS.get((from_unit.lower(), to_unit.lower()), "Unknown conversion")
```

### G. Quick Start Guide

```bash
# 1. Clone and navigate
git clone <repository-url>
cd weather-dashboard

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your OpenWeatherMap API key

# 5. Initialize the database
python -c "from database import init_db; init_db()"

# 6. Start the development server
python run.py

# 7. Test the API
curl http://localhost:5000/api/health
curl "http://localhost:5000/api/weather/current?city=London"
curl "http://localhost:5000/api/weather/convert?value=100&from=celsius&to=fahrenheit"

# 8. Run tests
pytest

# 9. Run tests with coverage
pytest --cov=. --cov-report=html
```

### H. Workshop Timeline

| Time          | Activity                                         | FR Covered |
|---------------|--------------------------------------------------|------------|
| 0:00 – 0:10  | Project setup, `pip install`, `.env` config       | —          |
| 0:10 – 0:25  | Implement Current Weather + external API call     | FR-1       |
| 0:25 – 0:40  | Implement 5-Day Forecast with grouping            | FR-2       |
| 0:40 – 0:50  | Implement Temperature Conversion                  | FR-3       |
| 0:50 – 1:05  | Implement Severe Weather Alerts                   | FR-4       |
| 1:05 – 1:15  | Implement SQLite Caching                          | FR-5       |
| 1:15 – 1:25  | Implement Favorites & Search History              | FR-6       |
| 1:25 – 1:30  | Write tests, review, Q&A                          | All        |

---

*Document Version: 1.0 | Last Updated: 2025-01-15 | Faculty Development Program — AI-Native Software Development*
