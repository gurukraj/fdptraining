"""Mock weather provider using local JSON datasets."""
import json
import os
import random
from datetime import datetime, timedelta, timezone

from app.providers.base_provider import BaseWeatherProvider


class MockWeatherProvider(BaseWeatherProvider):
    """Weather provider using local JSON datasets with small random variations."""

    def __init__(self, data_dir=None):
        self._data_dir = data_dir
        self._weather_data = None
        self._forecast_data = None
        self._cities_data = None

    @property
    def data_dir(self):
        if self._data_dir:
            return self._data_dir
        from flask import current_app
        return current_app.config.get('DATA_DIR', os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data'
        ))

    def _load_weather_data(self):
        """Load weather dataset from JSON file."""
        if self._weather_data is None:
            path = os.path.join(self.data_dir, 'weather_dataset.json')
            with open(path, 'r') as f:
                self._weather_data = json.load(f)
        return self._weather_data

    def _load_forecast_data(self):
        """Load forecast dataset from JSON file."""
        if self._forecast_data is None:
            path = os.path.join(self.data_dir, 'forecast_dataset.json')
            with open(path, 'r') as f:
                self._forecast_data = json.load(f)
        return self._forecast_data

    def _load_cities_data(self):
        """Load cities metadata from JSON file."""
        if self._cities_data is None:
            path = os.path.join(self.data_dir, 'cities.json')
            with open(path, 'r') as f:
                self._cities_data = json.load(f)
        return self._cities_data

    def _find_city_by_coordinates(self, lat, lon):
        """Find city name by coordinates (nearest match)."""
        cities = self._load_cities_data()
        min_distance = float('inf')
        closest_city = None
        city_list = cities if isinstance(cities, list) else cities.get('cities', [])
        for city in city_list:
            clat = city.get('lat', city.get('coordinates', {}).get('lat', 0))
            clon = city.get('lon', city.get('coordinates', {}).get('lon', 0))
            distance = ((clat - lat) ** 2 + (clon - lon) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_city = city['name']
        # Only match if reasonably close (within ~1 degree)
        if min_distance < 1.0:
            return closest_city
        return None

    def _add_variation(self, temp, variation=2.0):
        """Add small random variation to temperature."""
        return round(temp + random.uniform(-variation, variation), 1)

    def get_current_weather(self, city=None, lat=None, lon=None):
        """Get current weather data from mock dataset."""
        if city is None and (lat is None or lon is None):
            raise ValueError("Either city name or both lat and lon must be provided")

        if city is None:
            city = self._find_city_by_coordinates(lat, lon)
            if city is None:
                return None

        data = self._load_weather_data()
        # Case-insensitive city lookup
        city_data = None
        for key, value in data['cities'].items():
            if key.lower() == city.lower():
                city_data = value
                city = key  # Use the canonical name
                break

        if city_data is None:
            return None

        now = datetime.now(timezone.utc)
        variation = random.uniform(-2.0, 2.0)

        return {
            'city_name': city_data['city_name'],
            'country_code': city_data['country_code'],
            'coordinates': city_data['coordinates'],
            'temperature': round(city_data['temperature'] + variation, 1),
            'feels_like': round(city_data['feels_like'] + variation, 1),
            'temp_min': round(city_data['temp_min'] + variation * 0.8, 1),
            'temp_max': round(city_data['temp_max'] + variation * 0.8, 1),
            'humidity': city_data['humidity'],
            'pressure': city_data['pressure'],
            'wind_speed': city_data['wind_speed'],
            'wind_direction': city_data['wind_direction'],
            'condition': city_data['condition'],
            'description': city_data['description'],
            'icon': city_data['icon'],
            'visibility': city_data['visibility'],
            'fetched_at': now.isoformat()
        }

    def get_forecast(self, city=None, lat=None, lon=None):
        """Get 5-day forecast data from mock dataset."""
        if city is None and (lat is None or lon is None):
            raise ValueError("Either city name or both lat and lon must be provided")

        if city is None:
            city = self._find_city_by_coordinates(lat, lon)
            if city is None:
                return None

        data = self._load_forecast_data()
        # Case-insensitive city lookup
        city_data = None
        for key, value in data['cities'].items():
            if key.lower() == city.lower():
                city_data = value
                city = key
                break

        if city_data is None:
            # If no forecast data, generate basic forecast from current weather
            weather_data = self._load_weather_data()
            weather_city = None
            for key, value in weather_data['cities'].items():
                if key.lower() == city.lower():
                    weather_city = value
                    city = key
                    break
            if weather_city is None:
                return None
            return self._generate_basic_forecast(weather_city)

        now = datetime.now(timezone.utc)
        forecast_list = []
        for entry in city_data['forecast']:
            dt = now + timedelta(hours=entry['dt_offset_hours'])
            variation = random.uniform(-1.0, 1.0)
            forecast_list.append({
                'dt': dt.isoformat(),
                'temperature': round(entry['temperature'] + variation, 1),
                'feels_like': round(entry['feels_like'] + variation, 1),
                'temp_min': round(entry['temp_min'] + variation * 0.8, 1),
                'temp_max': round(entry['temp_max'] + variation * 0.8, 1),
                'humidity': entry['humidity'],
                'pressure': entry['pressure'],
                'wind_speed': entry['wind_speed'],
                'condition': entry['condition'],
                'description': entry['description'],
                'icon': entry['icon']
            })

        return {
            'city_name': city_data['city_name'],
            'country_code': city_data['country_code'],
            'forecast': forecast_list,
            'fetched_at': now.isoformat()
        }

    def _generate_basic_forecast(self, weather_city):
        """Generate a basic forecast from current weather when no forecast data available."""
        now = datetime.now(timezone.utc)
        forecast_list = []
        base_temp = weather_city['temperature']

        for i in range(40):  # 40 entries = 5 days * 8 (3-hour intervals)
            hours_offset = i * 3
            dt = now + timedelta(hours=hours_offset)
            # Simulate diurnal variation
            hour_of_day = (dt.hour) % 24
            diurnal = -3 + 6 * (1 - abs(hour_of_day - 14) / 14)
            variation = random.uniform(-1.5, 1.5)
            temp = round(base_temp + diurnal + variation, 1)

            forecast_list.append({
                'dt': dt.isoformat(),
                'temperature': temp,
                'feels_like': round(temp - 1.2, 1),
                'temp_min': round(temp - 1.5, 1),
                'temp_max': round(temp + 1.5, 1),
                'humidity': weather_city['humidity'],
                'pressure': weather_city['pressure'],
                'wind_speed': weather_city['wind_speed'],
                'condition': weather_city['condition'],
                'description': weather_city['description'],
                'icon': weather_city['icon']
            })

        return {
            'city_name': weather_city['city_name'],
            'country_code': weather_city['country_code'],
            'forecast': forecast_list,
            'fetched_at': now.isoformat()
        }

    @property
    def provider_name(self):
        return 'mock'
