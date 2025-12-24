"""
Visualization Generator
Hauptklasse für automatische Visualisierung von Architekturübersichten
"""

import re
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

from .mermaid_renderer import MermaidRenderer
from .mindmap_builder import MindmapBuilder
from .chat_snapshot_extractor import ChatSnapshotExtractor

logger = logging.getLogger(__name__)


class VisualizationGenerator:
    """
    Generiert Visualisierungen aus Plan-Dateien
    
    Features:
    - Extrahiert Mermaid-Diagramme aus Plänen
    - Generiert SVG/PNG Bilder
    - Erstellt interaktive Mindmaps
    - Integriert Chat-Snapshots
    """

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialisiert VisualizationGenerator
        
        Args:
            output_dir: Optional: Ausgabe-Verzeichnis (Standard: docs/visualizations/)
        """
        # Bestimme Base-Dir relativ zu diesem Modul
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = output_dir or (self.base_dir / "docs" / "visualizations")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.mermaid_renderer = MermaidRenderer()
        self.mindmap_builder = MindmapBuilder()
        self.snapshot_extractor = ChatSnapshotExtractor()

    def generate_from_plan(self, plan_file_path: Path) -> Dict[str, Any]:
        """
        Generiert Visualisierungen aus Plan-Datei
        
        Args:
            plan_file_path: Pfad zur Plan-Datei
            
        Returns:
            Dict mit Generierungs-Ergebnissen
        """
        if not plan_file_path.exists():
            return {
                "success": False,
                "error": f"Plan-Datei nicht gefunden: {plan_file_path}"
            }

        try:
            plan_content = plan_file_path.read_text(encoding='utf-8')
            plan_name = plan_file_path.stem

            # Extrahiere Mermaid-Diagramme
            mermaid_diagrams = self._extract_mermaid_diagrams(plan_content)

            results = {
                "plan_name": plan_name,
                "mermaid_diagrams": [],
                "mindmap": None,
                "success": True
            }

            # Generiere Mermaid-Visualisierungen
            for i, diagram in enumerate(mermaid_diagrams):
                diagram_result = self._generate_mermaid_visualization(
                    diagram, plan_name, index=i
                )
                results["mermaid_diagrams"].append(diagram_result)

            # Generiere Mindmap
            mindmap_result = self._generate_mindmap(
                plan_content, plan_name, mermaid_diagrams, plan_file_path
            )
            results["mindmap"] = mindmap_result

            return results

        except Exception as e:
            logger.error(f"Fehler beim Generieren von Visualisierungen: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _extract_mermaid_diagrams(self, content: str) -> List[Dict[str, Any]]:
        """
        Extrahiert Mermaid-Diagramme aus Text
        
        Args:
            content: Text-Inhalt
            
        Returns:
            Liste von Diagramm-Dicts mit 'code' und 'title'
        """
        diagrams = []

        # Suche nach ```mermaid Blöcken
        pattern = r'```mermaid\s*\n(.*?)```'
        matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)

        for i, match in enumerate(matches):
            diagram_code = match.group(1).strip()
            
            # Versuche Titel aus vorherigen Zeilen zu extrahieren
            title = self._extract_diagram_title(content, match.start())
            
            diagrams.append({
                "code": diagram_code,
                "title": title or f"Diagram {i + 1}",
                "index": i
            })

        return diagrams

    def _extract_diagram_title(self, content: str, diagram_start: int) -> Optional[str]:
        """Extrahiert Titel für Diagramm aus umgebendem Text"""
        # Suche nach Header vor Diagramm
        before_diagram = content[:diagram_start]
        
        # Suche nach letztem Header (## oder ###)
        header_pattern = r'^#{2,3}\s+(.+)$'
        headers = re.findall(header_pattern, before_diagram, re.MULTILINE)
        
        if headers:
            return headers[-1].strip()
        
        return None

    def _generate_mermaid_visualization(
        self,
        diagram: Dict[str, Any],
        plan_name: str,
        index: int = 0
    ) -> Dict[str, Any]:
        """
        Generiert SVG/PNG aus Mermaid-Diagramm
        
        Args:
            diagram: Diagramm-Dict mit 'code' und 'title'
            plan_name: Name des Plans
            index: Index des Diagramms
            
        Returns:
            Dict mit Generierungs-Ergebnissen
        """
        diagram_name = f"{plan_name}_diagram_{index}"
        
        # Generiere SVG
        svg_path = self.output_dir / f"{diagram_name}.svg"
        svg_result = self.mermaid_renderer.render_to_svg(
            diagram["code"],
            svg_path
        )

        # Generiere PNG (optional)
        png_path = self.output_dir / f"{diagram_name}.png"
        png_result = self.mermaid_renderer.render_to_png(
            diagram["code"],
            png_path
        )

        return {
            "title": diagram["title"],
            "index": index,
            "svg": svg_result,
            "png": png_result
        }

    def _generate_mindmap(
        self,
        plan_content: str,
        plan_name: str,
        mermaid_diagrams: List[Dict[str, Any]],
        plan_file_path: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Generiert Mindmap aus Plan-Inhalt
        
        Args:
            plan_content: Vollständiger Plan-Inhalt
            plan_name: Name des Plans
            mermaid_diagrams: Liste von Mermaid-Diagrammen
            plan_file_path: Optional: Pfad zur Plan-Datei für Snapshot-Extraktion
            
        Returns:
            Dict mit Generierungs-Ergebnissen
        """
        # Extrahiere Architektur-Daten aus Plan
        architecture_data = self._parse_architecture_from_plan(plan_content)

        # Extrahiere Chat-Snapshots
        chat_snapshots = []
        if plan_file_path and plan_file_path.exists():
            chat_snapshots = self.snapshot_extractor.extract_from_plan_file(plan_file_path)

        # Organisiere Snapshots nach Knoten
        snapshots_by_node = self._organize_snapshots_by_node(chat_snapshots, architecture_data)

        # Extrahiere Tags
        tags = self._extract_tags_from_plan(plan_content, architecture_data)

        # Baue Mindmap
        mindmap_path = self.output_dir / f"{plan_name}_mindmap.html"
        
        self.mindmap_builder.build_mindmap(
            architecture_data,
            chat_snapshots=snapshots_by_node,
            tags=tags
        )

        result = self.mindmap_builder.generate_html(
            mindmap_path,
            title=f"Architektur Mindmap - {plan_name}"
        )

        return result

    def _parse_architecture_from_plan(self, plan_content: str) -> Dict[str, Any]:
        """Parst Architektur-Daten aus Plan-Inhalt"""
        # Extrahiere Komponenten aus Plan-Struktur
        components = []

        # Suche nach Sektionen (## oder ###)
        section_pattern = r'^#{2,3}\s+(.+)$'
        sections = re.findall(section_pattern, plan_content, re.MULTILINE)

        for i, section_title in enumerate(sections):
            components.append({
                "id": str(i),
                "name": section_title.strip(),
                "description": "",
                "group": "section"
            })

        # Wenn keine Sektionen gefunden, erstelle Root-Knoten
        if not components:
            # Versuche Titel zu extrahieren
            title_match = re.search(r'^#\s+(.+)$', plan_content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else "Root"

            components.append({
                "id": "0",
                "name": title,
                "description": "",
                "group": "root"
            })

        return {
            "components": components,
            "connections": self._generate_connections(components)
        }

    def _generate_connections(self, components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generiert Verbindungen zwischen Komponenten"""
        connections = []
        for i in range(len(components) - 1):
            connections.append({
                "from": components[i]["id"],
                "to": components[i + 1]["id"]
            })
        return connections

    def _organize_snapshots_by_node(
        self,
        snapshots: List[Dict[str, Any]],
        architecture_data: Dict[str, Any]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Organisiert Snapshots nach Knoten"""
        snapshots_by_node = {}

        # Ordne Snapshots Knoten zu basierend auf Inhalt
        for snapshot in snapshots:
            content = snapshot.get("content", "").lower()
            
            # Finde passenden Knoten
            node_id = self._find_matching_node(content, architecture_data)
            
            if node_id not in snapshots_by_node:
                snapshots_by_node[node_id] = []
            
            snapshots_by_node[node_id].append(snapshot)

        return snapshots_by_node

    def _find_matching_node(
        self,
        content: str,
        architecture_data: Dict[str, Any]
    ) -> str:
        """Findet passenden Knoten für Snapshot"""
        components = architecture_data.get("components", [])
        
        # Suche nach Keyword-Matches
        for component in components:
            name = component.get("name", "").lower()
            if name in content or any(word in content for word in name.split()):
                return component["id"]

        # Fallback: Erster Knoten
        return components[0]["id"] if components else "0"

    def _extract_tags_from_plan(
        self,
        plan_content: str,
        architecture_data: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Extrahiert Tags aus Plan und ordnet sie Knoten zu"""
        tags_by_node = {}

        # Extrahiere alle Tags aus Plan
        all_tags = self.snapshot_extractor._extract_tags(plan_content)

        # Ordne Tags Knoten zu
        components = architecture_data.get("components", [])
        for component in components:
            node_id = component["id"]
            name = component.get("name", "").lower()
            
            # Finde relevante Tags
            relevant_tags = [
                tag for tag in all_tags
                if tag.lower() in name or name in tag.lower()
            ]
            
            tags_by_node[node_id] = relevant_tags if relevant_tags else []

        return tags_by_node

    def generate_all_from_plans_directory(self, plans_dir: Path) -> Dict[str, Any]:
        """
        Generiert Visualisierungen für alle Pläne in einem Verzeichnis
        
        Args:
            plans_dir: Verzeichnis mit Plan-Dateien
            
        Returns:
            Dict mit Ergebnissen für alle Pläne
        """
        results = {
            "plans_processed": 0,
            "plans_successful": 0,
            "plans_failed": 0,
            "results": []
        }

        if not plans_dir.exists():
            return {
                **results,
                "error": f"Plans-Verzeichnis nicht gefunden: {plans_dir}"
            }

        # Finde alle .plan.md Dateien
        plan_files = list(plans_dir.glob("*.plan.md"))
        plan_files.extend(plans_dir.glob("**/*.plan.md"))

        for plan_file in plan_files:
            results["plans_processed"] += 1
            
            result = self.generate_from_plan(plan_file)
            
            if result.get("success"):
                results["plans_successful"] += 1
            else:
                results["plans_failed"] += 1
            
            results["results"].append({
                "file": str(plan_file),
                "result": result
            })

        return results

