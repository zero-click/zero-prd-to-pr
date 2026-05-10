#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

LOCAL_PROFILE_SKILLS=(
  "woos-development-workflow"
  "woos-prd-authoring"
  "woos-prd-review-gate"
  "woos-feature-design"
  "woos-design-review-gate"
  "woos-code-review-gate"
  "woos-pr-readiness"
)

ECC_AGENT_ADAPTER_SKILLS=(
  "planner"
  "architect"
  "code-reviewer"
  "security-reviewer"
)

ECC_SKILLS=(
  "git-workflow"
  "search-first"
  "dmux-workflows"
  "product-capability"
  "tdd-workflow"
  "coding-standards"
  "verification-loop"
)

PROFILE_ROOT_DEFAULT="${HERMES_PROFILE_ROOT:-$HOME/.hermes/profiles/coding}"
ECC_PATH=""
PROFILE_ROOT="$PROFILE_ROOT_DEFAULT"
INSTALL_SOUL="false"

print_usage() {
  cat <<'EOF'
Usage: ./install-profile.sh [options]

Options:
  --ecc-path <path>      Local ECC repo path. If omitted, script prompts for it.
  --profile-root <path>  Hermes coding profile root (default: ~/.hermes/profiles/coding).
  --install-soul         Also install SOUL.md into profile root.
  -h, --help             Show this help.
EOF
}

fail() {
  echo "Error: $1" >&2
  exit 1
}

copy_skill_dir() {
  local src="$1"
  local dest="$2"
  [[ -d "$src" ]] || fail "Missing skill directory: $src"
  rm -rf "$dest"
  mkdir -p "$(dirname "$dest")"
  cp -R "$src" "$dest"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --ecc-path)
      [[ $# -ge 2 ]] || fail "--ecc-path requires a value"
      ECC_PATH="$2"
      shift 2
      ;;
    --profile-root)
      [[ $# -ge 2 ]] || fail "--profile-root requires a value"
      PROFILE_ROOT="$2"
      shift 2
      ;;
    --install-soul)
      INSTALL_SOUL="true"
      shift
      ;;
    -h|--help)
      print_usage
      exit 0
      ;;
    *)
      fail "Unknown option: $1"
      ;;
  esac
done

if [[ -z "$ECC_PATH" ]]; then
  read -r -p "Enter local ECC repo path: " ECC_PATH
fi

[[ -d "$ECC_PATH" ]] || fail "ECC path does not exist: $ECC_PATH"
[[ -d "$ECC_PATH/skills" ]] || fail "Invalid ECC path (missing skills/): $ECC_PATH"

echo "Installing profile skills into: $PROFILE_ROOT"
mkdir -p "$PROFILE_ROOT/skills/software-development" "$PROFILE_ROOT/skills/ecc-import" "$PROFILE_ROOT/skills/ecc-agent-skills"

for skill in "${LOCAL_PROFILE_SKILLS[@]}"; do
  src="$SCRIPT_DIR/skills/software-development/$skill"
  dest="$PROFILE_ROOT/skills/software-development/$skill"
  copy_skill_dir "$src" "$dest"
  echo "  ✓ local skill: $skill"
done

for skill in "${ECC_SKILLS[@]}"; do
  src="$ECC_PATH/skills/$skill"
  dest="$PROFILE_ROOT/skills/ecc-import/$skill"
  copy_skill_dir "$src" "$dest"
  echo "  ✓ imported skill: $skill"
done

for skill in "${ECC_AGENT_ADAPTER_SKILLS[@]}"; do
  src="$SCRIPT_DIR/ecc-agent-skills/$skill"
  dest="$PROFILE_ROOT/skills/ecc-agent-skills/$skill"
  copy_skill_dir "$src" "$dest"
  echo "  ✓ agent-adapter skill: $skill"
done

if [[ "$INSTALL_SOUL" == "true" ]]; then
  [[ -f "$SCRIPT_DIR/SOUL.md" ]] || fail "Missing SOUL.md in profile repo"
  cp "$SCRIPT_DIR/SOUL.md" "$PROFILE_ROOT/SOUL.md"
  echo "  ✓ profile SOUL.md installed"
fi

echo
echo "Install complete."
echo "Profile root: $PROFILE_ROOT"
echo "ECC path: $ECC_PATH"
