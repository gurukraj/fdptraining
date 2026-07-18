"""Tests for weather alerts."""
import json
import pytest


class TestAlertConfiguration:
    """Tests for POST /api/alerts/configure."""

    def test_configure_alert(self, client, db):
        """Test configuring alert thresholds."""
        response = client.post('/api/alerts/configure',
                              json={
                                  'user_id': 'user1',
                                  'temp_high': 35.0,
                                  'temp_low': 0.0,
                                  'wind_speed': 10.0,
                                  'humidity': 80.0
                              })
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Alert thresholds configured successfully'
        assert data['config']['temp_high_threshold'] == 35.0
        assert data['config']['temp_low_threshold'] == 0.0
        assert data['config']['wind_speed_threshold'] == 10.0
        assert data['config']['humidity_threshold'] == 80.0

    def test_update_alert(self, client, db):
        """Test updating existing alert thresholds."""
        # Create initial config
        client.post('/api/alerts/configure',
                   json={'user_id': 'user1', 'temp_high': 35.0})

        # Update
        response = client.post('/api/alerts/configure',
                              json={'user_id': 'user1', 'temp_high': 40.0})
        assert response.status_code == 201
        data = response.get_json()
        assert data['config']['temp_high_threshold'] == 40.0

    def test_configure_missing_user_id(self, client, db):
        """Test configuration without user_id."""
        response = client.post('/api/alerts/configure',
                              json={'temp_high': 35.0})
        assert response.status_code == 400

    def test_configure_no_json(self, client, db):
        """Test configuration without JSON body."""
        response = client.post('/api/alerts/configure')
        assert response.status_code in (400, 415)

    def test_configure_with_header_user_id(self, client, db):
        """Test configuration with user_id from header."""
        response = client.post('/api/alerts/configure',
                              json={'temp_high': 35.0},
                              headers={'X-User-ID': 'user2'})
        assert response.status_code == 201
        data = response.get_json()
        assert data['config']['user_id'] == 'user2'


class TestAlertCheck:
    """Tests for GET /api/alerts/check."""

    def test_check_alerts_no_config(self, client, db):
        """Test checking alerts with no configuration."""
        response = client.get('/api/alerts/check?city=London&user_id=noconfig')
        assert response.status_code == 200
        data = response.get_json()
        assert data['alerts'] == []
        assert data['alert_count'] == 0

    def test_check_alerts_triggered(self, client, db):
        """Test alerts that should be triggered."""
        # Dubai has temp ~42C, set low threshold
        client.post('/api/alerts/configure',
                   json={'user_id': 'user1', 'temp_high': 30.0})

        response = client.get('/api/alerts/check?city=Dubai&user_id=user1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['alert_count'] > 0
        assert any(a['type'] == 'high_temperature' for a in data['alerts'])

    def test_check_alerts_not_triggered(self, client, db):
        """Test alerts that should NOT be triggered."""
        # London has temp ~15C, set high threshold at 50
        client.post('/api/alerts/configure',
                   json={'user_id': 'user1', 'temp_high': 50.0, 'temp_low': -50.0})

        response = client.get('/api/alerts/check?city=London&user_id=user1')
        assert response.status_code == 200
        data = response.get_json()
        # Should not trigger any temp alerts
        temp_alerts = [a for a in data['alerts']
                      if a['type'] in ('high_temperature', 'low_temperature')]
        assert len(temp_alerts) == 0

    def test_check_alerts_critical_severity(self, client, db):
        """Test that extreme conditions trigger critical severity."""
        # Dubai temp ~42C, threshold at 30 (12+ above = critical)
        client.post('/api/alerts/configure',
                   json={'user_id': 'user1', 'temp_high': 30.0})

        response = client.get('/api/alerts/check?city=Dubai&user_id=user1')
        assert response.status_code == 200
        data = response.get_json()
        high_temp_alerts = [a for a in data['alerts'] if a['type'] == 'high_temperature']
        assert len(high_temp_alerts) > 0
        assert high_temp_alerts[0]['severity'] == 'critical'

    def test_check_alerts_missing_city(self, client, db):
        """Test checking alerts without city."""
        response = client.get('/api/alerts/check?user_id=user1')
        assert response.status_code == 400

    def test_check_alerts_missing_user_id(self, client, db):
        """Test checking alerts without user_id."""
        response = client.get('/api/alerts/check?city=London')
        assert response.status_code == 400

    def test_check_alerts_invalid_city(self, client, db):
        """Test checking alerts for non-existent city."""
        client.post('/api/alerts/configure',
                   json={'user_id': 'user1', 'temp_high': 30.0})
        response = client.get('/api/alerts/check?city=FakeCity&user_id=user1')
        assert response.status_code == 404

    def test_check_alerts_wind_speed(self, client, db):
        """Test wind speed alert check."""
        # Set very low wind threshold to trigger
        client.post('/api/alerts/configure',
                   json={'user_id': 'user1', 'wind_speed': 1.0})

        response = client.get('/api/alerts/check?city=London&user_id=user1')
        assert response.status_code == 200
        data = response.get_json()
        wind_alerts = [a for a in data['alerts'] if a['type'] == 'high_wind_speed']
        assert len(wind_alerts) > 0

    def test_check_alerts_humidity(self, client, db):
        """Test humidity alert check."""
        # Mumbai has humidity ~85%, set threshold at 70
        client.post('/api/alerts/configure',
                   json={'user_id': 'user1', 'humidity': 70.0})

        response = client.get('/api/alerts/check?city=Mumbai&user_id=user1')
        assert response.status_code == 200
        data = response.get_json()
        humidity_alerts = [a for a in data['alerts'] if a['type'] == 'high_humidity']
        assert len(humidity_alerts) > 0

    def test_check_alerts_weather_summary(self, client, db):
        """Test that alert response includes weather summary."""
        client.post('/api/alerts/configure',
                   json={'user_id': 'user1', 'temp_high': 30.0})

        response = client.get('/api/alerts/check?city=London&user_id=user1')
        assert response.status_code == 200
        data = response.get_json()
        assert 'weather_summary' in data
        assert 'temperature' in data['weather_summary']
        assert 'wind_speed' in data['weather_summary']
        assert 'humidity' in data['weather_summary']
