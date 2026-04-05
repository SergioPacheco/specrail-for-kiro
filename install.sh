#!/usr/bin/env bash
# KiroRails installer — zero dependencies, works with any project
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/SergioPacheco/KiroRails/main/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/SergioPacheco/KiroRails/main/install.sh | bash -s -- --pack java-legacy
#   curl -fsSL https://raw.githubusercontent.com/SergioPacheco/KiroRails/main/install.sh | bash -s -- --pack spring-boot,postgres
#
# Available blueprints: java-legacy, spring-boot, postgres, python-fastapi, compliance

set -euo pipefail

REPO="https://raw.githubusercontent.com/SergioPacheco/KiroRails/main"
KIRO=".kiro"
PACKS=""

# ── Parse args ──────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case $1 in
    --pack) PACKS="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# ── Helpers ─────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

_get() {
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [ -f "$dst" ]; then
    echo "  ~ $dst (exists)"
    return
  fi
  if curl -fsSL "$REPO/$src" -o "$dst" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} $dst"
  else
    echo -e "  ${YELLOW}✗${NC} $dst (download failed)"
  fi
}

_state_file() {
  local name="$1"
  local dst="$KIRO/state/$name"
  if [ ! -f "$dst" ]; then
    printf "# %s\n\n<!-- Append-only. Updated by agents during execution. -->\n" "${name%.md}" > "$dst"
    echo -e "  ${GREEN}✓${NC} state/$name"
  else
    echo "  ~ state/$name (exists)"
  fi
}

# ── Banner ───────────────────────────────────────────────────────────────────
echo ""
echo "🛤️  KiroRails — installing into $KIRO/"
[ -n "$PACKS" ] && echo "   Blueprints: $PACKS"
echo ""

# ── Core steering ────────────────────────────────────────────────────────────
echo "[expert guardrails]"
for f in product.md tech.md structure.md coding-standards.md skills.md testing.md security.md; do
  _get "src/kirorails/data/core/steering/$f" "$KIRO/steering/$f"
done

# ── Agents ───────────────────────────────────────────────────────────────────
echo ""
echo "[specialist personas]"
for f in verifier.md clarifier.md analyzer.md learner.md bugfix-investigator.md; do
  _get "src/kirorails/data/agents/$f" "$KIRO/agents/$f"
done

# ── Executable hooks ─────────────────────────────────────────────────────────
echo ""
echo "[executable hooks]"
_get "src/kirorails/data/hooks-exec/kirorails.conf" "$KIRO/kirorails.conf"
for sh in pre-task.sh post-task.sh; do
  _get "src/kirorails/data/hooks-exec/$sh" "$KIRO/hooks-exec/$sh"
  chmod +x "$KIRO/hooks-exec/$sh" 2>/dev/null || true
done

# ── Kiro-native hooks (JSON) ─────────────────────────────────────────────────
echo ""
echo "[kiro hooks]"
for f in pre-task-health-check.json post-task-verification.json security-guardrails.json spec-validator.json; do
  _get "src/kirorails/data/hooks-kiro/$f" "$KIRO/hooks/$f"
done

# ── Templates ────────────────────────────────────────────────────────────────
echo ""
echo "[templates]"
_get "src/kirorails/data/templates/specs/feature/tasks.template.md" "$KIRO/specs/feature/tasks.template.md"
_get "src/kirorails/data/templates/specs/feature/design.template.md" "$KIRO/specs/feature/design.template.md"
_get "src/kirorails/data/templates/specs/bugfix/bugfix.template.md"  "$KIRO/specs/bugfix/bugfix.template.md"

# ── Skills template ──────────────────────────────────────────────────────────
_get "src/kirorails/data/skills/_template/SKILL.md" "$KIRO/skills/_template/SKILL.md"

# ── State files ──────────────────────────────────────────────────────────────
echo ""
echo "[state files]"
mkdir -p "$KIRO/state"
for sf in STATE.md CHANGELOG_AI.md DECISIONS.md RISKS.md; do
  _state_file "$sf"
done

# ── Blueprint overlays ───────────────────────────────────────────────────────
if [ -n "$PACKS" ]; then
  IFS=',' read -ra PACK_LIST <<< "$PACKS"
  for pack in "${PACK_LIST[@]}"; do
    pack="${pack// /}"
    echo ""
    echo "[blueprint: $pack]"
    case "$pack" in
      java-legacy)
        _get "src/kirorails/data/packs/java-legacy/steering/brownfield-java.md" "$KIRO/steering/brownfield-java.md"
        ;;
      spring-boot)
        _get "src/kirorails/data/packs/spring-boot/steering/spring-boot.md" "$KIRO/steering/spring-boot.md"
        ;;
      postgres)
        _get "src/kirorails/data/packs/postgres/steering/postgres.md" "$KIRO/steering/postgres.md"
        ;;
      python-fastapi)
        _get "src/kirorails/data/packs/python-fastapi/steering/fastapi.md" "$KIRO/steering/fastapi.md"
        ;;
      compliance)
        _get "src/kirorails/data/packs/compliance/steering/compliance.md"  "$KIRO/steering/compliance.md"
        _get "src/kirorails/data/packs/compliance/steering/regulatory.md"  "$KIRO/steering/regulatory.md"
        ;;
      *)
        echo "  ⚠️  Unknown blueprint: $pack (available: java-legacy, spring-boot, postgres, python-fastapi, compliance)"
        ;;
    esac
  done
fi

# ── Done ─────────────────────────────────────────────────────────────────────
TOTAL=$(find "$KIRO" -type f 2>/dev/null | wc -l | tr -d ' ')
echo ""
echo -e "${GREEN}✅ Done. $TOTAL files in $KIRO/${NC}"
echo ""
echo "📝 Edit .kiro/kirorails.conf to configure your build commands:"
echo "   compile=./mvnw compile -q"
echo "   test=./mvnw test -q"
echo "   lint=./mvnw checkstyle:check -q"
echo ""
echo "🚀 Next steps:"
echo "   Edit .kiro/steering/product.md   # describe your product"
echo "   Edit .kiro/steering/tech.md      # describe your tech stack"
echo "   Edit .kiro/kirorails.conf        # configure build commands"
echo ""
echo "💡 For full CLI (check-phantom, sprint management, skill learning):"
echo "   pip install kirorails"
