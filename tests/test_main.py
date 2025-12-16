"""
Unit tests for the Demo Flask API
"""

import pytest
from app.main import app, add_numbers, multiply_numbers


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestHealthCheck:
    """Tests for the health check endpoint"""

    def test_home_returns_200(self, client):
        """Test that home endpoint returns 200"""
        response = client.get("/")
        assert response.status_code == 200

    def test_home_returns_healthy_status(self, client):
        """Test that home endpoint returns healthy status"""
        response = client.get("/")
        data = response.get_json()
        assert data["status"] == "healthy"

    def test_home_returns_version(self, client):
        """Test that home endpoint returns version"""
        response = client.get("/")
        data = response.get_json()
        assert "version" in data


class TestItemsAPI:
    """Tests for the items CRUD endpoints"""

    def test_get_items_empty(self, client):
        """Test getting items when list is empty"""
        response = client.get("/api/items")
        assert response.status_code == 200
        data = response.get_json()
        assert "items" in data
        assert "count" in data

    def test_create_item_success(self, client):
        """Test creating an item successfully"""
        response = client.post(
            "/api/items",
            json={"name": "Test Item", "description": "A test item"}
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["item"]["name"] == "Test Item"

    def test_create_item_without_name(self, client):
        """Test creating an item without name fails"""
        response = client.post("/api/items", json={})
        assert response.status_code == 400

    def test_get_item_not_found(self, client):
        """Test getting non-existent item returns 404"""
        response = client.get("/api/items/9999")
        assert response.status_code == 404


class TestUtilityFunctions:
    """Tests for utility functions"""

    def test_add_numbers(self):
        """Test add_numbers function"""
        assert add_numbers(2, 3) == 5
        assert add_numbers(-1, 1) == 0
        assert add_numbers(0, 0) == 0

    def test_multiply_numbers(self):
        """Test multiply_numbers function"""
        assert multiply_numbers(2, 3) == 6
        assert multiply_numbers(-1, 5) == -5
        assert multiply_numbers(0, 100) == 0

    def test_add_numbers_floats(self):
        """Test add_numbers with floats"""
        result = add_numbers(1.5, 2.5)
        assert result == 4.0

    def test_multiply_numbers_floats(self):
        """Test multiply_numbers with floats"""
        result = multiply_numbers(2.5, 4.0)
        assert result == 10.0
