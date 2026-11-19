#!/usr/bin/env bash
# Deterministic export of the approved Nuitka logo suite.
# Source masters live in _art/; only exported derivatives are written to _static/.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
CLI="${VECTORCRAFT_CLI:-vectorcraft-cli}"
SRC="$ROOT/_art/vectorcraft/src/nuitka-logos.vectorcraft"
OUT="$ROOT/_static/brand"
REVIEW="$ROOT/_art/vectorcraft/review"

if ! command -v "$CLI" >/dev/null 2>&1; then
  echo "vectorcraft-cli not found on PATH (set VECTORCRAFT_CLI to override)." >&2
  exit 1
fi
if [[ ! -f "$SRC" ]]; then
  echo "Missing source master: $SRC" >&2
  exit 1
fi

mkdir -p "$OUT" "$REVIEW"

svg() {
  local artboard="$1" dest="$2"
  "$CLI" convert "$SRC" "$dest" --artboard "$artboard" --outline-text --decimals 3 >/dev/null
}

png() {
  local artboard="$1" ppi="$2" dest="$3"
  "$CLI" convert "$SRC" "$dest" --artboard "$artboard" --ppi "$ppi" >/dev/null
}

# Approved light/mono/symbol assets
svg 0 "$OUT/nuitka-logo-horizontal-light.svg"
png 0 72  "$OUT/nuitka-logo-horizontal-light.png"
png 0 144 "$OUT/nuitka-logo-horizontal-light@2x.png"

svg 2 "$OUT/nuitka-logo-horizontal-mono.svg"
png 2 72  "$OUT/nuitka-logo-horizontal-mono.png"

svg 3 "$OUT/nuitka-symbol-light.svg"
png 3 72  "$OUT/nuitka-symbol-light.png"
png 3 144 "$OUT/nuitka-symbol-light@2x.png"

# Approved CI / Watch / Docs lockups
svg 5 "$OUT/nuitka-ci-lockup.svg"
png 5 72  "$OUT/nuitka-ci-lockup.png"

svg 6 "$OUT/nuitka-watch-lockup.svg"
png 6 72  "$OUT/nuitka-watch-lockup.png"

svg 7 "$OUT/nuitka-docs-lockup.svg"
png 7 72  "$OUT/nuitka-docs-lockup.png"

# Approved commercial lockup (palette approved 2026-11-18)
svg 4 "$OUT/nuitka-commercial-lockup.svg"
png 4 72  "$OUT/nuitka-commercial-lockup.png"

# Review-only variants (never published; dark theme is still TODO-001)
svg 1 "$REVIEW/nuitka-logo-horizontal-dark-review.svg"
png 1 72  "$REVIEW/nuitka-logo-horizontal-dark-review.png"

svg 8 "$REVIEW/nuitka-logo-horizontal-mono-dark-review.svg"
png 8 72  "$REVIEW/nuitka-logo-horizontal-mono-dark-review.png"

# The legacy footer symbol is a cropped selection of the emblem and is generated
# by the MCP selection export; it is intentionally not rewritten here.
echo "Exported approved and review assets."
echo "Note: _static/Nuitka-Logo-Symbol.svg is a cropped emblem selection; regenerate it with the MCP selection export."
"$ROOT/_art/vectorcraft/scripts/verify-exports.sh"
