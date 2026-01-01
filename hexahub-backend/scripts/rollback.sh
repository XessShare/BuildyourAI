#!/bin/bash
# Rollback script for HexaHub Backend
# Usage: ./scripts/rollback.sh

set -e

STAGING_HOST="rtx1080.local"
STAGING_USER="fitna"

echo "🔄 Rolling back HexaHub Backend deployment..."

ssh ${STAGING_USER}@${STAGING_HOST} << 'ENDSSH'
    # Find most recent backup
    LATEST_BACKUP=$(ls -dt ~/hexahub-backup-* 2>/dev/null | head -1)

    if [ -z "$LATEST_BACKUP" ]; then
        echo "❌ No backup found to rollback to!"
        exit 1
    fi

    echo "📦 Rolling back to: $LATEST_BACKUP"

    # Stop current deployment
    cd ~/hexahub-backend
    docker compose down

    # Restore backup
    rm -rf ~/hexahub-backend
    cp -r "$LATEST_BACKUP" ~/hexahub-backend

    # Start services
    cd ~/hexahub-backend
    docker compose up -d

    # Health check
    echo "⏳ Waiting for services..."
    sleep 5

    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Rollback successful! Backend is healthy."
        docker compose ps
    else
        echo "❌ Rollback health check failed!"
        exit 1
    fi
ENDSSH

echo "✅ Rollback complete!"
