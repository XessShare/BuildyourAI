# n8n Proof of Concept

## Übersicht

Dieser Proof of Concept demonstriert Workflow-zu-Workflow-Integration mit n8n.

## Setup

### 1. Start n8n

```bash
docker-compose up -d
```

### 2. Zugriff auf n8n

Öffne http://localhost:5678 im Browser

- **Username:** admin
- **Password:** admin

## Workflows

### Workflow 1: GitHub Actions → GitLab CI

**Ziel:** Automatische Weiterleitung von GitHub Actions zu GitLab CI

**Schritte:**
1. Webhook von GitHub Actions empfangen
2. Status prüfen
3. GitLab CI Pipeline triggern
4. Status überwachen

**Import:**
- Importiere `workflows/github-to-gitlab.json` in n8n

### Workflow 2: Multi-Platform Status Aggregation

**Ziel:** Aggregation von Status-Informationen aus verschiedenen CI/CD-Plattformen

**Schritte:**
1. Status von GitHub Actions abrufen
2. Status von GitLab CI abrufen
3. Status von Jenkins abrufen
4. Status aggregieren
5. Benachrichtigung senden

**Import:**
- Importiere `workflows/status-aggregation.json` in n8n

## Konfiguration

### GitHub Webhook Setup

1. Gehe zu GitHub Repository Settings → Webhooks
2. Füge Webhook hinzu:
   - **Payload URL:** http://localhost:5678/webhook/github-actions
   - **Content type:** application/json
   - **Secret:** (optional, für Signature-Verifikation)

### GitLab CI Trigger Setup

1. Gehe zu GitLab Project Settings → CI/CD → Pipeline triggers
2. Erstelle Trigger Token
3. Konfiguriere in n8n Workflow

## Testing

### Test Webhook

```bash
curl -X POST http://localhost:5678/webhook/github-actions \
  -H "Content-Type: application/json" \
  -d '{
    "ref": "refs/heads/main",
    "repository": {
      "name": "test-repo"
    },
    "workflow_run": {
      "status": "completed",
      "conclusion": "success"
    }
  }'
```

## Nächste Schritte

1. Workflows anpassen für eigene Use Cases
2. Webhook-Endpunkte konfigurieren
3. Credentials in n8n einrichten
4. Workflows aktivieren

## Ressourcen

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Workflow Examples](https://n8n.io/workflows/)

