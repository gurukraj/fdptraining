# Weather Dashboard API

A RESTful API service for weather data retrieval, caching, temperature conversion, alerts, and user favorites management. Built with Flask 3.x and SQLite.

## Overview

The Weather Dashboard API provides:
- **Current Weather**: Real-time weather data for 25+ major cities worldwide
- **5-Day Forecast**: Hourly forecasts grouped by date with daily summaries
- **Temperature Conversion**: Convert between Celsius, Fahrenheit, and Kelvin
- **Weather Alerts**: Configurable thresholds with severity levels
- **Favorites & History**: Save favorite cities and track search history
- **Smart Caching**: SQLite-backed cache with configurable TTL

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.12+ | Runtime |
| Flask 3.x | Web framework |
| SQLAlchemy | ORM / Database |
| SQLite | Database engine |
| requests | HTTP client |
| pytest | Testing |

## Quick Start

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Seed the database
python seed_database.py

# Run the application
flask --app app.main run
```

The API will be available at `http://127.0.0.1:5000`.

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_weather.py -v
```

## API Documentation

### Current Weather

```
GET /api/weather/current?city=London
GET /api/weather/current?lat=51.5074&lon=-0.1278
GET /api/weather/current?city=London&units=fahrenheit
```

**Query Parameters:**
- `city` - City name (e.g., "London", "New York")
- `lat` / `lon` - Coordinates (alternative to city)
- `units` - Temperature units: `celsius` (default), `fahrenheit`, `kelvin`

**Response:**
```json
{
  "city_name": "London",
  "country_code": "GB",
  "coordinates": {"lat": 51.5074, "lon": -0.1278},
  "temperature": 15.2,
  "feels_like": 13.8,
  "temp_min": 12.1,
  "temp_max": 17.5,
  "humidity": 72,
  "pressure": 1013,
  "wind_speed": 5.4,
  "wind_direction": 220,
  "condition": "Clouds",
  "description": "scattered clouds",
  "icon": "03d",
  "visibility": 10000,
  "units": "celsius",
  "source": "mock",
  "fetched_at": "2024-01-15T10:30:00+00:00"
}
```

### 5-Day Forecast

```
GET /api/weather/forecast?city=London&units=celsius
```

**Response includes:**
- `forecast` - Array of 3-hour interval entries
- `daily` - Array of daily summaries with `temp_high`, `temp_low`, `avg_humidity`, `dominant_condition`, and `hourly` array

### Temperature Conversion

```
GET /api/weather/convert?value=100&from=celsius&to=fahrenheit
```

**Batch conversion:**
```
POST /api/weather/convert
Content-Type: application/json

{
  "values": [0, 25, 100],
  "from": "celsius",
  "to": "fahrenheit"
}
```

### Weather Alerts

**Configure thresholds:**
```
POST /api/alerts/configure
Content-Type: application/json

{
  "user_id": "user1",
  "temp_high": 35.0,
  "temp_low": 0.0,
  "wind_speed": 10.0,
  "humidity": 80.0
}
```

**Check alerts:**
```
GET /api/alerts/check?city=Dubai&user_id=user1
```

### Favorites

```
POST /api/favorites          - Add favorite (JSON: {user_id, city})
GET  /api/favorites?user_id=user1  - List favorites
DELETE /api/favorites/London?user_id=user1 - Remove favorite
```

### Search History

```
GET /api/history?user_id=user1&limit=50
```

### Cache Management

```
GET    /api/cache/stats   - Cache hit/miss statistics
DELETE /api/cache          - Clear all cached data
```

### Health Check

```
GET /api/health
```

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `WEATHER_PROVIDER` | `mock` | Weather data provider (`mock` or `openweathermap`) |
| `OPENWEATHERMAP_API_KEY` | `` | API key for OpenWeatherMap (only if provider is `openweathermap`) |
| `CACHE_TTL_CURRENT` | `600` | Cache TTL for current weather (seconds) |
| `CACHE_TTL_FORECAST` | `3600` | Cache TTL for forecast data (seconds) |
| `DATABASE_URL` | `sqlite:///weather_dashboard.db` | Database connection string |
| `DATA_DIR` | `./data` | Path to weather dataset directory |

## Architecture

```
app/
├── main.py              # Flask app factory
├── config.py            # Configuration
├── database.py          # SQLAlchemy setup
├── models.py            # Database models
├── routes/              # API endpoints
│   ├── weather.py       # Weather & conversion routes
│   ├── alerts.py        # Alert configuration & checking
│   └── favorites.py     # Favorites & history
├── services/            # Business logic
│   ├── weather_service.py    # Weather fetching & caching
│   ├── conversion_service.py # Temperature conversion
│   └── alert_service.py      # Alert threshold checking
└── providers/           # Data source abstraction
    ├── base_provider.py      # Abstract base class
    ├── mock_provider.py      # Mock data from JSON files
    └── openweathermap.py     # Real API provider
```

### Provider Pattern

The application uses a **Provider Pattern** to abstract weather data sources:

- **MockWeatherProvider**: Loads data from local JSON datasets with small random variations. Default provider - no API key needed.
- **OpenWeatherMapProvider**: Fetches real data from OpenWeatherMap API. Requires an API key.

Set `WEATHER_PROVIDER=openweathermap` and provide `OPENWEATHERMAP_API_KEY` to use real weather data.

## Available Cities (Mock Provider)

London, New York, Tokyo, Paris, Sydney, Mumbai, Dubai, Berlin, Moscow, Beijing, Singapore, Toronto, San Francisco, Cairo, Rome, Bangkok, Seoul, Mexico City, Nairobi, Buenos Aires, Cape Town, Istanbul, Bangalore, Chicago, Los Angeles

## Error Responses

All errors follow a consistent format:
```json
{
  "error": "Description of the error",
  "status": 400
}
```

| Status Code | Meaning |
|------------|---------|
| 400 | Bad request / Missing parameters |
| 404 | City not found |
| 409 | Conflict (duplicate favorite) |
| 500 | Internal server error |
