#!/usr/bin/env python3
"""
Interaktives CLI um direkt mit verschiedenen LLMs zu chatten
Nützlich zum schnellen Testen verschiedener Modelle

Usage:
    python chat_with_model.py
    python chat_with_model.py --model claude-3-5-sonnet-20241022
    python chat_with_model.py --model gemini-2.0-flash-exp
"""

import asyncio
import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from agents.base_agent import BaseAgent
from config import AGENT_CONFIG


AVAILABLE_MODELS = {
    "1": ("GPT-4o", "gpt-4o"),
    "2": ("GPT-4o-mini (günstig)", "gpt-4o-mini"),
    "3": ("Claude 3.5 Sonnet", "claude-3-5-sonnet-20241022"),
    "4": ("Gemini 2.0 Flash", "gemini-2.0-flash-exp"),
}


def print_header():
    """Zeige Header"""
    print("\n" + "=" * 60)
    print("  J-Jeco AI Platform - Interactive Model Chat")
    print("=" * 60 + "\n")


def select_model() -> str:
    """Lasse User ein Modell wählen"""
    print("Verfügbare Modelle:\n")

    for key, (name, model_id) in AVAILABLE_MODELS.items():
        print(f"  {key}. {name}")

    print("\n  5. Custom (eigenes Modell eingeben)")
    print("  q. Beenden\n")

    while True:
        choice = input("Wähle ein Modell (1-5): ").strip()

        if choice.lower() == 'q':
            print("Auf Wiedersehen!")
            sys.exit(0)

        if choice in AVAILABLE_MODELS:
            _, model_id = AVAILABLE_MODELS[choice]
            return model_id

        if choice == "5":
            custom = input("Modell-Name eingeben: ").strip()
            return custom

        print("Ungültige Auswahl. Bitte 1-5 wählen.")


async def chat_loop(model: str):
    """Hauptchat-Loop"""
    print(f"\n✓ Verbinde mit {model}...\n")

    # Erstelle Agent
    agent = BaseAgent(
        agent_type="chat",
        custom_config={
            "model": model,
            "temperature": 0.7
        }
    )

    print("Chat gestartet! Kommandos:")
    print("  /clear  - Lösche Conversation Memory")
    print("  /stats  - Zeige Statistiken")
    print("  /switch - Wechsle Modell")
    print("  /quit   - Beenden")
    print("\n" + "-" * 60 + "\n")

    while True:
        try:
            # User Input
            user_input = input("Du: ").strip()

            if not user_input:
                continue

            # Kommandos
            if user_input.lower() == '/quit':
                print("\nAuf Wiedersehen!")
                break

            if user_input.lower() == '/clear':
                agent.clear_memory()
                print("✓ Memory gelöscht\n")
                continue

            if user_input.lower() == '/stats':
                metrics = agent.get_metrics()
                print(f"\nStatistiken:")
                print(f"  Modell: {model}")
                print(f"  Tasks: {metrics['tasks_completed']}")
                print(f"  Tokens: {metrics['tokens_used']:,}")
                print(f"  Memory: {metrics['memory_size']} Nachrichten")
                print(f"  Errors: {metrics['errors']}")
                print()
                continue

            if user_input.lower() == '/switch':
                return True  # Signal zum Modellwechsel

            # Normaler Chat
            print(f"{model}: ", end="", flush=True)

            response = await agent.think(user_input)

            print(response + "\n")

        except KeyboardInterrupt:
            print("\n\nChat unterbrochen. /quit zum Beenden.")
            continue

        except Exception as e:
            print(f"\n❌ Fehler: {str(e)}\n")
            continue

    return False


async def main(args):
    """Hauptfunktion"""
    print_header()

    # Modell auswählen
    if args.model:
        model = args.model
        print(f"Nutze Modell: {model}")
    else:
        model = select_model()

    print(f"\nGewähltes Modell: {model}")

    # Chat starten
    while True:
        should_switch = await chat_loop(model)

        if should_switch:
            print("\n")
            model = select_model()
            print(f"\nWechsle zu: {model}\n")
        else:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat mit verschiedenen AI Modellen")
    parser.add_argument(
        "--model",
        type=str,
        help="Modell-Name (z.B. gpt-4o-mini, claude-3-5-sonnet-20241022)"
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="Zeige verfügbare Modelle"
    )

    args = parser.parse_args()

    if args.list_models:
        print("\nVerfügbare Modelle:")
        for _, (name, model_id) in AVAILABLE_MODELS.items():
            print(f"  - {model_id} ({name})")
        print()
        sys.exit(0)

    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print("\n\nProgramm beendet.")
        sys.exit(0)
