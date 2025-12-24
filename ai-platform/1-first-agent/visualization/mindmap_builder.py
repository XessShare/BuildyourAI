"""
Mindmap Builder
Generiert interaktive HTML-Mindmaps mit Chat-Snapshots und Tags
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MindmapBuilder:
    """
    Erstellt interaktive HTML-Mindmaps
    
    Features:
    - Interaktive Navigation mit vis.js Network
    - Eingebettete Chat-Snapshots
    - Tag-Filter
    - Suchfunktion
    """

    def __init__(self):
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []
        self.chat_snapshots: Dict[str, List[Dict[str, Any]]] = {}
        self.tags: Dict[str, List[str]] = {}

    def build_mindmap(
        self,
        architecture_data: Dict[str, Any],
        chat_snapshots: Optional[Dict[str, List[Dict[str, Any]]]] = None,
        tags: Optional[Dict[str, List[str]]] = None
    ) -> 'MindmapBuilder':
        """
        Erstellt Mindmap aus Architektur-Daten
        
        Args:
            architecture_data: Dict mit Architektur-Informationen
            chat_snapshots: Optional Dict mit Chat-Snapshots pro Knoten
            tags: Optional Dict mit Tags pro Knoten
            
        Returns:
            self für Method-Chaining
        """
        self.chat_snapshots = chat_snapshots or {}
        self.tags = tags or {}

        # Extrahiere Knoten und Kanten aus Architektur-Daten
        if "nodes" in architecture_data:
            self.nodes = architecture_data["nodes"]
        else:
            # Generiere Knoten aus Struktur
            self.nodes = self._extract_nodes_from_structure(architecture_data)

        if "edges" in architecture_data:
            self.edges = architecture_data["edges"]
        else:
            # Generiere Kanten aus Struktur
            self.edges = self._extract_edges_from_structure(architecture_data)

        return self

    def add_chat_snapshot(self, node_id: str, snapshot: Dict[str, Any]) -> 'MindmapBuilder':
        """
        Fügt Chat-Snapshot zu einem Knoten hinzu
        
        Args:
            node_id: ID des Knotens
            snapshot: Dict mit Snapshot-Daten
            
        Returns:
            self für Method-Chaining
        """
        if node_id not in self.chat_snapshots:
            self.chat_snapshots[node_id] = []
        
        self.chat_snapshots[node_id].append(snapshot)
        return self

    def add_tags(self, node_id: str, tags: List[str]) -> 'MindmapBuilder':
        """
        Fügt Tags zu einem Knoten hinzu
        
        Args:
            node_id: ID des Knotens
            tags: Liste von Tags
            
        Returns:
            self für Method-Chaining
        """
        self.tags[node_id] = tags
        return self

    def generate_html(self, output_path: Path, title: str = "Architektur Mindmap") -> Dict[str, Any]:
        """
        Generiert HTML-Datei mit interaktiver Mindmap
        
        Args:
            output_path: Pfad für HTML-Ausgabe
            title: Titel der Mindmap
            
        Returns:
            Dict mit 'success' (bool), 'output_path' (Optional[Path]), 'error' (Optional[str])
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Lade Template
            template_path = Path(__file__).parent.parent / "docs" / "visualizations" / "templates" / "mindmap_template.html"
            
            if template_path.exists():
                html_content = template_path.read_text(encoding='utf-8')
            else:
                # Fallback: Generiere Template inline
                html_content = self._generate_template_html()

            # Ersetze Platzhalter
            html_content = html_content.replace("{{TITLE}}", title)
            html_content = html_content.replace("{{NODES}}", json.dumps(self.nodes, indent=2, ensure_ascii=False))
            html_content = html_content.replace("{{EDGES}}", json.dumps(self.edges, indent=2, ensure_ascii=False))
            html_content = html_content.replace("{{CHAT_SNAPSHOTS}}", json.dumps(self.chat_snapshots, indent=2, ensure_ascii=False))
            html_content = html_content.replace("{{TAGS}}", json.dumps(self.tags, indent=2, ensure_ascii=False))
            html_content = html_content.replace("{{GENERATED_AT}}", datetime.now().isoformat())

            output_path.write_text(html_content, encoding='utf-8')

            return {
                "success": True,
                "output_path": output_path
            }

        except Exception as e:
            logger.error(f"Fehler beim Generieren der Mindmap: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _extract_nodes_from_structure(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extrahiert Knoten aus Architektur-Struktur"""
        nodes = []
        node_id = 0

        # Wenn es eine Hierarchie gibt
        if "components" in data:
            for component in data["components"]:
                nodes.append({
                    "id": str(node_id),
                    "label": component.get("name", f"Component {node_id}"),
                    "title": component.get("description", ""),
                    "group": component.get("group", "default")
                })
                node_id += 1

        # Wenn es eine einfache Liste gibt
        elif isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    nodes.append({
                        "id": str(node_id),
                        "label": key,
                        "title": str(value)[:100] if isinstance(value, dict) else "",
                        "group": "default"
                    })
                    node_id += 1

        # Fallback: Erstelle einen Root-Knoten
        if not nodes:
            nodes.append({
                "id": "0",
                "label": data.get("title", "Root"),
                "title": data.get("description", ""),
                "group": "root"
            })

        return nodes

    def _extract_edges_from_structure(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extrahiert Kanten aus Architektur-Struktur"""
        edges = []

        # Wenn es explizite Verbindungen gibt
        if "connections" in data:
            for i, connection in enumerate(data["connections"]):
                edges.append({
                    "id": f"e{i}",
                    "from": str(connection.get("from", 0)),
                    "to": str(connection.get("to", 1)),
                    "label": connection.get("label", "")
                })

        # Generiere Kanten zwischen aufeinanderfolgenden Knoten
        elif "components" in data:
            for i in range(len(data["components"]) - 1):
                edges.append({
                    "id": f"e{i}",
                    "from": str(i),
                    "to": str(i + 1)
                })

        return edges

    def _generate_template_html(self) -> str:
        """Generiert HTML-Template inline"""
        return """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}}</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        #mindmap-container {
            width: 100%;
            height: 600px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 8px;
        }
        .controls {
            margin-bottom: 20px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .tag-filter {
            padding: 8px 16px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
        }
        .tag-filter.active {
            background: #007bff;
            color: white;
        }
        .chat-snapshot {
            margin: 20px 0;
            padding: 15px;
            background: #f9f9f9;
            border-left: 4px solid #007bff;
            border-radius: 4px;
        }
        .snapshot-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 0.9em;
            color: #666;
        }
        .snapshot-content {
            white-space: pre-wrap;
        }
        .tags {
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
        }
        .tag {
            padding: 2px 8px;
            background: #e3f2fd;
            border-radius: 3px;
            font-size: 0.85em;
        }
    </style>
