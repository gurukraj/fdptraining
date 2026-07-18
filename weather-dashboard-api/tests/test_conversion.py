"""Tests for temperature conversion."""
import json
import pytest

from app.services.conversion_service import ConversionService


class TestConversionService:
    """Tests for the ConversionService class."""

    def test_celsius_to_fahrenheit(self):
        """Test C to F: (C * 9/5) + 32."""
        assert ConversionService.convert(0, 'celsius', 'fahrenheit') == 32.0
        assert ConversionService.convert(100, 'celsius', 'fahrenheit') == 212.0
        assert ConversionService.convert(-40, 'celsius', 'fahrenheit') == -40.0

    def test_fahrenheit_to_celsius(self):
        """Test F to C: (F - 32) * 5/9."""
        assert ConversionService.convert(32, 'fahrenheit', 'celsius') == 0.0
        assert ConversionService.convert(212, 'fahrenheit', 'celsius') == 100.0
        assert ConversionService.convert(-40, 'fahrenheit', 'celsius') == -40.0

    def test_celsius_to_kelvin(self):
        """Test C to K: C + 273.15."""
        assert ConversionService.convert(0, 'celsius', 'kelvin') == 273.15
        assert ConversionService.convert(100, 'celsius', 'kelvin') == 373.15
        assert ConversionService.convert(-273.15, 'celsius', 'kelvin') == 0.0

    def test_kelvin_to_celsius(self):
        """Test K to C: K - 273.15."""
        assert ConversionService.convert(273.15, 'kelvin', 'celsius') == 0.0
        assert ConversionService.convert(373.15, 'kelvin', 'celsius') == 100.0
        assert ConversionService.convert(0, 'kelvin', 'celsius') == -273.15

    def test_fahrenheit_to_kelvin(self):
        """Test F to K."""
        result = ConversionService.convert(32, 'fahrenheit', 'kelvin')
        assert result == 273.15

    def test_kelvin_to_fahrenheit(self):
        """Test K to F."""
        result = ConversionService.convert(273.15, 'kelvin', 'fahrenheit')
        assert result == 32.0

    def test_same_unit_conversion(self):
        """Test converting to the same unit returns the same value."""
        assert ConversionService.convert(42.5, 'celsius', 'celsius') == 42.5
        assert ConversionService.convert(100, 'fahrenheit', 'fahrenheit') == 100.0
        assert ConversionService.convert(300, 'kelvin', 'kelvin') == 300.0

    def test_invalid_from_unit(self):
        """Test that invalid source unit raises ValueError."""
        with pytest.raises(ValueError, match="Invalid source unit"):
            ConversionService.convert(100, 'invalid', 'celsius')

    def test_invalid_to_unit(self):
        """Test that invalid target unit raises ValueError."""
        with pytest.raises(ValueError, match="Invalid target unit"):
            ConversionService.convert(100, 'celsius', 'invalid')

    def test_negative_temperatures(self):
        """Test conversions with negative temperatures."""
        assert ConversionService.convert(-10, 'celsius', 'fahrenheit') == 14.0
        assert ConversionService.convert(-459.67, 'fahrenheit', 'celsius') == -273.15

    def test_batch_convert(self):
        """Test batch conversion of multiple values."""
        values = [0, 25, 100]
        results = ConversionService.batch_convert(values, 'celsius', 'fahrenheit')
        assert results == [32.0, 77.0, 212.0]

    def test_batch_convert_empty_list(self):
        """Test batch conversion with empty list."""
        results = ConversionService.batch_convert([], 'celsius', 'fahrenheit')
        assert results == []


class TestConversionEndpoint:
    """Tests for GET /api/weather/convert."""

    def test_convert_endpoint(self, client, db):
        """Test the conversion endpoint."""
        response = client.get('/api/weather/convert?value=100&from=celsius&to=fahrenheit')
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == 212.0
        assert data['from'] == 'celsius'
        assert data['to'] == 'fahrenheit'
        assert data['value'] == 100.0

    def test_convert_missing_value(self, client, db):
        """Test conversion with missing value parameter."""
        response = client.get('/api/weather/convert?from=celsius&to=fahrenheit')
        assert response.status_code == 400

    def test_convert_missing_from(self, client, db):
        """Test conversion with missing from parameter."""
        response = client.get('/api/weather/convert?value=100&to=fahrenheit')
        assert response.status_code == 400

    def test_convert_missing_to(self, client, db):
        """Test conversion with missing to parameter."""
        response = client.get('/api/weather/convert?value=100&from=celsius')
        assert response.status_code == 400

    def test_convert_invalid_unit(self, client, db):
        """Test conversion with invalid unit."""
        response = client.get('/api/weather/convert?value=100&from=celsius&to=rankine')
        assert response.status_code == 400

    def test_batch_convert_endpoint(self, client, db):
        """Test the batch conversion endpoint."""
        response = client.post('/api/weather/convert',
                              json={'values': [0, 25, 100], 'from': 'celsius', 'to': 'fahrenheit'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['results'] == [32.0, 77.0, 212.0]

    def test_batch_convert_missing_values(self, client, db):
        """Test batch conversion with missing values."""
        response = client.post('/api/weather/convert',
                              json={'from': 'celsius', 'to': 'fahrenheit'})
        assert response.status_code == 400

    def test_batch_convert_no_json(self, client, db):
        """Test batch conversion with no JSON body."""
        response = client.post('/api/weather/convert',
                              content_type='application/json',
                              data='not json')
        assert response.status_code == 400
