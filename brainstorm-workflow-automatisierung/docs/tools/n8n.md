# n8n - Workflow-Automatisierungstool

## Übersicht

**n8n** ist ein Open-Source Workflow-Automatisierungstool mit visuellem Editor, das sich ideal für Workflow-zu-Workflow-Integration eignet.

- **License:** Apache 2.0
- **Website:** https://n8n.io/
- **GitHub:** https://github.com/n8n-io/n8n
- **Dokumentation:** https://docs.n8n.io/

## Beschreibung

n8n ist ein Open-Source Workflow-Automatisierungstool, das Entwicklern und technisch versierten Benutzern große Flexibilität bietet. Es ermöglicht die Erstellung und Anpassung von Workflows durch Programmierung und Erweiterungen.

## Features

### Visueller Workflow-Builder
- Drag-and-Drop Interface
- Visuelle Darstellung von Workflows
- Einfache Workflow-Erstellung ohne Code

### 400+ Integrations
- GitHub, GitLab, Jenkins
- Slack, Discord, Teams
- AWS, Google Cloud, Azure
- Datenbanken (PostgreSQL, MySQL, MongoDB)
- APIs (REST, GraphQL, Webhooks)

### Self-hosted Option
- Vollständig self-hosted möglich
- Docker-Container verfügbar
- Keine Cloud-Abhängigkeit

### Workflow-Versionierung
- Git-Integration möglich
- Workflow-Export/Import
- Versionierung von Workflows

### Webhook-Support
- Incoming Webhooks
- Outgoing Webhooks
- Webhook-Trigger

### Code-Nodes für Custom Logic
- JavaScript/TypeScript Code-Nodes
- Python Code-Nodes (mit n8n-python)
- Custom Functionality

## Einsatzgebiete

### Workflow-zu-Workflow-Integration
- GitHub Actions → GitLab CI
- Jenkins → GitHub Actions
- Multi-Platform CI/CD Orchestrierung

### API-Orchestrierung
- API-Chaining
- Daten-Transformation zwischen APIs
- API-Aggregation

### Daten-Transformation zwischen Systemen
- ETL-Prozesse
- Daten-Migration
- Daten-Synchronisation

### Event-basierte Automatisierung
- Webhook-basierte Trigger
- Event-driven Workflows
- Real-time Automation

## Vorteile

✅ **Open Source** (Apache 2.0)  
✅ **Visuelle Oberfläche** - Einfach zu bedienen  
✅ **Große Community** - Aktive Entwicklung  
✅ **Self-hosted möglich** - Keine Cloud-Abhängigkeit  
✅ **Flexible Integration** - 400+ Nodes  
✅ **Webhook-Support** - Ideal für Workflow-zu-Workflow  

## Nachteile

⚠️ **Ressourcen-intensiv** - Benötigt ausreichend RAM/CPU  
⚠️ **Komplexe Workflows** können unübersichtlich werden  
⚠️ **Lernkurve** für komplexe Szenarien  

## Installation

### Docker

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### Docker Compose

```yaml
version: '3.8'
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
    volumes:
      - ~/.n8n:/home/node/.n8n
```

## Beispiel: GitHub Actions → GitLab CI

```json
{
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "github-webhook",
        "httpMethod": "POST"
      }
    },
    {
      "name": "GitLab CI Trigger",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://gitlab.com/api/v4/projects/:id/trigger/pipeline",
        "method": "POST",
        "bodyParameters": {
          "ref": "={{ $json.ref }}"
        }
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{"node": "GitLab CI Trigger"}]]
    }
  }
}
```

## Workflow-zu-Workflow-Patterns

### Pattern 1: Webhook Relay

```
GitHub Actions (Webhook) → n8n (Receive) → GitLab CI (Trigger)
```

### Pattern 2: Status Aggregation

```
GitHub Actions → n8n → Status Check → Slack Notification
GitLab CI → n8n → Status Check → Slack Notification
```

### Pattern 3: Conditional Routing

```
Workflow A → n8n → Condition Check → Workflow B oder Workflow C
```

## Best Practices

1. **Webhook-Sicherheit**: Nutze Signature-Verification
2. **Error Handling**: Implementiere Retry-Logik
3. **Logging**: Nutze n8n's Logging-Features
4. **Workflow-Organisation**: Strukturiere Workflows in Collections
5. **Secrets Management**: Nutze n8n's Credentials-System

## Ressourcen

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community Forum](https://community.n8n.io/)
- [n8n GitHub](https://github.com/n8n-io/n8n)
- [n8n Workflow Examples](https://n8n.io/workflows/)

## Fazit

n8n ist ideal für **einfache bis mittlere Workflow-zu-Workflow-Integration** mit visueller Oberfläche. Perfekt für Teams, die keine komplexe Code-basierte Lösung benötigen.

