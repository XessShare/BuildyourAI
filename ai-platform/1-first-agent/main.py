#!/usr/bin/env python3
"""
J-Jeco AI Platform - Main Orchestrator

Dein persönlicher AI-Assistent für Content-Creation, Newsletter,
und parallele Agent-Orchestrierung.

Usage:
    python main.py optimize-prompt "Ihr Prompt hier"
    python main.py plan-project "Projektbeschreibung"
    python main.py moonshot-check
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

from agents import ProjectManagerAgent, CommunicatorAgent
from config import OUTPUT_DIR


class JJecoOrchestrator:
    """
    Hauptsteuerung für alle J-Jeco Agenten

    Features:
    - Automatische Agent-Auswahl
    - Parallele Execution
    - Progress Tracking
    - Output Management
    """

    def __init__(self):
        self.pm_agent = None
        self.comm_agent = None
        self.agents_initialized = False

    async def initialize_agents(self):
        """Initialize all agents lazily"""
        if not self.agents_initialized:
            print("🚀 Initialisiere J-Jeco AI Agenten...")
            self.pm_agent = ProjectManagerAgent()
            self.comm_agent = CommunicatorAgent()
            self.agents_initialized = True
            print("✅ Agenten bereit!\n")

    async def optimize_prompt(self, prompt: str) -> str:
        """
        Optimize a user prompt for clarity

        Args:
            prompt: Original prompt

        Returns:
            Optimized prompt
        """
        await self.initialize_agents()

        print(f"📝 Original Prompt:\n{prompt}\n")
        print("🤔 Analysiere und optimiere...\n")

        optimized = await self.comm_agent.optimize_prompt(prompt)

        print(f"✨ Optimierter Prompt:\n{optimized}\n")

        # Save to file
        output_file = OUTPUT_DIR / "optimized_prompt.txt"
        output_file.write_text(f"ORIGINAL:\n{prompt}\n\nOPTIMIZED:\n{optimized}")
        print(f"💾 Gespeichert: {output_file}")

        return optimized

    async def plan_project(self, project_description: str, goals: Optional[list] = None):
        """
        Create action plan for a project

        Args:
            project_description: What to build
            goals: Optional list of goals
        """
        await self.initialize_agents()

        print(f"📋 Projekt: {project_description}\n")
        print("🎯 Erstelle Action Plan...\n")

        result = await self.pm_agent.execute({
            "project": project_description,
            "goals": goals or [],
        })

        print(f"📊 Action Plan:\n{result['action_plan']}\n")

        # Save to file
        output_file = OUTPUT_DIR / "action_plan.txt"
        output_file.write_text(result['action_plan'])
        print(f"💾 Gespeichert: {output_file}")

        return result

    async def moonshot_check(self):
        """Check progress towards moonshot goal"""
        await self.initialize_agents()

        print("🎯 Moonshot Progress Check\n")
        print("=" * 50)

        progress = await self.pm_agent.track_moonshot_progress()

        print(f"\n{progress['report']}\n")

        # Identify blockers
        print("\n🚧 Identifiziere Blocker...\n")
        blockers = await self.pm_agent.identify_blockers()

        for blocker in blockers[:5]:  # Top 5
            print(f"  - {blocker}")

        return progress

    async def simplify_technical(self, technical_text: str) -> str:
        """
        Simplify technical content for non-tech audience

        Args:
            technical_text: Technical explanation

        Returns:
            Simplified version
        """
        await self.initialize_agents()

        print(f"🔧 Technical:\n{technical_text}\n")
        print("🎨 Vereinfache für Non-Techs...\n")

        simplified = await self.comm_agent.simplify_for_non_tech(technical_text)

        print(f"✨ Simplified:\n{simplified}\n")

        return simplified

    async def interactive_mode(self):
        """Start interactive CLI mode"""
        await self.initialize_agents()

        print("""
╔═══════════════════════════════════════════════════╗
║     J-JECO AI PLATFORM - INTERACTIVE MODE         ║
║     Ihr Moonshot-Assistant ist bereit 🚀          ║
╚═══════════════════════════════════════════════════╝

Verfügbare Kommandos:
  1. optimize  - Prompt optimieren
  2. plan      - Projekt planen
  3. simplify  - Tech-Content vereinfachen
  4. moonshot  - Progress checken
  5. help      - Diese Hilfe anzeigen
  6. quit      - Beenden

""")

        while True:
            try:
                command = input("J-Jeco> ").strip().lower()

                if command == "quit" or command == "exit":
                    print("👋 Bis bald! Viel Erfolg mit Ihrem Moonshot!")
                    break

                elif command == "help":
                    print("\n[Hilfe wird angezeigt... (nicht implementiert in dieser Version)]")

                elif command == "optimize":
                    prompt = input("Ihr Prompt: ").strip()
                    if prompt:
                        await self.optimize_prompt(prompt)

                elif command == "plan":
                    project = input("Projektbeschreibung: ").strip()
                    if project:
                        await self.plan_project(project)

                elif command == "simplify":
                    tech_text = input("Technical Text: ").strip()
                    if tech_text:
                        await self.simplify_technical(tech_text)

                elif command == "moonshot":
                    await self.moonshot_check()

                else:
                    print(f"❌ Unbekanntes Kommando: {command}")
                    print("💡 Tippen Sie 'help' für Hilfe")

                print()  # Empty line for readability

            except KeyboardInterrupt:
                print("\n👋 Unterbrochen. Bis bald!")
                break
            except Exception as e:
                print(f"❌ Fehler: {str(e)}")


async def main():
    """Main entry point"""
    orchestrator = JJecoOrchestrator()

    if len(sys.argv) < 2:
        # No arguments - start interactive mode
        await orchestrator.interactive_mode()
        return

    command = sys.argv[1].lower()

    if command == "optimize-prompt" and len(sys.argv) > 2:
        prompt = " ".join(sys.argv[2:])
        await orchestrator.optimize_prompt(prompt)

    elif command == "plan-project" and len(sys.argv) > 2:
        project = " ".join(sys.argv[2:])
        await orchestrator.plan_project(project)

    elif command == "moonshot-check":
        await orchestrator.moonshot_check()

    elif command == "simplify" and len(sys.argv) > 2:
        text = " ".join(sys.argv[2:])
        await orchestrator.simplify_technical(text)

    elif command == "interactive" or command == "-i":
        await orchestrator.interactive_mode()

    else:
        print("""
J-Jeco AI Platform - Usage:

  python main.py                              Start interactive mode
  python main.py optimize-prompt "..."        Optimize a prompt
  python main.py plan-project "..."           Plan a project
  python main.py simplify "..."               Simplify technical text
  python main.py moonshot-check               Check moonshot progress
  python main.py interactive                  Interactive mode

Examples:
  python main.py optimize-prompt "mach mal content"
  python main.py plan-project "Erstes Tutorial-Video erstellen"
  python main.py moonshot-check
""")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Beendet.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
