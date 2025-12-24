"""
Webhook Handler Agent für GitHub Integration
Empfängt GitHub Webhooks und triggert DeploymentOrchestratorAgent

Features:
- GitHub Webhook Signature Verification
- Rate Limiting
- Event Filtering (push, pull_request, etc.)
- DeploymentAgent Integration
- Logging & Monitoring
"""

import asyncio
import hmac
import hashlib
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse
import uvicorn

from .base_agent import BaseAgent
from .deployment_orchestrator import DeploymentOrchestratorAgent

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import AGENT_CONFIG


class RateLimiter:
    """Simple in-memory rate limiter"""

    def __init__(self, max_requests: int = 10, time_window: int = 60):
        """
        Args:
            max_requests: Maximum requests per time window
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = defaultdict(list)

    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed"""
        now = time.time()
        cutoff = now - self.time_window

        # Remove old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > cutoff
        ]

        # Check limit
        if len(self.requests[identifier]) >= self.max_requests:
            return False

        # Add current request
        self.requests[identifier].append(now)
        return True

    def get_remaining(self, identifier: str) -> int:
        """Get remaining requests"""
        now = time.time()
        cutoff = now - self.time_window

        recent = [
            req_time for req_time in self.requests[identifier]
            if req_time > cutoff
        ]

        return max(0, self.max_requests - len(recent))


