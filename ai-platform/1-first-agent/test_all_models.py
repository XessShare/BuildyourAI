"""
Test Script für alle konfigurierten LLMs
Testet ob alle API Keys funktionieren und Modelle erreichbar sind
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from config import AGENT_CONFIG, OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, PERPLEXITY_API_KEY
from agents.base_agent import BaseAgent
from agents.content_creator_agent import ContentCreatorAgent
from agents.researcher_agent import ResearcherAgent
from agents.project_manager_agent import ProjectManagerAgent


def check_api_keys():
    """Prüfe ob API Keys gesetzt sind"""
    print("\n=== API Key Status ===")

    keys = {
        "OpenAI": OPENAI_API_KEY,
        "Anthropic (Claude)": ANTHROPIC_API_KEY,
        "Google (Gemini)": GOOGLE_API_KEY,
        "Perplexity": PERPLEXITY_API_KEY
    }

    all_set = True
    for name, key in keys.items():
        status = "✓ SET" if key and len(key) > 10 else "✗ MISSING"
        print(f"{name:25} {status}")
        if "MISSING" in status:
            all_set = False

    return all_set


async def test_agent(agent_type: str, config: dict):
    """Teste einzelnen Agent"""
    print(f"\n--- Testing: {agent_type} ---")
    print(f"Model: {config.get('model')}")
    print(f"Temperature: {config.get('temperature')}")

    try:
        # Erstelle Agent
        if agent_type == "content_creator":
            agent = ContentCreatorAgent()
        elif agent_type == "researcher":
            agent = ResearcherAgent()
        elif agent_type == "project_manager":
            agent = ProjectManagerAgent()
        else:
            # Nutze BaseAgent für andere
            agent = BaseAgent(
                agent_type=agent_type,
                custom_config=config
            )

        # Einfacher Test-Prompt
        prompt = f"Antworte mit genau einem Satz: Was ist deine Hauptaufgabe als {agent_type}?"

        response = await agent.think(prompt)

        # Zeige Ergebnis
        print(f"✓ SUCCESS")
        print(f"Response: {response[:150]}...")
        print(f"Tokens used: {agent.metrics['tokens_used']}")

        return True

    except Exception as e:
        print(f"✗ FAILED")
        print(f"Error: {str(e)}")
        return False


async def test_model_comparison():
    """Vergleiche Outputs verschiedener Modelle"""
    print("\n\n=== Model Comparison Test ===")

    prompt = "Erkläre in genau einem Satz was ein AI Agent ist."

    models_to_test = [
        ("GPT-4o-mini", "gpt-4o-mini"),
        ("Claude 3.5 Sonnet", "claude-3-5-sonnet-20241022"),
        ("Gemini 2.0 Flash", "gemini-2.0-flash-exp")
    ]

    results = []

    for name, model in models_to_test:
        print(f"\nTesting: {name}")
        try:
            agent = BaseAgent(
                agent_type="test",
                custom_config={
                    "model": model,
                    "temperature": 0.7
                }
            )

            response = await agent.think(prompt)

            result = {
                "model": name,
                "response": response,
                "tokens": agent.metrics["tokens_used"],
                "success": True
            }

            print(f"✓ {name}: {response[:80]}...")

        except Exception as e:
            result = {
                "model": name,
                "error": str(e),
                "success": False
            }
            print(f"✗ {name}: {str(e)}")

        results.append(result)

    return results


async def test_researcher_with_perplexity():
    """Teste Researcher Agent mit Perplexity"""
    print("\n\n=== Researcher Agent (Perplexity) Test ===")

    if not PERPLEXITY_API_KEY or len(PERPLEXITY_API_KEY) < 10:
        print("⚠ Perplexity API Key nicht gesetzt - überspringe Test")
        return False

    try:
        researcher = ResearcherAgent()

        result = await researcher.execute({
            "task_type": "quick_research",
            "topic": "Neueste AI Entwicklungen Januar 2025",
            "max_sources": 3
        })

        print("✓ Perplexity Recherche erfolgreich")
        print(f"Sources found: {len(result.get('sources', []))}")

        return True

    except Exception as e:
        print(f"✗ Perplexity Test failed: {str(e)}")
        return False


async def main():
    """Hauptfunktion - führe alle Tests aus"""
    print("=" * 60)
    print("J-Jeco AI Platform - LLM Model Tester")
    print("=" * 60)

    # 1. Prüfe API Keys
    if not check_api_keys():
        print("\n⚠ WARNING: Nicht alle API Keys sind gesetzt!")
        print("Bearbeite die .env Datei und füge fehlende Keys hinzu.")
        print("Fahre trotzdem mit Tests fort...\n")

    # 2. Teste alle konfigurierten Agents
    print("\n\n=== Testing All Configured Agents ===")

    results = {}
    for agent_type, config in AGENT_CONFIG.items():
        success = await test_agent(agent_type, config)
        results[agent_type] = success

    # 3. Model Vergleich
    comparison_results = await test_model_comparison()

    # 4. Teste Perplexity
    perplexity_works = await test_researcher_with_perplexity()

    # 5. Zusammenfassung
    print("\n\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    print("\nAgent Tests:")
    for agent_type, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {agent_type:20} {status}")

    successful_agents = sum(1 for success in results.values() if success)
    total_agents = len(results)

    print(f"\nTotal: {successful_agents}/{total_agents} agents working")

    if successful_agents == total_agents:
        print("\n🎉 Alle Agents funktionieren perfekt!")
    elif successful_agents > 0:
        print(f"\n⚠ {total_agents - successful_agents} Agent(s) haben Probleme")
    else:
        print("\n❌ Keine Agents funktionieren - prüfe deine API Keys!")

    print("\nModel Comparison:")
    for result in comparison_results:
        status = "✓" if result.get("success") else "✗"
        print(f"  {status} {result['model']}")

    if perplexity_works:
        print("\n✓ Perplexity Online-Recherche funktioniert")
    else:
        print("\n⚠ Perplexity nicht verfügbar (optional)")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
