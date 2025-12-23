"""
Praktische Beispiele: Verschiedene LLMs für verschiedene Tasks nutzen

Dieses Script zeigt wie man:
1. Verschiedene Modelle für verschiedene Aufgaben nutzt
2. Zwischen Modellen wechselt
3. Outputs vergleicht
4. Kosten optimiert
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from agents.content_creator_agent import ContentCreatorAgent
from agents.researcher_agent import ResearcherAgent
from agents.project_manager_agent import ProjectManagerAgent
from agents.base_agent import BaseAgent


# ============================================
# Beispiel 1: Multi-Model Content Pipeline
# ============================================

async def example_1_content_pipeline():
    """
    Nutze verschiedene LLMs für verschiedene Schritte
    einer Content-Erstellung
    """
    print("\n" + "=" * 60)
    print("BEISPIEL 1: Multi-Model Content Pipeline")
    print("=" * 60)

    topic = "Einführung in AI Agents für Anfänger"

    # Schritt 1: Recherche mit Perplexity (Online-Daten)
    print("\n[1/4] Recherche läuft (Perplexity)...")
    researcher = ResearcherAgent()
    research_result = await researcher.execute({
        "task_type": "quick_research",
        "topic": topic,
        "max_sources": 3
    })
    print(f"✓ Recherche abgeschlossen: {len(research_result.get('sources', []))} Quellen")

    # Schritt 2: Strategische Planung mit Claude (Analytisch)
    print("\n[2/4] Content-Planung läuft (Claude)...")
    pm = ProjectManagerAgent()
    plan_result = await pm.execute({
        "task_type": "create_content_plan",
        "topic": topic,
        "research_data": research_result
    })
    print("✓ Content-Plan erstellt")

    # Schritt 3: Script-Erstellung mit GPT (Kreativ)
    print("\n[3/4] Script wird geschrieben (GPT-4o-mini)...")
    creator = ContentCreatorAgent()
    script_result = await creator.execute({
        "task_type": "video_script",
        "topic": topic,
        "structure": plan_result.get("structure", []),
        "duration_minutes": 10
    })
    print("✓ Video-Script erstellt")

    # Schritt 4: Qualitätsprüfung mit Gemini (Multimodal Analysis)
    print("\n[4/4] Qualitätsprüfung läuft (Gemini)...")
    analyst = BaseAgent(
        agent_type="analyst",
        custom_config={
            "model": "gemini-2.0-flash-exp",
            "temperature": 0.3
        }
    )
    quality_check = await analyst.think(
        "Bewerte dieses Video-Script auf einer Skala von 1-10 und gib konkrete Verbesserungsvorschläge.",
        context=f"Script: {script_result.get('script', '')[:500]}..."
    )
    print("✓ Qualitätsprüfung abgeschlossen")

    # Zusammenfassung
    print("\n" + "-" * 60)
    print("Pipeline abgeschlossen!")
    print(f"Recherche: {len(research_result.get('sources', []))} Quellen")
    print(f"Plan: {len(plan_result.get('structure', []))} Abschnitte")
    print(f"Script Länge: {len(script_result.get('script', ''))} Zeichen")
    print(f"Quality Score: {quality_check[:100]}...")


# ============================================
# Beispiel 2: Model Comparison A/B Test
# ============================================

async def example_2_model_comparison():
    """
    Vergleiche wie verschiedene Modelle die gleiche
    Aufgabe lösen
    """
    print("\n" + "=" * 60)
    print("BEISPIEL 2: Model Comparison A/B Test")
    print("=" * 60)

    prompt = """Erkläre in 3 Sätzen was ein AI Agent ist und nenne ein
    praktisches Beispiel aus dem Alltag."""

    models = [
        ("GPT-4o-mini (günstig)", "gpt-4o-mini"),
        ("Claude 3.5 Sonnet (premium)", "claude-3-5-sonnet-20241022"),
        ("Gemini 2.0 Flash (schnell)", "gemini-2.0-flash-exp")
    ]

    results = {}

    for name, model in models:
        print(f"\nTeste: {name}")

        agent = BaseAgent(
            agent_type="test",
            custom_config={
                "model": model,
                "temperature": 0.7
            }
        )

        response = await agent.think(prompt)

        results[name] = {
            "response": response,
            "tokens": agent.metrics["tokens_used"],
            "model": model
        }

        print(f"Tokens: {agent.metrics['tokens_used']}")
        print(f"Response: {response[:100]}...")

    # Vergleich
    print("\n" + "-" * 60)
    print("Vergleich:")
    for name, data in results.items():
        print(f"\n{name}:")
        print(f"  {data['response']}")
        print(f"  Tokens: {data['tokens']}")


# ============================================
# Beispiel 3: Kostenoptimierte Batch-Verarbeitung
# ============================================

async def example_3_cost_optimized_batch():
    """
    Verarbeite viele Tasks kostenoptimiert
    """
    print("\n" + "=" * 60)
    print("BEISPIEL 3: Kostenoptimierte Batch-Verarbeitung")
    print("=" * 60)

    # Liste von Tasks
    tasks = [
        "5 Titel-Ideen für ein AI Tutorial",
        "3 Tags für ein Homelab Video",
        "Kurze Beschreibung für einen Newsletter",
        "5 Content-Ideen für nächste Woche",
        "Zusammenfassung der letzten AI News"
    ]

    print(f"\n{len(tasks)} Tasks zu verarbeiten...")
    print("Strategie: Nutze günstigstes Modell (Gemini Flash)")

    # Nutze das günstigste verfügbare Modell
    agent = BaseAgent(
        agent_type="content_creator",
        custom_config={
            "model": "gemini-2.0-flash-exp",  # Sehr günstig: $0.10/$0.30 per 1M tokens
            "temperature": 0.8
        }
    )

    results = []
    total_tokens = 0

    for i, task in enumerate(tasks, 1):
        print(f"\n[{i}/{len(tasks)}] {task[:50]}...")

        response = await agent.think(task)

        results.append({
            "task": task,
            "result": response
        })

        tokens = agent.metrics["tokens_used"]
        total_tokens += tokens
        print(f"✓ Fertig ({tokens} tokens)")

    # Kosten-Schätzung (Gemini: ~$0.10 input + $0.30 output per 1M tokens)
    estimated_cost_usd = (total_tokens / 1_000_000) * 0.20  # Durchschnitt
    estimated_cost_eur = estimated_cost_usd * 0.92  # ca. Umrechnung

    print("\n" + "-" * 60)
    print(f"Batch abgeschlossen!")
    print(f"Total Tokens: {total_tokens:,}")
    print(f"Geschätzte Kosten: ~${estimated_cost_usd:.4f} (€{estimated_cost_eur:.4f})")
    print(f"\nAlternativ mit GPT-4o würde kosten: ~${(total_tokens/1_000_000)*6:.4f}")


# ============================================
# Beispiel 4: Dynamischer Model-Switch
# ============================================

async def example_4_dynamic_model_switch():
    """
    Wechsle automatisch zu einem besseren Modell
    wenn die Aufgabe komplex ist
    """
    print("\n" + "=" * 60)
    print("BEISPIEL 4: Dynamischer Model-Switch")
    print("=" * 60)

    async def smart_agent_call(prompt: str, complexity: str = "simple"):
        """
        Wähle Modell basierend auf Komplexität
        """
        model_strategy = {
            "simple": "gemini-2.0-flash-exp",  # Günstig & schnell
            "medium": "gpt-4o-mini",           # Balance
            "complex": "claude-3-5-sonnet-20241022"  # Premium
        }

        model = model_strategy.get(complexity, "gpt-4o-mini")

        print(f"\nKomplexität: {complexity.upper()}")
        print(f"Gewähltes Modell: {model}")

        agent = BaseAgent(
            agent_type="dynamic",
            custom_config={
                "model": model,
                "temperature": 0.7
            }
        )

        return await agent.think(prompt)

    # Test 1: Simple Task
    simple_result = await smart_agent_call(
        "Nenne 3 AI Tools",
        complexity="simple"
    )
    print(f"Result: {simple_result[:80]}...")

    # Test 2: Medium Task
    medium_result = await smart_agent_call(
        "Erkläre den Unterschied zwischen Supervised und Unsupervised Learning",
        complexity="medium"
    )
    print(f"Result: {medium_result[:80]}...")

    # Test 3: Complex Task
    complex_result = await smart_agent_call(
        """Analysiere folgende Situation: Ein Startup möchte ein AI-basiertes
        System bauen. Welche Architektur empfiehlst du und warum?
        Berücksichtige Kosten, Skalierbarkeit und Wartbarkeit.""",
        complexity="complex"
    )
    print(f"Result: {complex_result[:80]}...")

    print("\n" + "-" * 60)
    print("Smart Model Selection spart Kosten bei einfachen Tasks")
    print("und nutzt Premium-Modelle nur wenn wirklich nötig!")


# ============================================
# Hauptfunktion
# ============================================

async def main():
    """Führe alle Beispiele aus"""
    print("\n")
    print("=" * 60)
    print("Multi-Model Workflow Examples")
    print("J-Jeco AI Platform")
    print("=" * 60)

    examples = [
        ("Content Pipeline", example_1_content_pipeline),
        ("Model Comparison", example_2_model_comparison),
        ("Cost Optimization", example_3_cost_optimized_batch),
        ("Dynamic Switching", example_4_dynamic_model_switch)
    ]

    print("\nVerfügbare Beispiele:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print("\nWähle ein Beispiel (1-4) oder 'all' für alle:")
    # Für dieses Demo-Script führen wir Beispiel 2 und 4 aus
    # In der Praxis kann der User hier auswählen

    # Beispiel 2 und 4 sind am schnellsten
    await example_2_model_comparison()
    await example_4_dynamic_model_switch()

    print("\n\n" + "=" * 60)
    print("Fertig! Weitere Beispiele in diesem File verfügbar.")
    print("Passe die main() Funktion an um andere Beispiele zu testen.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
