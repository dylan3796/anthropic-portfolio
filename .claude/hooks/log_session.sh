#!/bin/sh
# Stop hook — evidence generator for the recursive improvement loop.
# Appends one line per session to retros/session-log.md; /improve-setup reads
# that log (plus git history and the big-rock plans) to propose edits to the
# setup itself. Deliberately minimal: its only job is to leave a trail.

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LOG="$ROOT/retros/session-log.md"

mkdir -p "$(dirname "$LOG")"
branch=$(git -C "$ROOT" branch --show-current 2>/dev/null)
printf -- "- %s | session ended | branch: %s\n" \
    "$(date '+%Y-%m-%d %H:%M')" "${branch:-unknown}" >> "$LOG"
