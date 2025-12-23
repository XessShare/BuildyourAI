# 👔 Mitarbeiter-Guide - Fitna Homelab

## Willkommen!

Dieser Guide zeigt dir, wie du die Homelab-Tools nutzen kannst.

---

## 🔐 Dein Zugang

### 1. VPN einrichten

**Du hast erhalten:**
- `vpn-config-deinname.conf` (Datei)
- `vpn-config-deinname-qr.png` (QR-Code für Handy)

#### Desktop (Windows/Mac/Linux):

1. **WireGuard installieren:**
   - Download: https://www.wireguard.com/install/
   - Installieren und starten

2. **Config importieren:**
   - "Tunnel hinzufügen" klicken
   - `vpn-config-deinname.conf` auswählen
   - "Aktivieren" klicken

3. **Verbunden?**
   - Icon wird grün ✅
   - Du kannst jetzt auf Homelab-Services zugreifen

#### Handy (iOS/Android):

1. **WireGuard App installieren:**
   - iOS: App Store
   - Android: Play Store

2. **QR-Code scannen:**
   - In App: "+" → "QR-Code scannen"
   - `vpn-config-deinname-qr.png` scannen

3. **Aktivieren** → Fertig! ✅

---

## 🛠️ Verfügbare Tools

### 1. Grafana - Dashboards & Monitoring

**Wofür?** System-Status ansehen, Metriken überwachen

**Zugriff:**
1. VPN aktivieren
2. Browser öffnen: `http://192.168.17.1:3000`
3. Login:
   - User: `dein.username`
   - Password: *[Du hast es per Email erhalten]*

**Was kannst du sehen?**
- System-Status (CPU, RAM, Disk)
- Docker-Container Status
- Network Traffic
- Uptime-Statistiken

**Dashboards:**
- "System Overview" → Gesamt-Status
- "Service Health" → Alle Services
- "J-Jeco AI" → AI-Agenten-Metriken

---

### 2. Uptime Kuma - Service-Monitoring

**Wofür?** Sehen welche Services laufen

**Zugriff:**
1. VPN aktivieren
2. Browser: `http://192.168.17.1:3001`
3. Login: *[Credentials per Email]*

**Was siehst du?**
- ✅ Grün = Service läuft
- ⏸️ Gelb = Warning
- ❌ Rot = Service down

**Bei Problemen:**
- Screenshot machen
- Admin benachrichtigen

---

### 3. Portainer - Docker-Management (Read-Only)

**Wofür?** Docker-Container-Status ansehen

**Zugriff:**
1. VPN aktivieren
2. Browser: `http://192.168.17.1:9000`
3. Login: *[Credentials per Email]*

**Was kannst du sehen?**
- Laufende Container
- Container-Logs (für Debugging)
- Resource Usage

**Was kannst du NICHT:**
- Container starten/stoppen (nur Admin)
- Konfiguration ändern
- Volumes löschen

---

### 4. Git Repository - Code ansehen

**Zugriff:**
- GitHub: https://github.com/XessShare/J-Jeco
- Oder lokal (wenn SSH-Zugriff)

**Was kannst du?**
- Code lesen
- Issues erstellen
- Pull Requests ansehen

**Commits machen:**
- Nur nach Freigabe vom Admin
- Feature-Branch erstellen
- Pull Request öffnen

---

## 📋 Tägliche Aufgaben

### Morgen-Check (5 Minuten)

1. **VPN verbinden**
2. **Uptime Kuma öffnen:** Alle Services grün?
3. **Grafana Dashboard:** System-Status OK?
4. **Falls Probleme:** Admin benachrichtigen

### Service-Logs prüfen

**Wenn ein Service Probleme macht:**

1. Portainer öffnen
2. Zum Container navigieren
3. "Logs" anklicken
4. Letzte 100 Zeilen durchsehen
5. Wichtige Fehler notieren
6. An Admin weiterleiten

---

## ❌ Was darfst du NICHT

- ❌ Services starten/stoppen
- ❌ Docker-Container löschen
- ❌ System-Konfiguration ändern
- ❌ Root/Admin-Passwörter teilen
- ❌ VPN-Config an Dritte weitergeben
- ❌ Production-Daten löschen

---

## 🆘 Hilfe & Support

### Bei technischen Problemen:

**1. Selbst prüfen:**
- VPN verbunden?
- Internet funktioniert?
- Browser-Cache geleert?

**2. Logs checken:**
- Grafana → Fehlermeldungen?
- Portainer → Container-Logs?

**3. Admin kontaktieren:**
- Email: admin@fitna.local
- Telegram: @fitna_admin
- Beschreibe Problem genau:
  - Was hast du versucht?
  - Welche Fehlermeldung?
  - Screenshot (falls möglich)

### Häufige Probleme

**"Seite nicht erreichbar"**
→ VPN aktiviert? Richtige IP?

**"Zugriff verweigert"**
→ Falsches Passwort? Account aktiv?

**"Service ist down"**
→ Uptime Kuma prüfen, Admin benachrichtigen

---

## 🎓 Best Practices

### Sicherheit

- ✅ VPN immer aktivieren vor Zugriff
- ✅ Passwort sicher aufbewahren (Password Manager!)
- ✅ Zwei-Faktor-Authentifizierung nutzen (wo verfügbar)
- ✅ Bei Verdacht auf Kompromittierung: Sofort Admin informieren

### Effizienz

- ✅ Bookmarks für häufig genutzte Tools
- ✅ Dashboard-Ansichten in Grafana speichern
- ✅ Regelmäßiger Morgen-Check
- ✅ Probleme sofort melden (nicht warten!)

---

## 📞 Kontakte

- **Admin:** Fitna
- **Email:** admin@fitna.local
- **Telegram:** @fitna_admin
- **Notfall:** *[Telefonnummer]*

---

**Viel Erfolg!** 🚀

Bei Fragen: Einfach fragen!

---

**Version:** 1.0
**Letzte Aktualisierung:** 2025-12-20
