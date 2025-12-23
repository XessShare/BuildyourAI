# AdGuard Home vs Pi-hole Vergleich
**Datum:** 2025-12-23
**Kontext:** DNS Ad-Blocking für Homelab

---

## 📊 DIREKTER VERGLEICH

| Feature | **AdGuard Home** | **Pi-hole** |
|---------|------------------|-------------|
| **Lizenz** | ✅ Open Source (GPL v3) | ✅ Open Source (EUPL v1.2) |
| **Kosten** | ✅ 100% Gratis | ✅ 100% Gratis |
| **Docker Support** | ✅ Offizielles Image | ✅ Offizielles Image |
| **Web Interface** | ✅ Modern (React) | ✅ Klassisch (PHP) |
| **DNS-over-HTTPS** | ✅ Native | ⚠️ Via Zusatztools |
| **DNS-over-TLS** | ✅ Native | ⚠️ Via Zusatztools |
| **DNS-over-QUIC** | ✅ Ja | ❌ Nein |
| **Encryption** | ✅ Built-in | ⚠️ Manuell |
| **Parental Controls** | ✅ Integriert | ❌ Nein |
| **Safe Search** | ✅ Integriert | ❌ Nein |
| **Query Log** | ✅ Detailliert | ✅ Detailliert |
| **Blocklists** | ✅ Built-in + Custom | ✅ Custom |
| **DHCP Server** | ✅ Ja | ✅ Ja |
| **IPv6 Support** | ✅ Vollständig | ✅ Vollständig |
| **Performance** | ⚡ Sehr schnell (Go) | ⚡ Schnell (C++) |
| **RAM Usage** | ~50-100 MB | ~30-70 MB |
| **API** | ✅ REST API | ⚠️ Limited |
| **Multi-User** | ✅ Ja | ❌ Nein (Single Admin) |
| **Rewrite Rules** | ✅ DNS Rewrites | ⚠️ Via dnsmasq |
| **Client Identification** | ✅ Per IP/Name/MAC | ✅ Per IP |
| **Statistics** | ✅ Detailliert + Export | ✅ Detailliert |
| **Community** | 🔥 Wachsend (23k⭐) | 🔥🔥 Etabliert (48k⭐) |
| **Updates** | ✅ Auto-Update | ✅ Manuell |
| **Dokumentation** | ✅ Gut | ✅✅ Exzellent |

---

## 🎯 EMPFEHLUNG FÜR DEIN SETUP

### ✅ **ADGUARD HOME** - EMPFOHLEN

**Warum AdGuard Home für dein Homelab?**

1. **Modern & Feature-Rich:**
   - DNS-over-HTTPS/TLS/QUIC out-of-the-box
   - Keine zusätzlichen Tools nötig
   - Modernes Web-Interface

2. **Better API:**
   - Vollständige REST API
   - Perfekt für J-Jeco AI Agents Integration
   - Monitoring via Prometheus

3. **Parental Controls & Safe Search:**
   - Integriert (bei Pi-hole manuell)
   - Nützlich für Haushalt

4. **Multi-User Support:**
   - Verschiedene Benutzer mit eigenen Dashboards
   - Pi-hole hat nur einen Admin

5. **Einfachere Konfiguration:**
   - Alles im Web-Interface
   - DNS Rewrites ohne dnsmasq-Fu

6. **Perfekt für Docker:**
   - Single Container
   - Keine komplexen Volumes

---

## 🚀 DEPLOYMENT: AdGuard Home

### Docker Compose Configuration

Ersetze in `infrastructure/docker/stacks/automation.yml`:

**ALT (Pi-hole):**
```yaml
pihole:
  image: pihole/pihole:latest
  container_name: pihole
  ...
```

**NEU (AdGuard Home):**
```yaml
adguardhome:
  image: adguard/adguardhome:latest
  container_name: adguardhome
  restart: unless-stopped
  networks:
    - homelab_network
  ports:
    - "53:53/tcp"      # DNS
    - "53:53/udp"      # DNS
    - "3000:3000/tcp"  # Web Interface (Initial Setup)
    - "80:80/tcp"      # Web Interface (after setup)
    - "443:443/tcp"    # HTTPS
    - "853:853/tcp"    # DNS-over-TLS
  volumes:
    - adguard_work:/opt/adguardhome/work
    - adguard_conf:/opt/adguardhome/conf
  environment:
    - TZ=${TZ}
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.adguard.rule=Host(`dns.${DOMAIN}`)"
    - "traefik.http.routers.adguard.entrypoints=websecure"
    - "traefik.http.routers.adguard.tls.certresolver=cloudflare"
    - "traefik.http.routers.adguard.middlewares=authentik@file"
    - "traefik.http.services.adguard.loadbalancer.server.port=80"

volumes:
  adguard_work:
  adguard_conf:
```

