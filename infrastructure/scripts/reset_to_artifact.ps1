<#
Reset helper: liest `.github/artifact-token.json` und führt einen kontrollierten Reset
Voraussetzungen:
- Repo ist ein Git-Repository
- Lokale Änderungen sind committed oder gestasht

Hinweis: Das Skript fragt vor destruktiven Aktionen nach Bestätigung.
#>

param(
    [string]$TokenPath = ".github/artifact-token.json",
    [switch]$Force
)

if (-not (Test-Path $TokenPath)) {
    Write-Error "Token file not found: $TokenPath. Erzeuge eines mit: `git rev-parse --short HEAD` und speichere in .github/artifact-token.json"
    exit 1
}

$token = Get-Content $TokenPath -Raw | ConvertFrom-Json
$commit = $token.commit
$timestamp = $token.timestamp
$note = $token.note

Write-Host "Artifact token: commit=$commit, timestamp=$timestamp, note=$note"

if (-not $Force) {
    $confirm = Read-Host "Dieses Skript wird Git-Checkout durchführen und Stacks neu starten. Fortfahren? (y/N)"
    if ($confirm -ne 'y' -and $confirm -ne 'Y') { Write-Host "Abgebrochen."; exit 0 }
}

Write-Host "Stashing local changes (if any)..."
git stash push -u | Out-Null

Write-Host "Checking out commit $commit"
git fetch --all --prune
git checkout $commit
if ($LASTEXITCODE -ne 0) { Write-Error "Git checkout failed"; exit 2 }

# Restart relevant docker stacks
Write-Host "Restarting stacks listed in token (if present)..."
if ($token.stacks) {
    foreach ($s in $token.stacks) {
        $file = Join-Path "docker/stacks" "$s.yml"
        if (Test-Path $file) {
            Write-Host "Recreating stack: $s (compose file: $file)"
            docker compose -f $file down
            docker compose -f $file up -d
        } else {
            Write-Warning "Compose file not found for stack: $s (expected $file)"
        }
    }
} else {
    Write-Warning "Keine stacks im Token angegeben. Nichts neu gestartet."
}

Write-Host "Fertig. Überprüfe Services und logs."
