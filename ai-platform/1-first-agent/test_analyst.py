"""
Quick test for AnalystAgent
"""

import asyncio
import sys
from pathlib import Path
import pandas as pd

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.analyst_agent import AnalystAgent


async def main():
    print("=" * 60)
    print("Testing AnalystAgent")
    print("=" * 60)

    agent = AnalystAgent()

    # Test 1: Analyze performance against targets
    print("\n[TEST 1] Analyzing performance metrics...")
    print("-" * 60)

    result1 = await agent.analyze_performance({
        "metrics": {
            "subscribers": 150,
            "videos": 3,
            "newsletters": 5,
            "engagement_rate": 8.5
        },
        "targets": {
            "subscribers": 100,
            "videos": 2,
            "newsletters": 4,
            "engagement_rate": 10.0
        },
        "period": "Month 3 - Q1 2025"
    })

    print(f"\nPeriod: {result1['period']}")
    print(f"Metrics Analyzed: {result1['metrics_analyzed']}")
    print("\nPerformance Summary:")
    for metric, perf in result1['performance'].items():
        status_symbol = "✓" if perf['status'] == 'on_track' else "⚠" if perf['status'] == 'behind' else "✗"
        print(f"  {status_symbol} {metric}: {perf['actual']}/{perf['target']} ({perf['achievement_pct']}%)")

    print("\n--- Analysis Preview (first 500 chars) ---")
    print(result1["analysis"][:500])
    print("...")

    # Test 2: Identify patterns in time series data
    print("\n\n[TEST 2] Identifying patterns in subscriber growth...")
    print("-" * 60)

    # Create sample time series data
    subscriber_data = pd.DataFrame({
        "date": pd.date_range(start="2024-01-01", periods=90, freq="D"),
        "subscribers": [100 + i * 2 + (i % 7) * 5 for i in range(90)]  # Growth with weekly pattern
    })

    result2 = await agent.identify_patterns({
        "data": subscriber_data,
        "metric": "subscribers",
        "timeframe": "daily"
    })

    print(f"\nMetric: {result2['metric']}")
    print(f"Data Points: {result2['data_points']}")
    print(f"Timeframe: {result2['timeframe']}")
    print("\nStatistics:")
    stats = result2['statistics']
    print(f"  Mean: {stats['mean']:.2f}")
    print(f"  Median: {stats['median']:.2f}")
    print(f"  Trend: {stats['trend_direction']} (strength: {stats['trend_strength']:.4f})")

    print("\n--- Pattern Analysis Preview (first 500 chars) ---")
    print(result2["analysis"][:500])
    print("...")

    # Test 3: Compare two periods
    print("\n\n[TEST 3] Comparing Month 1 vs Month 2...")
    print("-" * 60)

    month1_data = {
        "subscribers": [100, 105, 110, 115],
        "videos": [1, 1, 2, 2],
        "views": [500, 520, 600, 650]
    }

    month2_data = {
        "subscribers": [120, 130, 145, 160],
        "videos": [2, 3, 3, 4],
        "views": [700, 800, 900, 1000]
    }

    result3 = await agent.compare_data({
        "data_a": month1_data,
        "data_b": month2_data,
        "label_a": "Month 1",
        "label_b": "Month 2",
        "metrics": ["subscribers", "videos", "views"]
    })

    print(f"\nComparing: {result3['label_a']} vs {result3['label_b']}")
    print(f"Metrics Compared: {result3['metrics_compared']}")
    print("\nComparison Summary:")
    for metric, comp in result3['comparison'].items():
        trend_symbol = "↑" if comp['trend'] == 'up' else "↓" if comp['trend'] == 'down' else "→"
        print(f"  {trend_symbol} {metric}: {comp['percent_change']:+.1f}%")

    print("\n--- Comparative Analysis Preview (first 500 chars) ---")
    print(result3["analysis"][:500])
    print("...")

    # Test 4: Analyze a dataset
    print("\n\n[TEST 4] Analyzing content performance dataset...")
    print("-" * 60)

    content_data = pd.DataFrame({
        "video_id": ["V1", "V2", "V3", "V4", "V5"],
        "views": [1000, 1500, 800, 2000, 1200],
        "likes": [100, 180, 90, 250, 140],
        "comments": [20, 35, 15, 50, 28],
        "duration_min": [10, 15, 8, 12, 10]
    })

    result4 = await agent.analyze_dataset({
        "data": content_data,
        "name": "YouTube Video Performance",
        "focus_areas": ["engagement", "patterns", "recommendations"]
    })

    print(f"\nDataset: {result4['dataset_name']}")
    print(f"Rows: {result4['rows']}")
    print(f"Columns: {', '.join(result4['columns'])}")

    print("\n--- Dataset Analysis Preview (first 500 chars) ---")
    print(result4["analysis"][:500])
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
