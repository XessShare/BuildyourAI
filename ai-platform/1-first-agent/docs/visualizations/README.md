# Architektur Visualisierungen

Dieses Verzeichnis enthält automatisch generierte Visualisierungen von Architekturübersichten aus Plan-Dateien.

## Inhalt

- **SVG/PNG Bilder**: Statische Mermaid-Diagramme
- **HTML Mindmaps**: Interaktive Mindmaps mit Chat-Snapshots
- **index.html**: Übersichtsseite aller Visualisierungen

## Verwendung

### Automatische Generierung

Visualisierungen werden automatisch generiert, wenn:
- Ein neuer Plan erstellt wird
- Ein bestehender Plan aktualisiert wird
- Das `generate_visualizations.py` Script ausgeführt wird

### Manuelle Generierung

```bash
# Einzelne Plan-Datei
python generate_visualizations.py /path/to/plan.plan.md

# Alle Pläne in einem Verzeichnis
python generate_visualizations.py /path/to/plans/

# Standard-Verzeichnis (.cursor/plans)
python generate_visualizations.py
```

### Verzeichnis überwachen

```bash
# Überwache Verzeichnis auf Änderungen
python generate_visualizations.py /path/to/plans/ --watch
```

## Features

### Mermaid-Diagramme

- Automatische Extraktion aus Plan-Dateien
- Export als SVG und PNG
- Syntax-Validierung

### Interaktive Mindmaps

- Vis.js-basierte Navigation
- Chat-Snapshots eingebettet
- Tag-Filter
- Suchfunktion

### Chat-Snapshots

- Automatische Extraktion aus Plänen
- Verknüpfung mit Architektur-Knoten
- Zeitstempel und Tags

## Technische Details

### Abhängigkeiten

- `vis-network`: JavaScript-Bibliothek für interaktive Netzwerke
- `mermaid-cli` (optional): Für lokales Mermaid-Rendering
- `watchdog` (optional): Für Datei-Überwachung

### Dateistruktur

```
docs/visualizations/
├── index.html                    # Übersichtsseite
├── templates/
│   └── mindmap_template.html    # HTML-Template
├── [plan_name]_diagram_0.svg    # Mermaid-Diagramme
├── [plan_name]_diagram_0.png
└── [plan_name]_mindmap.html     # Interaktive Mindmap
```

## Troubleshooting

### Mermaid-Rendering schlägt fehl

Falls lokales Rendering nicht funktioniert:
1. Installiere `mermaid-cli`: `npm install -g @mermaid-js/mermaid-cli`
2. Oder nutze Online-Fallback (automatisch aktiviert)

### Mindmap wird nicht angezeigt

1. Prüfe Browser-Konsole auf JavaScript-Fehler
2. Stelle sicher, dass `vis-network` geladen wird
3. Prüfe ob JSON-Daten korrekt eingebettet sind

### Chat-Snapshots fehlen

- Snapshots werden nur extrahiert, wenn sie im Plan-Format vorhanden sind
- Format: ````chat` oder ````conversation` Blöcke

