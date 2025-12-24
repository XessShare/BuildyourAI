# Webhook Handler Setup Guide

## 🎯 Overview

WebhookHandlerAgent empfängt GitHub Webhooks und triggert automatische Deployments via DeploymentOrchestratorAgent.

## 🚀 Quick Start

### 1. Setup Webhook Secret

```bash
# Generate webhook secret
openssl rand -hex 32

# Add to .env
echo "GITHUB_WEBHOOK_SECRET=<your-secret>" >> .env
```

### 2. Start Webhook Server

```bash
cd /home/fitna/homelab/ai-platform/1-first-agent
source ../ai-agents-masterclass/bin/activate

# Start server
python -m agents.webhook_handler

# Or with custom port
WEBHOOK_PORT=8000 python -m agents.webhook_handler
```

### 3. Configure GitHub Webhook

**In your GitHub repository:**
1. Go to Settings → Webhooks → Add webhook
2. **Payload URL**: `https://your-vps.com:8000/webhook/github`
3. **Content type**: `application/json`
4. **Secret**: `<your-webhook-secret>`
5. **Events**: Select "Just the push event"
6. **Active**: ✅ Checked

### 4. Configure GitHub Actions Secrets

**Required secrets:**
```bash
VPS_WEBHOOK_URL=https://your-vps.com:8000/webhook/deploy
DEPLOY_TOKEN=<your-deploy-token>
HEALTH_CHECK_URL=https://your-service.com/health  # Optional
```

## 📋 Endpoints

### `GET /`
Health check endpoint

**Response:**
```json
{
  "service": "J-Jeco Webhook Handler",
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-12-24T23:45:00"
}
```

### `GET /health`
Detailed health check

**Response:**
```json
{
  "status": "healthy",
  "agent_type": "webhook_handler",
  "metrics": {
    "tasks_completed": 42,
    "tokens_used": 1337,
    "errors": 0
  },
  "rate_limiter": {
    "max_requests": 10,
    "time_window": 60
  }
}
```

### `POST /webhook/github`
GitHub webhook endpoint

**Headers:**
- `X-GitHub-Event`: Event type (push, pull_request, etc.)
- `X-Hub-Signature-256`: HMAC signature

**Payload:** GitHub webhook payload

**Response:**
```json
{
  "accepted": true,
  "event": "push",
  "action": "deployment_triggered",
  "deployment_triggered": true,
  "commit_hash": "abc123",
  "branch": "main",
  "timestamp": "2024-12-24T23:45:00"
}
```

### `POST /webhook/deploy`
Direct deployment trigger (for testing/manual triggers)

**Payload:**
```json
{
  "commit_hash": "main",
  "environment": "staging",
  "rollback_on_failure": true
}
```

**Response:**
```json
{
  "success": true,
  "status": "success",
  "duration": 120,
  "systems_deployed": ["thinkpad", "rtx1080", "vps"],
  "error": null
}
```

## 🔐 Security Features

### 1. Signature Verification
All GitHub webhooks are verified using HMAC-SHA256:

```python
webhook_secret = "your-secret-here"
agent = WebhookHandlerAgent(webhook_secret=webhook_secret)
```

### 2. Rate Limiting
Default: 10 requests per minute per repository

```python
# Configure rate limiter
agent.rate_limiter.max_requests = 20
agent.rate_limiter.time_window = 60  # seconds
```

### 3. Event Filtering
Only processes relevant events (push to main/master by default)

## 🧪 Testing

### Local Testing

```bash
# Terminal 1: Start webhook server
python -m agents.webhook_handler

# Terminal 2: Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/health

# Test deployment trigger
curl -X POST http://localhost:8000/webhook/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "commit_hash": "main",
    "environment": "staging",
    "rollback_on_failure": true
  }'
```

### GitHub Webhook Testing

```bash
# Simulate GitHub webhook
curl -X POST http://localhost:8000/webhook/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: push" \
  -H "X-Hub-Signature-256: sha256=..." \
  -d @github-webhook-payload.json
```

