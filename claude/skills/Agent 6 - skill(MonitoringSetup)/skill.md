# Skill: Monitoring Setup

## Name
**Monitoring Setup** - Automated Prometheus & Grafana Observability Stack

## Description
This skill automates the deployment and configuration of the complete monitoring and observability stack including Prometheus, Grafana, Loki, Promtail, and Uptime Kuma. It configures scrape targets, imports dashboards, sets up alert rules, and provisions datasources based on the configuration from `/home/fitna/homelab/infrastructure/docker/prometheus/` and `/home/fitna/homelab/infrastructure/docker/grafana/`.

## When to Use This Skill

### Trigger Conditions
Use this skill when the user requests ANY of the following:
- "Set up monitoring"
- "Deploy Prometheus and Grafana"
- "Configure observability stack"
- "Add monitoring dashboards"
- "Set up alerts for [service/metric]"
- "Deploy Uptime Kuma"
- "Configure log aggregation"

### Context Indicators
- User mentions metrics, dashboards, or alerts
- User discusses Prometheus, Grafana, Loki, or monitoring
- User needs visibility into infrastructure health
- User wants uptime tracking or status pages

## Process Steps

### Phase 1: Deploy Monitoring Stack (5-10 minutes)

1. **Deploy Monitoring Docker Compose Stack**
   Reference: `/home/fitna/homelab/infrastructure/docker/stacks/monitoring.yml`

   ```bash
   cd /home/fitna/homelab/infrastructure/docker/stacks
   docker compose -f monitoring.yml pull
   docker compose -f monitoring.yml up -d
   ```

   **Services Deployed:**
   - **Prometheus**: Metrics collection (port 9090)
   - **Grafana**: Visualization (port 3000)
   - **Loki**: Log aggregation (port 3100)
   - **Promtail**: Log shipping
   - **Uptime Kuma**: Status page (port 3001)

2. **Verify Services Health**
   ```bash
   # Check all containers running
   docker ps --filter "name=monitoring" --format "table {{.Names}}\t{{.Status}}"

   # Test Prometheus
   curl -s http://localhost:9090/-/healthy

   # Test Grafana
   curl -s http://localhost:3000/api/health

   # Test Loki
   curl -s http://localhost:3100/ready
   ```

   **Expected:** All services respond with 200 OK

### Phase 2: Configure Prometheus (10-15 minutes)

3. **Review Prometheus Configuration**
   Reference: `/home/fitna/homelab/infrastructure/docker/prometheus/prometheus.yml`

   **Scrape Targets:**
   ```yaml
   scrape_configs:
     - job_name: 'prometheus'
       static_configs:
         - targets: ['localhost:9090']

     - job_name: 'node-exporter'
       static_configs:
         - targets:
           - '192.168.17.1:9100'  # RTX1080
           - '192.168.16.7:9100'  # ThinkPad
           - '91.107.198.37:9100' # VPS

     - job_name: 'cadvisor'
       static_configs:
         - targets: ['cadvisor:8080']

     - job_name: 'traefik'
       static_configs:
         - targets: ['traefik:8082']
   ```

4. **Deploy Node Exporter on All Hosts**
   ```bash
   # Run on each host (VPS, ThinkPad, RTX1080)
   docker run -d \
     --name=node-exporter \
     --net="host" \
     --pid="host" \
     -v "/:/host:ro,rslave" \
     --restart=unless-stopped \
     prom/node-exporter:latest \
     --path.rootfs=/host
   ```

5. **Configure Alert Rules**
   Reference: `/home/fitna/homelab/infrastructure/docker/prometheus/alerts/basic-alerts.yml`

   **Critical Alerts:**
   ```yaml
   groups:
     - name: infrastructure
       interval: 30s
       rules:
         - alert: HighCPUUsage
           expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
           for: 5m
           labels:
             severity: warning
           annotations:
             summary: "High CPU usage on {{ $labels.instance }}"

         - alert: HighMemoryUsage
           expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 90
           for: 5m
           labels:
             severity: critical
           annotations:
             summary: "High memory usage on {{ $labels.instance }}"

         - alert: DiskSpaceLow
           expr: (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100 < 10
           for: 5m
           labels:
             severity: critical
           annotations:
             summary: "Disk space low on {{ $labels.instance }}"

         - alert: ContainerRestarting
           expr: rate(docker_container_restart_count[1h]) > 3
           for: 5m
           labels:
             severity: warning
           annotations:
             summary: "Container {{ $labels.name }} restarting frequently"

         - alert: SSLCertExpiringSoon
           expr: (probe_ssl_earliest_cert_expiry - time()) / 86400 < 14
           for: 1h
           labels:
             severity: warning
           annotations:
             summary: "SSL certificate for {{ $labels.instance }} expires in <14 days"
   ```

6. **Reload Prometheus Configuration**
   ```bash
   docker exec monitoring-prometheus kill -HUP 1
   # Or restart
   docker restart monitoring-prometheus
   ```

### Phase 3: Configure Grafana (10-15 minutes)

7. **Access Grafana UI**
   ```
   URL: http://localhost:3000
   Default Login: admin / admin (change on first login)
   ```

