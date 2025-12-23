# Projekt-Navigation & Dokumentation

## Übersicht

Dieses Projekt enthält verschiedene Agenten- und KI-Komponenten, darunter:

- **Pydantic AI Web Search Agent** (Brave API)
- **Brainstorm-Service** (Docker/Compose, fortune)
- **Streamlit UI**
- **CLI-Tools**

## Verzeichnisstruktur

- `Dockerfile` – Container-Build für Brainstorm
- `compose.yaml` – Standard-Compose-Konfiguration
- `compose.debug.yaml` – Debug-Compose-Konfiguration
- `README.md` – Hauptdokumentation für Pydantic AI
- `README_NAVIGATION.md` – Diese Navigationsübersicht
- `web_search_agent.py` – CLI-Agent
- `streamlit_ui.py` – Streamlit Web-UI

## Einstiegspunkte

- **Brainstorm-Service starten:**  
  `docker compose -f compose.yaml up --build`
- **Debug-Modus:**  
  `docker compose -f compose.debug.yaml up --build`
- **Web Search Agent:**  
  Siehe [README.md](./README.md) für Details zur Nutzung.

## Weitere Hinweise

- API-Keys und Modellkonfigurationen bitte in `.env` hinterlegen.
- Für weiterführende Informationen siehe die jeweiligen README-Dateien in den Unterverzeichnissen.
