"""Abstract base weather provider."""
from abc import ABC, abstractmethod


class BaseWeatherProvider(ABC):
    """Abstract base class for weather data providers."""

    @abstractmethod
    def get_current_weather(self, city=None, lat=None, lon=None):
        """
        Get current weather data.

        Args:
            city: City name (e.g., 'London')
            lat: Latitude
            lon: Longitude

        Returns:
            dict with weather data or None if city not found

        Raises:
            ValueError: If neither city nor coordinates are provided
        """
        pass

    @abstractmethod
    def get_forecast(self, city=None, lat=None, lon=None):
        """
        Get 5-day forecast data.

        Args:
            city: City name
            lat: Latitude
            lon: Longitude

        Returns:
            dict with forecast data or None if city not found

        Raises:
            ValueError: If neither city nor coordinates are provided
        """
        pass

    @property
    @abstractmethod
    def provider_name(self):
        """Return the provider name (e.g., 'mock', 'openweathermap')."""
        pass
