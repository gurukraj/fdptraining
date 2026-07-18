"""Alert routes - configure and check weather alerts."""
from flask import Blueprint, jsonify, request

from app.services.alert_service import AlertService
from app.services.weather_service import get_current_weather

alerts_bp = Blueprint('alerts', __name__)


@alerts_bp.route('/alerts/configure', methods=['POST'])
def configure_alerts():
    """
    Configure alert thresholds for a user.

    JSON body:
        user_id: User identifier (required)
        temp_high: High temperature threshold (Celsius)
        temp_low: Low temperature threshold (Celsius)
        wind_speed: Wind speed threshold (m/s)
        humidity: Humidity threshold (%)
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body must be JSON', 'status': 400}), 400

    user_id = data.get('user_id') or request.headers.get('X-User-ID')
    if not user_id:
        return jsonify({'error': 'user_id is required (in body or X-User-ID header)', 'status': 400}), 400

    result = AlertService.configure_alert(
        user_id=user_id,
        temp_high=data.get('temp_high'),
        temp_low=data.get('temp_low'),
        wind_speed=data.get('wind_speed'),
        humidity=data.get('humidity')
    )

    return jsonify({
        'message': 'Alert thresholds configured successfully',
        'config': result
    }), 201


@alerts_bp.route('/alerts/check')
def check_alerts():
    """
    Check current weather against configured thresholds.

    Query params:
        city: City name (required)
        user_id: User identifier (or use X-User-ID header)
    """
    city = request.args.get('city')
    user_id = request.args.get('user_id') or request.headers.get('X-User-ID')

    if not city:
        return jsonify({'error': 'Missing required parameter: city', 'status': 400}), 400
    if not user_id:
        return jsonify({'error': 'user_id is required (as query param or X-User-ID header)', 'status': 400}), 400

    # Get current weather
    weather_data, status_code = get_current_weather(city=city, user_id=user_id)
    if status_code != 200:
        return jsonify(weather_data), status_code

    # Check against thresholds
    alerts = AlertService.check_alerts(user_id, weather_data)

    return jsonify({
        'city': city,
        'alerts': alerts,
        'alert_count': len(alerts),
        'weather_summary': {
            'temperature': weather_data.get('temperature'),
            'wind_speed': weather_data.get('wind_speed'),
            'humidity': weather_data.get('humidity'),
            'condition': weather_data.get('condition')
        }
    })
