# HexaHub Backend API Documentation

Complete API reference with examples, authentication, and best practices.

## Table of Contents
- [Overview](#overview)
- [Base URL](#base-url)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)
- [SDKs and Client Libraries](#sdks-and-client-libraries)

## Overview

The HexaHub Backend API is a RESTful API built with FastAPI that provides:
- User authentication and authorization
- User management (CRUD operations)
- Health monitoring endpoints
- Prometheus metrics for observability

### API Version
Current Version: **1.0.0**

### Response Format
All responses are in JSON format with UTF-8 encoding.

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## Base URL

**Local Development:**
```
http://localhost:8000
```

**Production:**
```
https://api.hexahub.com
```

## Authentication

### JWT Bearer Token Authentication

The API uses JWT (JSON Web Tokens) for authentication. Tokens are obtained via the `/auth/login` endpoint and must be included in the Authorization header for protected endpoints.

#### Token Lifecycle

1. **Obtain Token**: POST to `/auth/login` with credentials
2. **Use Token**: Include in Authorization header
3. **Token Expiration**: 30 minutes (configurable)
4. **Refresh Token**: Use `/auth/refresh` (future)

#### Example Authentication Flow

**1. Login to get token:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=secret"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**2. Use token in subsequent requests:**
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Security Considerations

- Tokens are signed with HS256 algorithm
- Tokens expire after 30 minutes by default
- Store tokens securely (httpOnly cookies recommended for web apps)
- Never commit SECRET_KEY to version control
- Use HTTPS in production

## API Endpoints

### Root Endpoint

#### GET /

Get API information and navigation links.

**Parameters:** None

**Response:**
```json
{
  "name": "HexaHub Backend API",
  "version": "1.0.0",
  "description": "FastAPI backend for HexaHub platform",
  "documentation": {
    "interactive": "/docs",
    "redoc": "/redoc"
  },
  "endpoints": {
    "health": "/health",
    "metrics": "/metrics"
  }
}
```

**Example:**
```bash
curl http://localhost:8000/
```

---

### Health Check Endpoints

#### GET /health

Check application health status.

**Tag:** `health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-01T12:00:00Z",
  "version": "1.0.0"
}
```

**Status Codes:**
- `200 OK`: Application is healthy
- `503 Service Unavailable`: Application is unhealthy

**Example:**
```bash
curl http://localhost:8000/health
```

#### GET /health/db

Check database connectivity.

**Tag:** `health`

**Response:**
```json
{
  "database": "connected",
  "timestamp": "2026-01-01T12:00:00Z"
}
```

**Status Codes:**
- `200 OK`: Database is connected
- `503 Service Unavailable`: Database connection failed

**Example:**
```bash
curl http://localhost:8000/health/db
```

---

### Authentication Endpoints

#### POST /auth/login

Authenticate user and obtain JWT token.

**Tag:** `auth`

**Request Body** (form-urlencoded):
```
username=string (required)
password=string (required)
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Status Codes:**
- `200 OK`: Login successful
- `401 Unauthorized`: Invalid credentials

**Example:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=secret123"
```

**Note**: In demo mode, users are automatically created if they don't exist.

#### GET /auth/me

Get current authenticated user information.

**Tag:** `auth`

**Authentication:** Required (Bearer token)

**Response:**
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "john",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2026-01-01T10:00:00Z"
}
```

**Status Codes:**
- `200 OK`: User information retrieved
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

---

### User Management Endpoints

#### GET /users

List all users (paginated).

**Tag:** `users`

**Authentication:** Required

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum number of records to return (default: 100, max: 100)

**Response:**
```json
[
  {
    "id": 1,
    "email": "john@example.com",
    "username": "john",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2026-01-01T10:00:00Z"
  },
  {
    "id": 2,
    "email": "jane@example.com",
    "username": "jane",
    "full_name": "Jane Smith",
    "is_active": true,
    "created_at": "2026-01-01T11:00:00Z"
  }
]
```

**Status Codes:**
- `200 OK`: Users retrieved successfully
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
curl -X GET "http://localhost:8000/users?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

#### GET /users/{user_id}

Get a specific user by ID.

**Tag:** `users`

**Authentication:** Required

**Path Parameters:**
- `user_id` (integer, required): The user ID

**Response:**
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "john",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2026-01-01T10:00:00Z"
}
```

**Status Codes:**
- `200 OK`: User found
- `404 Not Found`: User does not exist
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
curl -X GET "http://localhost:8000/users/1" \
  -H "Authorization: Bearer $TOKEN"
```

#### POST /users

Create a new user.

**Tag:** `users`

**Authentication:** Required

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "username": "newuser",
  "full_name": "New User",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": 3,
  "email": "newuser@example.com",
  "username": "newuser",
  "full_name": "New User",
  "is_active": true,
  "created_at": "2026-01-01T12:00:00Z"
}
```

**Status Codes:**
- `201 Created`: User created successfully
- `400 Bad Request`: Invalid input data
- `409 Conflict`: User with email/username already exists
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
curl -X POST "http://localhost:8000/users" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "username": "newuser",
    "full_name": "New User",
    "password": "securepassword123"
  }'
```

#### PUT /users/{user_id}

Update an existing user.

**Tag:** `users`

**Authentication:** Required

**Path Parameters:**
- `user_id` (integer, required): The user ID

**Request Body:**
```json
{
  "email": "updated@example.com",
  "full_name": "Updated Name",
  "is_active": true
}
```

**Response:**
```json
{
  "id": 1,
  "email": "updated@example.com",
  "username": "john",
  "full_name": "Updated Name",
  "is_active": true,
  "created_at": "2026-01-01T10:00:00Z",
  "updated_at": "2026-01-01T12:30:00Z"
}
```

**Status Codes:**
- `200 OK`: User updated successfully
- `404 Not Found`: User does not exist
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
curl -X PUT "http://localhost:8000/users/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "updated@example.com",
    "full_name": "Updated Name"
  }'
```

#### DELETE /users/{user_id}

Delete a user.

**Tag:** `users`

**Authentication:** Required

**Path Parameters:**
- `user_id` (integer, required): The user ID

**Response:**
```json
{
  "message": "User deleted successfully",
  "user_id": 1
}
```

**Status Codes:**
- `200 OK`: User deleted successfully
- `404 Not Found`: User does not exist
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
curl -X DELETE "http://localhost:8000/users/1" \
  -H "Authorization: Bearer $TOKEN"
```

---

### Metrics Endpoint

#### GET /metrics

Prometheus metrics endpoint for monitoring.

**Tag:** `metrics`

**Authentication:** Not required

**Response Format:** Prometheus text format

**Response Example:**
```
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/health",status="200"} 1234.0

# HELP http_request_duration_seconds HTTP request latency
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{le="0.005"} 100.0
http_request_duration_seconds_bucket{le="0.01"} 200.0
...
```

**Example:**
```bash
curl http://localhost:8000/metrics
```

## Error Handling

### Error Response Format

All errors return a consistent JSON structure:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (e.g., duplicate username)
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service temporarily unavailable

### Validation Errors

Validation errors (422) return detailed field-level errors:

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

### Example Error Handling

```python
import requests

response = requests.post(
    "http://localhost:8000/users",
    json={"email": "invalid-email"},
    headers={"Authorization": f"Bearer {token}"}
)

if response.status_code == 422:
    errors = response.json()["detail"]
    for error in errors:
        print(f"Field: {error['loc']}, Error: {error['msg']}")
elif response.status_code == 401:
    print("Authentication required")
elif response.status_code == 409:
    print("User already exists")
else:
    user = response.json()
    print(f"User created: {user['id']}")
```

## Rate Limiting

**Current Status**: Not implemented (future enhancement)

**Planned Implementation:**
- Rate limit: 100 requests per minute per IP
- Authenticated users: 1000 requests per minute
- Rate limit headers will be included in responses:
  - `X-RateLimit-Limit`: Total requests allowed
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Time when limit resets

## Examples

### Complete Authentication Workflow

```bash
#!/bin/bash

# 1. Login
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=secret")

# Extract token
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')

# 2. Get current user info
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer $TOKEN"

# 3. List all users
curl -X GET "http://localhost:8000/users?limit=10" \
  -H "Authorization: Bearer $TOKEN"

# 4. Create a new user
curl -X POST "http://localhost:8000/users" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "username": "alice",
    "full_name": "Alice Johnson",
    "password": "securepass123"
  }'