8. **Auto-Provision Prometheus Datasource**
   Reference: `/home/fitna/homelab/infrastructure/docker/grafana/provisioning/datasources/prometheus.yml`

   ```yaml
   apiVersion: 1
   datasources:
     - name: Prometheus
       type: prometheus
       access: proxy
       url: http://prometheus:9090
       isDefault: true
       editable: false

     - name: Loki
       type: loki
       access: proxy
       url: http://loki:3100
       editable: false
   ```

9. **Import Pre-Built Dashboards**
   Reference: `/home/fitna/homelab/infrastructure/docker/grafana/provisioning/dashboards/`

   **Recommended Dashboard IDs (from Grafana.com):**
   - **Node Exporter Full**: 1860
   - **Docker Container & Host Metrics**: 893
   - **Traefik 2**: 11462
   - **Loki Logs**: 13639

   **Import via UI:**
   1. Grafana → Dashboards → Import
   2. Enter dashboard ID (e.g., 1860)
   3. Select Prometheus datasource
   4. Click Import

   **Import via Provisioning:**
   ```bash
   # Download dashboard JSON
   curl -o /home/fitna/homelab/infrastructure/docker/grafana/provisioning/dashboards/node-exporter-full.json \
     https://grafana.com/api/dashboards/1860/revisions/latest/download

   # Restart Grafana to load
   docker restart monitoring-grafana
   ```

10. **Create Custom Dashboard for Homelab**
    Create `/home/fitna/homelab/infrastructure/docker/grafana/provisioning/dashboards/homelab-overview.json`:

    **Panels:**
    - **Host Resources**: CPU, Memory, Disk per host (VPS, ThinkPad, RTX1080)
    - **Container Health**: Running/stopped containers, restart count
    - **Network Traffic**: Inbound/outbound traffic per host
    - **Service Uptime**: Uptime percentage for critical services
    - **Traefik Metrics**: Request rate, response time, status codes
    - **Disk I/O**: Read/write operations per host

### Phase 4: Configure Loki and Promtail (5-10 minutes)

11. **Verify Loki Log Aggregation**
    ```bash
    # Check Loki is receiving logs
    curl -s "http://localhost:3100/loki/api/v1/labels"

    # Query recent logs
    curl -s "http://localhost:3100/loki/api/v1/query_range?query={job=\"docker\"}" | jq
    ```

12. **Configure Promtail Log Scraping**
    Reference: `/home/fitna/homelab/infrastructure/docker/promtail/promtail-config.yml`

    **Log Sources:**
    ```yaml
    scrape_configs:
      - job_name: docker
        static_configs:
          - targets: ['localhost']
            labels:
              job: docker
              __path__: /var/lib/docker/containers/*/*.log

      - job_name: system
        static_configs:
          - targets: ['localhost']
            labels:
              job: syslog
              __path__: /var/log/syslog
    ```

### Phase 5: Configure Uptime Kuma (5 minutes)

13. **Set Up Uptime Kuma Status Page**
    ```
    URL: http://localhost:3001
    First-time setup: Create admin account
    ```

