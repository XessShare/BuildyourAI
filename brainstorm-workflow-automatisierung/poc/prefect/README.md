# Prefect Proof of Concept

## Übersicht

Dieser Proof of Concept demonstriert Workflow-zu-Workflow-Integration mit Prefect.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Erstelle `.env` Datei:

```env
GITHUB_TOKEN=your_github_token
GITLAB_TOKEN=your_gitlab_token
GITLAB_PROJECT_ID=12345
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/... (optional)
```

### 3. Start Prefect Server (Optional)

```bash
prefect server start
```

Oder nutze Prefect Cloud.

## Usage

### Run Flow

```bash
python flows/github_to_gitlab.py
```

### Oder als Prefect Flow

```python
from flows.github_to_gitlab import github_to_gitlab_workflow

result = github_to_gitlab_workflow(
    github_repo="owner/repo",
    github_run_id="123456789",
    gitlab_project_id="12345",
    gitlab_ref="main"
)
```

## Features

- ✅ GitHub Actions Status Check
- ✅ GitLab CI Pipeline Trigger
- ✅ Error Handling
- ✅ Notifications
- ✅ Caching

## Nächste Schritte

1. Anpassen für eigene Use Cases
2. Prefect Cloud Setup (optional)
3. Scheduling konfigurieren
4. Monitoring einrichten

## Ressourcen

- [Prefect Documentation](https://docs.prefect.io/)
- [Prefect Examples](https://docs.prefect.io/latest/guides/)

