# VectorCraft / Nuitka artwork - TODO compilation

Open decisions and follow-ups from the Phase 1 audit. This file is the canonical index; the style
spec and guide refer to these IDs.

**Status legend:** `TODO` = not decided / not started, `WIP` = in progress, `BLOCKED` = waiting on a
decision or another task, `DONE` = closed and reflected in the spec.

| ID       | Status  | Topic                                         | Blocks publishing?                      |
| -------- | ------- | --------------------------------------------- | --------------------------------------- |
| TODO-001 | BLOCKED | Dark theme and dark artwork                   | Yes, for dark variants                  |
| TODO-002 | DONE    | Commercial palette                            | No, approved 2026-11-18                 |
| TODO-003 | TODO    | WCAG 2.2 AA contrast/compliance               | Yes, for new artwork text               |
| TODO-004 | DONE    | Footer logo references a missing SVG          | No, fixed                               |
| TODO-005 | DONE    | `_art/` → `_static/` post-processing pipeline | No, deterministic script exists         |
| TODO-006 | TODO    | OpenGraph meta tags for raster companions     | No, but OG files are unused until added |
| TODO-007 | DONE    | Confirm MCP roots and headless install        | No, verified                            |

______________________________________________________________________

## TODO-001 - Dark theme and dark artwork

**Why:** the current site has no dark theme. `_static/my_theme.css` contains no
`prefers-color-scheme` block, and the theme has no dark stylesheet. The only dark values in use are
Read the Docs chrome colours (`#1F1D1D`, `#343131`, `#B3B3B3`).

**Decision:** dark artwork may be produced for review, but **cannot be used yet**. The dark palette
in `style-spec.json` is anchored to the existing chrome and marked `review-only`.

**Rules until closed:**

- Keep dark variants in `_art/vectorcraft/review/` with a `-review` suffix.
- Do not write dark variants to `_static/` or reference them from templates.
- Do not treat the proposed dark tokens as approved site colours.

**Acceptance:** a dark theme is implemented or explicitly approved, the dark tokens are reviewed for
contrast, and the manifest gains approved `dark` outputs.

______________________________________________________________________

## TODO-002 - Commercial palette - **DONE**

**Resolved 2026-11-18:** the commercial palette is approved. It uses the metallic ramp derived from
sponsor amber `#B45F06` and brand yellow `#FFD43B`, plus the gold **outer-arm inlay** selected for
the emblem. The light commercial lockup is promoted to
`_static/brand/nuitka-commercial-lockup.svg/png` (gitignored until the site references it). The
legacy flat tier-card colours remain unchanged for now.

______________________________________________________________________

## TODO-003 - WCAG 2.2 AA contrast/compliance

This is the fifth Phase 1 finding (contrast on white) promoted to a tracked item.

**Why:** several official/site colours are not body-text safe on white:

- `#599DD2` on white: **2.93:1**
- `#78C933` on white: **2.06:1**
- `#00916E` on white: **3.88:1**
- `#D99A2B` (commercial gold) on white: too low for small text

The artwork rules already forbid these for small text, but the wider site has not been audited.

**Acceptance:**

1. Audit the site for small text set directly in the failing colours.
2. Replace with `#1C5E89`, `#404040`, or a darker semantic token.
3. Keep brand fills for graphics, large display type, and non-text accents.
4. Add automated contrast checks to the artwork export pipeline and a manual check for each new
   `_static/brand` file.
5. Re-run the audit when dark and commercial palettes are approved.
6. Publish an audit result; do not claim WCAG 2.2 AA compliance before then.

______________________________________________________________________

## TODO-004 - Footer logo references a missing SVG - **DONE**

`_templates/footer.html` loads `/_static/Nuitka-Logo-Symbol.svg` at 28 × 28, but `_static/`
contained only `Nuitka-Logo-Symbol.png`.

**Resolved:** `_static/Nuitka-Logo-Symbol.svg` now exists as a clean, outlined 299.759 × 300.451
selection of the approved emblem. It contains no `<text>` or `<image>` and preserves the footer's
existing path.

**Follow-up if the symbol changes:** regenerate it with the MCP selection export and re-run
`_art/vectorcraft/scripts/verify-exports.sh`.

