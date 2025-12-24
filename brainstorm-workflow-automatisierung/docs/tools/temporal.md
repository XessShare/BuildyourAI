# Temporal - Durable Workflow-Engine

## Übersicht

**Temporal** ist eine Workflow-Engine für zuverlässige Anwendungen mit Durable Execution, Multi-Language Support und Enterprise-ready Features.

- **License:** MIT
- **Website:** https://temporal.io/
- **GitHub:** https://github.com/temporalio/temporal
- **Dokumentation:** https://docs.temporal.io/

## Beschreibung

Temporal ist eine Workflow-Engine für zuverlässige Anwendungen mit Durable Execution, Microservice-Orchestrierung und Multi-Language Support. Entwickelt für hochzuverlässige, lang laufende Workflows.

## Features

### Durable Execution
- Workflow-State wird persistent gespeichert
- Automatische Recovery bei Fehlern
- Zuverlässige Execution

### Workflow-Versionierung
- Workflow-Versioning
- Backward Compatibility
- Migration-Tools

### Multi-Language SDKs
- Go, Java, Python, TypeScript
- .NET, PHP, Ruby
- Weitere Sprachen in Entwicklung

### Event Sourcing
- Event-basierte Architektur
- Event-History
- Replay-Funktionalität

### Retry und Timeout Management
- Automatische Retries
- Timeout-Management
- Exponential Backoff

## Einsatzgebiete

### Microservice-Orchestrierung
- Microservice-Workflows
- Distributed Systems
- Service-Coordination

### Zuverlässige Workflow-Execution
- Long-running Workflows
- Critical Workflows
- High-Availability Requirements

### Distributed Systems
- Multi-Service Coordination
- Saga-Pattern Implementation
- Distributed Transactions

## Vorteile

✅ **Sehr zuverlässig** - Durable Execution  
✅ **Multi-Language Support** - Viele SDKs  
✅ **Durable Execution** - State Persistence  
✅ **Enterprise-ready** - Production-ready  
✅ **Event Sourcing** - Vollständige History  

## Nachteile

⚠️ **Komplexe Architektur** - Steile Lernkurve  
⚠️ **Overkill für einfache Workflows** - Zu komplex  
⚠️ **Ressourcen-intensiv** - Benötigt Infrastruktur  

## Installation

### Docker Compose

```yaml
version: '3.8'
services:
  postgresql:
    image: postgres:14
    environment:
      POSTGRES_PWD: temporal
      POSTGRES_SEEDS: postgresql
    volumes:
      - postgresql-data:/var/lib/postgresql/data

  temporal:
    image: temporalio/auto-setup:latest
    ports:
      - "7233:7233"
      - "8088:8088"
    environment:
      - DB=postgresql
      - DB_PORT=5432
      - POSTGRES_USER=temporal
      - POSTGRES_PWD=temporal
      - POSTGRES_SEEDS=postgresql
    depends_on:
      - postgresql
```

## Beispiel: Workflow-zu-Workflow mit Temporal

### Python SDK

```python
from temporalio import workflow, activity
from temporalio.client import Client
import asyncio

@activity
async def check_github_actions(repo: str) -> dict:
    """Check GitHub Actions status"""
    import requests
    response = requests.get(
        f'https://api.github.com/repos/{repo}/actions/runs'
    )
    return response.json()

@activity
async def trigger_gitlab_ci(project_id: str) -> dict:
    """Trigger GitLab CI pipeline"""
    import requests
    response = requests.post(
        f'https://gitlab.com/api/v4/projects/{project_id}/trigger/pipeline',
        data={'ref': 'main'}
    )
    return response.json()

@workflow.defn
class GitHubToGitLabWorkflow:
    @workflow.run
    async def run(self, repo: str, gitlab_project_id: str) -> dict:
        # Check GitHub Actions
        github_status = await workflow.execute_activity(
            check_github_actions,
            repo,
            start_to_close_timeout=60,
        )
        
        if github_status['workflow_runs'][0]['status'] == 'completed':
            # Trigger GitLab CI
            result = await workflow.execute_activity(
                trigger_gitlab_ci,
                gitlab_project_id,
                start_to_close_timeout=60,
            )
            return result
        else:
            raise Exception("GitHub Actions not completed")
```

## Workflow-zu-Workflow-Patterns

### Pattern 1: Sequential Workflow

```python
@workflow.defn
class SequentialWorkflow:
    @workflow.run
    async def run(self):
        result1 = await workflow.execute_activity(task1)
        result2 = await workflow.execute_activity(task2, result1)
        return result2
```

### Pattern 2: Parallel Execution

```python
@workflow.defn
class ParallelWorkflow:
    @workflow.run
    async def run(self):
        results = await asyncio.gather(
            workflow.execute_activity(task1),
            workflow.execute_activity(task2),
            workflow.execute_activity(task3),
        )
        return results
```

### Pattern 3: Saga Pattern

```python
@workflow.defn
class SagaWorkflow:
    @workflow.run
    async def run(self):
        try:
            result1 = await workflow.execute_activity(step1)
            result2 = await workflow.execute_activity(step2, result1)
            return result2
        except Exception:
            # Compensating transactions
            await workflow.execute_activity(compensate_step1)
            raise
```

## Best Practices

1. **Idempotenz**: Mache Activities idempotent
2. **Timeouts**: Setze angemessene Timeouts
3. **Error Handling**: Nutze Temporal's Error-Handling
4. **Versioning**: Nutze Workflow-Versioning
5. **Monitoring**: Nutze Temporal's Monitoring-Features

## Ressourcen

- [Temporal Documentation](https://docs.temporal.io/)
- [Temporal GitHub](https://github.com/temporalio/temporal)
- [Temporal Community](https://temporal.io/community)
- [Temporal Examples](https://github.com/temporalio/samples-python)

## Fazit

Temporal ist ideal für **Microservice-Orchestrierung** und **hochzuverlässige Workflows**. Für einfache Workflow-zu-Workflow-Integration möglicherweise zu komplex.

