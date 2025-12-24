#!/usr/bin/env python3
"""
CLI-Tool zum Generieren von Visualisierungen aus Plan-Dateien

Usage:
    python generate_visualizations.py [plan_file_or_directory]
    
Ohne Argumente werden alle Pläne im Standard-Verzeichnis verarbeitet.
"""

import sys
import argparse
from pathlib import Path
import logging

from visualization.visualization_generator import VisualizationGenerator
from visualization.plan_integration import generate_visualizations_for_existing_plans

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Generiere Visualisierungen aus Plan-Dateien"
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Pfad zu Plan-Datei oder Verzeichnis mit Plänen"
    )
    parser.add_argument(
        "--output-dir",
        help="Ausgabe-Verzeichnis (Standard: docs/visualizations/)"
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Überwache Verzeichnis auf Änderungen"
    )

    args = parser.parse_args()

    # Bestimme Eingabe-Pfad
    if args.path:
        input_path = Path(args.path)
    else:
        # Standard: .cursor/plans im Home-Verzeichnis
        input_path = Path.home() / ".cursor" / "plans"

    if not input_path.exists():
        logger.error(f"Pfad nicht gefunden: {input_path}")
        sys.exit(1)

    # Initialisiere Generator
    output_dir = Path(args.output_dir) if args.output_dir else None
    generator = VisualizationGenerator(output_dir=output_dir)

    # Verarbeite Eingabe
    if input_path.is_file():
        # Einzelne Datei
        logger.info(f"Generiere Visualisierung für: {input_path}")
        result = generator.generate_from_plan(input_path)
        
        if result.get("success"):
            logger.info("✅ Visualisierung erfolgreich generiert")
            logger.info(f"   Mermaid-Diagramme: {len(result.get('mermaid_diagrams', []))}")
            if result.get("mindmap", {}).get("success"):
                logger.info(f"   Mindmap: {result['mindmap']['output_path']}")
        else:
            logger.error(f"❌ Fehler: {result.get('error')}")
            sys.exit(1)

    elif input_path.is_dir():
        # Verzeichnis
        if args.watch:
            logger.info(f"Überwache Verzeichnis: {input_path}")
            try:
                from visualization.plan_integration import watch_plans_directory
                watch_plans_directory(input_path, generator)
            except ImportError:
                logger.error("watchdog ist nicht installiert. Installiere mit: pip install watchdog")
                sys.exit(1)
        else:
            logger.info(f"Generiere Visualisierungen für alle Pläne in: {input_path}")
            result = generate_visualizations_for_existing_plans(input_path)
            
            logger.info(f"\n📊 Ergebnis:")
            logger.info(f"   Verarbeitet: {result['plans_processed']}")
            logger.info(f"   Erfolgreich: {result['plans_successful']}")
            logger.info(f"   Fehlgeschlagen: {result['plans_failed']}")
            
            if result['plans_failed'] > 0:
                logger.warning("\n⚠️  Einige Pläne konnten nicht verarbeitet werden:")
                for item in result['results']:
                    if not item['result'].get('success'):
                        logger.warning(f"   - {item['file']}: {item['result'].get('error')}")

    else:
        logger.error(f"Ungültiger Pfad: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()