</head>
<body>
    <h1>{{TITLE}}</h1>
    <div class="controls">
        <input type="text" id="search" placeholder="Suche..." style="padding: 8px; flex: 1; max-width: 300px;">
        <div id="tag-filters" class="tags"></div>
    </div>
    <div id="mindmap-container"></div>
    <div id="chat-snapshots"></div>

    <script type="text/javascript">
        // Daten
        const nodes = new vis.DataSet({{NODES}});
        const edges = new vis.DataSet({{EDGES}});
        const chatSnapshots = {{CHAT_SNAPSHOTS}};
        const tags = {{TAGS}};

        // Netzwerk erstellen
        const container = document.getElementById('mindmap-container');
        const data = { nodes: nodes, edges: edges };
        const options = {
            nodes: {
                shape: 'box',
                font: { size: 14 },
                borderWidth: 2,
                shadow: true
            },
            edges: {
                arrows: { to: { enabled: true } },
                smooth: { type: 'continuous' }
            },
            layout: {
                hierarchical: {
                    direction: 'UD',
                    sortMethod: 'directed'
                }
            },
            physics: {
                enabled: true,
                stabilization: { iterations: 200 }
            }
        };

        const network = new vis.Network(container, data, options);

        // Chat-Snapshots anzeigen wenn Knoten geklickt wird
        network.on("click", function (params) {
            if (params.nodes.length > 0) {
                const nodeId = params.nodes[0];
                displayChatSnapshots(nodeId);
            }
        });

        function displayChatSnapshots(nodeId) {
            const container = document.getElementById('chat-snapshots');
            const snapshots = chatSnapshots[nodeId] || [];
            
            if (snapshots.length === 0) {
                container.innerHTML = '<p>Keine Chat-Snapshots für diesen Knoten.</p>';
                return;
            }

            let html = '<h2>Chat-Snapshots</h2>';
            snapshots.forEach((snapshot, index) => {
                html += `
                    <div class="chat-snapshot" data-timestamp="${snapshot.timestamp || ''}" data-tags="${(snapshot.tags || []).join(',')}">
                        <div class="snapshot-header">
                            <span class="timestamp">${snapshot.timestamp || ''}</span>
                            <div class="tags">
                                ${(snapshot.tags || []).map(tag => `<span class="tag">${tag}</span>`).join('')}
                            </div>
                        </div>
                        <div class="snapshot-content">${escapeHtml(snapshot.content || '')}</div>
                    </div>
                `;
            });
            container.innerHTML = html;
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // Tag-Filter
        const allTags = new Set();
        Object.values(tags).forEach(tagList => {
            tagList.forEach(tag => allTags.add(tag));
        });

        const tagFiltersContainer = document.getElementById('tag-filters');
        allTags.forEach(tag => {
            const button = document.createElement('button');
            button.className = 'tag-filter';
            button.textContent = tag;
            button.onclick = () => filterByTag(tag, button);
            tagFiltersContainer.appendChild(button);
        });

        function filterByTag(tag, button) {
            button.classList.toggle('active');
            const activeTags = Array.from(document.querySelectorAll('.tag-filter.active'))
                .map(btn => btn.textContent);
            
            if (activeTags.length === 0) {
                nodes.forEach(node => node.hidden = false);
            } else {
                nodes.forEach(node => {
                    const nodeTags = tags[node.id] || [];
                    node.hidden = !activeTags.some(t => nodeTags.includes(t));
                });
            }
        }

        // Suche
        document.getElementById('search').addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            nodes.forEach(node => {
                node.hidden = !node.label.toLowerCase().includes(query);
            });
        });
    </script>
</body>
</html>"""

