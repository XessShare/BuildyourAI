"""
Mock/Dry-Run Mode für DeploymentOrchestratorAgent
Erlaubt Testing ohne echte SSH-Verbindungen

Usage:
    from agents.deployment_orchestrator_mock import MockDeploymentAgent

    agent = MockDeploymentAgent(mock_mode=True, simulate_failures=False)
    result = await agent.execute({
        "commit_hash": "main",
        "environment": "production"
    })
"""

import asyncio
import random
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from .deployment_orchestrator import (
    DeploymentOrchestratorAgent,
    DeploymentStatus,
    SystemTarget
)


class MockDeploymentAgent(DeploymentOrchestratorAgent):
    """
    Mock version of DeploymentOrchestratorAgent for testing without SSH

    Features:
    - Simulates SSH connections
    - Simulates deployment delays
    - Can simulate random failures
    - Provides realistic test scenarios
    """

    def __init__(self, mock_mode: bool = True, simulate_failures: bool = False, failure_rate: float = 0.1):
        """
        Initialize Mock Deployment Agent

        Args:
            mock_mode: Enable mock mode (default True)
            simulate_failures: Randomly simulate failures for testing
            failure_rate: Probability of random failures (0.0 - 1.0)
        """
        super().__init__()

        self.mock_mode = mock_mode
        self.simulate_failures = simulate_failures
        self.failure_rate = failure_rate

        # Mock state tracking
        self.mock_state = {
            "systems_healthy": {
                SystemTarget.VPS: True,
                SystemTarget.THINKPAD: True,
                SystemTarget.RTX1080: True
            },
            "deployed_commits": {},
            "snapshots_created": [],
            "deployment_count": 0
        }

        self.logger.info(f"MockDeploymentAgent initialized (mock_mode={mock_mode}, simulate_failures={simulate_failures})")

    async def _run_ssh_command(
        self,
        host: str,
        command: str,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """Mock SSH command execution"""

        if not self.mock_mode:
            # Fall back to real SSH
            return await super()._run_ssh_command(host, command, timeout)

        # Simulate network delay
        await asyncio.sleep(random.uniform(0.1, 0.5))

        # Simulate random failures
        if self.simulate_failures and random.random() < self.failure_rate:
            return {
                "success": False,
                "output": "",
                "error": f"Mock: Random failure simulated for: {command}"
            }

        # Determine system from host
        system = None
        for sys_name, sys_host in self.systems.items():
            if sys_host == host:
                system = sys_name
                break

        # Check if system is "healthy" in mock state
        if system and not self.mock_state["systems_healthy"].get(system, True):
            return {
                "success": False,
                "output": "",
                "error": f"Mock: System {system} marked as unhealthy"
            }

        # Mock successful responses for common commands
        if "echo" in command.lower():
            return {
                "success": True,
                "output": "OK\n",
                "error": None
            }

        if "docker ps" in command:
            return {
                "success": True,
                "output": "CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES\n",
                "error": None
            }

        if "pg_isready" in command:
            return {
                "success": True,
                "output": "accepting connections\n",
                "error": None
            }

        if "redis-cli ping" in command:
            return {
                "success": True,
                "output": "PONG\n",
                "error": None
            }

        if "df -BG" in command:
            return {
                "success": True,
                "output": "50\n",  # 50GB free
                "error": None
            }

        if "git" in command:
            return {
                "success": True,
                "output": "Mock: Git operation successful\n",
                "error": None
            }

        if "docker compose" in command or "docker-compose" in command:
            await asyncio.sleep(2)  # Simulate compose up delay
            return {
                "success": True,
                "output": "Mock: Docker Compose completed\n",
                "error": None
            }

        if "pytest" in command:
            await asyncio.sleep(3)  # Simulate test execution
            return {
                "success": True,
                "output": "Mock: All tests passed\n",
                "error": None
            }

        # Default success for unknown commands
        return {
            "success": True,
            "output": f"Mock: Command executed: {command[:50]}...\n",
            "error": None
        }

    async def _sync_secrets(self) -> Dict[str, Any]:
        """Mock secrets synchronization"""

        if not self.mock_mode:
            return await super()._sync_secrets()

        await asyncio.sleep(1)  # Simulate sync delay

        if self.simulate_failures and random.random() < self.failure_rate:
            return {
                "success": False,
                "error": "Mock: Secrets sync failed (simulated)"
            }

        return {
            "success": True,
            "output": "Mock: Secrets synced to all systems",
            "error": None
        }

    async def _create_snapshots(self) -> Dict[str, Any]:
        """Mock snapshot creation"""

        if not self.mock_mode:
            return await super()._create_snapshots()

        await asyncio.sleep(2)  # Simulate snapshot creation delay

        snapshot_name = f"mock-deploy-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        if self.simulate_failures and random.random() < self.failure_rate:
            return {
                "success": False,
                "error": "Mock: Snapshot creation failed (simulated)",
                "snapshots": {}
            }

        snapshots = {
            "rtx1080": {
                "name": snapshot_name,
                "created": True,
                "timestamp": datetime.now().isoformat()
            }
        }

        self.mock_state["snapshots_created"].append(snapshot_name)

        return {
            "success": True,
            "snapshots": snapshots
        }

    async def _rollback_system(self, system: str, snapshots: Dict) -> Dict[str, Any]:
        """Mock system rollback"""

        if not self.mock_mode:
            return await super()._rollback_system(system, snapshots)

        await asyncio.sleep(1.5)  # Simulate rollback delay

        snapshot = snapshots.get("snapshots", {}).get(system)
        if not snapshot:
            return {
                "success": False,
                "error": "Mock: No snapshot available for rollback"
            }

        self.logger.info(f"Mock: Rolling back {system} to snapshot {snapshot.get('name')}")

        return {
            "success": True,
            "snapshot": snapshot.get("name", "unknown")
        }

    async def _alert_deployment_coordinator(self, alert: Dict[str, Any]) -> None:
        """Mock alert sending"""

        self.logger.warning(f"Mock ALERT: {alert}")

        if not self.mock_mode:
            return await super()._alert_deployment_coordinator(alert)

        # In mock mode, just log
        await asyncio.sleep(0.1)

    def set_system_health(self, system: str, healthy: bool):
        """
        Manually set system health for testing

        Args:
            system: SystemTarget (vps, thinkpad, rtx1080)
            healthy: True if healthy, False to simulate unhealthy
        """
        self.mock_state["systems_healthy"][system] = healthy
        self.logger.info(f"Mock: Set {system} health to {healthy}")

    def simulate_failure_scenario(self, scenario: str):
        """
        Simulate specific failure scenarios for testing

        Scenarios:
        - "thinkpad_deploy_fail": ThinkPad deployment fails
        - "tests_fail": Automated tests fail
        - "rtx1080_deploy_fail": RTX1080 deployment fails
        - "vps_deploy_fail": VPS deployment fails
        - "verification_fail": Verification fails
        - "all_healthy": All systems healthy (reset)
        """

        scenarios = {
            "all_healthy": lambda: self._reset_health(),
            "thinkpad_deploy_fail": lambda: self.set_system_health(SystemTarget.THINKPAD, False),
            "rtx1080_deploy_fail": lambda: self.set_system_health(SystemTarget.RTX1080, False),
            "vps_deploy_fail": lambda: self.set_system_health(SystemTarget.VPS, False),
        }

        if scenario in scenarios:
            scenarios[scenario]()
            self.logger.info(f"Mock: Activated failure scenario: {scenario}")
        else:
            self.logger.warning(f"Mock: Unknown scenario: {scenario}")

    def _reset_health(self):
        """Reset all systems to healthy"""
        for system in self.mock_state["systems_healthy"]:
            self.mock_state["systems_healthy"][system] = True

    def get_mock_state(self) -> Dict[str, Any]:
        """Get current mock state for inspection"""
        return {
            **self.mock_state,
            "mock_mode": self.mock_mode,
            "simulate_failures": self.simulate_failures,
            "failure_rate": self.failure_rate
        }


# Convenience function for quick testing
async def quick_test():
    """Quick test of mock deployment"""

    print("=" * 70)
    print("MockDeploymentAgent - Quick Test")
    print("=" * 70)

    agent = MockDeploymentAgent(mock_mode=True, simulate_failures=False)

    print("\n1. Testing normal deployment...")
    result = await agent.execute({
        "commit_hash": "main",
        "environment": "production",
        "rollback_on_failure": True,
        "skip_tests": False
    })

    print(f"\nResult: {result['status']}")
    print(f"Duration: {result['duration_seconds']}s")
    print(f"Systems deployed: {result['systems_deployed']}")

    print("\n" + "=" * 70)
    print("2. Testing failure scenario (VPS fails)...")
    print("=" * 70)

    agent.simulate_failure_scenario("vps_deploy_fail")

    result2 = await agent.execute({
        "commit_hash": "feature-branch",
        "environment": "staging"
    })

    print(f"\nResult: {result2['status']}")
    print(f"Error: {result2.get('error', 'None')}")
    print(f"Systems deployed: {result2['systems_deployed']}")

    print("\n" + "=" * 70)
    print("Mock State:")
    print("=" * 70)

    import json
    print(json.dumps(agent.get_mock_state(), indent=2))


if __name__ == "__main__":
    asyncio.run(quick_test())
