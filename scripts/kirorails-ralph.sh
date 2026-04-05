#!/usr/bin/env bash
# kirorails-ralph.sh — Autonomous task execution loop (EXPERIMENTAL)
#
# Runs kiro-cli in a loop, one task per iteration.
# Each iteration: health check → pick task → implement → test → commit → update state.
#
# Features:
#   - Rate limit detection with exponential backoff
#   - Configurable max iterations
#   - Progress tracking via PROGRESS.md
#
# ⚠️  This script is experimental. The kiro-cli interface may change.
#     Test with --dry-run first. Start with HITL before going AFK.
#
# Usage:
#   ./kirorails-ralph.sh <spec-name> [max-iterations]
#
# Examples:
#   ./kirorails-ralph.sh order-email-notification        # default 10 iterations
#   ./kirorails-ralph.sh order-email-notification 5      # max 5 iterations

set -e

SPEC_NAME="${1:?Usage: $0 <spec-name> [max-iterations]}"
MAX_ITERATIONS="${2:-10}"
SPEC_DIR=".kiro/specs/${SPEC_NAME}"
PROGRESS_FILE="${SPEC_DIR}/PROGRESS.md"

# Rate limit config
RATE_LIMIT_WAIT=60        # initial wait (seconds)
RATE_LIMIT_MAX_WAIT=600   # max wait (10 min)
RATE_LIMIT_MAX_RETRIES=5  # max consecutive retries before giving up

# Validate spec exists
if [ ! -d "$SPEC_DIR" ]; then
  echo "Error: spec directory not found: $SPEC_DIR"
  echo "Available specs:"
  ls -1 .kiro/specs/ 2>/dev/null | grep -v archive || echo "  (none)"
  exit 1
fi

if [ ! -f "${SPEC_DIR}/tasks.md" ]; then
  echo "Error: tasks.md not found in $SPEC_DIR"
  exit 1
fi

echo "=== KiroRails Ralph Loop (experimental) ==="
echo "Spec: ${SPEC_NAME}"
echo "Max iterations: ${MAX_ITERATIONS}"
echo ""

# Initialize progress file
if [ ! -f "$PROGRESS_FILE" ]; then
  echo "# Progress — ${SPEC_NAME}" > "$PROGRESS_FILE"
  echo "" >> "$PROGRESS_FILE"
  echo "## Iterations" >> "$PROGRESS_FILE"
fi

# Extract feedback loops from tasks.md
FEEDBACK_LOOPS=$(sed -n '/^## Feedback loops$/,/^#/{/^## Feedback loops$/d;/^#/d;/^```/d;/^$/d;p;}' "${SPEC_DIR}/tasks.md" | head -1)

# Rate limit detection
is_rate_limited() {
  local output="$1"
  echo "$output" | grep -qiE "rate.?limit|too many requests|429|quota exceeded|throttl|overloaded"
}

wait_for_rate_limit() {
  local wait_time="$1"
  local retry_num="$2"
  echo ""
  echo "⏳ Rate limit detected (retry ${retry_num}/${RATE_LIMIT_MAX_RETRIES})"
  echo "   Waiting ${wait_time}s before retrying..."
  echo "   $(date '+%H:%M:%S') → resuming at $(date -d "+${wait_time} seconds" '+%H:%M:%S' 2>/dev/null || date -v+${wait_time}S '+%H:%M:%S' 2>/dev/null || echo '~')"
  sleep "$wait_time"
  echo "   ✓ Resuming."
  echo ""
}

for ((i=1; i<=MAX_ITERATIONS; i++)); do
  echo "--- Iteration ${i}/${MAX_ITERATIONS} ---"

  # Health check
  HEALTH_STATUS="CLEAN"
  if [ -n "$FEEDBACK_LOOPS" ]; then
    echo "Health check: ${FEEDBACK_LOOPS}"
    if ! eval "$FEEDBACK_LOOPS" > /dev/null 2>&1; then
      echo "Health check FAILED — this iteration will fix the build."
      HEALTH_STATUS="BROKEN"
    fi
  fi

  PROMPT="You are executing tasks from a KiroRails spec.

Get your bearings:
1. Read ${PROGRESS_FILE} — what previous iterations did
2. Run: git log --oneline -10
3. Read ${SPEC_DIR}/tasks.md — task list with done criteria
4. Read .kiro/steering/ — project standards
5. Check .kiro/skills/ — load any matching skills for the current task

Environment health: ${HEALTH_STATUS}

Instructions:
- If health is BROKEN: fix the build first. Do NOT start a new task.
- If ALL tasks are complete, output exactly: KIRORAILS_COMPLETE
- Otherwise, implement ONLY the next uncompleted task.
- Run feedback loops. Fix failures before committing.
- Commit with the message specified in the task.
- Append to ${PROGRESS_FILE}: iteration number, task completed, files changed.
- Mark done criteria as [x] in tasks.md.

Rules:
- ONE task per iteration.
- Do NOT edit tasks.md except to mark checkboxes.
- Leave the codebase in a clean, mergeable state."

  # Run kiro-cli with rate limit retry
  RATE_RETRIES=0
  CURRENT_WAIT=$RATE_LIMIT_WAIT
  RESULT=""

  while true; do
    RESULT=$(kiro-cli chat --no-interactive --trust-tools read,write,shell "$PROMPT" 2>&1) || true

    if is_rate_limited "$RESULT"; then
      RATE_RETRIES=$((RATE_RETRIES + 1))
      if [ "$RATE_RETRIES" -ge "$RATE_LIMIT_MAX_RETRIES" ]; then
        echo "❌ Rate limit: max retries (${RATE_LIMIT_MAX_RETRIES}) exceeded. Stopping."
        echo "" >> "$PROGRESS_FILE"
        echo "### ⏳ Rate limited — stopped at iteration ${i} after ${RATE_RETRIES} retries" >> "$PROGRESS_FILE"
        exit 2
      fi
      wait_for_rate_limit "$CURRENT_WAIT" "$RATE_RETRIES"
      # Exponential backoff: 60 → 120 → 240 → 480, capped at max
      CURRENT_WAIT=$((CURRENT_WAIT * 2))
      if [ "$CURRENT_WAIT" -gt "$RATE_LIMIT_MAX_WAIT" ]; then
        CURRENT_WAIT=$RATE_LIMIT_MAX_WAIT
      fi
    else
      # Reset rate limit state on success
      RATE_RETRIES=0
      CURRENT_WAIT=$RATE_LIMIT_WAIT
      break
    fi
  done

  echo "$RESULT"

  # Check completion
  if echo "$RESULT" | grep -q "KIRORAILS_COMPLETE"; then
    echo ""
    echo "=== All tasks complete! ==="
    echo "Spec: ${SPEC_NAME}"
    echo "Iterations used: ${i}/${MAX_ITERATIONS}"
    exit 0
  fi

  echo "Iteration ${i} complete."
  echo ""
done

echo "=== Max iterations reached (${MAX_ITERATIONS}) ==="
echo "Check ${SPEC_DIR}/tasks.md for remaining tasks."
exit 1
