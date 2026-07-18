"""SQLAlchemy database models."""
from datetime import datetime, timezone
from app.database import db


class WeatherCache(db.Model):
    __tablename__ = "weather_cache"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cache_key = db.Column(db.Text, unique=True, nullable=False)
    city_name = db.Column(db.Text, nullable=False)
    data_type = db.Column(db.Text, nullable=False)
    data = db.Column(db.Text, nullable=False)
    fetched_at = db.Column(db.DateTime, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def is_expired(self):
        """Check if the cache entry has expired."""
        return datetime.now(timezone.utc) > self.expires_at.replace(tzinfo=timezone.utc)


class Favorite(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Text, nullable=False)
    city_name = db.Column(db.Text, nullable=False)
    added_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    __table_args__ = (db.UniqueConstraint("user_id", "city_name"),)


class SearchHistory(db.Model):
    __tablename__ = "search_history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Text)
    city_name = db.Column(db.Text, nullable=False)
    search_type = db.Column(db.Text, nullable=False)
    searched_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class AlertConfig(db.Model):
    __tablename__ = "alert_configs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Text, unique=True, nullable=False)
    temp_high_threshold = db.Column(db.Float)
    temp_low_threshold = db.Column(db.Float)
    wind_speed_threshold = db.Column(db.Float)
    humidity_threshold = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime)


class CacheStats(db.Model):
    __tablename__ = "cache_stats"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hits = db.Column(db.Integer, default=0)
    misses = db.Column(db.Integer, default=0)
    last_reset = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