14. **Add Service Monitors**
    **Critical Services to Monitor:**
    - Traefik (https://yourdomain.com)
    - Authentik (https://auth.yourdomain.com)
    - Portainer (https://portainer.yourdomain.com)
    - Grafana (http://localhost:3000)
    - Prometheus (http://localhost:9090)
    - Home Assistant (http://localhost:8123)
    - Jellyfin (http://localhost:8096)

    **Monitor Configuration:**
    - Type: HTTP(s)
    - Interval: 60 seconds
    - Retries: 3
    - Timeout: 10 seconds
    - Accepted Status Codes: 200-299

15. **Configure Status Page**
    - Enable public status page (optional)
    - Group monitors by category (Core, Apps, Media)
    - Set custom domain (status.yourdomain.com)

### Phase 6: Set Up Alerting (10 minutes)

16. **Configure Alertmanager (Optional)**
    Reference: `/home/fitna/homelab/infrastructure/docker/prometheus/alertmanager.yml`

    ```yaml
    global:
      resolve_timeout: 5m

    route:
      group_by: ['alertname', 'cluster']
      group_wait: 10s
      group_interval: 10s
      repeat_interval: 12h
      receiver: 'default'

    receivers:
      - name: 'default'
        email_configs:
          - to: 'your-email@example.com'
            from: 'alertmanager@yourdomain.com'
            smarthost: 'smtp.gmail.com:587'
            auth_username: 'your-email@example.com'
            auth_password: 'YOUR_APP_PASSWORD'

      - name: 'telegram'
        telegram_configs:
          - bot_token: 'YOUR_BOT_TOKEN'
            chat_id: YOUR_CHAT_ID
            parse_mode: 'HTML'
    ```

17. **Test Alert Firing**
    ```bash
    # Manually trigger test alert
    curl -X POST http://localhost:9090/api/v1/alerts \
      -d '[{"labels":{"alertname":"TestAlert","severity":"warning"},"annotations":{"summary":"Test alert"}}]'
    ```

## Rules and Constraints

### Hard Rules (Must Follow)
1. **Prometheus MUST scrape at least: prometheus, node-exporter, cadvisor**
2. **Grafana datasources MUST be provisioned** (not manually configured)
3. **Alert rules MUST include: CPU, memory, disk, container restarts**
4. **Uptime Kuma MUST monitor all public-facing services**
5. **Loki MUST aggregate Docker container logs**
6. **Retention period: Prometheus 15 days, Loki 7 days** (disk space)

### Soft Rules (Best Practices)
- Set scrape interval to 15s (balance between granularity and load)
- Create separate dashboards per service category
- Use Grafana folders to organize dashboards
- Tag alerts with severity (critical, warning, info)
- Document dashboard panels with descriptions

### Quality Gates
Before marking monitoring setup complete:
- [ ] All services healthy (HTTP 200 OK)
- [ ] Node exporters running on all 3 hosts
- [ ] At least 3 Grafana dashboards imported
- [ ] Alert rules configured and validated
- [ ] Uptime Kuma monitoring 5+ services
- [ ] Loki receiving and indexing logs

## Expected Outputs

### Deliverables
1. **Prometheus Configuration** - Scrape targets and alert rules
2. **Grafana Dashboards** - Imported and custom dashboards
3. **Loki Configuration** - Log aggregation setup
4. **Uptime Kuma Monitors** - Service uptime tracking
5. **Alerting Configuration** - Alert rules and notification channels

### Success Metrics
- ✅ Prometheus scraping 10+ targets
- ✅ Grafana showing live metrics (not "No Data")
- ✅ 5+ dashboards imported and functional
- ✅ Alert rules firing on threshold breaches
- ✅ Uptime Kuma showing 100% uptime for healthy services
- ✅ Loki logs queryable via Grafana

## Error Handling

### Common Issues & Solutions

**Issue: Prometheus "target down"**
- **Solution**: Check node-exporter running on target host
- **Command**: `docker ps | grep node-exporter`

**Issue: Grafana shows "No Data"**
- **Solution**: Verify datasource URL is correct (http://prometheus:9090)
- **Test**: Query Prometheus directly: `curl http://localhost:9090/api/v1/query?query=up`

**Issue: Loki not receiving logs**
- **Solution**: Check Promtail configuration and Docker socket mount
- **Verify**: `docker logs promtail`

**Issue: Uptime Kuma service shows "Down"**
- **Solution**: Check service is accessible from Uptime Kuma container
- **Test**: `docker exec uptime-kuma curl -I http://service:port`

**Issue: Alerts not firing**
- **Solution**: Check alert expression syntax in PromQL
- **Validate**: Prometheus UI → Alerts → verify "Pending" state

## Example Usage

### User Request
"Set up complete monitoring for the homelab with Prometheus, Grafana, and Uptime Kuma."

### Agent Response
```markdown
I'll deploy and configure the complete monitoring stack.

**Phase 1: Deploying Services...**
✅ Prometheus deployed (port 9090)
✅ Grafana deployed (port 3000)
✅ Loki deployed (port 3100)
✅ Promtail deployed
✅ Uptime Kuma deployed (port 3001)

**Phase 2: Configuring Prometheus...**
✅ 4 scrape jobs configured (prometheus, node-exporter, cadvisor, traefik)
✅ Node exporters running on 3 hosts (VPS, ThinkPad, RTX1080)
✅ 5 alert rules configured (CPU, memory, disk, restarts, SSL)

**Phase 3: Configuring Grafana...**
✅ Prometheus datasource provisioned
✅ Loki datasource provisioned
✅ Imported 3 dashboards:
   - Node Exporter Full (ID: 1860)
   - Docker Metrics (ID: 893)
   - Traefik 2 (ID: 11462)

**Phase 4: Configuring Uptime Kuma...**
✅ 7 service monitors added:
   - Traefik, Authentik, Portainer (Core)
   - Grafana, Prometheus (Monitoring)
   - Home Assistant, Jellyfin (Apps)

**Access URLs:**
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/[set password])
- Uptime Kuma: http://localhost:3001

**Status:** ✅ Monitoring stack fully operational!
```

## Integration Points

### Related Skills
- **Agent 2 - DeploymentOrchestrator**: Deploy monitoring after infrastructure deployment
- **Agent 5 - InfrastructureProvisioner**: Install node-exporter during provisioning
- **Agent 7 - RoadmapTracker**: Track infrastructure KPIs via Grafana

### External Tools
- Docker stack: `/home/fitna/homelab/infrastructure/docker/stacks/monitoring.yml`
- Prometheus config: `/home/fitna/homelab/infrastructure/docker/prometheus/prometheus.yml`
- Grafana provisioning: `/home/fitna/homelab/infrastructure/docker/grafana/provisioning/`

### Data Sources
- Infrastructure README: `/home/fitna/homelab/infrastructure/README.md`
- Alert rules: `/home/fitna/homelab/infrastructure/docker/prometheus/alerts/basic-alerts.yml`

## Version
v1.0 - Initial skill definition based on monitoring stack analysis
