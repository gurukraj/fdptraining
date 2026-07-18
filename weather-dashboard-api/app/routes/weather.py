"""Weather routes - current weather, forecast, conversion, and cache management."""
from flask import Blueprint, jsonify, request

from app.services.conversion_service import ConversionService
from app.services.weather_service import (
    clear_cache,
    get_cache_stats,
    get_current_weather,
    get_forecast,
)

weather_bp = Blueprint('weather', __name__)


@weather_bp.route('/weather/current')
def current_weather():
    """
    Get current weather data.

    Query params:
        city: City name (e.g., 'London')
        lat: Latitude (use with lon)
        lon: Longitude (use with lat)
        units: Temperature units - celsius (default), fahrenheit, kelvin
    """
    city = request.args.get('city')
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    units = request.args.get('units', 'celsius').lower()
    user_id = request.headers.get('X-User-ID')

    if units not in ('celsius', 'fahrenheit', 'kelvin'):
        return jsonify({'error': f'Invalid units: {units}. Must be celsius, fahrenheit, or kelvin.', 'status': 400}), 400

    if city is None and (lat is None or lon is None):
        return jsonify({'error': 'Missing required parameters. Provide city or both lat and lon.', 'status': 400}), 400

    data, status_code = get_current_weather(
        city=city, lat=lat, lon=lon, units=units, user_id=user_id
    )
    return jsonify(data), status_code


@weather_bp.route('/weather/forecast')
def forecast():
    """
    Get 5-day weather forecast.

    Query params:
        city: City name
        lat: Latitude
        lon: Longitude
        units: Temperature units - celsius (default), fahrenheit, kelvin
    """
    city = request.args.get('city')
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    units = request.args.get('units', 'celsius').lower()
    user_id = request.headers.get('X-User-ID')

    if units not in ('celsius', 'fahrenheit', 'kelvin'):
        return jsonify({'error': f'Invalid units: {units}. Must be celsius, fahrenheit, or kelvin.', 'status': 400}), 400

    if city is None and (lat is None or lon is None):
        return jsonify({'error': 'Missing required parameters. Provide city or both lat and lon.', 'status': 400}), 400

    data, status_code = get_forecast(
        city=city, lat=lat, lon=lon, units=units, user_id=user_id
    )
    return jsonify(data), status_code


@weather_bp.route('/weather/convert')
def convert_temperature():
    """
    Convert temperature between units.

    Query params:
        value: Temperature value
        from: Source unit (celsius, fahrenheit, kelvin)
        to: Target unit (celsius, fahrenheit, kelvin)
    """
    value = request.args.get('value', type=float)
    from_unit = request.args.get('from', '').lower()
    to_unit = request.args.get('to', '').lower()

    if value is None:
        return jsonify({'error': 'Missing required parameter: value', 'status': 400}), 400
    if not from_unit:
        return jsonify({'error': 'Missing required parameter: from', 'status': 400}), 400
    if not to_unit:
        return jsonify({'error': 'Missing required parameter: to', 'status': 400}), 400

    try:
        result = ConversionService.convert(value, from_unit, to_unit)
    except ValueError as e:
        return jsonify({'error': str(e), 'status': 400}), 400

    return jsonify({
        'value': value,
        'from': from_unit,
        'to': to_unit,
        'result': result
    })


@weather_bp.route('/weather/convert', methods=['POST'])
def batch_convert_temperature():
    """
    Batch convert temperatures.

    JSON body:
        values: List of temperature values
        from: Source unit
        to: Target unit
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body must be JSON', 'status': 400}), 400

    values = data.get('values')
    from_unit = data.get('from', '').lower()
    to_unit = data.get('to', '').lower()

    if not values or not isinstance(values, list):
        return jsonify({'error': 'Missing or invalid parameter: values (must be a list)', 'status': 400}), 400
    if not from_unit:
        return jsonify({'error': 'Missing required parameter: from', 'status': 400}), 400
    if not to_unit:
        return jsonify({'error': 'Missing required parameter: to', 'status': 400}), 400

    try:
        results = ConversionService.batch_convert(values, from_unit, to_unit)
    except ValueError as e:
        return jsonify({'error': str(e), 'status': 400}), 400

    return jsonify({
        'values': values,
        'from': from_unit,
        'to': to_unit,
        'results': results
    })


@weather_bp.route('/cache/stats')
def cache_stats():
    """Get cache hit/miss statistics."""
    stats = get_cache_stats()
    return jsonify(stats)


@weather_bp.route('/cache', methods=['DELETE'])
def clear_cache_route():
    """Clear all cached weather data."""
    result = clear_cache()
    return jsonify(result)
