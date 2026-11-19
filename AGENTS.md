# Nuitka Website - VectorCraft agent rules

These rules apply to artwork produced with the VectorCraft MCP server for the Nuitka website. Read
`_art/vectorcraft/STYLE_GUIDE.md`, `_art/vectorcraft/style-spec.json`, and
`_art/vectorcraft/TODO.md` before creating or changing an asset.

## Folders

| Folder                           | Purpose                                     | Copied to the site? |
| -------------------------------- | ------------------------------------------- | ------------------- |
| `_art/vectorcraft/src/`          | Editable `.vectorcraft` masters             | No                  |
| `_art/vectorcraft/manifests/`    | Declarative asset intents                   | No                  |
| `_art/vectorcraft/review/`       | Review-only dark exports                    | No                  |
| `_art/vectorcraft/scripts/`      | Export and verification helpers             | No                  |
| `_static/brand/`                 | Approved, outlined SVG/PNG/WebP derivatives | Yes                 |
| `_static/Nuitka-Logo-Symbol.svg` | Legacy footer logo path                     | Yes                 |

Never copy `_art/` into `_static/`. Only post-processed, approved derivatives are published.

## MCP setup

The project MCP server is configured in `.opencode/opencode.json` and `.mcp.json`:

```text
vectorcraft-cli mcp --headless \
  --automation-read-root . \
  --automation-write-root _art/vectorcraft \
  --automation-write-root _static
```

Use the tools through Code Mode (`tools.vectorcraft.*`). The important tools are `command_batch`,
`command_run`, `doc_inspect`, `render_preview`, `screenshot`, `export`, `open_file`, and
`save_file`.

## Batching

- **Prefer `command_batch` over repeated `command_run` calls.** It cuts round-trips and keeps
  related edits together.
- Use `atomic: true` with a descriptive `label` for a logical edit (for example
  `"Build core lockup"`), so a failed attempt is one undo step.
- **`command_batch` is non-transactional.** If a step fails, the earlier steps remain applied.
  - Inspect the document with `doc_inspect`.
  - If the state is not what you intended, undo to the saved checkpoint or reopen the last
    `.vectorcraft` save. Save a known-good checkpoint with `save_file` before risky batches.
- A batch holds at most 256 steps. Split large construction jobs into named phases.
- Never assume a batch succeeded because the call returned. Check `failed` and the per-step
  `results`.

### Known pitfalls

- **`draw_shape` and `draw_path` are MCP tools, not engine commands.** Call
  `tools.vectorcraft.draw_shape(...)` directly, or use `"id": "draw_shape"` as a `command_batch`
  step. `run_command({command: "draw_shape"})` fails with `unknown command`.
- **Failures can revert the in-memory document to the last saved file.** Save a checkpoint with
  `save_file` after each successful artboard or variant. Do not chain an uncertain edit after
  unsaved work.
- **Verify the active document before editing.** `file.new` and `open_file` return document indices,
  and `document.activate` uses a 0-based index. Run `doc_inspect` and check `title`/`path` before
  applying edits; it is easy to clear or paint the wrong document.
- **IDs change after saves/reopens.** Re-inspect the object before using a numeric ID in a later
  call. Do not assume an ID from an earlier session still names the same object.
- **A failed atomic batch may undo edits made in that batch.** If the document is not what you
  expect, inspect, reopen the saved checkpoint, and rebuild the small failed step.

## Visual verification loop

After every major layout change, boolean operation, logo reconstruction, or text update:

1. Run `doc_inspect` (or `inspect_document`) and check:
   - artboard bounds and object bounds;
   - clipping / unexpected negative coordinates;
   - selection and layer structure;
   - text overflow, if any.
2. Run `render_preview` with `max_side: 1024` (or `screenshot` with an explicit path when you need
   to inspect the PNG with the `read` tool).
3. Visually check:
   - alignment to the artboard and safe area;
   - kerning and word spacing;
   - optical balance of the emblem against the wordmark;
   - contrast on light and dark backgrounds.
4. Only then export.
5. Re-check the exported SVG for `<text>`, `<image>`, clipping, and a plausible file size.

## Clean SVG exports

- Standalone SVGs for `<img>` tags, CSS backgrounds, favicons, social cards, and downloads must have
  all text outlined.
  - Use `export` with `outlineText: true`, or run `type.createOutlines` on an export copy.
  - Master `.vectorcraft` files keep editable text.
