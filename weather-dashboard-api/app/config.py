"""Application configuration."""
import os


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///weather_dashboard.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Weather provider: 'mock' or 'openweathermap'
    WEATHER_PROVIDER = os.environ.get('WEATHER_PROVIDER', 'mock')

    # OpenWeatherMap API key (only needed if WEATHER_PROVIDER='openweathermap')
    OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY', '')

    # Cache TTL in seconds
    CACHE_TTL_CURRENT = int(os.environ.get('CACHE_TTL_CURRENT', 600))  # 10 minutes
    CACHE_TTL_FORECAST = int(os.environ.get('CACHE_TTL_FORECAST', 3600))  # 1 hour

    # Data directory
    DATA_DIR = os.environ.get('DATA_DIR', os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data'
    ))


class TestConfig(Config):
    """Test configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WEATHER_PROVIDER = 'mock'
    CACHE_TTL_CURRENT = 600
    CACHE_TTL_FORECAST = 3600
