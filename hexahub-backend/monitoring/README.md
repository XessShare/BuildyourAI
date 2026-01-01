# HexaHub Monitoring Stack

Complete observability solution for HexaHub Backend with Prometheus, Grafana, cAdvisor, and PostgreSQL Exporter.

## Table of Contents
- [Overview](#overview)
- [Components](#components)
- [Quick Start](#quick-start)
- [Metrics Overview](#metrics-overview)
- [Dashboards](#dashboards)
- [Alerts](#alerts)
- [Troubleshooting](#troubleshooting)
- [Advanced Configuration](#advanced-configuration)

## Overview

The HexaHub monitoring stack provides comprehensive observability across:
- **Application Metrics**: Request rates, latencies, error rates
- **Infrastructure Metrics**: CPU, memory, network, disk I/O
- **Database Metrics**: Connections, queries, locks, performance
- **Container Metrics**: Resource usage per container

### Architecture

```
┌──────────────┐
│   Backend    │──┐
│   (FastAPI)  │  │
└──────────────┘  │
                  ├──> Prometheus ──> Grafana
┌──────────────┐  │    (Scrape)      (Visualize)
│  PostgreSQL  │──┤
└──────────────┘  │
                  │
┌──────────────┐  │
│   cAdvisor   │──┘
└──────────────┘
```

## Components

### 1. Prometheus

**Purpose**: Metrics collection and alerting
**Port**: 9090
**URL**: http://localhost:9090

**Configuration:**
- Scrape interval: 10-30s (service-dependent)
- Retention: 15 days (default)
- Storage: Persistent volume `prometheus_data`

**Scrape Targets:**
- **hexahub-backend** (port 8000): Application metrics
- **postgresql** (port 9187): Database metrics via postgres-exporter
- **cadvisor** (port 8080): Container metrics
- **prometheus** (port 9090): Self-monitoring

**Files:**
- `prometheus/prometheus.yml`: Main configuration
- `prometheus/alerts/backend-alerts.yml`: Alerting rules

### 2. Grafana

**Purpose**: Metrics visualization and dashboards
**Port**: 3000
**URL**: http://localhost:3000
**Credentials**: admin / admin

**Features:**
- Pre-configured Prometheus datasource
- HexaHub Backend Overview dashboard
- Automatic provisioning on startup
- Persistent storage for dashboards

**Configuration:**
- `grafana/provisioning/datasources/prometheus.yml`: Datasource config
- `grafana/provisioning/dashboards/dashboard.yml`: Dashboard provider
- `grafana/provisioning/dashboards/hexahub-overview.json`: Main dashboard

### 3. cAdvisor

**Purpose**: Container resource metrics
**Port**: 8081
**URL**: http://localhost:8081

**Metrics Collected:**
- CPU usage per container
- Memory usage and limits
- Network I/O (bytes sent/received)
- Filesystem usage
- Process count

**Note**: cAdvisor runs in privileged mode to access container metrics.

### 4. PostgreSQL Exporter

**Purpose**: Database metrics export
**Port**: 9187
**Internal**: Connects to PostgreSQL

**Metrics Collected:**
- Active connections
- Database size
- Transaction rates
- Cache hit ratio
- Lock statistics
- Query performance

## Quick Start

### 1. Start Monitoring Stack

```bash
# Start all services including monitoring
docker compose up -d

# Verify all services are running
docker compose ps
```

### 2. Access Interfaces

**Prometheus:**
```bash
# Open Prometheus UI
open http://localhost:9090

# Check targets status
open http://localhost:9090/targets

# View alerts
open http://localhost:9090/alerts
```

**Grafana:**
```bash
# Open Grafana
open http://localhost:3000

# Login: admin / admin
# Navigate to: Dashboards > HexaHub > HexaHub Backend Overview
```

**cAdvisor:**
```bash
# Open cAdvisor UI
open http://localhost:8081

# View container metrics
```

### 3. Generate Test Traffic

```bash
# Generate sample requests to populate metrics
for i in {1..100}; do
  curl -s http://localhost:8000/health > /dev/null
  curl -s http://localhost:8000/ > /dev/null
done
```

### 4. Verify Metrics

**Check backend metrics:**
```bash
curl http://localhost:8000/metrics | head -50
```

**Query Prometheus:**
```bash
# Request rate
curl 'http://localhost:9090/api/v1/query?query=rate(http_requests_total[1m])'

# Memory usage
curl 'http://localhost:9090/api/v1/query?query=process_resident_memory_bytes'
```

## Metrics Overview

### Application Metrics

**Request Metrics:**
- `http_requests_total`: Total HTTP requests (counter)
  - Labels: method, endpoint, status
- `http_request_duration_seconds`: Request latency (histogram)
  - Buckets: 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10
- `http_request_size_bytes`: Request body size (summary)
- `http_response_size_bytes`: Response body size (summary)

**Python Runtime:**
- `python_gc_collections_total`: GC collections by generation
- `python_gc_objects_collected_total`: Objects collected
- `process_cpu_seconds_total`: Process CPU time
- `process_resident_memory_bytes`: Process memory usage
- `process_open_fds`: Open file descriptors

### Database Metrics

**Connection Stats:**
- `pg_stat_database_numbackends`: Active connections
- `pg_stat_database_xact_commit`: Committed transactions
- `pg_stat_database_xact_rollback`: Rolled back transactions

**Performance:**
- `pg_stat_database_blks_hit`: Buffer cache hits
- `pg_stat_database_blks_read`: Disk reads
- `pg_stat_database_tup_returned`: Rows returned
- `pg_stat_database_tup_fetched`: Rows fetched

**Size:**
- `pg_database_size_bytes`: Database size
- `pg_stat_user_tables_n_live_tup`: Live rows per table

### Container Metrics

**Resource Usage:**
- `container_cpu_usage_seconds_total`: CPU usage
- `container_memory_usage_bytes`: Memory usage
- `container_memory_max_usage_bytes`: Peak memory
- `container_spec_memory_limit_bytes`: Memory limit

**Network:**
- `container_network_receive_bytes_total`: Network RX
- `container_network_transmit_bytes_total`: Network TX
- `container_network_receive_errors_total`: RX errors
- `container_network_transmit_errors_total`: TX errors

## Dashboards

### HexaHub Backend Overview

**Panels:**

1. **Backend Status** (Stat)
   - Query: `up{job="hexahub-backend"}`
   - Shows: UP (1) or DOWN (0)
   - Color: Green when up, Red when down

2. **Request Rate** (Time Series)
   - Query: `rate(http_requests_total{job="hexahub-backend"}[1m])`
   - Unit: requests per second (reqps)
   - Legend: `{{method}} {{endpoint}}`

3. **Response Time** (Time Series)
   - Query: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))`
   - Shows: p50 and p95 latency
   - Thresholds: Yellow > 0.5s, Red > 1s

4. **CPU Usage** (Time Series)
   - Query: `rate(container_cpu_usage_seconds_total{name="hexahub-backend"}[1m]) * 100`
   - Unit: Percent
   - Shows: CPU utilization over time

5. **Memory Usage** (Time Series)
   - Query: `container_memory_usage_bytes{name="hexahub-backend"}`
   - Unit: Bytes
   - Shows: Memory consumption with mean/max

6. **Database Connections** (Gauge)
   - Query: `pg_stat_database_numbackends{datname="hexahub"}`
   - Thresholds: Yellow > 50, Red > 80
   - Shows: Active DB connections

**Access:**
- URL: http://localhost:3000/d/hexahub-overview/hexahub-backend-overview
- Folder: HexaHub
- Refresh: Auto-refresh every 5s

### Creating Custom Dashboards

1. **Via Grafana UI:**
   ```
   1. Login to Grafana
   2. Click "+" > "Dashboard"
   3. Add Panel > Select Prometheus datasource
   4. Enter PromQL query
   5. Configure visualization
   6. Save dashboard
   ```

2. **Via Provisioning:**
   ```bash
   # Create dashboard JSON
   cat > grafana/provisioning/dashboards/custom-dashboard.json <<EOF
   {
     "title": "Custom Dashboard",
     "panels": [...]
   }
   EOF

   # Restart Grafana
   docker compose restart grafana
   ```

## Alerts

### Configured Alerts

**Backend Alerts** (`prometheus/alerts/backend-alerts.yml`)

1. **BackendDown**
   - Condition: `up{job="hexahub-backend"} == 0`
   - Duration: 1 minute
   - Severity: critical

2. **HighErrorRate**
   - Condition: Error rate > 5% over 5 minutes
   - Query: `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05`
   - Severity: critical

3. **HighLatency**
   - Condition: p95 latency > 1 second
   - Query: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1.0`
   - Duration: 5 minutes
   - Severity: warning

**Database Alerts**

1. **DatabaseConnectionsHigh**
   - Condition: > 80 connections
   - Query: `pg_stat_database_numbackends{datname="hexahub"} > 80`
   - Severity: warning

2. **PostgreSQLDown**
   - Condition: `up{job="postgresql"} == 0`
   - Duration: 1 minute
   - Severity: critical

**Resource Alerts**

1. **HighMemoryUsage**
   - Condition: > 80% of limit
   - Query: `container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.8`
   - Duration: 5 minutes
   - Severity: warning

2. **HighCPUUsage**
   - Condition: > 70% for 5 minutes
   - Query: `rate(container_cpu_usage_seconds_total[1m]) > 0.7`
   - Severity: warning

### Alert Status

**View Alerts in Prometheus:**
```bash
# List all alerts
curl http://localhost:9090/api/v1/rules

# Check firing alerts
curl http://localhost:9090/api/v1/alerts | jq '.data.alerts[] | select(.state=="firing")'
```

**View Alerts in Grafana:**
```
1. Navigate to Alerting > Alert Rules
2. View alert history and current state
3. Configure notification channels (future)
```

### Adding Custom Alerts

1. **Create alert rule:**
```yaml
# prometheus/alerts/custom-alerts.yml
groups:
  - name: custom
    interval: 30s
    rules:
      - alert: CustomAlert
        expr: your_metric > threshold
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Alert description"
          description: "{{ $value }} is above threshold"
```

2. **Update Prometheus config:**
```yaml
# prometheus/prometheus.yml
rule_files:
  - /etc/prometheus/alerts/*.yml
```

3. **Restart Prometheus:**
```bash
docker compose restart prometheus
```

## Troubleshooting

### Common Issues

#### 1. Prometheus Not Scraping Targets

**Symptoms**: Targets show as DOWN in http://localhost:9090/targets

**Solutions:**
```bash
# Check Prometheus logs
docker logs hexahub-prometheus

# Verify network connectivity
docker compose exec prometheus wget -O- http://backend:8000/metrics

# Check service is exposing metrics
curl http://localhost:8000/metrics
```

#### 2. Grafana Dashboard Empty

**Symptoms**: Dashboard shows "No Data"

**Solutions:**
```bash
# Verify Prometheus datasource
curl http://admin:admin@localhost:3000/api/datasources

# Check Prometheus has data
curl 'http://localhost:9090/api/v1/query?query=up'

# Generate test traffic
for i in {1..50}; do curl http://localhost:8000/health; done

# Adjust dashboard time range (top right in Grafana)
```

#### 3. Permission Denied Errors

**Symptoms**: Prometheus or Grafana fail to start

**Solutions:**
```bash
# Fix Prometheus config permissions
chmod 644 monitoring/prometheus/prometheus.yml
chmod 644 monitoring/prometheus/alerts/*.yml
chmod 755 monitoring/prometheus/alerts

# Fix Grafana provisioning permissions
chmod -R 755 monitoring/grafana/provisioning
find monitoring/grafana -type f -exec chmod 644 {} \;

# Restart services
docker compose restart prometheus grafana
```

#### 4. Port Already in Use

**Symptoms**: `Bind for 0.0.0.0:PORT failed: port is already allocated`

**Solutions:**
```bash
# Find process using port
lsof -i :3000  # or :9090, :8081

# Stop conflicting container
docker stop <container-name>

# Or change port in docker-compose.yml
ports:
  - "3001:3000"  # Use different host port
```

### Logs and Debugging

**View service logs:**
```bash
# Prometheus
docker logs hexahub-prometheus --tail 100 -f

# Grafana
docker logs hexahub-grafana --tail 100 -f

# cAdvisor
docker logs hexahub-cadvisor --tail 100 -f

# Postgres Exporter
docker logs hexahub-postgres-exporter --tail 100 -f
```

**Check configuration:**
```bash
# Validate Prometheus config
docker compose exec prometheus promtool check config /etc/prometheus/prometheus.yml

# Check alert rules
docker compose exec prometheus promtool check rules /etc/prometheus/alerts/backend-alerts.yml
```

## Advanced Configuration

### Prometheus Retention

Adjust data retention period:

```yaml
# docker-compose.yml
services:
  prometheus:
    command:
      - '--storage.tsdb.retention.time=30d'  # Keep 30 days
      - '--storage.tsdb.retention.size=10GB' # Or max 10GB
```

### Custom Scrape Intervals

Different intervals for different services:

```yaml
# prometheus/prometheus.yml
scrape_configs:
  - job_name: 'critical-service'
    scrape_interval: 5s  # Scrape every 5 seconds
    static_configs:
      - targets: ['service:port']
```

### Remote Storage

Send metrics to remote storage (e.g., Thanos, Cortex):

```yaml
# prometheus/prometheus.yml
remote_write:
  - url: http://remote-storage:9000/api/v1/push
    basic_auth:
      username: user
      password: pass
```

### Grafana Plugins

Install additional plugins:

```yaml
# docker-compose.yml
services:
  grafana:
    environment:
      - GF_INSTALL_PLUGINS=grafana-piechart-panel,grafana-worldmap-panel
```

### Alert Manager Integration

Configure AlertManager for notifications:

```yaml
# prometheus/prometheus.yml
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

# Alert rules remain in alerts/*.yml
```

## Performance Tuning

### Optimize Scrape Targets

```yaml
# Reduce metric cardinality
metric_relabel_configs:
  - source_labels: [__name__]
    regex: 'unwanted_metric.*'
    action: drop
```

### Grafana Query Optimization

```
# Use recording rules for expensive queries
groups:
  - name: performance
    interval: 1m
    rules:
      - record: job:http_requests:rate1m
        expr: rate(http_requests_total[1m])
```

### Resource Limits

```yaml
# docker-compose.yml
services:
  prometheus:
    mem_limit: 1g
    cpus: 0.5
```

## Backup and Restore

### Prometheus Data

```bash
# Backup
docker run --rm -v hexahub-backend_prometheus_data:/data \
  -v $(pwd)/backups:/backup alpine \
  tar czf /backup/prometheus-$(date +%Y%m%d).tar.gz /data

# Restore
docker run --rm -v hexahub-backend_prometheus_data:/data \
  -v $(pwd)/backups:/backup alpine \
  tar xzf /backup/prometheus-20260101.tar.gz -C /
```

### Grafana Dashboards

```bash
# Export dashboard
curl http://admin:admin@localhost:3000/api/dashboards/uid/hexahub-overview \
  | jq '.dashboard' > backup-dashboard.json

# Import dashboard
curl -X POST http://admin:admin@localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @backup-dashboard.json
```

## Further Reading

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/)
- [cAdvisor GitHub](https://github.com/google/cadvisor)

## Support

For issues or questions:
- Check [ARCHITECTURE.md](../ARCHITECTURE.md) for system overview
- Review [Troubleshooting](#troubleshooting) section
- Open an issue on GitHub
