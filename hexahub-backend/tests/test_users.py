"""Tests for user endpoints."""

def test_get_current_user(client):
    """Test getting current user information."""
    # First, login to get token
    login_response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpass"}
    )
    token = login_response.json()["access_token"]

    # Get current user
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "email" in data
    assert "id" in data


def test_create_user(client):
    """Test creating a new user."""
    user_data = {
        "email": "newuser@hexahub.local",
        "username": "newuser",
        "full_name": "New User"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@hexahub.local"
    assert data["is_active"] is True


def test_create_duplicate_user_fails(client):
    """Test creating duplicate user fails."""
    user_data = {
        "email": "duplicate@hexahub.local",
        "username": "duplicate",
        "full_name": "Duplicate User"
    }
    # Create first user
    response1 = client.post("/users/", json=user_data)
    assert response1.status_code == 201

    # Try to create duplicate
    response2 = client.post("/users/", json=user_data)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]


def test_list_users(client):
    """Test listing users."""
    # Login to get token
    login_response = client.post(
        "/auth/login",
        data={"username": "listtest", "password": "testpass"}
    )
    token = login_response.json()["access_token"]

    # List users
    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # At least the user we just created


def test_update_current_user(client):
    """Test updating current user information."""
    # Login
    login_response = client.post(
        "/auth/login",
        data={"username": "updatetest", "password": "testpass"}
    )
    token = login_response.json()["access_token"]

    # Update user
    update_data = {"full_name": "Updated Name"}
    response = client.patch(
        "/users/me",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