### Initial Setup

1. **Nach dem Start:**
   ```bash
   docker logs adguardhome
   # Zugriff: http://192.168.16.7:3000
   ```

2. **Setup Wizard:**
   - Admin Interface Port: 80
   - DNS Port: 53
   - Admin Benutzer erstellen
   - Upstream DNS: Cloudflare (1.1.1.1), Google (8.8.8.8)

3. **DNS-over-HTTPS aktivieren:**
   - Settings → Encryption
   - HTTPS Port: 443
   - Zertifikat: Let's Encrypt (auto via Traefik)

4. **Blocklists hinzufügen:**
   - Filters → DNS Blocklists
   - Standard AdGuard Liste aktiviert
   - Optional: Steven Black's Unified Hosts

---

## 🔄 MIGRATION VON PI-HOLE (falls vorhanden)

### 1. Blocklists exportieren

```bash
# Von Pi-hole
docker exec pihole sqlite3 /etc/pihole/gravity.db \
  "SELECT address FROM adlist;" > blocklists.txt
```

### 2. In AdGuard Home importieren

- Settings → DNS Blocklists → Add Blocklist
- Jede URL aus `blocklists.txt` hinzufügen

### 3. Custom DNS Records

```bash
# Pi-hole custom.list exportieren
docker exec pihole cat /etc/pihole/custom.list > dns-records.txt

# In AdGuard: Filters → DNS Rewrites
# Manuell eintragen oder via API
```

---

## 📈 INTEGRATION MIT HOMELAB

### Prometheus Monitoring

AdGuard Home hat native Prometheus Metriken:

```yaml
# In prometheus.yml:
scrape_configs:
  - job_name: 'adguardhome'
    static_configs:
      - targets: ['adguardhome:80']
    metrics_path: '/control/stats'
```

### Grafana Dashboard

Offizielles Dashboard: https://grafana.com/grafana/dashboards/13330

### n8n Automation

```javascript
// n8n HTTP Request Node
{
  "method": "GET",
  "url": "http://adguardhome/control/stats",
  "authentication": "basicAuth",
  "credentials": {
    "user": "admin",
    "password": "${ADGUARD_PASSWORD}"
  }
}
```

### J-Jeco AI Agents Integration

```python
# In J-Jeco agents/network_agent.py:
import requests

class NetworkAgent:
    def get_dns_stats(self):
        response = requests.get(
            "http://192.168.16.7/control/stats",
            auth=("admin", os.getenv("ADGUARD_PASSWORD"))
        )
        return response.json()
```

---

## 🎯 FINAL VERDICT

### **WINNER: AdGuard Home** 🏆

**Gründe:**
1. ✅ Moderne Architektur (Go statt C++)
2. ✅ Bessere API für Automation
3. ✅ DNS-over-HTTPS/TLS/QUIC native
4. ✅ Parental Controls integriert
5. ✅ Multi-User Support
6. ✅ Einfachere Konfiguration
7. ✅ Perfekt für Docker
8. ✅ Aktive Entwicklung

**Pi-hole bleibt gut für:**
- Etablierte Community
- Umfangreiche Dokumentation
- Gewohnheit (wenn man es schon nutzt)

**Für ein NEUES Deployment: AdGuard Home ist die bessere Wahl!**

---

## 🔧 NÄCHSTE SCHRITTE

1. **Ersetze Pi-hole in `automation.yml`** mit AdGuard Home Config
2. **Füge zu `.env.master` hinzu:**
   ```bash
   ADGUARD_USERNAME=admin
   ADGUARD_PASSWORD=generate-strong-password
   ```
3. **Update Dokumentation** (DEPLOYMENT.md, README.md)
4. **Deploy & Test**

---

**Decision:** AdGuard Home für dein Homelab! ✅
