# Apache Airflow - Data Pipeline Orchestrierung

## Übersicht

**Apache Airflow** ist eine Workflow-Orchestrierungsplattform, die primär für Data Pipelines entwickelt wurde, aber auch für allgemeine Workflow-Automatisierung genutzt werden kann.

- **License:** Apache 2.0
- **Website:** https://airflow.apache.org/
- **GitHub:** https://github.com/apache/airflow
- **Dokumentation:** https://airflow.apache.org/docs/

## Beschreibung

Apache Airflow ist eine Workflow-Orchestrierung für Data Pipelines, Python-basiert, mit DAG-basierten Workflows und Enterprise-ready Features.

## Features

### DAG (Directed Acyclic Graph) Definition
- Python-basierte Workflow-Definition
- DAG-Struktur für Dependencies
- Task-Dependencies

### Python-basierte Workflow-Definition
- Code-as-Configuration
- Python Operators
- Custom Operators

### Rich UI für Monitoring
- Web-Interface
- DAG-Visualisierung
- Task-Logs
- Monitoring-Dashboards

### Scheduling und Retry-Logik
- Cron-basierte Scheduling
- Automatische Retries
- Backfill-Funktionalität

### Plugin-System
- Custom Operators
- Custom Hooks
- Plugin-Architektur

## Einsatzgebiete

### Data Pipeline Orchestrierung
- ETL-Prozesse
- Data Transformation
- Data Loading

### Komplexe Workflow-Dependencies
- DAG-basierte Workflows
- Task-Dependencies
- Parallel Execution

### Batch-Processing
- Scheduled Jobs
- Batch-Operations
- Data Processing

## Vorteile

✅ **Mature und stabil** - Production-ready  
✅ **Python-basiert** - Entwicklerfreundlich  
✅ **Gute Monitoring-Tools** - Rich UI  
✅ **Skalierbar** - Horizontal scaling  
✅ **Große Community** - Viele Plugins  

## Nachteile

⚠️ **Primär für Data Pipelines** - Nicht ideal für einfache Workflows  
⚠️ **Steile Lernkurve** - Komplexe Konzepte  
⚠️ **Ressourcen-intensiv** - Benötigt ausreichend Infrastruktur  
⚠️ **Code-basiert** - Kein visueller Editor  

## Installation

### Docker Compose

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data

  airflow-webserver:
    image: apache/airflow:2.7.0
    command: webserver
    ports:
      - "8080:8080"
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
    volumes:
      - ./dags:/opt/airflow/dags
    depends_on:
      - postgres

  airflow-scheduler:
    image: apache/airflow:2.7.0
    command: scheduler
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
    volumes:
      - ./dags:/opt/airflow/dags
    depends_on:
      - postgres
```

## Beispiel: Workflow-zu-Workflow mit Airflow

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def trigger_gitlab_ci(**context):
    import requests
    response = requests.post(
        'https://gitlab.com/api/v4/projects/:id/trigger/pipeline',
        data={'ref': 'main'}
    )
    return response.json()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'github_to_gitlab_workflow',
    default_args=default_args,
    description='Trigger GitLab CI after GitHub Actions',
    schedule_interval=timedelta(hours=1),
)

wait_for_github = BashOperator(
    task_id='wait_for_github_actions',
    bash_command='curl -f https://api.github.com/repos/owner/repo/actions/runs',
    dag=dag,
)

trigger_gitlab = PythonOperator(
    task_id='trigger_gitlab_ci',
    python_callable=trigger_gitlab_ci,
    dag=dag,
)

wait_for_github >> trigger_gitlab
```

## Workflow-zu-Workflow-Patterns

### Pattern 1: Sequential Workflow Chain

```python
github_task >> gitlab_task >> jenkins_task
```

### Pattern 2: Parallel Execution

```python
github_task >> [gitlab_task, jenkins_task] >> deploy_task
```

### Pattern 3: Conditional Branching

```python
check_task >> branch_task
branch_task >> gitlab_task  # if condition A
branch_task >> jenkins_task  # if condition B
```

## Best Practices

1. **DAG-Struktur**: Organisiere DAGs logisch
2. **Task-Idempotenz**: Mache Tasks idempotent
3. **Error Handling**: Nutze Retries und Error-Callbacks
4. **Secrets Management**: Nutze Airflow Variables/Connections
5. **Monitoring**: Nutze Airflow's Monitoring-Features

## Ressourcen

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow GitHub](https://github.com/apache/airflow)
- [Airflow Community](https://airflow.apache.org/community/)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)

## Fazit

Airflow ist ideal für **Data Pipeline Orchestrierung** und **komplexe Workflow-Dependencies**. Für einfache Workflow-zu-Workflow-Integration möglicherweise Overkill.

