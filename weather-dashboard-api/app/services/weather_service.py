"""Weather data fetching and caching service."""
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from flask import current_app

from app.database import db
from app.models import CacheStats, SearchHistory, WeatherCache
from app.providers.mock_provider import MockWeatherProvider
from app.providers.openweathermap import OpenWeatherMapProvider
from app.services.conversion_service import ConversionService


def get_provider():
    """Get the configured weather provider."""
    provider_type = current_app.config.get('WEATHER_PROVIDER', 'mock')
    if provider_type == 'openweathermap':
        return OpenWeatherMapProvider()
    return MockWeatherProvider()


def _record_cache_hit():
    """Record a cache hit in statistics."""
    stats = CacheStats.query.first()
    if stats:
        stats.hits += 1
        db.session.commit()


def _record_cache_miss():
    """Record a cache miss in statistics."""
    stats = CacheStats.query.first()
    if stats:
        stats.misses += 1
        db.session.commit()


def _record_search(city_name, search_type, user_id=None):
    """Record a search in the history."""
    entry = SearchHistory(
        user_id=user_id,
        city_name=city_name,
        search_type=search_type
    )
    db.session.add(entry)
    db.session.commit()


def get_current_weather(city=None, lat=None, lon=None, units='celsius', user_id=None):
    """
    Get current weather data with caching.

    Returns:
        tuple: (weather_data dict, status_code)
    """
    if city is None and (lat is None or lon is None):
        return {'error': 'Missing required parameters. Provide city or both lat and lon.', 'status': 400}, 400

    # Build cache key
    if city:
        cache_key = f"current:{city.lower()}"
    else:
        cache_key = f"current:{lat}:{lon}"

    # Check cache
    cached = WeatherCache.query.filter_by(cache_key=cache_key).first()
    if cached and not cached.is_expired():
        _record_cache_hit()
        data = json.loads(cached.data)
        data['source'] = 'cache'
        data['units'] = units
        if units != 'celsius':
            data = _convert_weather_units(data, units)
        if city:
            _record_search(city, 'current', user_id)
        return data, 200

    # Cache miss - fetch from provider
    _record_cache_miss()
    provider = get_provider()

    try:
        weather_data = provider.get_current_weather(city=city, lat=lat, lon=lon)
    except ValueError as e:
        return {'error': str(e), 'status': 400}, 400

    if weather_data is None:
        return {'error': f'City not found: {city or f"lat={lat}, lon={lon}"}', 'status': 404}, 404

    weather_data['source'] = provider.provider_name

    # Store in cache
    now = datetime.now(timezone.utc)
    ttl = current_app.config.get('CACHE_TTL_CURRENT', 600)
    expires_at = now + timedelta(seconds=ttl)

    city_name = weather_data.get('city_name', city or 'Unknown')

    if cached:
        cached.data = json.dumps(weather_data)
        cached.fetched_at = now
        cached.expires_at = expires_at
        cached.city_name = city_name
    else:
        cached = WeatherCache(
            cache_key=cache_key,
            city_name=city_name,
            data_type='current',
            data=json.dumps(weather_data),
            fetched_at=now,
            expires_at=expires_at
        )
        db.session.add(cached)

    db.session.commit()

    # Record search
    _record_search(city_name, 'current', user_id)

    # Convert units if needed
    result = weather_data.copy()
    result['units'] = units
    if units != 'celsius':
        result = _convert_weather_units(result, units)

    return result, 200


def get_forecast(city=None, lat=None, lon=None, units='celsius', user_id=None):
    """
    Get 5-day forecast data with caching.

    Returns:
        tuple: (forecast_data dict, status_code)
    """
    if city is None and (lat is None or lon is None):
        return {'error': 'Missing required parameters. Provide city or both lat and lon.', 'status': 400}, 400

    # Build cache key
    if city:
        cache_key = f"forecast:{city.lower()}"
    else:
        cache_key = f"forecast:{lat}:{lon}"

    # Check cache
    cached = WeatherCache.query.filter_by(cache_key=cache_key).first()
    if cached and not cached.is_expired():
        _record_cache_hit()
        data = json.loads(cached.data)
        data['source'] = 'cache'
        data['units'] = units
        if units != 'celsius':
            data = _convert_forecast_units(data, units)
        if city:
            _record_search(city, 'forecast', user_id)
        return data, 200

    # Cache miss
    _record_cache_miss()
    provider = get_provider()

    try:
        forecast_data = provider.get_forecast(city=city, lat=lat, lon=lon)
    except ValueError as e:
        return {'error': str(e), 'status': 400}, 400

    if forecast_data is None:
        return {'error': f'City not found: {city or f"lat={lat}, lon={lon}"}', 'status': 404}, 404

    forecast_data['source'] = provider.provider_name

    # Group forecast by date and compute daily summaries
    grouped = _group_forecast_by_date(forecast_data)
    forecast_data['daily'] = grouped

    # Store in cache
    now = datetime.now(timezone.utc)
    ttl = current_app.config.get('CACHE_TTL_FORECAST', 3600)
    expires_at = now + timedelta(seconds=ttl)

    city_name = forecast_data.get('city_name', city or 'Unknown')

    if cached:
        cached.data = json.dumps(forecast_data)
        cached.fetched_at = now
        cached.expires_at = expires_at
        cached.city_name = city_name
    else:
        cached = WeatherCache(
            cache_key=cache_key,
            city_name=city_name,
            data_type='forecast',
            data=json.dumps(forecast_data),
            fetched_at=now,
            expires_at=expires_at
        )
        db.session.add(cached)

    db.session.commit()

    # Record search
    _record_search(city_name, 'forecast', user_id)

    result = forecast_data.copy()
    result['units'] = units
    if units != 'celsius':
        result = _convert_forecast_units(result, units)

    return result, 200


