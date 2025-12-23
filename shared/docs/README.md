# Fitna Homelab Stack

## Quick Start

```bash
cd ~/homelab
docker-compose up -d
```

## Services & Zugänge

| Service | URL | Default Login |
|---------|-----|---------------|
| Portainer | http://localhost:9000 | Erstelle Admin beim ersten Start |
| Nginx Proxy Manager | http://localhost:81 | admin@example.com / changeme |
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9090 | - |
| Uptime Kuma | http://localhost:3001 | Erstelle Account |
| Pi-hole | http://localhost:8080/admin | changeme |

## SSH-Zugang

```bash
# Key anzeigen (für andere Hosts)
cat ~/.ssh/homelab_master.pub

# Zu einem Host kopieren
ssh-copy-id -i ~/.ssh/homelab_master.pub user@host

# Verbinden
ssh -i ~/.ssh/homelab_master user@host
```

## Befehle

```bash
	# Alle Services starten
docker-compose up -d

# Status prüfen
docker-compose ps

# Logs anzeigen
docker-compose logs -f [service]

# Alles stoppen
docker-compose down

# Update aller Images
docker-compose pull && docker-compose up -d
```

## WireGuard VPN

Nach dem Start findest du die Client-Configs unter:
```
~/homelab/wireguard/peer1/peer1.conf
~/homelab/wireguard/peer2/peer2.conf
~/homelab/wireguard/peer3/peer3.conf
```

QR-Codes für Mobile:
```bash
docker exec wireguard cat /config/peer1/peer1.png | base64 -d > peer1_qr.png
```
