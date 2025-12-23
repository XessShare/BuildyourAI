# 👋 Freunde-Guide - Fitna's Homelab Services

## Hey!

Willkommen! Fitna hat dir Zugriff auf ein paar coole Services gegeben.

---

## 🌐 Was kannst du nutzen?

### 1. Sicheres Internet (VPN)

**Was ist das?**
Ein VPN schützt deine Internet-Verbindung. Wie ein privater Tunnel durchs Internet.

**Warum nutzen?**
- ✅ Öffentliches WLAN sicherer nutzen (Café, Flughafen)
- ✅ Privatsphäre schützen
- ✅ Geo-Blocking umgehen (manchmal)

---

## 📱 VPN einrichten

### Handy (einfachste Methode!)

**1. App installieren:**
- iOS: "WireGuard" im App Store
- Android: "WireGuard" im Play Store

**2. QR-Code scannen:**
- Fitna hat dir einen QR-Code geschickt (`vpn-XXX-qr.png`)
- In WireGuard-App: "+" → "QR-Code scannen"
- Code scannen → Fertig!

**3. Aktivieren:**
- Tunnel-Name antippen
- Schieberegler auf "Ein"
- Grünes Symbol = Verbunden ✅

**4. Nutzen:**
- Einfach aktivieren wenn du Schutz willst
- Deaktivieren wenn nicht gebraucht (spart Akku)

### Computer

**1. WireGuard installieren:**
- Download: https://www.wireguard.com/install/
- Für Windows/Mac/Linux verfügbar

**2. Config-Datei importieren:**
- Fitna hat dir `vpn-XXX.conf` geschickt
- WireGuard öffnen
- "Tunnel hinzufügen" → Datei auswählen

**3. Aktivieren:**
- "Aktivieren" klicken
- Status wird grün → Connected!

---

## 🚫 Werbung blockieren (Pi-hole)

**Was ist das?**
Ein Werbe-Blocker für ALLE deine Geräte!

**Wie nutzen?**

### Automatisch (wenn VPN an):
- VPN aktivieren → Werbung automatisch geblockt!
- Funktioniert in:
  - Websites
  - Apps
  - YouTube (teilweise)
  - Smart-TV-Werbung

### Manuell (ohne VPN):

**Handy:**
1. WLAN-Einstellungen öffnen
2. Dein WLAN antippen
3. "DNS" ändern zu: `192.168.17.1`
4. Speichern

**Computer:**
1. Netzwerkeinstellungen
2. DNS-Server: `192.168.17.1`

---

## 📊 System-Status (Uptime Kuma)

**Nur wenn du neugierig bist:**

- VPN aktivieren
- Browser öffnen: `http://192.168.17.1:3001`
- Login: *[Fitna hat dir Username/Password geschickt]*

**Was siehst du?**
- Status der Homelab-Services
- Uptime-Statistiken
- Ist alles am Laufen?

**Nicht anfassen!** Nur gucken 👀

---

## ⚠️ Wichtig!

### Do's ✅

- VPN nutzen in öffentlichen WLANs
- Bei Problemen Fitna fragen
- VPN ausschalten wenn nicht gebraucht (spart Daten)

### Don'ts ❌

- VPN-Config NICHT an andere weitergeben!
- Nicht für illegale Sachen nutzen
- Settings nicht ändern (läuft schon optimal)
- Passwörter nicht teilen

---

## 🆘 Probleme?

### "VPN verbindet nicht"

**Checkliste:**
1. Internet funktioniert? (WLAN/Mobile Daten an?)
2. WireGuard App aktuell? (Update checken)
3. QR-Code richtig gescannt?
4. Fitna fragen 😊

### "Werbung wird nicht geblockt"

**Checkliste:**
1. VPN wirklich aktiviert? (Grünes Symbol?)
2. App neu starten
3. Browser-Cache leeren
4. Manche Werbung kann nicht geblockt werden (z.B. YouTube-Werbung in App)

### Sonstiges

**Bei allen Problemen:**
- WhatsApp/Telegram an Fitna
- Oder Email
- Beschreib kurz was nicht funktioniert
- Screenshot hilft!

---

## 🎉 Cool, oder?

Genieße:
- Sicheres Internet
- Weniger Werbung
- Mehr Privatsphäre

**Danke Fitna! 🙌**

---

## 💡 Fun Facts

**Wusstest du?**
- Pi-hole blockt durchschnittlich 20-30% deines Web-Traffics
- VPN verschlüsselt ALLE deine Daten
- Viele Websites tracken dich - Pi-hole stoppt das!

**Datenschutz-Tipp:**
Nutze VPN + Pi-hole = Maximum Privacy! 🔒

---

**Fragen?** → Frag Fitna! 😊

**Version:** 1.0 (Super einfach Edition)
**Für:** Nicht-Techies ❤️
