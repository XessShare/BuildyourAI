"""Tests for authentication endpoints."""

def test_login_creates_user(client):
    """Test login endpoint creates demo user if not exists."""
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_returns_token(client):
    """Test login returns valid token."""
    # First login
    response = client.post(
        "/auth/login",
        data={"username": "testuser2", "password": "testpass"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    assert len(token) > 0


def test_oauth_callback_placeholder(client):
    """Test OAuth callback endpoint (placeholder)."""
    response = client.get("/auth/callback?code=test_code&state=test_state")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["code"] == "test_code"
