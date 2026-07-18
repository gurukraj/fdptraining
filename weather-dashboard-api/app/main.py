"""Flask application factory."""
from flask import Flask, jsonify
from .config import Config
from .database import init_db
from .providers.mock_provider import MockWeatherProvider
from .routes.weather import weather_bp
from .routes.alerts import alerts_bp
from .routes.favorites import favorites_bp


def create_app(config=None, config_class=None):
    app = Flask(__name__)

    cfg = config or config_class or Config
    if isinstance(cfg, type):
        cfg = cfg()

    app.config["SQLALCHEMY_DATABASE_URI"] = cfg.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = getattr(cfg, "TESTING", False)

    init_db(app)

    if cfg.WEATHER_PROVIDER == "openweathermap" and cfg.OPENWEATHERMAP_API_KEY:
        from .providers.openweathermap import OpenWeatherMapProvider
        provider = OpenWeatherMapProvider(cfg.OPENWEATHERMAP_API_KEY)
    else:
        provider = MockWeatherProvider()

    app.config["WEATHER_PROVIDER_NAME"] = cfg.WEATHER_PROVIDER
    app.config["WEATHER_PROVIDER"] = provider
    app.config["CACHE_TTL_CURRENT"] = cfg.CACHE_TTL_CURRENT
    app.config["CACHE_TTL_FORECAST"] = cfg.CACHE_TTL_FORECAST

    app.register_blueprint(weather_bp, url_prefix="/api")
    app.register_blueprint(alerts_bp, url_prefix="/api")
    app.register_blueprint(favorites_bp, url_prefix="/api")

    @app.route("/api/health")
    def health():
        return jsonify({"status": "healthy", "provider": cfg.WEATHER_PROVIDER})

    @app.route("/health")
    def health_root():
        return jsonify({"status": "healthy", "provider": cfg.WEATHER_PROVIDER})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
