#!/usr/bin/env bash
set -euo pipefail

LOG_DIR="/Exercise1/logs"
LOG_FILE="$LOG_DIR/countdown.log"
MARK_FILE="$LOG_DIR/.events_header_done"

# Kör bara EN gång
if [ -f "$MARK_FILE" ]; then
  exit 0
fi

mkdir -p "$LOG_DIR"
touch "$LOG_FILE"

# Bygg event-tabellen (anpassad till dina 2026-datum)
HEADER="$(cat <<'TAB'
=== EVENTS (one-time header) ===
event,date
summer_break,2026-06-09 15:00
lia_start,2026-09-25 08:00
christmas,2026-12-24 00:00
bellas_birthday,2026-12-07 00:00
new_year,2026-01-01 00:00
graduation_party,2026-06-09 16:30

TAB
)"

# Prepend: skriv header + gammalt innehåll till temp, ersätt sen loggen
TMP="$(mktemp)"
printf "%s" "$HEADER" > "$TMP"
cat "$LOG_FILE" >> "$TMP"
mv "$TMP" "$LOG_FILE"

# Markera som klart
touch "$MARK_FILE"
