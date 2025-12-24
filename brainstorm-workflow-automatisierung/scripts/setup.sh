#!/bin/bash

# Setup script for Brainstorm Workflow Automation Repository

set -e

echo "🚀 Setting up Brainstorm Workflow Automation Repository..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# GitHub Configuration
GITHUB_TOKEN=your_github_token_here

# GitLab Configuration
GITLAB_TOKEN=your_gitlab_token_here
GITLAB_PROJECT_ID=your_project_id_here

# Slack Configuration (optional)
SLACK_WEBHOOK_URL=your_slack_webhook_url_here
EOF
    echo "✅ .env file created. Please update it with your credentials."
fi

# Start n8n
echo "🐳 Starting n8n..."
cd poc/n8n
docker-compose up -d
echo "✅ n8n started. Access it at http://localhost:5678"

# Check Python for Prefect
if command -v python3 &> /dev/null; then
    echo "🐍 Python found. Setting up Prefect..."
    cd ../prefect
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    source venv/bin/activate
    pip install -r requirements.txt
    echo "✅ Prefect setup complete."
else
    echo "⚠️  Python not found. Skipping Prefect setup."
fi

echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "1. Update .env file with your credentials"
echo "2. Access n8n at http://localhost:5678 (admin/admin)"
echo "3. Import workflows from poc/n8n/workflows/"
echo "4. Run Prefect flows from poc/prefect/flows/"

