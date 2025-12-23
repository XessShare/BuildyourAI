"""
Quick test for ResearcherAgent
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.researcher_agent import ResearcherAgent


async def main():
    print("=" * 60)
    print("Testing ResearcherAgent")
    print("=" * 60)
    
    agent = ResearcherAgent()
    
    # Test: Quick trend analysis
    print("\n[TEST] Analyzing AI Self-Hosting trend...")
    print("-" * 60)
    
    result = await agent.analyze_tech_trend({
        "trend": "Local AI Models and Self-Hosted LLMs",
        "timeframe": "next_year",
        "focus": ["adoption", "technology", "homelab_integration"]
    })
    
    print(f"\nTrend Analyzed: {result['trend_analyzed']}")
    print(f"Timeframe: {result['timeframe']}")
    print(f"Research Date: {result['analysis_date']}")
    print("\n--- Report Preview (first 600 chars) ---")
    print(result["report"][:600])
    print("...")
    
    if result["sources"]:
        print(f"\nSources: {len(result['sources'])} citations found")
    else:
        print("\nNote: Using fallback LLM (Perplexity key might be missing)")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
