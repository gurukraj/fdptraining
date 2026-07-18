# Weather Dashboard Microservice

## What You'll Build

A backend microservice that provides current weather data, 5-day forecasts, temperature unit conversion, configurable severe weather alerts, and user favorites — all powered by a bundled mock weather dataset (no external API key required).

**Scenario:** A smart-campus initiative needs a weather dashboard backend. The service must aggregate weather information for multiple cities, let users set alert thresholds for dangerous conditions, and cache results in SQLite to minimize redundant lookups. A mock weather provider with data for 25 cities is included so the service runs fully offline.

## Technology Stack

| Component     | Technology                  |
|---------------|-----------------------------|
| Language      | Python 3.12+                |
| Framework     | Flask                       |
| Database      | SQLite                      |
| ORM           | SQLAlchemy                  |
| HTTP Client   | requests (mock provider)    |
| Testing       | pytest                      |

## Functional Requirements

| FR-ID | Title                    | Description                                                                                         | Key Acceptance Criteria                                                                                      |
|-------|--------------------------|-----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| FR-1  | Get Current Weather      | Retrieve current weather by city name or latitude/longitude coordinates.                            | Returns temperature, humidity, wind speed, and condition; supports `units` param: celsius, fahrenheit, kelvin.|
| FR-2  | Get 5-Day Forecast       | Return a 5-day forecast with daily summaries (high, low, dominant condition) and hourly breakdowns. | Each day includes high/low temps, dominant weather condition, and a list of hourly data points.               |
| FR-3  | Temperature Conversion   | Convert temperature values between Celsius, Fahrenheit, and Kelvin.                                 | Single conversion via GET; batch conversion via POST; all 6 directional pairs supported.                     |
| FR-4  | Severe Weather Alerts    | Allow users to configure alert thresholds and check current conditions against them.                | Thresholds for `temp_high`, `temp_low`, `wind_speed`, `humidity`; severity levels: **warning** vs **critical**.|
| FR-5  | Weather Data Caching     | Cache weather responses in SQLite with a configurable TTL; expose cache statistics.                 | Cache key by city+data_type; track hit/miss counts; provide a cache-clear endpoint.                          |
| FR-6  | Favorites & History      | Let users save favorite cities and automatically track search history.                              | Add/list/remove favorites per user; search history records city, search type, and timestamp.                 |

## API Endpoints Summary

| Method | Path                       | Description                                        | Success | Error Codes   |
|--------|----------------------------|----------------------------------------------------|---------|---------------|
| GET    | `/api/weather/current`     | Current weather by city or coordinates              | 200     | 400, 404      |
| GET    | `/api/weather/forecast`    | 5-day forecast for a city                           | 200     | 400, 404      |
| GET    | `/api/weather/convert`     | Single temperature conversion                       | 200     | 400, 422      |
| POST   | `/api/weather/convert`     | Batch temperature conversion                        | 200     | 400, 422      |
| GET    | `/api/cache/stats`         | Cache hit/miss statistics                           | 200     | -             |
| DELETE | `/api/cache`               | Clear all cached weather data                       | 200     | -             |
| POST   | `/api/alerts/configure`    | Set or update alert thresholds for a user           | 200     | 400, 422      |
| GET    | `/api/alerts/check`        | Check current conditions against configured alerts  | 200     | 400, 404      |
| POST   | `/api/favorites`           | Add a city to a user's favorites                    | 201     | 400, 409      |
| GET    | `/api/favorites`           | List a user's favorite cities                       | 200     | -             |
| DELETE | `/api/favorites/{city}`    | Remove a city from favorites                        | 200     | 404           |
| GET    | `/api/history`             | Retrieve a user's search history                    | 200     | -             |

## Data Model

### WeatherCache

| Field      | Type     | Constraints                                   |
|------------|----------|-----------------------------------------------|
| cache_key  | String   | Primary key (city_name + data_type composite)  |
| city_name  | String   | City associated with cached data              |
| data_type  | String   | "current" or "forecast"                       |
| data       | JSON     | Cached weather response payload               |
| fetched_at | DateTime | When the data was originally fetched          |
| expires_at | DateTime | Cache expiration time (fetched_at + TTL)      |

### Favorite

| Field     | Type   | Constraints                            |
|-----------|--------|----------------------------------------|
| user_id   | String | Identifies the user                    |
| city_name | String | Favorite city name                     |

Unique constraint on (user_id, city_name).

### SearchHistory

| Field       | Type     | Constraints                        |
|-------------|----------|------------------------------------|
| user_id     | String   | Identifies the user                |
| city_name   | String   | City that was searched             |
| search_type | String   | "current" or "forecast"            |
| searched_at | DateTime | Auto-set on creation               |

### AlertConfig

| Field     | Type   | Constraints                                        |
|-----------|--------|----------------------------------------------------|
| user_id   | String | Primary key, identifies the user                   |
| temp_high | Float  | Threshold for high temperature alert (optional)    |
| temp_low  | Float  | Threshold for low temperature alert (optional)     |
| wind_speed| Float  | Threshold for wind speed alert (optional)          |
| humidity  | Float  | Threshold for humidity alert (optional)            |

**Alert Severity Rules:** When a current reading exceeds a threshold by less than 20%, severity is **warning**. When it exceeds by 20% or more, severity is **critical**.

## Mock Weather Provider

The service includes a built-in mock weather data provider with a JSON dataset covering 25 cities worldwide. This eliminates the need for an external API key. The mock provider should return realistic weather data including temperature, humidity, wind speed, and conditions (sunny, cloudy, rainy, snowy, etc.).

## Success Criteria

- All 12 endpoints return correct status codes and response structures.
- Weather queries by city name and by coordinates both work correctly.
- Temperature conversions are accurate across all 6 directional pairs (C-F, C-K, F-C, F-K, K-C, K-F).
- Cache stores responses and serves them on subsequent requests within the TTL window.
- Cache statistics accurately reflect hit and miss counts.
- Alert configuration persists per user and the check endpoint evaluates current conditions against thresholds.
- Favorites and search history are correctly scoped per user.
- Application starts cleanly with no external API keys required.
