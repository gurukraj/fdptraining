"""Tests for forecast endpoints."""
import json
import pytest


class TestForecast:
    """Tests for GET /api/weather/forecast."""

    def test_get_forecast_by_city(self, client, db):
        """Test getting forecast by city name."""
        response = client.get('/api/weather/forecast?city=London')
        assert response.status_code == 200
        data = response.get_json()
        assert data['city_name'] == 'London'
        assert 'forecast' in data
        assert 'daily' in data
        assert 'source' in data
        assert data['units'] == 'celsius'

    def test_forecast_has_daily_summaries(self, client, db):
        """Test that forecast includes daily summaries."""
        response = client.get('/api/weather/forecast?city=London')
        assert response.status_code == 200
        data = response.get_json()
        daily = data['daily']
        assert len(daily) > 0

        # Check daily summary structure
        day = daily[0]
        assert 'date' in day
        assert 'temp_high' in day
        assert 'temp_low' in day
        assert 'avg_humidity' in day
        assert 'dominant_condition' in day
        assert 'hourly' in day

    def test_forecast_daily_temp_high_greater_than_low(self, client, db):
        """Test that daily temp_high is always >= temp_low."""
        response = client.get('/api/weather/forecast?city=London')
        data = response.get_json()
        for day in data['daily']:
            assert day['temp_high'] >= day['temp_low']

    def test_forecast_hourly_entries(self, client, db):
        """Test that daily summaries contain hourly entries."""
        response = client.get('/api/weather/forecast?city=London')
        data = response.get_json()
        # At least the first day should have hourly entries
        assert len(data['daily'][0]['hourly']) > 0

    def test_forecast_with_fahrenheit(self, client, db):
        """Test forecast with Fahrenheit units."""
        response = client.get('/api/weather/forecast?city=London&units=fahrenheit')
        assert response.status_code == 200
        data = response.get_json()
        assert data['units'] == 'fahrenheit'

    def test_forecast_invalid_city(self, client, db):
        """Test forecast for non-existent city."""
        response = client.get('/api/weather/forecast?city=FakeCity123')
        assert response.status_code == 404

    def test_forecast_missing_params(self, client, db):
        """Test forecast without any parameters."""
        response = client.get('/api/weather/forecast')
        assert response.status_code == 400

    def test_forecast_cached(self, client, db):
        """Test that forecast data is cached."""
        response1 = client.get('/api/weather/forecast?city=Tokyo')
        assert response1.status_code == 200
        data1 = response1.get_json()
        assert data1['source'] == 'mock'

        response2 = client.get('/api/weather/forecast?city=Tokyo')
        assert response2.status_code == 200
        data2 = response2.get_json()
        assert data2['source'] == 'cache'

    def test_forecast_multiple_days(self, client, db):
        """Test that forecast spans multiple days."""
        response = client.get('/api/weather/forecast?city=London')
        data = response.get_json()
        assert len(data['daily']) >= 2  # At least 2 days

    def test_forecast_by_coordinates(self, client, db):
        """Test getting forecast by coordinates."""
        response = client.get('/api/weather/forecast?lat=51.5074&lon=-0.1278')
        assert response.status_code == 200
        data = response.get_json()
        assert data['city_name'] == 'London'

    def test_forecast_city_without_forecast_data(self, client, db):
        """Test getting forecast for city with only current weather data."""
        response = client.get('/api/weather/forecast?city=Berlin')
        assert response.status_code == 200
        data = response.get_json()
        assert 'forecast' in data
        assert len(data['forecast']) > 0


class TestCacheManagement:
    """Tests for cache management endpoints."""

    def test_cache_stats(self, client, db):
        """Test getting cache statistics."""
        response = client.get('/api/cache/stats')
        assert response.status_code == 200
        data = response.get_json()
        assert 'hits' in data
        assert 'misses' in data
        assert 'total' in data
        assert 'hit_rate' in data

    def test_cache_stats_after_requests(self, client, db):
        """Test cache stats update after requests."""
        # Make requests to generate cache activity
        client.get('/api/weather/current?city=London')
        client.get('/api/weather/current?city=London')  # Should be cached

        response = client.get('/api/cache/stats')
        data = response.get_json()
        assert data['misses'] >= 1
        assert data['hits'] >= 1

    def test_clear_cache(self, client, db):
        """Test clearing the cache."""
        # Populate cache
        client.get('/api/weather/current?city=London')

        # Clear cache
        response = client.delete('/api/cache')
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Cache cleared successfully'

        # Verify stats are reset
        response = client.get('/api/cache/stats')
        data = response.get_json()
        assert data['hits'] == 0
        assert data['misses'] == 0