class WebhookHandlerAgent(BaseAgent):
    """
    Handles GitHub Webhooks and triggers deployments

    Workflow:
    1. Receive GitHub webhook
    2. Verify signature
    3. Filter events (push to main/master)
    4. Rate limit check
    5. Trigger DeploymentOrchestratorAgent
    6. Return status
    """

    def __init__(self, webhook_secret: Optional[str] = None, port: int = 8000):
        """
        Initialize Webhook Handler

        Args:
            webhook_secret: GitHub webhook secret for signature verification
            port: Port to run webhook server on
        """
        super().__init__("webhook_handler")

        self.webhook_secret = webhook_secret or ""
        self.port = port

        # Rate limiting
        self.rate_limiter = RateLimiter(
            max_requests=10,  # 10 requests
            time_window=60    # per minute
        )

        # Deployment agent
        self.deployment_agent = None  # Lazy initialization

        # FastAPI app
        self.app = FastAPI(
            title="J-Jeco Webhook Handler",
            description="GitHub Webhook → Deployment Pipeline",
            version="1.0.0"
        )

        self._setup_routes()

        self.logger.info(f"WebhookHandlerAgent initialized on port {port}")

    def _setup_routes(self):
        """Setup FastAPI routes"""

        @self.app.get("/")
        async def root():
            """Health check endpoint"""
            return {
                "service": "J-Jeco Webhook Handler",
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": datetime.now().isoformat()
            }

        @self.app.get("/health")
        async def health():
            """Detailed health check"""
            return {
                "status": "healthy",
                "agent_type": self.agent_type,
                "metrics": self.get_metrics(),
                "rate_limiter": {
                    "max_requests": self.rate_limiter.max_requests,
                    "time_window": self.rate_limiter.time_window
                }
            }

        @self.app.post("/webhook/github")
        async def github_webhook(
            request: Request,
            x_github_event: str = Header(None),
            x_hub_signature_256: str = Header(None)
        ):
            """
            GitHub webhook endpoint

            Headers required:
            - X-GitHub-Event: Event type (push, pull_request, etc.)
            - X-Hub-Signature-256: HMAC signature for verification
            """
            try:
                # Get payload
                payload = await request.body()
                payload_json = await request.json()

                # Rate limiting
                repo_name = payload_json.get("repository", {}).get("full_name", "unknown")
                if not self.rate_limiter.is_allowed(repo_name):
                    raise HTTPException(
                        status_code=429,
                        detail=f"Rate limit exceeded. Try again in {self.rate_limiter.time_window}s"
                    )

                # Verify signature
                if self.webhook_secret and not self._verify_signature(payload, x_hub_signature_256):
                    self.logger.warning(f"Invalid signature for webhook from {repo_name}")
                    raise HTTPException(status_code=401, detail="Invalid signature")

                # Handle webhook
                result = await self._handle_webhook(
                    event_type=x_github_event,
                    payload=payload_json
                )

                return JSONResponse(
                    status_code=200 if result["accepted"] else 202,
                    content=result
                )

            except HTTPException:
                raise
            except Exception as e:
                self.logger.error(f"Webhook handling error: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/webhook/deploy")
        async def deploy_webhook(request: Request):
            """
            Direct deployment trigger endpoint (for testing)

            Payload:
            {
                "commit_hash": "main",
                "environment": "staging",
                "rollback_on_failure": true
            }
            """
            try:
                payload = await request.json()

                # Trigger deployment
                result = await self._trigger_deployment(
                    commit_hash=payload.get("commit_hash", "HEAD"),
                    environment=payload.get("environment", "staging"),
                    rollback_on_failure=payload.get("rollback_on_failure", True)
                )

                return JSONResponse(
                    status_code=200,
                    content=result
                )

            except Exception as e:
                self.logger.error(f"Deployment trigger error: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

    def _verify_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify GitHub webhook signature

        Args:
            payload: Raw request body
            signature: X-Hub-Signature-256 header value

        Returns:
            True if signature is valid
        """
        if not signature:
            return False

        # Extract signature (format: "sha256=<hash>")
        if not signature.startswith("sha256="):
            return False

        expected_signature = signature.split("=")[1]

        # Compute HMAC
        mac = hmac.new(
            self.webhook_secret.encode(),
            msg=payload,
            digestmod=hashlib.sha256
        )
        computed_signature = mac.hexdigest()

        # Constant-time comparison
        return hmac.compare_digest(computed_signature, expected_signature)

    async def _handle_webhook(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle GitHub webhook event

        Args:
            event_type: GitHub event type (push, pull_request, etc.)
            payload: Webhook payload

        Returns:
            {
                "accepted": bool,
                "event": str,
                "action": str,
                "deployment_triggered": bool
            }
        """
        self.logger.info(f"Received webhook: {event_type}")

        result = {
            "accepted": False,
            "event": event_type,
            "action": "ignored",
            "deployment_triggered": False,
            "timestamp": datetime.now().isoformat()
        }

        # Handle push events
        if event_type == "push":
            ref = payload.get("ref", "")
            branch = ref.replace("refs/heads/", "")

            # Only deploy on main/master
            if branch in ["main", "master"]:
                commit_hash = payload.get("after", "HEAD")
                repo_name = payload.get("repository", {}).get("full_name", "unknown")

                self.logger.info(f"Triggering deployment for {repo_name}@{commit_hash}")

                # Trigger deployment (async, don't block webhook response)
                asyncio.create_task(self._trigger_deployment(
                    commit_hash=commit_hash,
                    environment="staging",  # Always staging first
                    rollback_on_failure=True
                ))

                result.update({
                    "accepted": True,
                    "action": "deployment_triggered",
                    "deployment_triggered": True,
                    "commit_hash": commit_hash,
                    "branch": branch
                })

            else:
                result["action"] = f"ignored_branch_{branch}"

        # Handle pull_request events
        elif event_type == "pull_request":
            action = payload.get("action", "")

            if action == "opened" or action == "synchronize":
                # Could trigger preview deployments here
                result["action"] = f"pr_{action}"

        # Log metrics
        self.metrics["tasks_completed"] += 1

        return result

    async def _trigger_deployment(
        self,
        commit_hash: str,
        environment: str = "staging",
        rollback_on_failure: bool = True
    ) -> Dict[str, Any]:
        """
        Trigger deployment via DeploymentOrchestratorAgent

        Args:
            commit_hash: Git commit hash to deploy
            environment: Target environment (staging/production)
            rollback_on_failure: Rollback on failure

        Returns:
            Deployment result
        """
        try:
            # Lazy initialize deployment agent
            if self.deployment_agent is None:
                self.deployment_agent = DeploymentOrchestratorAgent()

            # Execute deployment
            result = await self.deployment_agent.execute({
                "commit_hash": commit_hash,
                "environment": environment,
                "rollback_on_failure": rollback_on_failure,
                "skip_tests": False
            })

            self.logger.info(f"Deployment completed: {result['status']}")

            return {
                "success": result["status"] in ["success", "partial_success"],
                "status": result["status"],
                "duration": result["duration_seconds"],
                "systems_deployed": result["systems_deployed"],
                "error": result.get("error")
            }

        except Exception as e:
            self.logger.error(f"Deployment failed: {str(e)}")
            return {
                "success": False,
                "status": "error",
                "error": str(e)
            }

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute webhook handler task (not used for webhook server)

        This is here for BaseAgent compatibility.
        The actual webhook handling is done via FastAPI routes.
        """
        action = task.get("action", "unknown")

        if action == "start_server":
            return await self.start_server()
        elif action == "trigger_deployment":
            return await self._trigger_deployment(
                commit_hash=task.get("commit_hash", "HEAD"),
                environment=task.get("environment", "staging")
            )
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}"
            }

    async def start_server(self):
        """Start the webhook server"""
        self.logger.info(f"Starting webhook server on port {self.port}")

        config = uvicorn.Config(
            self.app,
            host="0.0.0.0",
            port=self.port,
            log_level="info"
        )
        server = uvicorn.Server(config)

        try:
            await server.serve()
            return {
                "success": True,
                "port": self.port
            }
        except Exception as e:
            self.logger.error(f"Server error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def run_server(self):
        """Run webhook server (blocking)"""
        uvicorn.run(
            self.app,
            host="0.0.0.0",
            port=self.port,
            log_level="info"
        )


# CLI for running webhook server
if __name__ == "__main__":
    import sys
    import os

    # Get webhook secret from environment
    webhook_secret = os.getenv("GITHUB_WEBHOOK_SECRET", "")

    if not webhook_secret:
        print("⚠️  Warning: GITHUB_WEBHOOK_SECRET not set. Signature verification disabled.")

    port = int(os.getenv("WEBHOOK_PORT", "8000"))

    agent = WebhookHandlerAgent(webhook_secret=webhook_secret, port=port)

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║     J-Jeco Webhook Handler                                ║
║     GitHub → Deployment Pipeline                          ║
╚═══════════════════════════════════════════════════════════╝

Port: {port}
Signature Verification: {'✅ Enabled' if webhook_secret else '❌ Disabled'}

Endpoints:
  GET  /              - Health check
  GET  /health        - Detailed health
  POST /webhook/github - GitHub webhooks
  POST /webhook/deploy - Direct deployment trigger

Starting server...
    """)

    agent.run_server()
