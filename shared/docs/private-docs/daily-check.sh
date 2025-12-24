#!/bin/bash
# Daily Morning Check

# 1. Alle Systeme erreichbar?
echo "🔌 Teste Verbindungen..."
for host in jonas-homelab-vps proxmox-rtx1080 pve-thinkpad; do
  if ssh -o ConnectTimeout=10 -o BatchMode=yes "$host" "uptime"; then
    echo "✅ $host erreichbar"
  else
    echo "❌ Fehler: $host nicht erreichbar"
  fi
done

# 2. Docker Services Status
echo "🐳 Docker Status..."
if cd /home/fitna/homelab; then
  docker-compose ps
else
  echo "❌ Fehler: /home/fitna/homelab nicht gefunden"
fi

# 3. Disk Space Check
echo "💾 Disk Space..."
df -h | grep -E '(Filesystem|/$|/home)'

# 4. Updates verfügbar?
echo "📦 Updates..."
if command -v apt &>/dev/null; then
  sudo apt update &>/dev/null && apt list --upgradable 2>/dev/null | grep -v "Listing" || echo "✅ Alle Pakete aktuell"
else
  echo "⚠️  apt nicht verfügbar auf diesem System"
fi
