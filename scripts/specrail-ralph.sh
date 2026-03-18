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

for ((i=1; i<=MAX_ITERATIONS; i++)); do
  echo "--- Iteration ${i}/${MAX_ITERATIONS} ---"

  PROMPT="You are executing tasks from a SpecRail spec.

Read these files for context:
- ${SPEC_DIR}/tasks.md (task list with done criteria)
- ${SPEC_DIR}/PROGRESS.md (what's been done so far)
- .kiro/state/CODEBASE.md (codebase map, if exists)
- .kiro/steering/ (project standards)

Instructions:
1. Read tasks.md and PROGRESS.md to find the next UNCOMPLETED task.
2. If ALL tasks are complete, output exactly: SPECRAIL_COMPLETE
3. Otherwise, implement ONLY that one task.
4. Run the project's test suite to verify your changes.
5. If tests fail, fix the issues before proceeding.
6. Stage and commit with the commit message specified in the task.
7. Append a brief entry to ${PROGRESS_FILE}: iteration number, task completed, files changed.
8. Update ${CHANGELOG} with what changed and why.
9. Mark the task's done criteria as [x] in tasks.md.

Rules:
- ONE task per iteration. Stop after completing one task.
- Follow .kiro/steering/coding-standards.md for commit format.
- If a task is blocked or unclear, document why in PROGRESS.md and move to the next task.
- Never skip feedback loops (tests, types, lint)."

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