## 🔄 Deployment Workflow

```
GitHub Push (main)
       ↓
GitHub Webhook → VPS:8000/webhook/github
       ↓
Signature Verification
       ↓
Rate Limit Check
       ↓
Event Filtering (only main/master)
       ↓
DeploymentOrchestratorAgent.execute()
       ↓
    [8-Phase Deployment]
       ↓
Response to GitHub
```

## 📊 Monitoring

### Logs

```bash
# Webhook handler logs
tail -f logs/webhook_handler.log

# Deployment logs
tail -f logs/deployment_orchestrator.log
```

### Metrics

```python
# Get agent metrics
agent = WebhookHandlerAgent()
metrics = agent.get_metrics()

print(f"Tasks: {metrics['tasks_completed']}")
print(f"Errors: {metrics['errors']}")
print(f"Uptime: {metrics['uptime']}s")
```

## 🚨 Troubleshooting

### Webhook not triggering

1. **Check GitHub webhook deliveries**
   - GitHub → Settings → Webhooks → Recent Deliveries

2. **Check signature**
   ```bash
   # Verify GITHUB_WEBHOOK_SECRET is set correctly
   echo $GITHUB_WEBHOOK_SECRET
   ```

3. **Check server logs**
   ```bash
   tail -f logs/webhook_handler.log
   ```

### Rate limit errors

```bash
# Increase rate limit
export WEBHOOK_RATE_LIMIT=20
python -m agents.webhook_handler
```

### Deployment failures

```bash
# Check deployment logs
tail -f logs/deployment_orchestrator.log

# Manual deployment test
curl -X POST http://localhost:8000/webhook/deploy \
  -H "Content-Type: application/json" \
  -d '{"commit_hash": "HEAD", "environment": "staging"}'
```

## 🎛️ Configuration

### Environment Variables

```bash
# .env file
GITHUB_WEBHOOK_SECRET=your-secret-here
WEBHOOK_PORT=8000
WEBHOOK_RATE_LIMIT=10
WEBHOOK_TIME_WINDOW=60

# Deployment settings
DEFAULT_ENVIRONMENT=staging
ROLLBACK_ON_FAILURE=true
```

### Programmatic Configuration

```python
from agents.webhook_handler import WebhookHandlerAgent

agent = WebhookHandlerAgent(
    webhook_secret="your-secret",
    port=8000
)

# Configure rate limiter
agent.rate_limiter.max_requests = 20
agent.rate_limiter.time_window = 60

# Start server
agent.run_server()
```

## 🔮 Advanced Usage

### Custom Event Handlers

```python
class CustomWebhookHandler(WebhookHandlerAgent):
    async def _handle_webhook(self, event_type, payload):
        if event_type == "pull_request":
            # Custom PR handling
            return await self._handle_pr(payload)

        return await super()._handle_webhook(event_type, payload)

    async def _handle_pr(self, payload):
        # Deploy to preview environment
        # ...
        pass
```

### Multi-Branch Deployments

```python
async def _handle_webhook(self, event_type, payload):
    if event_type == "push":
        branch = payload.get("ref", "").replace("refs/heads/", "")

        environment_map = {
            "main": "production",
            "staging": "staging",
            "dev": "development"
        }

        environment = environment_map.get(branch)
        if environment:
            await self._trigger_deployment(
                commit_hash=payload.get("after"),
                environment=environment
            )
```

## 📚 Integration Examples

### With GitHub Actions

See `.github/workflows/deploy.yml` for complete example.

### With Monitoring

```python
# Add Prometheus metrics
from prometheus_client import Counter, Histogram

webhook_requests = Counter('webhook_requests_total', 'Total webhook requests')
deployment_duration = Histogram('deployment_duration_seconds', 'Deployment duration')

# In webhook handler
webhook_requests.inc()
```

---

**Version:** 1.0
**Created:** 2024-12-24
**Status:** ✅ Production Ready
