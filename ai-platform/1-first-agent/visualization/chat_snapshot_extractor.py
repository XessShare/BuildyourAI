"""
Chat Snapshot Extractor
Extrahiert relevante Chat-Abschnitte aus Konversationen
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ChatSnapshotExtractor:
    """
    Extrahiert relevante Chat-Snapshots aus Konversationen
    
    Features:
    - Extrahiert Abschnitte basierend auf Themen
    - Verknüpft Snapshots mit Architektur-Knoten
    - Speichert Kontext (Datum, Teilnehmer, Thema)
    """

    def __init__(self):
        self.snapshots: List[Dict[str, Any]] = []

    def extract_snapshots(
        self,
        conversation_history: str,
        architecture_topic: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Extrahiert relevante Chat-Snapshots aus Konversation
        
        Args:
            conversation_history: Vollständige Chat-Historie als String
            architecture_topic: Optional: Thema für Filterung
            
        Returns:
            Liste von Snapshots
        """
        snapshots = []

        # Teile Konversation in Abschnitte
        sections = self._split_into_sections(conversation_history)

        for section in sections:
            # Prüfe ob Abschnitt relevant ist
            if architecture_topic and not self._is_relevant(section, architecture_topic):
                continue

            snapshot = self._create_snapshot(section)
            if snapshot:
                snapshots.append(snapshot)

        self.snapshots = snapshots
        return snapshots

    def format_snapshot(self, snapshot: Dict[str, Any]) -> str:
        """
        Formatiert Snapshot für HTML-Einbettung
        
        Args:
            snapshot: Snapshot-Dict
            
        Returns:
            Formatierter HTML-String
        """
        timestamp = snapshot.get("timestamp", "")
        content = snapshot.get("content", "")
        tags = snapshot.get("tags", [])

        tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in tags])

        return f"""
        <div class="chat-snapshot" data-timestamp="{timestamp}" data-tags="{','.join(tags)}">
            <div class="snapshot-header">
                <span class="timestamp">{timestamp}</span>
                <div class="tags">{tags_html}</div>
            </div>
            <div class="snapshot-content">{self._escape_html(content)}</div>
        </div>
        """

    def link_to_node(self, snapshot: Dict[str, Any], mindmap_node_id: str) -> Dict[str, Any]:
        """
        Verknüpft Snapshot mit Mindmap-Knoten
        
        Args:
            snapshot: Snapshot-Dict
            mindmap_node_id: ID des Mindmap-Knotens
            
        Returns:
            Aktualisierter Snapshot mit node_id
        """
        snapshot["node_id"] = mindmap_node_id
        return snapshot

    def extract_from_plan_file(self, plan_file_path: Path) -> List[Dict[str, Any]]:
        """
        Extrahiert Snapshots aus Plan-Datei (falls Chat-Historie enthalten)
        
        Args:
            plan_file_path: Pfad zur Plan-Datei
            
        Returns:
            Liste von Snapshots
        """
        if not plan_file_path.exists():
            logger.warning(f"Plan-Datei nicht gefunden: {plan_file_path}")
            return []

        try:
            content = plan_file_path.read_text(encoding='utf-8')
            
            # Suche nach Chat-Abschnitten im Plan
            # Format: ```chat oder ähnliche Marker
            chat_pattern = r'```(?:chat|conversation|snapshot)\s*\n(.*?)```'
            matches = re.finditer(chat_pattern, content, re.DOTALL | re.IGNORECASE)

            snapshots = []
            for match in matches:
                snapshot = self._create_snapshot(match.group(1))
                if snapshot:
                    snapshots.append(snapshot)

            return snapshots

        except Exception as e:
            logger.error(f"Fehler beim Extrahieren aus Plan-Datei: {e}")
            return []

    def _split_into_sections(self, conversation: str) -> List[str]:
        """Teilt Konversation in logische Abschnitte"""
        # Teile nach Zeilenumbrüchen und Zeitstempeln
        sections = []

        # Suche nach Zeitstempeln oder Trennern
        lines = conversation.split('\n')
        current_section = []

        for line in lines:
            # Prüfe ob neue Sektion (Zeitstempel, Trennlinie, etc.)
            if self._is_section_break(line):
                if current_section:
                    sections.append('\n'.join(current_section))
                    current_section = []
            current_section.append(line)

        if current_section:
            sections.append('\n'.join(current_section))

        return sections if sections else [conversation]

    def _is_section_break(self, line: str) -> bool:
        """Prüft ob Zeile einen Sektionsbruch markiert"""
        # Zeitstempel-Format
        timestamp_pattern = r'\d{4}-\d{2}-\d{2}.*\d{2}:\d{2}'
        if re.search(timestamp_pattern, line):
            return True

        # Trennlinien
        if re.match(r'^[-=]{3,}$', line.strip()):
            return True

        # Markdown-Header
        if re.match(r'^#{1,6}\s', line):
            return True

        return False

    def _is_relevant(self, section: str, topic: str) -> bool:
        """Prüft ob Abschnitt für Thema relevant ist"""
        topic_lower = topic.lower()
        section_lower = section.lower()

        # Einfache Keyword-Suche
        keywords = topic_lower.split()
        return any(keyword in section_lower for keyword in keywords)

    def _create_snapshot(self, content: str) -> Optional[Dict[str, Any]]:
        """Erstellt Snapshot-Dict aus Inhalt"""
        if not content or len(content.strip()) < 10:
            return None

        # Extrahiere Zeitstempel
        timestamp = self._extract_timestamp(content)

        # Extrahiere Tags
        tags = self._extract_tags(content)

        return {
            "content": content.strip(),
            "timestamp": timestamp or datetime.now().isoformat(),
            "tags": tags,
            "length": len(content)
        }

    def _extract_timestamp(self, content: str) -> Optional[str]:
        """Extrahiert Zeitstempel aus Inhalt"""
        # Verschiedene Zeitstempel-Formate
        patterns = [
            r'(\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2})',
            r'(\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2})',
            r'(\d{2}\.\d{2}\.\d{4}[\sT]\d{2}:\d{2})',
        ]

        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)

        return None

    def _extract_tags(self, content: str) -> List[str]:
        """Extrahiert Tags aus Inhalt"""
        tags = []

        # Suche nach #hashtags
        hashtags = re.findall(r'#(\w+)', content)
        tags.extend(hashtags)

        # Suche nach @mentions
        mentions = re.findall(r'@(\w+)', content)
        tags.extend(mentions)

        # Suche nach [tags] oder (tags)
        bracket_tags = re.findall(r'\[(\w+)\]|\((\w+)\)', content)
        tags.extend([t[0] or t[1] for t in bracket_tags])

        return list(set(tags))  # Entferne Duplikate

    def _escape_html(self, text: str) -> str:
        """Escaped HTML-Sonderzeichen"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))

