"""Database setup and initialization."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    with app.app_context():
        from app.models import CacheStats
        db.create_all()
        stats = CacheStats.query.first()
        if not stats:
            stats = CacheStats(hits=0, misses=0)
            db.session.add(stats)
            db.session.commit()