def _group_forecast_by_date(forecast_data):
    """Group forecast entries by date and compute daily summaries."""
    daily = defaultdict(lambda: {'entries': [], 'temps': [], 'humidities': [], 'conditions': []})

    for entry in forecast_data.get('forecast', []):
        dt_str = entry.get('dt', '')
        if dt_str:
            try:
                dt = datetime.fromisoformat(dt_str)
                date_key = dt.strftime('%Y-%m-%d')
            except (ValueError, TypeError):
                continue
        else:
            continue

        daily[date_key]['entries'].append(entry)
        daily[date_key]['temps'].append(entry.get('temperature', 0))
        daily[date_key]['humidities'].append(entry.get('humidity', 0))
        daily[date_key]['conditions'].append(entry.get('condition', ''))

    result = []
    for date_key in sorted(daily.keys()):
        day = daily[date_key]
        # Find dominant condition
        condition_counts = defaultdict(int)
        for c in day['conditions']:
            condition_counts[c] += 1
        dominant_condition = max(condition_counts, key=condition_counts.get) if condition_counts else 'Unknown'

        result.append({
            'date': date_key,
            'temp_high': round(max(day['temps']), 1) if day['temps'] else None,
            'temp_low': round(min(day['temps']), 1) if day['temps'] else None,
            'avg_humidity': round(sum(day['humidities']) / len(day['humidities']), 1) if day['humidities'] else None,
            'dominant_condition': dominant_condition,
            'hourly': day['entries']
        })

    return result


def _convert_weather_units(data, units):
    """Convert temperature fields in weather data to specified units."""
    temp_fields = ['temperature', 'feels_like', 'temp_min', 'temp_max']
    for field in temp_fields:
        if field in data and data[field] is not None:
            data[field] = ConversionService.convert(data[field], 'celsius', units)
    return data


def _convert_forecast_units(data, units):
    """Convert temperature fields in forecast data to specified units."""
    temp_fields = ['temperature', 'feels_like', 'temp_min', 'temp_max']

    # Convert in forecast list
    for entry in data.get('forecast', []):
        for field in temp_fields:
            if field in entry and entry[field] is not None:
                entry[field] = ConversionService.convert(entry[field], 'celsius', units)

    # Convert in daily summaries
    for day in data.get('daily', []):
        if 'temp_high' in day and day['temp_high'] is not None:
            day['temp_high'] = ConversionService.convert(day['temp_high'], 'celsius', units)
        if 'temp_low' in day and day['temp_low'] is not None:
            day['temp_low'] = ConversionService.convert(day['temp_low'], 'celsius', units)
        for entry in day.get('hourly', []):
            for field in temp_fields:
                if field in entry and entry[field] is not None:
                    entry[field] = ConversionService.convert(entry[field], 'celsius', units)

    return data


def get_cache_stats():
    """Get cache statistics."""
    stats = CacheStats.query.first()
    if not stats:
        return {'hits': 0, 'misses': 0, 'total': 0, 'hit_rate': 0.0,
                'last_reset': datetime.now(timezone.utc).isoformat()}

    total = stats.hits + stats.misses
    hit_rate = round(stats.hits / total * 100, 1) if total > 0 else 0.0

    # Count cached entries
    cached_entries = WeatherCache.query.count()

    return {
        'hits': stats.hits,
        'misses': stats.misses,
        'total': total,
        'hit_rate': hit_rate,
        'cached_entries': cached_entries,
        'last_reset': stats.last_reset.isoformat() if stats.last_reset else None
    }


def clear_cache():
    """Clear all cached weather data and reset statistics."""
    WeatherCache.query.delete()
    stats = CacheStats.query.first()
    if stats:
        stats.hits = 0
        stats.misses = 0
        stats.last_reset = datetime.now(timezone.utc)
    db.session.commit()
    return {'message': 'Cache cleared successfully'}
