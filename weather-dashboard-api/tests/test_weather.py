"""Tests for current weather endpoints."""
import json
import pytest


class TestCurrentWeather:
    """Tests for GET /api/weather/current."""

    def test_get_weather_by_city(self, client, db):
        """Test getting current weather by city name."""
        response = client.get('/api/weather/current?city=London')
        assert response.status_code == 200
        data = response.get_json()
        assert data['city_name'] == 'London'
        assert data['country_code'] == 'GB'
        assert 'temperature' in data
        assert 'humidity' in data
        assert 'wind_speed' in data
        assert 'condition' in data
        assert 'description' in data
        assert 'icon' in data
        assert 'visibility' in data
        assert 'source' in data
        assert 'fetched_at' in data
        assert data['units'] == 'celsius'

    def test_get_weather_by_coordinates(self, client, db):
        """Test getting current weather by lat/lon coordinates."""
        response = client.get('/api/weather/current?lat=51.5074&lon=-0.1278')
        assert response.status_code == 200
        data = response.get_json()
        assert data['city_name'] == 'London'

    def test_get_weather_fahrenheit(self, client, db):
        """Test getting weather with fahrenheit units."""
        response = client.get('/api/weather/current?city=London&units=fahrenheit')
        assert response.status_code == 200
        data = response.get_json()
        assert data['units'] == 'fahrenheit'
        # London temp ~15C should be ~59F
        assert data['temperature'] > 45  # Must be in Fahrenheit range

    def test_get_weather_kelvin(self, client, db):
        """Test getting weather with kelvin units."""
        response = client.get('/api/weather/current?city=London&units=kelvin')
        assert response.status_code == 200
        data = response.get_json()
        assert data['units'] == 'kelvin'
        # London temp ~15C should be ~288K
        assert data['temperature'] > 260

    def test_invalid_city_returns_404(self, client, db):
        """Test that an invalid city returns 404."""
        response = client.get('/api/weather/current?city=NonexistentCity12345')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_missing_params_returns_400(self, client, db):
        """Test that missing parameters return 400."""
        response = client.get('/api/weather/current')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_missing_lon_returns_400(self, client, db):
        """Test that providing lat without lon returns 400."""
        response = client.get('/api/weather/current?lat=51.5074')
        assert response.status_code == 400

    def test_invalid_units_returns_400(self, client, db):
        """Test that invalid units return 400."""
        response = client.get('/api/weather/current?city=London&units=invalid')
        assert response.status_code == 400

    def test_cache_behavior(self, client, db):
        """Test that second request returns cached data."""
        # First request - should be a cache miss
        response1 = client.get('/api/weather/current?city=London')
        assert response1.status_code == 200
        data1 = response1.get_json()
        assert data1['source'] == 'mock'

        # Second request - should be cached
        response2 = client.get('/api/weather/current?city=London')
        assert response2.status_code == 200
        data2 = response2.get_json()
        assert data2['source'] == 'cache'

    def test_case_insensitive_city(self, client, db):
        """Test that city lookup is case-insensitive."""
        response = client.get('/api/weather/current?city=london')
        assert response.status_code == 200
        data = response.get_json()
        assert data['city_name'] == 'London'

    def test_weather_has_all_fields(self, client, db):
        """Test that response contains all required fields."""
        response = client.get('/api/weather/current?city=Tokyo')
        assert response.status_code == 200
        data = response.get_json()
        required_fields = [
            'city_name', 'country_code', 'coordinates', 'temperature',
            'feels_like', 'temp_min', 'temp_max', 'humidity', 'pressure',
            'wind_speed', 'wind_direction', 'condition', 'description',
            'icon', 'visibility', 'source', 'fetched_at', 'units'
        ]
        for field in required_fields:
            assert field in data, f'Missing field: {field}'

    def test_search_recorded_in_history(self, client, db):
        """Test that searches are recorded in history."""
        client.get('/api/weather/current?city=Paris',
                   headers={'X-User-ID': 'testuser1'})
        response = client.get('/api/history?user_id=testuser1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] >= 1
        assert any(h['city_name'] == 'Paris' for h in data['history'])


class TestHealthCheck:
    """Tests for health check endpoint."""

    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
