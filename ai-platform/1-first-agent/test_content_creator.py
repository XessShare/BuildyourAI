"""
Quick test for ContentCreatorAgent
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.content_creator_agent import ContentCreatorAgent


async def main():
    print("=" * 60)
    print("Testing ContentCreatorAgent")
    print("=" * 60)
    
    agent = ContentCreatorAgent()
    
    # Test 1: Generate a short video script
    print("\n[TEST 1] Generating 5-minute video script...")
    print("-" * 60)
    
    result = await agent.create_video_script({
        "topic": "AI Avatars: Wie sie funktionieren und warum sie die Zukunft sind",
        "target_duration": 5,
        "key_points": [
            "Was sind AI Avatars?",
            "Wie erstellt man sie?",
            "Praktische Anwendungen"
        ],
        "style": "educational"
    })
    
    print(f"\nGenerated script ({result['metadata']['word_count']} words):")
    print(f"Estimated speaking time: {result['metadata']['estimated_speaking_time']:.1f} minutes")
    print("\n--- Script Preview (first 500 chars) ---")
    print(result["content"][:500])
    print("...\n")
    
    # Test 2: Generate content ideas
    print("\n[TEST 2] Generating content ideas...")
    print("-" * 60)
    
    ideas = await agent.generate_content_ideas("Homelab Self-Hosting für Anfänger", count=3)
    print(f"\nGenerated {len(ideas)} content ideas:")
    for i, idea in enumerate(ideas[:3], 1):
        print(f"\n{i}. {idea[:200]}...")
    
    print("\n" + "=" * 60)
    print("Tests completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
