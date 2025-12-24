#!/bin/bash
# SSH Key Setup Helper für DeploymentOrchestratorAgent
# Automatisiert das Kopieren von SSH-Keys auf Remote-Systeme

set -e

PUBLIC_KEY=$(cat ~/.ssh/id_ed25519.pub)

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     SSH Key Setup für DeploymentOrchestratorAgent        ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Ihr Public Key:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$PUBLIC_KEY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Funktion zum Installieren des Keys auf einem Remote-System
install_key() {
    local host=$1
    local user=$2
    local display_name=$3

    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "Setup: $display_name ($user@$host)"
    echo "═══════════════════════════════════════════════════════════"

    # Test ob bereits funktioniert
    if ssh -o BatchMode=yes -o ConnectTimeout=5 "$user@$host" "echo OK" &>/dev/null; then
        echo "✅ SSH-Key bereits installiert und funktioniert!"
        return 0
    fi

    echo ""
    echo "Der Key muss manuell installiert werden."
    echo ""
    echo "ANLEITUNG:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "1. Öffne ein neues Terminal-Fenster"
    echo "2. Verbinde dich zum Remote-System:"
    echo "   ssh $user@$host"
    echo ""
    echo "3. Auf dem Remote-System, führe aus:"
    echo "   mkdir -p ~/.ssh"
    echo "   chmod 700 ~/.ssh"
    echo "   nano ~/.ssh/authorized_keys"
    echo ""
    echo "4. Füge diese Zeile am ENDE der Datei ein:"
    echo "   $PUBLIC_KEY"
    echo ""
    echo "5. Speichern: Strg+O, Enter, Strg+X"
    echo ""
    echo "6. Permissions setzen:"
    echo "   chmod 600 ~/.ssh/authorized_keys"
    echo "   exit"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # Warten auf Benutzer-Bestätigung
    read -p "Drücke Enter wenn du fertig bist, oder 's' zum Überspringen: " choice

    if [[ "$choice" == "s" ]] || [[ "$choice" == "S" ]]; then
        echo "⏭️  Übersprungen"
        return 1
    fi

    # Test
    echo ""
    echo "Teste Verbindung..."
    if ssh -o BatchMode=yes -o ConnectTimeout=5 "$user@$host" "echo OK" &>/dev/null; then
        echo "✅ Erfolg! SSH-Key funktioniert!"
        return 0
    else
        echo "❌ Verbindung fehlgeschlagen. Bitte überprüfe die Schritte."
        echo ""
        read -p "Nochmal versuchen? (j/n): " retry
        if [[ "$retry" == "j" ]] || [[ "$retry" == "J" ]]; then
            install_key "$host" "$user" "$display_name"
        else
            return 1
        fi
    fi
}

# Installiere Keys auf allen Systemen
install_key "jonas-homelab-vps" "fitna" "VPS"
install_key "192.168.16.7" "fitna" "ThinkPad"
install_key "192.168.17.1" "fitna" "RTX1080"

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                 Abschließende Tests                       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Finale Tests
test_connection() {
    local host=$1
    local user=$2
    local name=$3

    echo -n "Testing $name... "
    if ssh -o BatchMode=yes -o ConnectTimeout=5 "$user@$host" "echo OK" &>/dev/null; then
        echo "✅"
        return 0
    else
        echo "❌"
        return 1
    fi
}

success=0
failed=0

test_connection "jonas-homelab-vps" "fitna" "VPS" && ((success++)) || ((failed++))
test_connection "192.168.16.7" "fitna" "ThinkPad" && ((success++)) || ((failed++))
test_connection "192.168.17.1" "fitna" "RTX1080" && ((success++)) || ((failed++))

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "Zusammenfassung:"
echo "  ✅ Erfolgreich: $success/3"
echo "  ❌ Fehlgeschlagen: $failed/3"
echo "═══════════════════════════════════════════════════════════"

if [ $success -eq 3 ]; then
    echo ""
    echo "🎉 Alle SSH-Verbindungen funktionieren!"
    echo ""
    echo "Nächste Schritte:"
    echo "1. Teste Deployment Agent:"
    echo "   cd /home/fitna/homelab/ai-platform/1-first-agent"
    echo "   source ../ai-agents-masterclass/bin/activate"
    echo "   python test_deployment.py"
    echo ""
    echo "2. Teste Secrets Sync:"
    echo "   ./shared/scripts/sync-secrets.sh test"
    exit 0
else
    echo ""
    echo "⚠️  Einige Verbindungen sind noch nicht eingerichtet."
    echo "Bitte wiederhole die Schritte für die fehlgeschlagenen Systeme."
    exit 1
fi
