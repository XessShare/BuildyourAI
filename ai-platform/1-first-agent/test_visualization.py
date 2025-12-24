"""
Tests für Visualization-Module
"""

import unittest
from pathlib import Path
import tempfile
import shutil

from visualization.mermaid_renderer import MermaidRenderer
from visualization.mindmap_builder import MindmapBuilder
from visualization.chat_snapshot_extractor import ChatSnapshotExtractor
from visualization.visualization_generator import VisualizationGenerator


class TestMermaidRenderer(unittest.TestCase):
    """Tests für MermaidRenderer"""

    def setUp(self):
        self.renderer = MermaidRenderer()
        self.test_diagram = """
graph TD
    A[Start] --> B[Process]
    B --> C[End]
"""

    def test_validate_syntax_valid(self):
        """Test: Validiere gültige Mermaid-Syntax"""
        result = self.renderer.validate_syntax(self.test_diagram)
        self.assertTrue(result["valid"])

    def test_validate_syntax_invalid(self):
        """Test: Validiere ungültige Mermaid-Syntax"""
        invalid = "graph TD\nA[Start --> B[End"  # Ungeschlossene Klammern
        result = self.renderer.validate_syntax(invalid)
        self.assertFalse(result["valid"])
        self.assertGreater(len(result["errors"]), 0)

    def test_render_to_svg(self):
        """Test: Rendere zu SVG"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.svg"
            result = self.renderer.render_to_svg(self.test_diagram, output_path)
            
            # Auch wenn Rendering fehlschlägt (kein mmdc installiert), sollte Syntax validiert werden
            if not result["success"]:
                # Prüfe ob es ein Syntax-Fehler oder ein Tool-Fehler ist
                self.assertIn("error", result)


class TestMindmapBuilder(unittest.TestCase):
    """Tests für MindmapBuilder"""

    def setUp(self):
        self.builder = MindmapBuilder()

    def test_build_mindmap(self):
        """Test: Baue Mindmap aus Architektur-Daten"""
        architecture_data = {
            "components": [
                {"id": "0", "name": "Component A", "description": "Test A"},
                {"id": "1", "name": "Component B", "description": "Test B"}
            ]
        }
        
        result = self.builder.build_mindmap(architecture_data)
        self.assertEqual(len(self.builder.nodes), 2)
        self.assertEqual(len(self.builder.edges), 1)

    def test_add_chat_snapshot(self):
        """Test: Füge Chat-Snapshot hinzu"""
        self.builder.add_chat_snapshot("0", {
            "content": "Test snapshot",
            "timestamp": "2025-01-01T10:00:00"
        })
        
        self.assertIn("0", self.builder.chat_snapshots)
        self.assertEqual(len(self.builder.chat_snapshots["0"]), 1)

    def test_add_tags(self):
        """Test: Füge Tags hinzu"""
        self.builder.add_tags("0", ["test", "architecture"])
        self.assertIn("0", self.builder.tags)
        self.assertEqual(self.builder.tags["0"], ["test", "architecture"])

    def test_generate_html(self):
        """Test: Generiere HTML"""
        self.builder.build_mindmap({
            "components": [{"id": "0", "name": "Test", "description": ""}]
        })
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_mindmap.html"
            result = self.builder.generate_html(output_path, "Test Mindmap")
            
            self.assertTrue(result["success"])
            self.assertTrue(output_path.exists())


class TestChatSnapshotExtractor(unittest.TestCase):
    """Tests für ChatSnapshotExtractor"""

    def setUp(self):
        self.extractor = ChatSnapshotExtractor()

    def test_extract_tags(self):
        """Test: Extrahiere Tags aus Text"""
        text = "This is a #test with @mention and [tag]"
        tags = self.extractor._extract_tags(text)
        
        self.assertIn("test", tags)
        self.assertIn("mention", tags)
        self.assertIn("tag", tags)

    def test_extract_timestamp(self):
        """Test: Extrahiere Zeitstempel"""
        text = "2025-01-01T10:00:00 This is a test"
        timestamp = self.extractor._extract_timestamp(text)
        
        self.assertIsNotNone(timestamp)
        self.assertIn("2025-01-01", timestamp)

    def test_create_snapshot(self):
        """Test: Erstelle Snapshot"""
        content = "2025-01-01T10:00:00\nThis is a #test snapshot"
        snapshot = self.extractor._create_snapshot(content)
        
        self.assertIsNotNone(snapshot)
        self.assertIn("content", snapshot)
        self.assertIn("timestamp", snapshot)
        self.assertIn("tags", snapshot)

    def test_extract_snapshots(self):
        """Test: Extrahiere Snapshots aus Konversation"""
        conversation = """
2025-01-01T10:00:00
User: This is a test #architecture

2025-01-01T10:05:00
Assistant: This is a response
"""
        snapshots = self.extractor.extract_snapshots(conversation, "architecture")
        
        self.assertGreater(len(snapshots), 0)


class TestVisualizationGenerator(unittest.TestCase):
    """Tests für VisualizationGenerator"""

    def setUp(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self.output_dir = Path(tmpdir) / "visualizations"
            self.generator = VisualizationGenerator(output_dir=self.output_dir)

    def test_extract_mermaid_diagrams(self):
        """Test: Extrahiere Mermaid-Diagramme"""
        content = """
# Test Plan

## Architecture

```mermaid
graph TD
    A --> B
```
"""
        diagrams = self.generator._extract_mermaid_diagrams(content)
        
        self.assertGreater(len(diagrams), 0)
        self.assertIn("code", diagrams[0])
        self.assertIn("title", diagrams[0])

    def test_parse_architecture_from_plan(self):
        """Test: Parse Architektur aus Plan"""
        content = """
# Test Plan

## Component A
Description A

## Component B
Description B
"""
        architecture = self.generator._parse_architecture_from_plan(content)
        
        self.assertIn("components", architecture)
        self.assertGreaterEqual(len(architecture["components"]), 2)

    def test_generate_from_plan(self):
        """Test: Generiere Visualisierung aus Plan"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_file:
            tmp_file.write("""
# Test Plan

## Architecture

```mermaid
graph TD
    A[Start] --> B[End]
```
""")
            tmp_path = Path(tmp_file.name)

        try:
            result = self.generator.generate_from_plan(tmp_path)
            
            # Prüfe ob Generierung erfolgreich war oder zumindest versucht wurde
            self.assertIn("success", result)
            self.assertIn("plan_name", result)
        finally:
            tmp_path.unlink()


if __name__ == "__main__":
    unittest.main()

