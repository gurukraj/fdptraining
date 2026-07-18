"""Pytest fixtures for Weather Dashboard API tests."""
import pytest

from app.config import TestConfig
from app.database import db as _db
from app.main import create_app


@pytest.fixture(scope='function')
def app():
    """Create application for testing."""
    app = create_app(config_class=TestConfig)
    yield app


@pytest.fixture(scope='function')
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def db(app):
    """Provide a clean database for each test."""
    with app.app_context():
        _db.create_all()
        from app.models import CacheStats
        stats = CacheStats.query.first()
        if not stats:
            stats = CacheStats(hits=0, misses=0)
            _db.session.add(stats)
            _db.session.commit()
        yield _db
        _db.session.rollback()
        _db.drop_all()
