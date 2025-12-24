"""
Test Script für DeploymentOrchestratorAgent im Mock-Mode
Erlaubt vollständiges Testing ohne SSH-Verbindungen
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from agents.deployment_orchestrator_mock import MockDeploymentAgent


async def test_scenario_1_normal_deployment():
    """Scenario 1: Normal successful deployment"""
    print("\n" + "=" * 70)
    print("SCENARIO 1: Normal Successful Deployment")
    print("=" * 70)

    agent = MockDeploymentAgent(mock_mode=True, simulate_failures=False)

    result = await agent.execute({
        "commit_hash": "main",
        "environment": "production",
        "rollback_on_failure": True,
        "skip_tests": False
    })

    print(f"\n✅ Status: {result['status']}")
    print(f"⏱️  Duration: {result['duration_seconds']}s")
    print(f"🖥️  Systems deployed: {', '.join(result['systems_deployed'])}")
    print(f"📊 Phase: {result['phase']}")

    assert result['status'] == 'success', "Expected successful deployment"
    assert len(result['systems_deployed']) == 3, "Expected 3 systems deployed"

    return True


async def test_scenario_2_vps_failure():
    """Scenario 2: VPS deployment fails (partial success)"""
    print("\n" + "=" * 70)
    print("SCENARIO 2: VPS Deployment Fails (Partial Success)")
    print("=" * 70)

    agent = MockDeploymentAgent(mock_mode=True, simulate_failures=False)
    agent.simulate_failure_scenario("vps_deploy_fail")

    result = await agent.execute({
        "commit_hash": "feature-branch",
        "environment": "production",
        "rollback_on_failure": True
    })

    print(f"\n⚠️  Status: {result['status']}")
    print(f"⏱️  Duration: {result['duration_seconds']}s")
    print(f"🖥️  Systems deployed: {', '.join(result['systems_deployed'])}")
    print(f"❌ Error: {result.get('error', 'None')}")

    assert result['status'] == 'partial_success', "Expected partial success"
    assert 'vps' not in result['systems_deployed'], "VPS should not be deployed"
    assert 'rtx1080' in result['systems_deployed'], "RTX1080 should be deployed"

    return True


async def test_scenario_3_thinkpad_failure():
    """Scenario 3: ThinkPad (staging) fails → full rollback"""
    print("\n" + "=" * 70)
    print("SCENARIO 3: ThinkPad Deployment Fails (Full Rollback)")
    print("=" * 70)

    agent = MockDeploymentAgent(mock_mode=True, simulate_failures=False)
    agent.simulate_failure_scenario("thinkpad_deploy_fail")

    result = await agent.execute({
        "commit_hash": "buggy-branch",
        "environment": "staging",
        "rollback_on_failure": True
    })

    print(f"\n❌ Status: {result['status']}")
    print(f"⏱️  Duration: {result['duration_seconds']}s")
    print(f"🖥️  Systems deployed: {', '.join(result['systems_deployed'])}")
    print(f"❌ Error: {result.get('error', 'None')}")

    assert result['status'] in ['failed', 'aborted'], "Expected failure or abort"
    assert len(result['systems_deployed']) == 0, "No systems should be deployed"

    return True


async def test_scenario_4_random_failures():
    """Scenario 4: Random failures enabled"""
    print("\n" + "=" * 70)
    print("SCENARIO 4: Random Failures Simulation (10% failure rate)")
    print("=" * 70)

    agent = MockDeploymentAgent(
        mock_mode=True,
        simulate_failures=True,
        failure_rate=0.1  # 10% chance of random failures
    )

    results = {
        'success': 0,
        'partial_success': 0,
        'failed': 0
    }

    print("\nRunning 5 deployments with random failures...")

    for i in range(5):
        result = await agent.execute({
            "commit_hash": f"commit-{i}",
            "environment": "staging",
            "rollback_on_failure": True,
            "skip_tests": True  # Speed up
        })

        status = result['status']
        results[status] = results.get(status, 0) + 1

        icon = "✅" if status == "success" else "⚠️" if status == "partial_success" else "❌"
        print(f"{icon} Deploy {i+1}/5: {status} ({result['duration_seconds']}s)")

    print(f"\nResults:")
    print(f"  ✅ Success: {results.get('success', 0)}/5")
    print(f"  ⚠️  Partial: {results.get('partial_success', 0)}/5")
    print(f"  ❌ Failed: {results.get('failed', 0)}/5")

    return True


async def test_scenario_5_performance():
    """Scenario 5: Performance test"""
    print("\n" + "=" * 70)
    print("SCENARIO 5: Performance Test (10 rapid deployments)")
    print("=" * 70)

    agent = MockDeploymentAgent(mock_mode=True, simulate_failures=False)

    import time
    start = time.time()

    tasks = []
    for i in range(10):
        task = agent.execute({
            "commit_hash": f"perf-test-{i}",
            "environment": "staging",
            "skip_tests": True
        })
        tasks.append(task)

    results = await asyncio.gather(*tasks)

    elapsed = time.time() - start

    successful = sum(1 for r in results if r['status'] == 'success')

    print(f"\n⏱️  Total time: {elapsed:.2f}s")
    print(f"📊 Avg per deployment: {elapsed/10:.2f}s")
    print(f"✅ Success rate: {successful}/10")

    return True


async def main():
    """Run all test scenarios"""

    print("\n" + "=" * 70)
    print("DeploymentOrchestratorAgent - Mock Mode Test Suite")
    print("=" * 70)
    print("\n🎭 Running in MOCK mode (no real SSH connections)")
    print("This allows full testing without access to actual systems.\n")

    tests = [
        ("Normal Deployment", test_scenario_1_normal_deployment),
        ("VPS Failure (Partial Success)", test_scenario_2_vps_failure),
        ("ThinkPad Failure (Full Rollback)", test_scenario_3_thinkpad_failure),
        ("Random Failures", test_scenario_4_random_failures),
        ("Performance Test", test_scenario_5_performance),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            print(f"\n🔬 Running: {test_name}")
            passed = await test_func()
            results.append((test_name, passed))
            print(f"✅ PASSED: {test_name}")
        except Exception as e:
            print(f"❌ FAILED: {test_name}")
            print(f"   Error: {str(e)}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)

    for test_name, passed in results:
        icon = "✅" if passed else "❌"
        print(f"{icon} {test_name}")

    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)

    print(f"\nPassed: {passed_count}/{total_count}")

    if passed_count == total_count:
        print("\n🎉 All tests passed!")
        print("\n📝 Note: These are MOCK tests. For real deployment:")
        print("   1. Setup SSH keys to VPS, ThinkPad, RTX1080")
        print("   2. Run: python test_deployment.py")
    else:
        print("\n⚠️  Some tests failed. Check logs for details.")

    return passed_count == total_count


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
