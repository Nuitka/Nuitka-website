#!/usr/bin/env bash
# Verify the published SVG derivatives. This script never edits them.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
FILES=(
  "$ROOT/_static/brand/nuitka-logo-horizontal-light.svg"
  "$ROOT/_static/brand/nuitka-logo-horizontal-mono.svg"
  "$ROOT/_static/brand/nuitka-symbol-light.svg"
  "$ROOT/_static/brand/nuitka-ci-lockup.svg"
  "$ROOT/_static/brand/nuitka-watch-lockup.svg"
  "$ROOT/_static/brand/nuitka-docs-lockup.svg"
  "$ROOT/_static/brand/nuitka-commercial-lockup.svg"
  "$ROOT/images/svg/nuitka-commercial-lockup.svg"
  "$ROOT/_static/Nuitka-Logo-Symbol.svg"
)

fail=0
for f in "${FILES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "MISSING  $f"
    fail=1
    continue
  fi
  size=$(wc -c < "$f")
  if grep -Eq '<text|<tspan|<image|<foreignObject' "$f"; then
    echo "DIRTY    $f (contains text/image/foreignObject)"
    fail=1
    continue
  fi
  if ! grep -q 'viewBox=' "$f"; then
    echo "NO VIEWBOX $f"
    fail=1
    continue
  fi
  if (( size > 524288 )); then
    echo "TOO BIG  $f ($size bytes)"
    fail=1
    continue
  fi
  echo "OK       $f ($size bytes)"
done

if (( fail != 0 )); then
  echo "Export verification failed." >&2
  exit 1
fi
echo "All published SVGs are clean, sized, and contain a viewBox."
