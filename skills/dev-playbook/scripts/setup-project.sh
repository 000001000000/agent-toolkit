#!/usr/bin/env bash
set -euo pipefail

FORCE=0

for arg in "$@"; do
  case "$arg" in
    --force)
      FORCE=1
      ;;
    *)
      echo "Unknown option: $arg"
      echo "Usage: bash .agents/skills/dev-playbook/scripts/setup-project.sh [--force]"
      exit 1
      ;;
  esac
done

echo "Installing dev-playbook skill..."
npx skills add 000001000000/agent-toolkit/skills/dev-playbook

echo "Installing companion tdd skill (mattpocock)..."
npx skills add https://github.com/mattpocock/skills --skill tdd

mkdir -p .github

SRC=".agents/skills/dev-playbook/templates/copilot-instructions.md"
DEST=".github/copilot-instructions.md"
MARKER_BEGIN="# BEGIN dev-playbook managed block"
MARKER_END="# END dev-playbook managed block"

if [[ ! -f "$SRC" ]]; then
  echo "Could not find template at $SRC."
  echo "Install may not have completed yet. Try running this script again."
  exit 1
fi

extract_source_block() {
  local src="$1"
  local out="$2"
  if grep -qF "$MARKER_BEGIN" "$src" && grep -qF "$MARKER_END" "$src"; then
    awk -v b="$MARKER_BEGIN" -v e="$MARKER_END" '
      $0 == b { in_block=1 }
      in_block { print }
      $0 == e { in_block=0 }
    ' "$src" > "$out"
  else
    cp "$src" "$out"
  fi
}

merge_managed_block() {
  local src="$1"
  local dest="$2"
  local tmp_block
  local tmp_out

  tmp_block="$(mktemp)"
  tmp_out="$(mktemp)"
  extract_source_block "$src" "$tmp_block"

  if grep -qF "$MARKER_BEGIN" "$dest" && grep -qF "$MARKER_END" "$dest"; then
    awk -v b="$MARKER_BEGIN" -v e="$MARKER_END" -v block_file="$tmp_block" '
      BEGIN {
        while ((getline line < block_file) > 0) {
          block = block line ORS
        }
        close(block_file)
      }
      $0 == b {
        printf "%s", block
        in_block = 1
        next
      }
      $0 == e {
        in_block = 0
        next
      }
      !in_block { print }
    ' "$dest" > "$tmp_out"
    mv "$tmp_out" "$dest"
    echo "Merged updated managed block into $dest"
  else
    {
      cat "$dest"
      echo
      cat "$tmp_block"
      echo
    } > "$tmp_out"
    mv "$tmp_out" "$dest"
    echo "Appended managed block to $dest"
  fi

  rm -f "$tmp_block" "$tmp_out"
}

if [[ -f "$DEST" && $FORCE -ne 1 ]]; then
  merge_managed_block "$SRC" "$DEST"
  echo "Setup complete."
  exit 0
fi

cp "$SRC" "$DEST"
echo "Installed workspace instructions at $DEST"

echo "Setup complete."
