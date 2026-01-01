#!/bin/bash
# Manual deployment script for HexaHub Backend
# Usage: ./scripts/deploy.sh [staging|production]

set -e

ENVIRONMENT=${1:-staging}
STAGING_HOST="rtx1080.local"
STAGING_USER="fitna"

echo "🚀 Deploying HexaHub Backend to $ENVIRONMENT..."

if [ "$ENVIRONMENT" = "staging" ]; then
    echo "📦 Syncing files to staging server..."
    rsync -avz --delete \
        --exclude '.git' \
        --exclude '.env' \
        --exclude 'venv' \
        --exclude '__pycache__' \
        --exclude '*.pyc' \
        --exclude 'test.db' \
        ./ \
        ${STAGING_USER}@${STAGING_HOST}:~/hexahub-backend/

    echo "🔧 Deploying with Docker Compose..."
    ssh ${STAGING_USER}@${STAGING_HOST} << 'ENDSSH'
        cd ~/hexahub-backend

        # Create .env if not exists
        if [ ! -f .env ]; then
            cp .env.example .env
            echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
        fi

        # Create backup
        BACKUP_DIR=~/hexahub-backup-$(date +%Y%m%d-%H%M%S)
        if [ -d ~/hexahub-backend ]; then
            echo "Creating backup at $BACKUP_DIR"
            cp -r ~/hexahub-backend $BACKUP_DIR
        fi

        # Deploy
        docker compose pull
        docker compose up -d --remove-orphans

        # Wait for health
        echo "⏳ Waiting for services to be healthy..."
        timeout 60 bash -c 'until docker compose exec postgres pg_isready -U hexahub; do sleep 2; done'

        # Health check
        sleep 5
        if curl -f http://localhost:8000/health > /dev/null 2>&1; then
            echo "✅ Deployment successful! Backend is healthy."
            docker compose ps
        else
            echo "❌ Health check failed! Rolling back..."
            docker compose down
            exit 1
        fi
ENDSSH

    echo "✅ Deployment to staging complete!"
    echo "🔗 API: http://${STAGING_HOST}:8000"
    echo "📖 Docs: http://${STAGING_HOST}:8000/docs"

elif [ "$ENVIRONMENT" = "production" ]; then
    echo "⚠️  Production deployment not yet implemented"
    echo "TODO: Implement K3s deployment"
    exit 1
else
    echo "❌ Invalid environment: $ENVIRONMENT"
    echo "Usage: ./scripts/deploy.sh [staging|production]"
    exit 1
fi
