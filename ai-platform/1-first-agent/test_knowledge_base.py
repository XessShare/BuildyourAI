"""
Quick test for Knowledge Base System
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from knowledge_base import KnowledgeBase


def main():
    print("=" * 60)
    print("Testing Knowledge Base System")
    print("=" * 60)

    # Initialize Knowledge Base
    kb = KnowledgeBase()

    # Test 1: Add research findings
    print("\n[TEST 1] Adding research findings...")
    print("-" * 60)

    research_id1 = kb.add_research(
        topic="GPT-4o-mini Performance",
        findings="GPT-4o-mini demonstrates strong performance with 128k context window, competitive pricing at $0.15/1M input tokens, and excellent response quality for most tasks.",
        sources=["OpenAI Documentation", "Performance Benchmarks 2024"],
        confidence=0.95
    )
    print(f"✓ Added research: {research_id1}")

    research_id2 = kb.add_research(
        topic="Claude 3.5 Sonnet Capabilities",
        findings="Claude 3.5 Sonnet excels at code generation, analysis, and long-form content. Shows improved reasoning over previous versions.",
        sources=["Anthropic Blog", "User Benchmarks"],
        confidence=0.92
    )
    print(f"✓ Added research: {research_id2}")

    # Test 2: Add verified facts
    print("\n[TEST 2] Adding verified facts...")
    print("-" * 60)

    fact_id1 = kb.add_fact(
        fact="ChromaDB is an open-source vector database optimized for embedding storage and retrieval",
        verified=True,
        sources=["ChromaDB Documentation"],
        confidence=1.0
    )
    print(f"✓ Added fact: {fact_id1}")

    fact_id2 = kb.add_fact(
        fact="Python 3.13 was released in October 2024 with improved performance",
        verified=True,
        sources=["Python.org Release Notes"],
        confidence=1.0
    )
    print(f"✓ Added fact: {fact_id2}")

    # Test 3: Add analytical insights
    print("\n[TEST 3] Adding analytical insights...")
    print("-" * 60)

    insight_id1 = kb.add_insight(
        insight="Subscriber growth shows consistent upward trend with 150% target achievement in Month 3",
        category="performance_metrics",
        source_data="Monthly KPI tracking data",
        actionable=True
    )
    print(f"✓ Added insight: {insight_id1}")

    insight_id2 = kb.add_insight(
        insight="Video content with 10-15 minute duration shows highest engagement rate",
        category="content_performance",
        source_data="YouTube analytics Q4 2024",
        actionable=True
    )
    print(f"✓ Added insight: {insight_id2}")

    # Test 4: Add content
    print("\n[TEST 4] Adding generated content...")
    print("-" * 60)

    content_id = kb.add_content(
        content="Tutorial: Getting Started with AI Agents\n\nIn this tutorial, we'll explore...",
        content_type="tutorial_script",
        metadata={"duration_min": 10, "platform": "YouTube"}
    )
    print(f"✓ Added content: {content_id}")

    # Test 5: Semantic search
    print("\n[TEST 5] Performing semantic search...")
    print("-" * 60)

    results = kb.search("AI model performance and capabilities", n_results=3)
    print(f"\nSearch: 'AI model performance and capabilities'")
    print(f"Found {results['count']} results:\n")
    for i, result in enumerate(results['results'], 1):
        print(f"{i}. {result['content'][:100]}...")
        print(f"   Type: {result['metadata'].get('type', 'unknown')}")
        if result['distance']:
            print(f"   Relevance: {(1 - result['distance']) * 100:.1f}%")
        print()

    # Test 6: Search specific collections
    print("\n[TEST 6] Searching specific collections...")
    print("-" * 60)

    research_results = kb.search_research("performance benchmarks", n_results=2)
    print(f"\nResearch Search: Found {research_results['count']} results")
    if research_results['results']:
        print(f"Top result: {research_results['results'][0]['content'][:80]}...")

    facts_results = kb.search_facts("database vector", verified_only=True, n_results=2)
    print(f"\nFacts Search: Found {facts_results['count']} verified facts")
    if facts_results['results']:
        print(f"Top result: {facts_results['results'][0]['content'][:80]}...")

    insights_results = kb.search_insights("performance growth", actionable_only=True, n_results=2)
    print(f"\nInsights Search: Found {insights_results['count']} actionable insights")
    if insights_results['results']:
        print(f"Top result: {insights_results['results'][0]['content'][:80]}...")

    # Test 7: Get by ID
    print("\n\n[TEST 7] Retrieving knowledge by ID...")
    print("-" * 60)

    retrieved = kb.get_by_id(research_id1, "research")
    if retrieved:
        print(f"✓ Retrieved: {retrieved['id']}")
        print(f"  Content: {retrieved['content'][:100]}...")
        print(f"  Collection: {retrieved.get('collection', 'unknown')}")

    # Test 8: Get statistics
    print("\n\n[TEST 8] Knowledge Base statistics...")
    print("-" * 60)

    stats = kb.get_stats()
    print(f"\nTotal Knowledge Items: {stats['total_knowledge']}")
    print("\nCollection Breakdown:")
    for name, info in stats['collections'].items():
        if info['count'] > 0:
            print(f"  ✓ {name}: {info['count']} items")

    # Test 9: Cross-collection search
    print("\n\n[TEST 9] Cross-collection semantic search...")
    print("-" * 60)

    all_results = kb.search("subscriber engagement metrics", n_results=5)
    print(f"\nSearch across all collections: Found {all_results['count']} results")
    types_found = set()
    for result in all_results['results']:
        types_found.add(result['metadata'].get('type', 'unknown'))
    print(f"Knowledge types found: {', '.join(types_found)}")

    print("\n" + "=" * 60)
    print("All Knowledge Base tests completed successfully!")
    print("=" * 60)
    print(f"\n✓ Knowledge Base persisted at: {kb.persist_directory}")
    print("✓ Data will be available across sessions")


if __name__ == "__main__":
    main()
