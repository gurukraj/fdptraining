"""Favorites and search history routes."""
from flask import Blueprint, jsonify, request

from app.database import db
from app.models import Favorite, SearchHistory

favorites_bp = Blueprint('favorites', __name__)


@favorites_bp.route('/favorites', methods=['POST'])
def add_favorite():
    """
    Add a city to user's favorites.

    JSON body:
        city: City name (required)
        user_id: User identifier (or use X-User-ID header)
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body must be JSON', 'status': 400}), 400

    user_id = data.get('user_id') or request.headers.get('X-User-ID')
    city = data.get('city')

    if not user_id:
        return jsonify({'error': 'user_id is required (in body or X-User-ID header)', 'status': 400}), 400
    if not city:
        return jsonify({'error': 'city is required', 'status': 400}), 400

    # Check for duplicate
    existing = Favorite.query.filter_by(user_id=user_id, city_name=city).first()
    if existing:
        return jsonify({'error': f'{city} is already in favorites', 'status': 409}), 409

    favorite = Favorite(user_id=user_id, city_name=city)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        'message': f'{city} added to favorites',
        'favorite': {
            'id': favorite.id,
            'user_id': favorite.user_id,
            'city_name': favorite.city_name,
            'added_at': favorite.added_at.isoformat()
        }
    }), 201


@favorites_bp.route('/favorites')
def list_favorites():
    """
    List user's favorite cities.

    Query params:
        user_id: User identifier (or use X-User-ID header)
    """
    user_id = request.args.get('user_id') or request.headers.get('X-User-ID')

    if not user_id:
        return jsonify({'error': 'user_id is required (as query param or X-User-ID header)', 'status': 400}), 400

    favorites = Favorite.query.filter_by(user_id=user_id).order_by(Favorite.added_at.desc()).all()

    return jsonify({
        'user_id': user_id,
        'favorites': [
            {
                'id': f.id,
                'city_name': f.city_name,
                'added_at': f.added_at.isoformat()
            }
            for f in favorites
        ],
        'count': len(favorites)
    })


@favorites_bp.route('/favorites/<city>', methods=['DELETE'])
def remove_favorite(city):
    """
    Remove a city from user's favorites.

    Path params:
        city: City name

    Query params:
        user_id: User identifier (or use X-User-ID header)
    """
    user_id = request.args.get('user_id') or request.headers.get('X-User-ID')

    if not user_id:
        return jsonify({'error': 'user_id is required (as query param or X-User-ID header)', 'status': 400}), 400

    favorite = Favorite.query.filter_by(user_id=user_id, city_name=city).first()

    if not favorite:
        return jsonify({'error': f'{city} not found in favorites', 'status': 404}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'message': f'{city} removed from favorites'})


@favorites_bp.route('/history')
def search_history():
    """
    Get user's search history.

    Query params:
        user_id: User identifier (or use X-User-ID header)
        limit: Max number of entries (default 50)
    """
    user_id = request.args.get('user_id') or request.headers.get('X-User-ID')
    limit = request.args.get('limit', 50, type=int)

    if not user_id:
        return jsonify({'error': 'user_id is required (as query param or X-User-ID header)', 'status': 400}), 400

    history = SearchHistory.query.filter_by(user_id=user_id)\
        .order_by(SearchHistory.searched_at.desc())\
        .limit(limit)\
        .all()

    return jsonify({
        'user_id': user_id,
        'history': [
            {
                'id': h.id,
                'city_name': h.city_name,
                'search_type': h.search_type,
                'searched_at': h.searched_at.isoformat()
            }
            for h in history
        ],
        'count': len(history)
    })
