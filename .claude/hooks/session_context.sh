#!/bin/sh
# SessionStart hook — the "data layer" entry point.
# Whatever this prints to stdout is injected into Claude's context at the
# start of every session, so each first instance wakes up already knowing
# the state of the big rocks and the headline scorecard numbers.
# POSIX sh + awk only: must run on any clean machine with zero dependencies.

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

echo "=== Operating context (injected by .claude/hooks/session_context.sh) ==="
echo ""
echo "Big rocks (plans/big-rocks/):"
for f in "$ROOT"/plans/big-rocks/*.md; do
    case "$f" in *00-INDEX.md) continue ;; esac
    [ -f "$f" ] || continue
    name=$(basename "$f" .md)
    status=$(awk -F': *' '/^status:/ {print $2; exit}' "$f")
    skills=$(awk -F': *' '/^owned-skills:/ {print $2; exit}' "$f")
    echo "  - ${name} | status: ${status:-unknown} | skills: ${skills:-none}"
done

CSV="$ROOT/data/partner_metrics.csv"
if [ -f "$CSV" ]; then
    echo ""
    awk -F',' 'NR > 1 {
        n++
        rev += $4
        if ($9 == "red") red++
    } END {
        printf "Scorecard headlines (data/partner_metrics.csv): %d partners | $%.1fM FY26 attributed revenue | %d red health flag(s)\n", n, rev / 1000000, red + 0
    }' "$CSV"
fi

echo ""
echo "Metric definitions: data/DATA_DICTIONARY.md (fiscal year is Feb-Jan)."
echo "Operating model: CLAUDE.md. After meaningful sessions, run /improve-setup."