- Do not let live effects bake raster `<image>` tags into an SVG unless the manifest explicitly
  marks the asset as intentionally raster-backed and records the source, licence, and reason.
  - Prefer expanding/removing effects that would rasterize.
  - `filter`/shadow effects are acceptable only if the exporter keeps them vector (the export reply
    must not report raster warnings).
- Required SVG checks:
  - no `<text>`, `<tspan>`, `<image>`, or `<foreignObject>`;
  - `viewBox` present;
  - `<title>` and `<desc>` present (or the manifest supplies alt text);
  - file size under 512 KB.
- Name outputs with the conventions in the style guide:
  - `_static/brand/{asset}-{theme}.svg`
  - `_static/brand/{asset}-{theme}{suffix}.png`
  - `_static/brand/{asset}-{theme}.webp`
  - review-only: `_art/vectorcraft/review/{asset}-{theme}-review.{svg,png,webp}`

## OpenGraph raster companions

`document.exportSettings` reads the last `document.exportForScreens` params saved in the document.
There is no separate setter. Configure the 1200 × 630 companions by running
`document.exportForScreens` with the `nuitka-opengraph` settings (and let it store them), or export
directly with explicit formats.

Target preset:

```json
{
  "artboard": "og-hero",
  "formats": [
    { "format": "png", "scale": 1, "suffix": "" },
    { "format": "png", "scale": 2, "suffix": "@2x" },
    { "format": "webp", "scale": 1, "suffix": "", "quality": 88 }
  ],
  "settings": {
    "png": { "background": "white", "antiAlias": "type" },
    "webp": { "background": "white" }
  }
}
```

Never generate the OpenGraph raster from a UI screenshot; render it from the approved vector master.

## TODOs that block publishing

- **TODO-001:** dark artwork is review-only until the site has a dark theme. Do not write dark
  variants to `_static/`.
- **TODO-002 (done):** the commercial palette was approved on 2026-11-18. The light commercial
  lockup with the gold outer-arm emblem inlay is in `_static/brand/` and is gitignored until used.
- **TODO-003:** target WCAG 2.2 AA. Do not put `#599DD2`, `#78C933`, `#00916E`, or commercial gold
  in small text on white. The site-wide audit is still open.
- **TODO-004 (done):** `_static/Nuitka-Logo-Symbol.svg` is the tight outlined footer symbol. It is a
  cropped selection export; regenerate it with `select.set {ids:[38]}` +
  `export {selection:true, outlineText:true}` if the emblem changes.
- **TODO-005 (done):** use `_art/vectorcraft/scripts/export-approved.sh` to regenerate the approved
  and review assets. It calls `_art/vectorcraft/scripts/verify-exports.sh`, which rejects text,
  images, missing `viewBox`, or oversized SVGs. Never hand-edit a published SVG.
- **TODO-007 (done):** the headless MCP server and roots are configured in `.opencode/opencode.json`
  and `.mcp.json`.

## Wordmark

The approved wordmark is **Inter SemiBold 600**, effective **216 px** in the 1200×260 lockup, with
**−27/1000 em** kerning on the `u`. Do not retype it in another face. NanumGothic was the previous
original; no archive is retained during development, and it must not be used for new artwork.

## Current outputs

Approved and published under `_static/brand/`:

- `nuitka-logo-horizontal-light.svg` + PNG/@2x
- `nuitka-logo-horizontal-mono.svg` + PNG
- `nuitka-symbol-light.svg` + PNG/@2x
- `nuitka-ci-lockup.svg` + PNG
- `nuitka-watch-lockup.svg` + PNG
- `nuitka-docs-lockup.svg` + PNG
- `nuitka-commercial-lockup.svg` + PNG
- `_static/Nuitka-Logo-Symbol.svg` (tight footer symbol)

Review-only, under `_art/vectorcraft/review/`:

- `nuitka-logo-horizontal-dark-review.svg` + PNG
- `nuitka-logo-horizontal-mono-dark-review.svg` + PNG

## Quick start

```text
1. file.new { width: 1200, height: 630, units: "Pixels", name: "Scratch" }
2. create swatches / gradients with swatch.new (global: true)
3. draw with tools.vectorcraft.draw_shape / draw_path; use text.create for batchable text
4. doc_inspect + render_preview (max_side 1024)
5. save_file after each successful variant
6. export approved SVG/PNG with outlineText:true to _static/brand/
```

If a command fails, read the error, run `doc_inspect`, and reopen the checkpoint. Do not retry a
failed batch blindly.
