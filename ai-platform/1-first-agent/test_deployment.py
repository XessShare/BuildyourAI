"""
Test Script for DeploymentOrchestratorAgent
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from agents.deployment_orchestrator import DeploymentOrchestratorAgent


async def test_pre_flight_checks():
    """Test pre-flight system validation"""
    print("=" * 70)
    print("Testing Pre-flight Checks")
    print("=" * 70)

    agent = DeploymentOrchestratorAgent()
    result = await agent._validate_systems_ready()

    print(f"\nStatus: {'✅ PASS' if result['success'] else '❌ FAIL'}")
    print(f"Systems checked: {len(result.get('systems', {}))}")

    for system, status in result.get('systems', {}).items():
        print(f"\n{system}:")
        for check, passed in status.items():
            icon = "✅" if passed else "❌"
            print(f"  {icon} {check}: {passed}")

    if not result['success']:
        print(f"\n⚠️  Error: {result.get('error', 'Unknown')}")

    return result['success']


async def test_secrets_sync():
    """Test secrets synchronization"""
    print("\n" + "=" * 70)
    print("Testing Secrets Synchronization")
    print("=" * 70)

    agent = DeploymentOrchestratorAgent()
    result = await agent._sync_secrets()

    print(f"\nStatus: {'✅ PASS' if result['success'] else '❌ FAIL'}")

    if result['success']:
        print("Secrets synced successfully!")
    else:
        print(f"⚠️  Error: {result.get('error', 'Unknown')}")

    return result['success']


async def test_health_checks():
    """Test system health checks"""
    print("\n" + "=" * 70)
    print("Testing System Health Checks")
    print("=" * 70)

    agent = DeploymentOrchestratorAgent()

    for system in ["thinkpad", "rtx1080", "vps"]:
        print(f"\n{system.upper()}:")
        health = await agent._check_system_health(system)

        print(f"Overall: {'✅ Healthy' if health['healthy'] else '❌ Unhealthy'}")

        for check, passed in health.get('checks', {}).items():
            icon = "✅" if passed else "❌"
            print(f"  {icon} {check}")


async def test_full_deployment_dry_run():
    """Test full deployment workflow (dry run)"""
    print("\n" + "=" * 70)
    print("Testing Full Deployment Workflow (Dry Run)")
    print("=" * 70)

    agent = DeploymentOrchestratorAgent()

    task = {
        "commit_hash": "HEAD",
        "environment": "staging",
        "rollback_on_failure": True,
        "skip_tests": True  # Skip for dry run
    }

    print(f"\nDeployment Task:")
    print(f"  Commit: {task['commit_hash']}")
    print(f"  Environment: {task['environment']}")
    print(f"  Rollback on failure: {task['rollback_on_failure']}")
    print(f"  Skip tests: {task['skip_tests']}")

    print("\n⚠️  This would trigger a real deployment!")
    print("Skipping actual execution for safety.")

    # Uncomment to run actual deployment:
    # result = await agent.execute(task)
    # print(f"\nResult: {result['status']}")
    # print(f"Duration: {result['duration_seconds']}s")


async def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("DeploymentOrchestratorAgent Test Suite")
    print("=" * 70)

    tests = [
        ("Pre-flight Checks", test_pre_flight_checks),
        ("Secrets Sync", test_secrets_sync),
        ("Health Checks", test_health_checks),
        ("Full Deployment (Dry Run)", test_full_deployment_dry_run),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)

    for test_name, passed in results:
        if passed is not None:
            icon = "✅" if passed else "❌"
            print(f"{icon} {test_name}")
        else:
            print(f"⚠️  {test_name} (skipped)")

    passed_count = sum(1 for _, p in results if p is True)
    total_count = sum(1 for _, p in results if p is not None)

    print(f"\nPassed: {passed_count}/{total_count}")

    if passed_count == total_count:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check logs for details.")


if __name__ == "__main__":
    asyncio.run(main())
