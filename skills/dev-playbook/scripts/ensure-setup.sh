#!/usr/bin/env bash
set -euo pipefail

MARKER_DIR=".dev-playbook"
MARKER_FILE="$MARKER_DIR/.initialized"

echo "Running dev-playbook setup/sync..."

mkdir -p .github

SRC=".agents/skills/dev-playbook/templates/copilot-instructions.md"
DEST=".github/copilot-instructions.md"
MARKER_BEGIN="# BEGIN dev-playbook managed block"
MARKER_END="# END dev-playbook managed block"

template_sha() {
  shasum -a 256 "$1" | awk '{print $1}'
}

read_marker_value() {
  local key="$1"
  if [[ -f "$MARKER_FILE" ]]; then
    awk -F '=' -v k="$key" '$1 == k { print $2 }' "$MARKER_FILE" | tail -n 1
  fi
}

if [[ ! -f "$SRC" ]]; then
  echo "Could not find template at $SRC"
  echo "Ensure dev-playbook is installed before running setup."
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

current_template_sha="$(template_sha "$SRC")"
stored_template_sha="$(read_marker_value template_sha)"

# One-time dependency install on first initialization only.
if [[ ! -f "$MARKER_FILE" ]]; then
  echo "Installing companion tdd skill (mattpocock)..."
  npx skills add https://github.com/mattpocock/skills --skill tdd
fi

if [[ ! -f "$DEST" ]]; then
  cp "$SRC" "$DEST"
  echo "Installed workspace instructions at $DEST"
else
  if [[ "$stored_template_sha" != "$current_template_sha" ]]; then
    merge_managed_block "$SRC" "$DEST"
  else
    echo "Managed instructions block already up to date."
  fi
fi

mkdir -p "$MARKER_DIR"
{
  printf '%s\n' "initialized_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf '%s\n' "template_sha=$current_template_sha"
} > "$MARKER_FILE"

echo "Setup/sync completed."
