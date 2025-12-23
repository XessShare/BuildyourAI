#!/bin/bash
# J-Jeco Project Snapshot Utility
# Erstellt timestamped Snapshots für Debugging und Rollback

set -e

# Konfiguration
PROJECT_DIR="/home/fitna/homelab/J-Jeco"
SNAP_DIR="${PROJECT_DIR}/../snap/J-Jeco"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SNAPSHOT_NAME="snapshot_${TIMESTAMP}"

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funktionen
print_header() {
    echo -e "${BLUE}╔═══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║    J-JECO SNAPSHOT UTILITY            ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════╝${NC}"
}

create_snapshot() {
    echo -e "${YELLOW}📸 Erstelle Snapshot: ${SNAPSHOT_NAME}${NC}"

    # Erstelle Snapshot-Verzeichnis falls nicht vorhanden
    mkdir -p "${SNAP_DIR}"

    local snap_path="${SNAP_DIR}/${SNAPSHOT_NAME}"

    # Prüfe ob Snapshot bereits existiert (sollte nicht passieren wegen Timestamp)
    if [ -d "${snap_path}" ]; then
        echo -e "${RED}❌ Snapshot existiert bereits: ${snap_path}${NC}"
        exit 1
    fi

    # Erstelle Snapshot
    echo -e "   Kopiere Projektdaten..."
    mkdir -p "${snap_path}"

    # Kopiere mit cp (rsync alternative)
    (cd "${PROJECT_DIR}" && tar --exclude='ai-agents-masterclass' \
                                --exclude='__pycache__' \
                                --exclude='*.pyc' \
                                --exclude='.git' \
                                --exclude='data' \
                                --exclude='logs' \
                                --exclude='output' \
                                --exclude='.env' \
                                -cf - .) | (cd "${snap_path}" && tar -xf -)

    # Erstelle Metadaten
    cat > "${snap_path}/snapshot_info.txt" << EOF
Snapshot erstellt: $(date)
Timestamp: ${TIMESTAMP}
Git Commit: $(cd "${PROJECT_DIR}" && git rev-parse --short HEAD 2>/dev/null || echo "N/A")
Git Branch: $(cd "${PROJECT_DIR}" && git branch --show-current 2>/dev/null || echo "N/A")
Beschreibung: ${1:-"Automatischer Snapshot"}
EOF

    # Berechne Größe
    local size=$(du -sh "${snap_path}" | cut -f1)

    echo -e "${GREEN}✅ Snapshot erstellt: ${snap_path}${NC}"
    echo -e "${GREEN}   Größe: ${size}${NC}"
    echo -e "${GREEN}   Info: ${snap_path}/snapshot_info.txt${NC}"
}

list_snapshots() {
    echo -e "${YELLOW}📋 Verfügbare Snapshots:${NC}"
    echo ""

    if [ ! -d "${SNAP_DIR}" ] || [ -z "$(ls -A ${SNAP_DIR} 2>/dev/null)" ]; then
        echo -e "${RED}   Keine Snapshots gefunden.${NC}"
        return
    fi

    local count=0
    for snap in "${SNAP_DIR}"/snapshot_*; do
        if [ -d "$snap" ]; then
            count=$((count + 1))
            local name=$(basename "$snap")
            local size=$(du -sh "$snap" | cut -f1)
            local date=$(stat -c %y "$snap" | cut -d' ' -f1,2 | cut -d'.' -f1)

            echo -e "${GREEN}${count}. ${name}${NC}"
            echo -e "   Erstellt: ${date}"
            echo -e "   Größe: ${size}"

            # Zeige Info-Datei falls vorhanden
            if [ -f "${snap}/snapshot_info.txt" ]; then
                local desc=$(grep "Beschreibung:" "${snap}/snapshot_info.txt" | cut -d':' -f2-)
                echo -e "   Info:${desc}"
            fi
            echo ""
        fi
    done

    if [ $count -eq 0 ]; then
        echo -e "${RED}   Keine Snapshots gefunden.${NC}"
    else
        echo -e "${BLUE}   Total: ${count} Snapshot(s)${NC}"
    fi
}

