#!/usr/bin/env python3
"""Seed the database with initial data."""
import json
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import Config
from app.database import db, init_db
from app.main import create_app
from app.models import CacheStats


def seed():
    """Seed the database."""
    app = create_app()

    with app.app_context():
        # Create all tables
        db.create_all()

        # Ensure cache stats row exists
        stats = CacheStats.query.first()
        if not stats:
            stats = CacheStats(hits=0, misses=0)
            db.session.add(stats)
            db.session.commit()
            print("Created cache_stats row.")
        else:
            print("Cache stats row already exists.")

        # Verify data files exist
        data_dir = app.config.get('DATA_DIR')
        files_to_check = ['weather_dataset.json', 'forecast_dataset.json', 'cities.json']

        for filename in files_to_check:
            filepath = os.path.join(data_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    data = json.load(f)
                if filename == 'cities.json':
                    count = len(data.get('cities', []))
                else:
                    count = len(data.get('cities', {}))
                print(f"  {filename}: {count} entries")
            else:
                print(f"  WARNING: {filename} not found at {filepath}")

        print("\nDatabase seeded successfully!")
        print(f"Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")


if __name__ == '__main__':
    seed()
