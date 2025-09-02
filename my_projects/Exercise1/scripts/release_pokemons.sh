#!/usr/bin/env bash
set -euo pipefail

# Hitta rotmappen (en nivå upp från denna fil)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
BELT_DIR="${ROOT_DIR}/pokedata/pokebelt"

YES=0
DRY_RUN=0
VERBOSE=0

usage() {
  cat <<EOF
Usage: $(basename "$0") [options]

Clean the pokebelt (delete all *.json in pokedata/pokebelt).

Options:
  -y, --yes       Run without confirmation
  -n, --dry-run   Show what would be deleted, do not delete
  -v, --verbose   Print extra info
  -h, --help      Show this help
EOF
}

log() { [ "$VERBOSE" -eq 1 ] && echo "[INFO] $*" >&2 || true; }

# --- parse args ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    -y|--yes) YES=1; shift ;;
    -n|--dry-run) DRY_RUN=1; shift ;;
    -v|--verbose) VERBOSE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

# --- sanity checks ---
if [[ ! -d "$BELT_DIR" ]]; then
  echo "[ERROR] Hittade inte pokebelt: $BELT_DIR" >&2
  echo "Kör b) först så att mappen och JSON-filer skapas." >&2
  exit 1
fi

shopt -s nullglob
files=( "${BELT_DIR}"/*.json )
shopt -u nullglob

if [[ ${#files[@]} -eq 0 ]]; then
  echo "Inget att rensa. Pokebelt är redan tomt: $BELT_DIR"
  exit 0
fi

echo "Följande filer kommer att tas bort från pokebelt:"
for f in "${files[@]}"; do
  echo "  $f"
done

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "(Dry-run) Inga filer togs bort."
  exit 0
fi

if [[ "$YES" -ne 1 ]]; then
  read -r -p "Bekräfta borttagning (ja/nej): " ans
  case "$ans" in
    ja|JA|j|J|yes|y|Y) ;;
    *) echo "Avbrutet."; exit 0 ;;
  esac
fi

log "Raderar filer..."
for f in "${files[@]}"; do
  rm -f -- "$f"
  log "Deleted: $f"
done

echo "Pokebelt rensat: $BELT_DIR"
exit 0