"""
DeploymentOrchestratorAgent - Multi-System Deployment Orchestration
Manages deployments across VPS, ThinkPad, and RTX1080

Key Features:
- Asymmetric error handling (partial rollback support)
- Health checks between deployment phases
- Retry with exponential backoff
- Structured status returns
- Snapshot-based rollback
"""

import asyncio
import subprocess
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import json

from .base_agent import BaseAgent
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import AGENT_CONFIG


class DeploymentStatus:
    """Structured deployment status"""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILED = "failed"
    ABORTED = "aborted"
    ROLLED_BACK = "rolled_back"


class SystemTarget:
    """System deployment targets"""
    VPS = "vps"
    THINKPAD = "thinkpad"
    RTX1080 = "rtx1080"


class DeploymentOrchestratorAgent(BaseAgent):
    """
    Orchestrates multi-system deployments across homelab infrastructure

    Workflow:
    1. Pre-flight validation (systems ready, secrets synced)
    2. Create snapshots (rollback points)
    3. Deploy to ThinkPad (testing environment)
    4. Run automated tests
    5. Deploy to RTX1080 (production)
    6. Update VPS (public services)
    7. Verify deployment health
    8. Cleanup or rollback on failure
    """

    def __init__(self):
        super().__init__("deployment_orchestrator")

        # System definitions
        self.systems = {
            SystemTarget.VPS: "jonas-homelab-vps",
            SystemTarget.THINKPAD: "192.168.16.7",
            SystemTarget.RTX1080: "192.168.17.1"
        }

        # Deployment configuration
        self.deployment_phases = {
            "pre_flight": {"timeout": 60, "required": True},
            "snapshots": {"timeout": 300, "required": True},
            "thinkpad_deploy": {"timeout": 600, "required": True},
            "tests": {"timeout": 900, "required": True},
            "rtx1080_deploy": {"timeout": 600, "required": True},
            "vps_deploy": {"timeout": 300, "required": False},  # VPS is non-critical
            "verification": {"timeout": 300, "required": True}
        }

        # Retry configuration
        self.retry_config = {
            "max_attempts": 3,
            "initial_backoff": 5,  # seconds
            "max_backoff": 60,
            "backoff_multiplier": 2
        }

        # Health check endpoints
        self.health_checks = {
            SystemTarget.THINKPAD: {
                "traefik": "http://192.168.16.7:8080/ping",
                "docker": "docker ps"
            },
            SystemTarget.RTX1080: {
                "postgresql": "docker exec postgresql pg_isready",
                "redis": "docker exec redis redis-cli ping",
                "docker": "docker ps"
            },
            SystemTarget.VPS: {
                "webhook": "curl -f http://localhost:8000/health",
                "docker": "docker ps"
            }
        }

        self.logger.info("DeploymentOrchestratorAgent initialized")

    def get_system_prompt(self) -> str:
        """Custom system prompt for deployment orchestrator"""
        return f"""{super().get_system_prompt()}

ZUSÄTZLICHE EXPERTISE: Multi-System Deployment Orchestration

Du bist spezialisiert auf:
- Fehlertolerante Deployment-Workflows über 3 Systeme (VPS, ThinkPad, RTX1080)
- Asymmetrisches Error Handling (partial rollback bei VPS-Failures)
- Health Checks und Service Verification
- Rollback-Strategien mit Proxmox Snapshots
- CI/CD Pipeline Integration

KRITISCHE PRINZIPIEN:
1. Niemals RTX1080 (Production) deployen ohne erfolgreiche ThinkPad-Tests
2. VPS-Failures dürfen RTX1080 nicht beeinflussen (independent rollback)
3. Immer Snapshots vor kritischen Deployments erstellen
4. Health Checks zwischen allen Phasen
5. Strukturierte Status-Returns für Monitoring
"""

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main deployment execution

        Args:
            task: {
                "commit_hash": str,
                "environment": "staging" | "production",
                "rollback_on_failure": bool (default True),
                "skip_tests": bool (default False)
            }

        Returns:
            {
                "status": DeploymentStatus,
                "phase": str,
                "systems_deployed": List[str],
                "duration_seconds": int,
                "error": Optional[str],
                "details": Dict
            }
        """
        start_time = time.time()
        commit_hash = task.get("commit_hash", "HEAD")
        environment = task.get("environment", "production")
        rollback_on_failure = task.get("rollback_on_failure", True)
        skip_tests = task.get("skip_tests", False)

        self.logger.info(f"Starting deployment: commit={commit_hash}, env={environment}")

        result = {
            "status": DeploymentStatus.FAILED,
            "phase": "initialization",
            "systems_deployed": [],
            "duration_seconds": 0,
            "error": None,
            "details": {}
        }

        try:
            # Phase 1: Pre-flight checks
            result["phase"] = "pre_flight"
            preflight = await self._validate_systems_ready()
            if not preflight["success"]:
                result["status"] = DeploymentStatus.ABORTED
                result["error"] = f"Pre-flight failed: {preflight['error']}"
                return result
            result["details"]["pre_flight"] = preflight

            # Phase 2: Sync secrets
            result["phase"] = "secrets_sync"
            secrets_sync = await self._sync_secrets()
            if not secrets_sync["success"]:
                result["status"] = DeploymentStatus.ABORTED
                result["error"] = f"Secrets sync failed: {secrets_sync['error']}"
                return result
            result["details"]["secrets_sync"] = secrets_sync

            # Phase 3: Create snapshots (rollback points)
            result["phase"] = "snapshots"
            snapshots = await self._create_snapshots()
            if not snapshots["success"]:
                result["status"] = DeploymentStatus.ABORTED
                result["error"] = "Snapshot creation failed"
                return result
            result["details"]["snapshots"] = snapshots

            # Phase 4: Deploy to ThinkPad (testing)
            result["phase"] = "thinkpad_deploy"
            thinkpad_result = await self._deploy_to_system(
                SystemTarget.THINKPAD,
                commit_hash,
                environment="staging"
            )
            if not thinkpad_result["success"]:
                await self._handle_deployment_failure(
                    snapshots,
                    failed_system=SystemTarget.THINKPAD,
                    rollback=rollback_on_failure
                )
                result["error"] = f"ThinkPad deployment failed: {thinkpad_result['error']}"
                return result
            result["systems_deployed"].append(SystemTarget.THINKPAD)
            result["details"]["thinkpad"] = thinkpad_result

            # Phase 5: Run automated tests
            if not skip_tests:
                result["phase"] = "tests"
                test_result = await self._run_tests(SystemTarget.THINKPAD)
                if not test_result["passed"]:
                    await self._handle_deployment_failure(
                        snapshots,
                        failed_system=SystemTarget.THINKPAD,
                        rollback=rollback_on_failure
                    )
                    result["error"] = f"Tests failed: {test_result['summary']}"
                    return result
                result["details"]["tests"] = test_result

            # Phase 6: Deploy to RTX1080 (production)
            result["phase"] = "rtx1080_deploy"
            rtx1080_result = await self._deploy_to_system(
                SystemTarget.RTX1080,
                commit_hash,
                environment=environment
            )
            if not rtx1080_result["success"]:
                await self._handle_deployment_failure(
                    snapshots,
                    failed_system=SystemTarget.RTX1080,
                    rollback=rollback_on_failure
                )
                result["error"] = f"RTX1080 deployment failed: {rtx1080_result['error']}"
                return result
            result["systems_deployed"].append(SystemTarget.RTX1080)
            result["details"]["rtx1080"] = rtx1080_result

            # Phase 7: Update VPS (with retry and independent rollback)
            result["phase"] = "vps_deploy"
            vps_result = await self._deploy_to_vps_with_retry(commit_hash)

            if not vps_result["success"]:
                # CRITICAL: RTX1080 is already deployed
                # VPS failure should NOT rollback RTX1080
                self.logger.warning(f"VPS deployment failed, but RTX1080 is live: {vps_result['error']}")

                # Rollback VPS only
                await self._rollback_system(SystemTarget.VPS, snapshots)

                # Alert for manual intervention
                await self._alert_deployment_coordinator({
                    "system": SystemTarget.VPS,
                    "status": "failed",
                    "rtx1080_status": "deployed",
                    "action": "manual_intervention_required",
                    "error": vps_result["error"]
                })

                result["status"] = DeploymentStatus.PARTIAL_SUCCESS
                result["error"] = f"VPS deployment failed (RTX1080 deployed successfully)"
                result["details"]["vps"] = vps_result
                result["requires_review"] = True

                # Don't return early - continue to verification
            else:
                result["systems_deployed"].append(SystemTarget.VPS)
                result["details"]["vps"] = vps_result

            # Phase 8: Verification
            result["phase"] = "verification"
            verification = await self._verify_deployment(result["systems_deployed"])
            result["details"]["verification"] = verification

            if not verification["healthy"]:
                # Verification failed - rollback everything
                if rollback_on_failure:
                    await self._handle_deployment_failure(
                        snapshots,
                        failed_system="verification",
                        rollback=True
                    )
                    result["status"] = DeploymentStatus.ROLLED_BACK
                    result["error"] = "Verification failed, deployment rolled back"
                else:
                    result["status"] = DeploymentStatus.FAILED
                    result["error"] = "Verification failed"
                return result

            # Success!
            if result["status"] != DeploymentStatus.PARTIAL_SUCCESS:
                result["status"] = DeploymentStatus.SUCCESS

            self.metrics["tasks_completed"] += 1
            self.logger.info(f"Deployment completed: {result['status']}")

        except Exception as e:
            self.logger.error(f"Unexpected deployment error: {str(e)}")
            result["error"] = f"Unexpected error: {str(e)}"
            result["status"] = DeploymentStatus.FAILED

            if rollback_on_failure:
                await self._handle_deployment_failure(
                    snapshots if 'snapshots' in locals() else {},
                    failed_system="unknown",
                    rollback=True
                )
                result["status"] = DeploymentStatus.ROLLED_BACK

        finally:
            result["duration_seconds"] = int(time.time() - start_time)

        return result

    async def _validate_systems_ready(self) -> Dict[str, Any]:
        """
        Validate all systems are ready for deployment

        Checks:
        - SSH connectivity to all systems
        - Docker daemon running
        - Sufficient disk space
        - No ongoing deployments
        """
        self.logger.info("Running pre-flight checks...")

        results = {
            "success": True,
            "systems": {},
            "error": None
        }

        for system_name, host in self.systems.items():
            system_status = {
                "ssh_reachable": False,
                "docker_running": False,
                "disk_space_ok": False
            }

            try:
                # Test SSH connection
                ssh_test = await self._run_ssh_command(host, "echo OK", timeout=5)
                system_status["ssh_reachable"] = ssh_test["success"]

                if not ssh_test["success"]:
                    results["success"] = False
                    results["error"] = f"{system_name} not reachable via SSH"
                    continue

                # Test Docker
                docker_test = await self._run_ssh_command(host, "docker ps", timeout=10)
                system_status["docker_running"] = docker_test["success"]

                # Check disk space (require at least 10GB free)
                disk_check = await self._run_ssh_command(
                    host,
                    "df -BG / | tail -1 | awk '{print $4}' | sed 's/G//'",
                    timeout=5
                )
                if disk_check["success"]:
                    free_gb = int(disk_check["output"].strip())
                    system_status["disk_space_ok"] = free_gb >= 10
                    system_status["free_disk_gb"] = free_gb

                results["systems"][system_name] = system_status

                # All checks must pass
                if not all(system_status.values()):
                    results["success"] = False
                    results["error"] = f"{system_name} failed pre-flight checks"

            except Exception as e:
                self.logger.error(f"Pre-flight check failed for {system_name}: {e}")
                results["success"] = False
                results["error"] = str(e)
                results["systems"][system_name] = system_status

        return results

    async def _sync_secrets(self) -> Dict[str, Any]:
        """Sync secrets using sync-secrets.sh"""
        self.logger.info("Syncing secrets...")

        try:
            script_path = Path.home() / "homelab" / "shared" / "scripts" / "sync-secrets.sh"

            result = subprocess.run(
                [str(script_path), "sync"],
                capture_output=True,
                text=True,
                timeout=60
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _create_snapshots(self) -> Dict[str, Any]:
        """Create Proxmox snapshots for rollback"""
        self.logger.info("Creating snapshots...")

        snapshots = {}
        snapshot_name = f"deploy-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        try:
            # Create snapshot on RTX1080 (critical production system)
            # Note: This requires Proxmox API or snapshot.sh script
            script_path = Path.home() / "homelab" / "shared" / "scripts" / "snapshot.sh"

            result = subprocess.run(
                [str(script_path), "create", snapshot_name],
                capture_output=True,
                text=True,
                timeout=300
            )

            snapshots["rtx1080"] = {
                "name": snapshot_name,
                "created": result.returncode == 0,
                "timestamp": datetime.now().isoformat()
            }

            return {
                "success": result.returncode == 0,
                "snapshots": snapshots
            }
        except Exception as e:
            self.logger.error(f"Snapshot creation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "snapshots": snapshots
            }

    async def _deploy_to_system(
        self,
        system: str,
        commit_hash: str,
        environment: str = "production"
    ) -> Dict[str, Any]:
        """Deploy to a specific system"""
        self.logger.info(f"Deploying to {system} (commit: {commit_hash})")

        host = self.systems[system]

        try:
            # Pull latest changes
            git_pull = await self._run_ssh_command(
                host,
                f"cd ~/homelab && git fetch && git checkout {commit_hash}",
                timeout=60
            )

            if not git_pull["success"]:
                return {
                    "success": False,
                    "error": f"Git pull failed: {git_pull['error']}"
                }

            # Run docker compose up
            compose_up = await self._run_ssh_command(
                host,
                "cd ~/homelab && docker compose up -d",
                timeout=300
            )

            if not compose_up["success"]:
                return {
                    "success": False,
                    "error": f"Docker compose failed: {compose_up['error']}"
                }

            # Health check
            await asyncio.sleep(10)  # Wait for services to start
            health = await self._check_system_health(system)

            return {
                "success": health["healthy"],
                "commit": commit_hash,
                "health": health,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _deploy_to_vps_with_retry(self, commit_hash: str) -> Dict[str, Any]:
        """
        Deploy to VPS with exponential backoff retry

        CodeRabbit recommendation: Retry VPS deployment independently
        """
        max_attempts = self.retry_config["max_attempts"]
        backoff = self.retry_config["initial_backoff"]

        for attempt in range(1, max_attempts + 1):
            self.logger.info(f"VPS deployment attempt {attempt}/{max_attempts}")

            result = await self._deploy_to_system(SystemTarget.VPS, commit_hash)

            if result["success"]:
                return result

            if attempt < max_attempts:
                self.logger.warning(f"VPS deployment failed, retrying in {backoff}s...")
                await asyncio.sleep(backoff)
                backoff = min(
                    backoff * self.retry_config["backoff_multiplier"],
                    self.retry_config["max_backoff"]
                )

        # All retries exhausted
        return {
            "success": False,
            "error": f"VPS deployment failed after {max_attempts} attempts",
            "last_attempt": result
        }

    async def _run_tests(self, system: str) -> Dict[str, Any]:
        """Run automated tests on deployed system"""
        self.logger.info(f"Running tests on {system}...")

        host = self.systems[system]

        try:
            # Run test suite (customize based on your tests)
            test_result = await self._run_ssh_command(
                host,
                "cd ~/homelab && python -m pytest tests/ -v",
                timeout=900
            )

            return {
                "passed": test_result["success"],
                "output": test_result["output"],
                "summary": "Tests passed" if test_result["success"] else "Tests failed"
            }
        except Exception as e:
            return {
                "passed": False,
                "error": str(e),
                "summary": f"Test execution failed: {str(e)}"
            }

    async def _check_system_health(self, system: str) -> Dict[str, Any]:
        """Run health checks for a system"""
        checks = self.health_checks.get(system, {})
        results = {}
        all_healthy = True

        host = self.systems[system]

        for check_name, check_cmd in checks.items():
            try:
                if check_cmd.startswith("http"):
                    # HTTP health check
                    result = await self._run_ssh_command(
                        host,
                        f"curl -f {check_cmd}",
                        timeout=10
                    )
                else:
                    # Command-based check
                    result = await self._run_ssh_command(host, check_cmd, timeout=10)

                results[check_name] = result["success"]
                if not result["success"]:
                    all_healthy = False
            except Exception as e:
                results[check_name] = False
                all_healthy = False

        return {
            "healthy": all_healthy,
            "checks": results
        }

    async def _verify_deployment(self, systems: List[str]) -> Dict[str, Any]:
        """Verify deployment across all deployed systems"""
        self.logger.info(f"Verifying deployment on: {systems}")

        verification = {
            "healthy": True,
            "systems": {}
        }

        for system in systems:
            health = await self._check_system_health(system)
            verification["systems"][system] = health

            if not health["healthy"]:
                verification["healthy"] = False

        return verification

    async def _handle_deployment_failure(
        self,
        snapshots: Dict,
        failed_system: str,
        rollback: bool = True
    ) -> None:
        """Handle deployment failure with optional rollback"""
        self.logger.error(f"Deployment failed at {failed_system}")

        if rollback and snapshots:
            self.logger.info("Initiating rollback...")
            await self._rollback_all_systems(snapshots)

        # Alert
        await self._alert_deployment_coordinator({
            "status": "failed",
            "failed_system": failed_system,
            "rollback_performed": rollback,
            "timestamp": datetime.now().isoformat()
        })

    async def _rollback_system(self, system: str, snapshots: Dict) -> Dict[str, Any]:
        """Rollback a specific system"""
        self.logger.info(f"Rolling back {system}...")

        snapshot = snapshots.get("snapshots", {}).get(system)
        if not snapshot:
            return {"success": False, "error": "No snapshot available"}

        try:
            script_path = Path.home() / "homelab" / "shared" / "scripts" / "snapshot.sh"
            result = subprocess.run(
                [str(script_path), "rollback", snapshot["name"]],
                capture_output=True,
                text=True,
                timeout=300
            )

            return {
                "success": result.returncode == 0,
                "snapshot": snapshot["name"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _rollback_all_systems(self, snapshots: Dict) -> None:
        """Rollback all systems to snapshots"""
        for system in [SystemTarget.RTX1080, SystemTarget.THINKPAD]:
            await self._rollback_system(system, snapshots)

    async def _alert_deployment_coordinator(self, alert: Dict[str, Any]) -> None:
        """Send alert to deployment coordinator (Telegram, etc.)"""
        self.logger.warning(f"DEPLOYMENT ALERT: {json.dumps(alert, indent=2)}")

        # TODO: Integrate with Telegram notifications
        # telegram_send(f"🚨 Deployment Alert: {alert['status']}")

    async def _run_ssh_command(
        self,
        host: str,
        command: str,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """Execute SSH command on remote host"""
        try:
            result = subprocess.run(
                ["ssh", "-o", "ConnectTimeout=5", host, command],
                capture_output=True,
                text=True,
                timeout=timeout
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Command timed out after {timeout}s"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_deployment_script(
        self,
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generiert Deployment-Scripts mit Code-Generation-Agent
        
        Nutzt intelligentes Routing:
        - OpenCode/Code-X für Standard-Scripts
        - Claude für komplexe Deployment-Strategien
        
        Args:
            task: {
                "type": "generate_code",
                "description": "Deployment script description",
                "language": "bash" | "python" | "yaml",
                "context": "Deployment context",
                "complexity": "simple" | "standard" | "complex"
            }
            
        Returns:
            Dict mit generiertem Script
        """
        # Prüfe Routing
        routing = self.route_task(task)
        
        if routing["tool"] == "claude":
            # Nutze Claude für komplexe Deployment-Strategien
            prompt = f"""Generate a {task.get('language', 'bash')} deployment script:

Description: {task.get('description', '')}
Context: {task.get('context', '')}

Requirements:
- Error handling
- Logging
- Rollback capability
- Health checks
- Idempotent execution

Provide production-ready, well-documented code."""
            
            script = await self.think(prompt)
            return {
                "success": True,
                "script": script,
                "method": "claude",
                "priority": routing["priority"]
            }
        else:
            # Nutze lokale Tools für Standard-Scripts
            return await self.use_local_tool(task)