______________________________________________________________________

## TODO-005 - `_art/` → `_static/` post-processing pipeline - **DONE**

**Why:** source files must not be copied into the published tree. The working sources live in
`_art/vectorcraft/`; only processed exports belong in `_static/`.

**Implemented:** `_art/vectorcraft/scripts/export-approved.sh` regenerates every approved asset and
review-only variant with `vectorcraft-cli convert --outline-text`. It writes only to
`_static/brand/` and `_art/vectorcraft/review/`, then calls
`_art/vectorcraft/scripts/verify-exports.sh`, which checks for forbidden elements, `viewBox`, and
file size.

**Required pipeline:**

1. Open the `.vectorcraft` master from `_art/vectorcraft/src/`.
2. Duplicate or mark an export copy; never outline the saved master.
3. Run `type.createOutlines` on the export copy.
4. Export SVG with `outlineText: true` and `preserveEditing: false`.
5. Verify no `<text>`, `<tspan>`, `<image>`, or `<foreignObject>` remains.
6. Verify `viewBox`, `<title>`, `<desc>`, and file size < 512 KB.
7. Render PNG/WebP companions from the outlined master where the manifest requires them.
8. Write only approved derivatives to `_static/brand/`; write review-only outputs to
   `_art/vectorcraft/review/`.

**Acceptance:** a deterministic script or documented command sequence performs the above, and a
dry-run check reports no source files copied wholesale.

______________________________________________________________________

## TODO-006 - OpenGraph meta tags for raster companions

No `og:image` or `twitter:image` meta tags were found in the current templates or page sources. The
1200 × 630 PNG/WebP presets can be generated, but they will not be consumed by social previews until
the HTML head includes them.

**Acceptance:** decide where OG metadata is injected (template or per-page front matter), add the
tags, and point them at the approved 1200 × 630 output.

______________________________________________________________________

## TODO-007 - Confirm MCP roots and headless install - **DONE**

Phase 2 installed `vectorcraft-cli` 0.24.1 and configured MCP.

**Resolved:**

- `vectorcraft-cli` 0.24.1 is installed at `~/.local/bin/vectorcraft-cli`.
- `.opencode/opencode.json` and `.mcp.json` configure a headless server with the repo root as the
  read root and both `_art/vectorcraft` and `_static` as write roots.
- A live MCP session served 33 tools, and the logo suite exported successfully to `_static/brand`
  and `_art/vectorcraft/review`.
- The review folder is covered by the `_art/vectorcraft` write root.

**Use:**
`vectorcraft-cli mcp --headless --automation-read-root . --automation-write-root _art/vectorcraft --automation-write-root _static`.

______________________________________________________________________

## Decision log

| Date       | ID         | Change                                                                                                                         |
| ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 2026-11-17 | TODO-001   | Dark theme confirmed as later work; dark artwork is review-only.                                                               |
| 2026-11-17 | TODO-002   | Commercial palette confirmed as undecided; metal ramp is provisional.                                                          |
| 2026-11-17 | TODO-003   | Fifth Phase 1 finding promoted to a tracked WCAG 2.2 AA TODO.                                                                  |
| 2026-11-17 | TODO-005   | Source content moved from `assets/vectorcraft/` to `_art/vectorcraft/`.                                                        |
| 2026-11-17 | TODO-004   | Footer symbol exported to `_static/Nuitka-Logo-Symbol.svg`; TODO closed.                                                       |
| 2026-11-17 | TODO-005   | Deterministic `export-approved.sh` and `verify-exports.sh` added; TODO closed.                                                 |
| 2026-11-17 | TODO-007   | MCP server installed/configured and verified headless; TODO closed.                                                            |
| 2026-11-17 | WORDMARK   | Inter SemiBold 600 approved; effective 216 px; −27/1000 em N-u kerning. NanumGothic replaced, not retained during development. |
| 2026-11-17 | COMMERCIAL | Gold inlay outer arms selected for the commercial emblem; light lockup. Palette approved 2026-11-18.                           |
| 2026-11-18 | TODO-002   | Commercial palette approved; gold outer-arm inlay; light commercial lockup promoted to `_static/brand`.                        |
