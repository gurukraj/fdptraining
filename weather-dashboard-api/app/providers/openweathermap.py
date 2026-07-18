"""OpenWeatherMap weather provider."""
import requests
from datetime import datetime, timezone

from app.providers.base_provider import BaseWeatherProvider


class OpenWeatherMapProvider(BaseWeatherProvider):
    """Weather provider using OpenWeatherMap API."""

    BASE_URL = 'https://api.openweathermap.org/data/2.5'

    def __init__(self, api_key=None):
        self._api_key = api_key

    @property
    def api_key(self):
        if self._api_key:
            return self._api_key
        from flask import current_app
        return current_app.config.get('OPENWEATHERMAP_API_KEY', '')

    def get_current_weather(self, city=None, lat=None, lon=None):
        """Get current weather from OpenWeatherMap API."""
        if city is None and (lat is None or lon is None):
            raise ValueError("Either city name or both lat and lon must be provided")

        params = {
            'appid': self.api_key,
            'units': 'metric'
        }

        if city:
            params['q'] = city
        else:
            params['lat'] = lat
            params['lon'] = lon

        try:
            response = requests.get(f'{self.BASE_URL}/weather', params=params, timeout=10)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            return None

        now = datetime.now(timezone.utc)

        return {
            'city_name': data.get('name', city or 'Unknown'),
            'country_code': data.get('sys', {}).get('country', ''),
            'coordinates': {
                'lat': data.get('coord', {}).get('lat'),
                'lon': data.get('coord', {}).get('lon')
            },
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data.get('wind', {}).get('speed', 0),
            'wind_direction': data.get('wind', {}).get('deg', 0),
            'condition': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'visibility': data.get('visibility', 10000),
            'fetched_at': now.isoformat()
        }

    def get_forecast(self, city=None, lat=None, lon=None):
        """Get 5-day forecast from OpenWeatherMap API."""
        if city is None and (lat is None or lon is None):
            raise ValueError("Either city name or both lat and lon must be provided")

        params = {
            'appid': self.api_key,
            'units': 'metric'
        }

        if city:
            params['q'] = city
        else:
            params['lat'] = lat
            params['lon'] = lon

        try:
            response = requests.get(f'{self.BASE_URL}/forecast', params=params, timeout=10)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            return None

        now = datetime.now(timezone.utc)
        forecast_list = []

        for entry in data.get('list', []):
            forecast_list.append({
                'dt': datetime.fromtimestamp(entry['dt'], tz=timezone.utc).isoformat(),
                'temperature': entry['main']['temp'],
                'feels_like': entry['main']['feels_like'],
                'temp_min': entry['main']['temp_min'],
                'temp_max': entry['main']['temp_max'],
                'humidity': entry['main']['humidity'],
                'pressure': entry['main']['pressure'],
                'wind_speed': entry.get('wind', {}).get('speed', 0),
                'condition': entry['weather'][0]['main'],
                'description': entry['weather'][0]['description'],
                'icon': entry['weather'][0]['icon']
            })

        return {
            'city_name': data.get('city', {}).get('name', city or 'Unknown'),
            'country_code': data.get('city', {}).get('country', ''),
            'forecast': forecast_list,
            'fetched_at': now.isoformat()
        }

    @property
    def provider_name(self):
        return 'openweathermap'