restore_snapshot() {
    local snapshot_name=$1

    if [ -z "${snapshot_name}" ]; then
        echo -e "${RED}❌ Bitte Snapshot-Namen angeben${NC}"
        echo -e "${YELLOW}Verfügbare Snapshots:${NC}"
        ls -1 "${SNAP_DIR}" 2>/dev/null | grep "snapshot_" || echo "Keine Snapshots"
        exit 1
    fi

    local snap_path="${SNAP_DIR}/${snapshot_name}"

    if [ ! -d "${snap_path}" ]; then
        echo -e "${RED}❌ Snapshot nicht gefunden: ${snapshot_name}${NC}"
        exit 1
    fi

    echo -e "${YELLOW}⚠️  WARNUNG: Dies überschreibt das aktuelle Projekt!${NC}"
    echo -e "${YELLOW}   Snapshot: ${snapshot_name}${NC}"

    # Zeige Snapshot-Info
    if [ -f "${snap_path}/snapshot_info.txt" ]; then
        echo ""
        cat "${snap_path}/snapshot_info.txt"
        echo ""
    fi

    read -p "Fortfahren? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo -e "${BLUE}Abgebrochen.${NC}"
        exit 0
    fi

    # Erstelle Backup des aktuellen Zustands
    echo -e "${YELLOW}📸 Erstelle automatisches Backup vor Restore...${NC}"
    local backup_name="snapshot_pre_restore_${TIMESTAMP}"
    local backup_path="${SNAP_DIR}/${backup_name}"
    mkdir -p "${backup_path}"

    (cd "${PROJECT_DIR}" && tar --exclude='ai-agents-masterclass' \
                                --exclude='__pycache__' \
                                --exclude='*.pyc' \
                                --exclude='.git' \
                                --exclude='data' \
                                --exclude='logs' \
                                --exclude='output' \
                                -cf - .) | (cd "${backup_path}" && tar -xf -)

    echo -e "${GREEN}✅ Backup erstellt: ${backup_name}${NC}"

    # Restore Snapshot
    echo -e "${YELLOW}🔄 Restore Snapshot...${NC}"

    # Lösche aktuelle Dateien (außer spezielle Verzeichnisse)
    find "${PROJECT_DIR}" -mindepth 1 -maxdepth 1 \
        ! -name 'ai-agents-masterclass' \
        ! -name '.git' \
        ! -name 'data' \
        ! -name 'logs' \
        ! -name 'output' \
        -exec rm -rf {} +

    # Kopiere Snapshot zurück
    (cd "${snap_path}" && tar -cf - .) | (cd "${PROJECT_DIR}" && tar -xf -)

    # Entferne snapshot_info.txt aus restored Project
    rm -f "${PROJECT_DIR}/snapshot_info.txt"

    echo -e "${GREEN}✅ Snapshot restored: ${snapshot_name}${NC}"
    echo -e "${BLUE}   Backup gespeichert als: ${backup_name}${NC}"
}

delete_snapshot() {
    local snapshot_name=$1

    if [ -z "${snapshot_name}" ]; then
        echo -e "${RED}❌ Bitte Snapshot-Namen angeben${NC}"
        exit 1
    fi

    local snap_path="${SNAP_DIR}/${snapshot_name}"

    if [ ! -d "${snap_path}" ]; then
        echo -e "${RED}❌ Snapshot nicht gefunden: ${snapshot_name}${NC}"
        exit 1
    fi

    echo -e "${YELLOW}⚠️  Lösche Snapshot: ${snapshot_name}${NC}"
    read -p "Fortfahren? (yes/no): " confirm

    if [ "$confirm" == "yes" ]; then
        rm -rf "${snap_path}"
        echo -e "${GREEN}✅ Snapshot gelöscht${NC}"
    else
        echo -e "${BLUE}Abgebrochen.${NC}"
    fi
}

cleanup_old() {
    local keep=${1:-10}

    echo -e "${YELLOW}🧹 Cleanup: Behalte die letzten ${keep} Snapshots${NC}"

    if [ ! -d "${SNAP_DIR}" ]; then
        echo -e "${BLUE}Keine Snapshots vorhanden.${NC}"
        return
    fi

    # Zähle Snapshots
    local total=$(find "${SNAP_DIR}" -maxdepth 1 -type d -name "snapshot_*" | wc -l)

    if [ $total -le $keep ]; then
        echo -e "${BLUE}Nur ${total} Snapshot(s) vorhanden. Nichts zu löschen.${NC}"
        return
    fi

    local to_delete=$((total - keep))
    echo -e "${YELLOW}Lösche ${to_delete} alte Snapshot(s)...${NC}"

    # Lösche älteste Snapshots
    find "${SNAP_DIR}" -maxdepth 1 -type d -name "snapshot_*" -printf '%T+ %p\n' | \
        sort | head -n $to_delete | cut -d' ' -f2- | while read snap; do
        echo -e "   Lösche: $(basename "$snap")"
        rm -rf "$snap"
    done

    echo -e "${GREEN}✅ Cleanup abgeschlossen${NC}"
}

show_usage() {
    cat << EOF
Usage: ./snapshot.sh [COMMAND] [OPTIONS]

COMMANDS:
  create [beschreibung]    Erstelle neuen Snapshot
  list                     Liste alle Snapshots
  restore <name>           Restore einen Snapshot
  delete <name>            Lösche einen Snapshot
  cleanup [anzahl]         Behalte nur die letzten N Snapshots (default: 10)
  info <name>              Zeige Snapshot-Informationen

EXAMPLES:
  ./snapshot.sh create "Vor Content Creator Implementation"
  ./snapshot.sh list
  ./snapshot.sh restore snapshot_20241219_230000
  ./snapshot.sh cleanup 5

SNAPSHOT LOCATION:
  ${SNAP_DIR}

NOTES:
  - Snapshots werden nie überschrieben (Timestamp-basiert)
  - Vor jedem Restore wird automatisch ein Backup erstellt
  - .git, data/, logs/, output/ werden nicht gesnapshot

EOF
}

# Main
print_header

case "${1:-help}" in
    create)
        create_snapshot "${2:-Automatischer Snapshot}"
        ;;
    list|ls)
        list_snapshots
        ;;
    restore)
        restore_snapshot "$2"
        ;;
    delete|rm)
        delete_snapshot "$2"
        ;;
    cleanup)
        cleanup_old "${2:-10}"
        ;;
    info)
        if [ -f "${SNAP_DIR}/${2}/snapshot_info.txt" ]; then
            cat "${SNAP_DIR}/${2}/snapshot_info.txt"
        else
            echo -e "${RED}Snapshot nicht gefunden oder keine Info verfügbar${NC}"
        fi
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        echo -e "${RED}❌ Unbekanntes Kommando: $1${NC}"
        echo ""
        show_usage
        exit 1
        ;;
esac
