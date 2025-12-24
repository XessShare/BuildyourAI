"""
Plan Integration
Automatische Visualisierung bei Plan-Updates
"""

import asyncio
from pathlib import Path
from typing import Optional
import logging

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    Observer = None
    FileSystemEventHandler = None

from .visualization_generator import VisualizationGenerator

logger = logging.getLogger(__name__)


if WATCHDOG_AVAILABLE:
    class PlanFileHandler(FileSystemEventHandler):
        """Handler für Plan-Datei-Änderungen"""

        def __init__(self, generator: VisualizationGenerator):
            self.generator = generator

        def on_modified(self, event):
            """Wird aufgerufen wenn Datei geändert wird"""
            if event.is_directory:
                return

            file_path = Path(event.src_path)
            if file_path.suffix == '.md' and 'plan' in file_path.name.lower():
                logger.info(f"Plan-Datei geändert: {file_path}")
                self._generate_visualization(file_path)

        def on_created(self, event):
            """Wird aufgerufen wenn neue Datei erstellt wird"""
            if event.is_directory:
                return

            file_path = Path(event.src_path)
            if file_path.suffix == '.md' and 'plan' in file_path.name.lower():
                logger.info(f"Neue Plan-Datei erstellt: {file_path}")
                self._generate_visualization(file_path)

        def _generate_visualization(self, plan_path: Path):
            """Generiert Visualisierung für Plan"""
            try:
                result = self.generator.generate_from_plan(plan_path)
                if result.get("success"):
                    logger.info(f"Visualisierung erfolgreich generiert für: {plan_path}")
                else:
                    logger.warning(f"Visualisierung fehlgeschlagen: {result.get('error')}")
            except Exception as e:
                logger.error(f"Fehler beim Generieren der Visualisierung: {e}")
else:
    PlanFileHandler = None


def watch_plans_directory(plans_dir: Path, generator: Optional[VisualizationGenerator] = None):
    """
    Überwacht Plans-Verzeichnis und generiert automatisch Visualisierungen
    
    Args:
        plans_dir: Verzeichnis mit Plan-Dateien
        generator: Optional: VisualizationGenerator-Instanz
    """
    if not WATCHDOG_AVAILABLE:
        logger.error("watchdog ist nicht installiert. Installiere mit: pip install watchdog")
        return

    if generator is None:
        generator = VisualizationGenerator()

    # Erstelle Observer
    event_handler = PlanFileHandler(generator)
    observer = Observer()
    observer.schedule(event_handler, str(plans_dir), recursive=True)
    observer.start()

    logger.info(f"Überwache Plans-Verzeichnis: {plans_dir}")

    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def generate_visualizations_for_existing_plans(plans_dir: Path):
    """
    Generiert Visualisierungen für alle bestehenden Pläne
    
    Args:
        plans_dir: Verzeichnis mit Plan-Dateien
    """
    generator = VisualizationGenerator()
    result = generator.generate_all_from_plans_directory(plans_dir)
    
    logger.info(f"Verarbeitet: {result['plans_processed']} Pläne")
    logger.info(f"Erfolgreich: {result['plans_successful']}")
    logger.info(f"Fehlgeschlagen: {result['plans_failed']}")
    
    return result


if __name__ == "__main__":
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) > 1:
        plans_dir = Path(sys.argv[1])
    else:
        # Standard: .cursor/plans im Home-Verzeichnis
        plans_dir = Path.home() / ".cursor" / "plans"
    
    if not plans_dir.exists():
        print(f"Plans-Verzeichnis nicht gefunden: {plans_dir}")
        sys.exit(1)
    
    # Generiere Visualisierungen für bestehende Pläne
    print(f"Generiere Visualisierungen für Pläne in: {plans_dir}")
    result = generate_visualizations_for_existing_plans(plans_dir)
    
    print(f"\nErgebnis:")
    print(f"  Verarbeitet: {result['plans_processed']}")
    print(f"  Erfolgreich: {result['plans_successful']}")
    print(f"  Fehlgeschlagen: {result['plans_failed']}")

