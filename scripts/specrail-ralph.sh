#!/usr/bin/env bash
# specrail-ralph.sh — Autonomous task execution loop for SpecRail + Kiro
#
# Runs kiro-cli in a loop, one task per iteration.
# Each iteration: pick task → implement → test → commit → update state.
#
# Usage:
#   ./specrail-ralph.sh <spec-name> [max-iterations]
#
# Examples:
#   ./specrail-ralph.sh order-email-notification        # default 10 iterations
#   ./specrail-ralph.sh order-email-notification 5      # max 5 iterations
#   ./specrail-ralph.sh fix-discount-rounding 3         # bugfix, 3 iterations

set -e

SPEC_NAME="${1:?Usage: $0 <spec-name> [max-iterations]}"
MAX_ITERATIONS="${2:-10}"
SPEC_DIR=".kiro/specs/${SPEC_NAME}"
STATE_FILE=".kiro/state/STATE.md"
CHANGELOG=".kiro/state/CHANGELOG_AI.md"
PROGRESS_FILE="${SPEC_DIR}/PROGRESS.md"

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

echo "=== SpecRail Ralph Loop ==="
echo "Spec: ${SPEC_NAME}"
echo "Max iterations: ${MAX_ITERATIONS}"
echo "Tasks file: ${SPEC_DIR}/tasks.md"
echo ""

# Initialize progress file
if [ ! -f "$PROGRESS_FILE" ]; then
  echo "# Progress — ${SPEC_NAME}" > "$PROGRESS_FILE"
  echo "" >> "$PROGRESS_FILE"
  echo "## Iterations" >> "$PROGRESS_FILE"
fi

# Extract feedback loops from tasks.md (line after "## Feedback loops")
FEEDBACK_LOOPS=$(sed -n '/^## Feedback loops$/,/^#/{/^## Feedback loops$/d;/^#/d;/^```/d;/^$/d;p;}' "${SPEC_DIR}/tasks.md" | head -1)

if [ -z "$FEEDBACK_LOOPS" ]; then
  echo "Warning: no feedback loops found in tasks.md. Skipping health checks."
fi

for ((i=1; i<=MAX_ITERATIONS; i++)); do
  echo "--- Iteration ${i}/${MAX_ITERATIONS} ---"

  # Health check: run feedback loops BEFORE starting work
  if [ -n "$FEEDBACK_LOOPS" ]; then
    echo "Running health check: ${FEEDBACK_LOOPS}"
    if ! eval "$FEEDBACK_LOOPS" > /dev/null 2>&1; then
      echo "Health check FAILED. This iteration will fix the broken state."
      HEALTH_STATUS="BROKEN — feedback loops failed before this iteration started"
    else
      echo "Health check passed."
      HEALTH_STATUS="CLEAN"
    fi
  else
    HEALTH_STATUS="SKIPPED — no feedback loops defined"
  fi

  PROMPT="You are executing tasks from a SpecRail spec.

Read these files to get your bearings:
1. ${PROGRESS_FILE} — what previous iterations did
2. git log --oneline -10 — recent commits
3. ${SPEC_DIR}/tasks.md — task list with done criteria
4. .kiro/state/CODEBASE.md — codebase map (if exists)
5. .kiro/steering/ — project standards

Environment health: ${HEALTH_STATUS}

Instructions:
1. If health is BROKEN: fix the build first. Do NOT start a new task. Run the feedback loops defined at the top of tasks.md until they pass, commit the fix, and stop.
2. Read tasks.md and PROGRESS.md to find the next UNCOMPLETED task.
3. If ALL tasks are complete, output exactly: SPECRAIL_COMPLETE
4. Implement ONLY that one task.
5. Run the feedback loops defined at the top of tasks.md to verify your changes.
6. If feedback loops fail, fix the issues before proceeding.
7. Stage and commit with the commit message specified in the task.
8. Append a brief entry to ${PROGRESS_FILE}: iteration number, task completed, files changed.
9. Update ${CHANGELOG} with what changed and why.
10. Mark the task's done criteria as [x] in tasks.md.

Rules:
- ONE task per iteration. Stop after completing one task.
- Follow .kiro/steering/coding-standards.md for commit format.
- If a task is blocked or unclear, document why in PROGRESS.md and move to the next task.
- Never skip feedback loops (tests, types, lint).
- Do NOT edit tasks.md except to mark done criteria checkboxes as [x]. Never remove, reorder, or rewrite tasks.
- Leave the codebase in a clean, mergeable state. No half-implemented features, no broken builds."

  # Run kiro-cli with the prompt
  RESULT=$(kiro-cli chat --print -p "$PROMPT" 2>&1) || true

  echo "$RESULT"

  # Check if all tasks are complete
  if echo "$RESULT" | grep -q "SPECRAIL_COMPLETE"; then
    echo ""
    echo "=== All tasks complete! ==="
    echo "Spec: ${SPEC_NAME}"
    echo "Iterations used: ${i}/${MAX_ITERATIONS}"

    # Update STATE.md
    echo "" >> "$STATE_FILE"
    echo "## $(date +%Y-%m-%d) — ${SPEC_NAME} completed" >> "$STATE_FILE"
    echo "Completed in ${i} Ralph iterations." >> "$STATE_FILE"

    exit 0
  fi

  echo "Iteration ${i} complete."
  echo ""
done

echo "=== Max iterations reached (${MAX_ITERATIONS}) ==="
echo "Some tasks may still be incomplete. Check ${SPEC_DIR}/tasks.md"
exit 1