```

### Python Client Example

```python
import requests
from typing import Optional

class HexaHubClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token: Optional[str] = None

    def login(self, username: str, password: str) -> bool:
        """Authenticate and store token."""
        response = requests.post(
            f"{self.base_url}/auth/login",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            return True
        return False

    def _headers(self) -> dict:
        """Get headers with auth token."""
        if not self.token:
            raise ValueError("Not authenticated. Call login() first.")
        return {"Authorization": f"Bearer {self.token}"}

    def get_users(self, skip: int = 0, limit: int = 100) -> list:
        """Get list of users."""
        response = requests.get(
            f"{self.base_url}/users",
            params={"skip": skip, "limit": limit},
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def create_user(self, email: str, username: str,
                   full_name: str, password: str) -> dict:
        """Create a new user."""
        response = requests.post(
            f"{self.base_url}/users",
            json={
                "email": email,
                "username": username,
                "full_name": full_name,
                "password": password
            },
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

# Usage
client = HexaHubClient()
client.login("john", "secret")
users = client.get_users(limit=10)
print(f"Found {len(users)} users")
```

### JavaScript (Node.js) Client Example

```javascript
const axios = require('axios');

class HexaHubClient {
  constructor(baseURL = 'http://localhost:8000') {
    this.client = axios.create({ baseURL });
    this.token = null;
  }

  async login(username, password) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    const response = await this.client.post('/auth/login', params);
    this.token = response.data.access_token;

    // Set default authorization header
    this.client.defaults.headers.common['Authorization'] =
      `Bearer ${this.token}`;
  }

  async getUsers(skip = 0, limit = 100) {
    const response = await this.client.get('/users', {
      params: { skip, limit }
    });
    return response.data;
  }

  async createUser(userData) {
    const response = await this.client.post('/users', userData);
    return response.data;
  }
}

// Usage
(async () => {
  const client = new HexaHubClient();
  await client.login('john', 'secret');

  const users = await client.getUsers(0, 10);
  console.log(`Found ${users.length} users`);

  const newUser = await client.createUser({
    email: 'bob@example.com',
    username: 'bob',
    full_name: 'Bob Wilson',
    password: 'securepass123'
  });
  console.log(`Created user: ${newUser.id}`);
})();
```

## SDKs and Client Libraries

### Official SDKs
- Python SDK: Coming soon
- JavaScript/TypeScript SDK: Coming soon
- Go SDK: Coming soon

### Community Libraries
Contributions welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md)

### OpenAPI Generator

Generate client libraries for any language using the OpenAPI spec:

```bash
# Download OpenAPI spec
curl http://localhost:8000/openapi.json > openapi.json

# Generate Python client
openapi-generator-cli generate \
  -i openapi.json \
  -g python \
  -o ./python-client

# Generate TypeScript client
openapi-generator-cli generate \
  -i openapi.json \
  -g typescript-axios \
  -o ./typescript-client
```

## Best Practices

### Security
1. **Always use HTTPS** in production
2. **Store tokens securely** (httpOnly cookies for web apps)
3. **Implement token refresh** before expiration
4. **Validate all inputs** on client side before sending
5. **Handle errors gracefully** without exposing sensitive information

### Performance
1. **Use pagination** for large datasets
2. **Cache responses** when appropriate
3. **Implement retry logic** with exponential backoff
4. **Use connection pooling** for HTTP clients
5. **Monitor API usage** with metrics endpoint

### Error Handling
1. **Check HTTP status codes** before processing responses
2. **Parse error messages** for user-friendly display
3. **Log errors** for debugging
4. **Implement fallback behavior** for critical operations

## Support and Contributing

- **Bug Reports**: Open an issue on GitHub
- **Feature Requests**: Open an issue with the `enhancement` label
- **Documentation**: Pull requests welcome
- **Questions**: Use GitHub Discussions

## Changelog

See [CHANGELOG.md](../CHANGELOG.md) for version history and updates.

## License

MIT License - see [LICENSE](../LICENSE) for details
