"""Tests for favorites and search history."""
import json
import pytest


class TestFavorites:
    """Tests for favorites CRUD operations."""

    def test_add_favorite(self, client, db):
        """Test adding a city to favorites."""
        response = client.post('/api/favorites',
                              json={'user_id': 'user1', 'city': 'London'})
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'London added to favorites'
        assert data['favorite']['city_name'] == 'London'
        assert data['favorite']['user_id'] == 'user1'

    def test_add_favorite_with_header(self, client, db):
        """Test adding a favorite using X-User-ID header."""
        response = client.post('/api/favorites',
                              json={'city': 'Tokyo'},
                              headers={'X-User-ID': 'user2'})
        assert response.status_code == 201

    def test_add_duplicate_favorite(self, client, db):
        """Test adding the same city twice returns 409."""
        client.post('/api/favorites',
                   json={'user_id': 'user1', 'city': 'London'})
        response = client.post('/api/favorites',
                              json={'user_id': 'user1', 'city': 'London'})
        assert response.status_code == 409
        data = response.get_json()
        assert 'already in favorites' in data['error']

    def test_list_favorites(self, client, db):
        """Test listing user favorites."""
        client.post('/api/favorites',
                   json={'user_id': 'user1', 'city': 'London'})
        client.post('/api/favorites',
                   json={'user_id': 'user1', 'city': 'Tokyo'})
        client.post('/api/favorites',
                   json={'user_id': 'user1', 'city': 'Paris'})

        response = client.get('/api/favorites?user_id=user1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 3
        city_names = [f['city_name'] for f in data['favorites']]
        assert 'London' in city_names
        assert 'Tokyo' in city_names
        assert 'Paris' in city_names

    def test_list_favorites_empty(self, client, db):
        """Test listing favorites for user with none."""
        response = client.get('/api/favorites?user_id=newuser')
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 0
        assert data['favorites'] == []

    def test_remove_favorite(self, client, db):
        """Test removing a city from favorites."""
        client.post('/api/favorites',
                   json={'user_id': 'user1', 'city': 'London'})

        response = client.delete('/api/favorites/London?user_id=user1')
        assert response.status_code == 200
        data = response.get_json()
        assert 'removed from favorites' in data['message']

        # Verify it's gone
        response = client.get('/api/favorites?user_id=user1')
        data = response.get_json()
        assert data['count'] == 0

    def test_remove_nonexistent_favorite(self, client, db):
        """Test removing a city that isn't in favorites."""
        response = client.delete('/api/favorites/NotThere?user_id=user1')
        assert response.status_code == 404

    def test_add_favorite_missing_city(self, client, db):
        """Test adding favorite without city."""
        response = client.post('/api/favorites',
                              json={'user_id': 'user1'})
        assert response.status_code == 400

    def test_add_favorite_missing_user_id(self, client, db):
        """Test adding favorite without user_id."""
        response = client.post('/api/favorites',
                              json={'city': 'London'})
        assert response.status_code == 400

    def test_list_favorites_missing_user_id(self, client, db):
        """Test listing favorites without user_id."""
        response = client.get('/api/favorites')
        assert response.status_code == 400

    def test_different_users_have_separate_favorites(self, client, db):
        """Test that different users have independent favorites."""
        client.post('/api/favorites',
                   json={'user_id': 'user1', 'city': 'London'})
        client.post('/api/favorites',
                   json={'user_id': 'user2', 'city': 'Tokyo'})

        response1 = client.get('/api/favorites?user_id=user1')
        response2 = client.get('/api/favorites?user_id=user2')

        data1 = response1.get_json()
        data2 = response2.get_json()

        assert data1['count'] == 1
        assert data2['count'] == 1
        assert data1['favorites'][0]['city_name'] == 'London'
        assert data2['favorites'][0]['city_name'] == 'Tokyo'


class TestSearchHistory:
    """Tests for search history."""

    def test_search_recorded(self, client, db):
        """Test that weather searches are recorded in history."""
        client.get('/api/weather/current?city=London',
                  headers={'X-User-ID': 'user1'})
        client.get('/api/weather/current?city=Tokyo',
                  headers={'X-User-ID': 'user1'})

        response = client.get('/api/history?user_id=user1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] >= 2

    def test_history_missing_user_id(self, client, db):
        """Test history without user_id."""
        response = client.get('/api/history')
        assert response.status_code == 400

    def test_history_empty(self, client, db):
        """Test history for user with no searches."""
        response = client.get('/api/history?user_id=newuser')
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 0

    def test_history_records_search_type(self, client, db):
        """Test that history records the search type."""
        client.get('/api/weather/current?city=London',
                  headers={'X-User-ID': 'user1'})

        response = client.get('/api/history?user_id=user1')
        data = response.get_json()
        assert data['history'][0]['search_type'] == 'current'
