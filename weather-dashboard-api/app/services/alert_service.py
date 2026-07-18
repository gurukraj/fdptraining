"""Weather alert threshold checking service."""
from datetime import datetime, timezone

from app.database import db
from app.models import AlertConfig


class AlertService:
    """Service for managing and checking weather alerts."""

    @staticmethod
    def configure_alert(user_id, temp_high=None, temp_low=None,
                        wind_speed=None, humidity=None):
        """
        Configure alert thresholds for a user.

        Args:
            user_id: User identifier
            temp_high: High temperature threshold (Celsius)
            temp_low: Low temperature threshold (Celsius)
            wind_speed: Wind speed threshold (m/s)
            humidity: Humidity threshold (%)

        Returns:
            dict with the configured alert settings
        """
        config = AlertConfig.query.filter_by(user_id=user_id).first()

        if config:
            if temp_high is not None:
                config.temp_high_threshold = temp_high
            if temp_low is not None:
                config.temp_low_threshold = temp_low
            if wind_speed is not None:
                config.wind_speed_threshold = wind_speed
            if humidity is not None:
                config.humidity_threshold = humidity
            config.updated_at = datetime.now(timezone.utc)
        else:
            config = AlertConfig(
                user_id=user_id,
                temp_high_threshold=temp_high,
                temp_low_threshold=temp_low,
                wind_speed_threshold=wind_speed,
                humidity_threshold=humidity
            )
            db.session.add(config)

        db.session.commit()

        return {
            'user_id': config.user_id,
            'temp_high_threshold': config.temp_high_threshold,
            'temp_low_threshold': config.temp_low_threshold,
            'wind_speed_threshold': config.wind_speed_threshold,
            'humidity_threshold': config.humidity_threshold,
            'created_at': config.created_at.isoformat() if config.created_at else None,
            'updated_at': config.updated_at.isoformat() if config.updated_at else None
        }

    @staticmethod
    def check_alerts(user_id, weather_data):
        """
        Check current weather against user's configured thresholds.

        Args:
            user_id: User identifier
            weather_data: dict with current weather data

        Returns:
            list of triggered alerts
        """
        config = AlertConfig.query.filter_by(user_id=user_id).first()

        if not config:
            return []

        alerts = []
        temp = weather_data.get('temperature')
        wind = weather_data.get('wind_speed')
        humidity = weather_data.get('humidity')

        # Check high temperature
        if config.temp_high_threshold is not None and temp is not None:
            if temp >= config.temp_high_threshold:
                severity = 'critical' if temp >= config.temp_high_threshold + 5 else 'warning'
                alerts.append({
                    'type': 'high_temperature',
                    'severity': severity,
                    'message': f'Temperature {temp}°C exceeds threshold of {config.temp_high_threshold}°C',
                    'current_value': temp,
                    'threshold': config.temp_high_threshold
                })

        # Check low temperature
        if config.temp_low_threshold is not None and temp is not None:
            if temp <= config.temp_low_threshold:
                severity = 'critical' if temp <= config.temp_low_threshold - 5 else 'warning'
                alerts.append({
                    'type': 'low_temperature',
                    'severity': severity,
                    'message': f'Temperature {temp}°C is below threshold of {config.temp_low_threshold}°C',
                    'current_value': temp,
                    'threshold': config.temp_low_threshold
                })

        # Check wind speed
        if config.wind_speed_threshold is not None and wind is not None:
            if wind >= config.wind_speed_threshold:
                severity = 'critical' if wind >= config.wind_speed_threshold * 1.5 else 'warning'
                alerts.append({
                    'type': 'high_wind_speed',
                    'severity': severity,
                    'message': f'Wind speed {wind} m/s exceeds threshold of {config.wind_speed_threshold} m/s',
                    'current_value': wind,
                    'threshold': config.wind_speed_threshold
                })

        # Check humidity
        if config.humidity_threshold is not None and humidity is not None:
            if humidity >= config.humidity_threshold:
                severity = 'critical' if humidity >= 95 else 'warning'
                alerts.append({
                    'type': 'high_humidity',
                    'severity': severity,
                    'message': f'Humidity {humidity}% exceeds threshold of {config.humidity_threshold}%',
                    'current_value': humidity,
                    'threshold': config.humidity_threshold
                })

        return alerts
