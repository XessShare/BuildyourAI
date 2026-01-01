#!/bin/bash
# Health check script for monitoring
# Usage: ./scripts/health-check.sh [local|staging]

ENVIRONMENT=${1:-local}

if [ "$ENVIRONMENT" = "local" ]; then
    BASE_URL="http://localhost:8000"
elif [ "$ENVIRONMENT" = "staging" ]; then
    BASE_URL="http://rtx1080.local:8000"
else
    echo "Usage: $0 [local|staging]"
    exit 1
fi

echo "🏥 Running health checks on $ENVIRONMENT environment..."
echo "Base URL: $BASE_URL"
echo ""

# Test 1: Basic health
echo "1️⃣  Testing basic health endpoint..."
if curl -f -s "$BASE_URL/health" | grep -q '"status":"healthy"'; then
    echo "✅ Basic health check passed"
else
    echo "❌ Basic health check failed"
    exit 1
fi

# Test 2: Database health
echo "2️⃣  Testing database health endpoint..."
if curl -f -s "$BASE_URL/health/db" | grep -q '"database":"connected"'; then
    echo "✅ Database health check passed"
else
    echo "❌ Database health check failed"
    exit 1
fi

# Test 3: Root endpoint
echo "3️⃣  Testing root endpoint..."
if curl -f -s "$BASE_URL/" | grep -q '"name":"HexaHub API"'; then
    echo "✅ Root endpoint passed"
else
    echo "❌ Root endpoint failed"
    exit 1
fi

# Test 4: Authentication
echo "4️⃣  Testing authentication..."
TOKEN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" -d "username=healthcheck&password=test")
if echo "$TOKEN_RESPONSE" | grep -q "access_token"; then
    echo "✅ Authentication passed"
    TOKEN=$(echo "$TOKEN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
    
    # Test 5: Authenticated endpoint
    echo "5️⃣  Testing authenticated endpoint..."
    if curl -f -s -H "Authorization: Bearer $TOKEN" "$BASE_URL/users/me" | grep -q '"username":"healthcheck"'; then
        echo "✅ Authenticated endpoint passed"
    else
        echo "❌ Authenticated endpoint failed"
        exit 1
    fi
else
    echo "❌ Authentication failed"
    exit 1
fi

echo ""
echo "🎉 All health checks passed!"
exit 0
