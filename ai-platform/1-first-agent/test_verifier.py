"""
Quick test for VerifierAgent
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.verifier_agent import VerifierAgent


async def main():
    print("=" * 60)
    print("Testing VerifierAgent")
    print("=" * 60)

    agent = VerifierAgent()

    # Test 1: Verify factual claims
    print("\n[TEST 1] Verifying factual claims about AI models...")
    print("-" * 60)

    result1 = await agent.verify_facts({
        "claims": [
            "GPT-4 has a context window of 128k tokens",
            "Claude 3.5 Sonnet is faster than GPT-4o",
            "Llama 3.1 is available for self-hosting"
        ],
        "context": "AI model capabilities in 2024-2025"
    })

    print(f"\nClaims Verified: {result1['claims_checked']}")
    print(f"Report Date: {result1['report_date']}")
    print("\n--- First Claim Verification Preview (first 500 chars) ---")
    print(result1["verifications"][0]["verification"][:500])
    print("...")

    if result1["verifications"][0]["sources"]:
        print(f"\nSources: {len(result1['verifications'][0]['sources'])} citations")
    else:
        print("\nNote: Using fallback LLM (Perplexity key might be missing)")

    # Test 2: Verify sources
    print("\n\n[TEST 2] Verifying source credibility...")
    print("-" * 60)

    result2 = await agent.verify_sources({
        "sources": [
            "OpenAI official documentation",
            "Anthropic research blog",
            "Random tech blog",
            "ArXiv papers"
        ],
        "topic": "AI model performance benchmarks"
    })

    print(f"\nSources Checked: {result2['sources_checked']}")
    print(f"Topic: {result2['topic']}")
    print("\n--- Source Assessment Preview (first 500 chars) ---")
    print(result2["assessment"][:500])
    print("...")

    # Test 3: Check actuality
    print("\n\n[TEST 3] Checking content actuality...")
    print("-" * 60)

    content_to_check = """
    GPT-4 is the latest model from OpenAI with a 32k context window.
    Claude 3 Opus is Anthropic's most capable model.
    Local LLMs like Llama 2 are gaining popularity for self-hosting.
    """

    result3 = await agent.check_actuality({
        "content": content_to_check,
        "topic": "AI Models Overview"
    })

    print(f"\nTopic: {result3['topic']}")
    print(f"Checked At: {result3['checked_at']}")
    print("\n--- Actuality Assessment Preview (first 500 chars) ---")
    print(result3["assessment"][:500])
    print("...")

    # Show agent metrics
    print("\n\n[AGENT METRICS]")
    print("-" * 60)
    metrics = agent.get_metrics()
    print(f"Tasks Completed: {metrics['tasks_completed']}")
    print(f"Tokens Used: {metrics['tokens_used']}")
    print(f"Errors: {metrics['errors']}")
    print(f"Memory Size: {metrics['memory_size']} messages")

    print("\n" + "=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
