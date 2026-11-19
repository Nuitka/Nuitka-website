# Nuitka VectorCraft Style Guide

Companion to [`style-spec.json`](./style-spec.json). This guide records the visual DNA that is
actually present in the Nuitka Website repository as of **2026-11-17**, then defines the controlled
extensions used for new VectorCraft artwork.

The short version:

> **Blue `#599DD2`, Yellow `#FFD43B`, Grey `#CCCCCC`, Dark Blue `#2A3990`, Green `#00916E` are the
> only official brand colours.** The site is a Sphinx 7 / `sphinx_rtd_theme` 3 site with a small
> override stylesheet. It has no dark theme: dark tokens below are TODO/review-only, not extracted
> and not shippable. The commercial palette was **approved on 2026-11-18**; its metal ramp and gold
> outer-arm inlay are now the approved commercial treatment. The logo is a rounded grey square with
> interlocking blue/yellow 45-degree ribbon paths whose negative space forms an N. Master artwork
> keeps editable text; every exported standalone SVG is outlined.

> **Source vs. published content.** Working sources live in `_art/vectorcraft/`. That folder is
> outside the Sphinx source tree and is never copied as-is. Only post-processed, approved export
> copies are written to `_static/brand/`. Review-only variants stay under `_art/` and use the
> `-review` suffix.

______________________________________________________________________

## 1. Where the DNA comes from

| What                                              | Source                                                                          |
| ------------------------------------------------- | ------------------------------------------------------------------------------- |
| Official brand colour list                        | `site/pages/website-manual.rst`, section **Color Palette**                      |
| Base typography, surfaces, borders, code          | `sphinx_rtd_theme` 3.0.2 `static/css/theme.css`                                 |
| Site-specific colour and layout overrides         | `_static/my_theme.css`                                                          |
| Build-time font substitution and CSS minification | `postcss.config.js`, `update.py`                                                |
| Logo masters                                      | `Nuitka-develop/doc/Logo/Nuitka-Logo-{Symbol,Horizontal,Vertical}.svg`          |
| Logo raster references                            | `Nuitka-develop/doc/images/Nuitka-Logo-*.png`, `images/nuitka-website-logo.png` |
| Website logo placement                            | `_templates/footer.html` (28 x 28 symbol)                                       |
| Art source root                                   | `_art/vectorcraft/` (working sources; outside the Sphinx source tree)           |
| Published static root                             | `_static/` (Sphinx `html_static_path`, copied to `output/_static`)              |
| Site build                                        | Sphinx `site/conf.py` + `shared_conf.py`; post-processing in `update.py`        |

The site is **not** Hugo, Tailwind, or Sphinx Design-only. It is Sphinx + reStructuredText with the
Read the Docs theme, plus Sphinx Design cards and ABlog. Do not invent a Tailwind token layer.

### Light vs. dark reality - **TODO-001**

`_static/my_theme.css` contains no `prefers-color-scheme` block, and the theme has no dark theme
stylesheet. The only genuinely dark values are the chrome colours used by the Read the Docs theme
(`#1F1D1D`, `#343131`, `#B3B3B3`). Dark artwork tokens are therefore marked **TODO / review-only**,
with those chrome values as their anchor.

**Production rule:** dark images and logo variants may be produced and reviewed now, but they must
not be written to `_static/` or referenced from templates until the dark theme exists and the
palette is approved. Use the `-review` suffix for those files.

______________________________________________________________________

## 2. Colour swatches

### 2.1 Official brand colours (source)

| Semantic name      | Hex       | RGB           | Use                                                 |
| ------------------ | --------- | ------------- | --------------------------------------------------- |
| `nuitka-primary`   | `#599DD2` | 89, 157, 210  | Primary blue; graphics, fills, large display shapes |
| `nuitka-accent`    | `#FFD43B` | 255, 212, 59  | Accent yellow; highlights, badges, focus marks      |
| `nuitka-neutral`   | `#CCCCCC` | 204, 204, 204 | Brand grey; emblem substrate, disabled UI, dividers |
| `nuitka-secondary` | `#2A3990` | 42, 57, 144   | Dark blue; CI/enterprise, deep gradient anchors     |
| `nuitka-green`     | `#00916E` | 0, 145, 110   | Secondary green; CI/action, success                 |

These five values come verbatim from the website manual. Do not substitute “close” blues or yellows
found on other Nuitka properties.

### 2.2 Logo gradient stops (source)

| Stop              | Hex       | RGB           | Notes            |
| ----------------- | --------- | ------------- | ---------------- |
| Logo blue start   | `#5A9FD4` | 90, 159, 212  | 135° light end   |
| Logo blue end     | `#306998` | 48, 105, 152  | 135° dark end    |
| Logo yellow start | `#FFD43B` | 255, 212, 59  | Official accent  |
| Logo yellow end   | `#FFE873` | 255, 232, 115 | Highlight end    |
| Logo grey bottom  | `#ADADAD` | 173, 173, 173 | Substrate shadow |
| Logo grey top     | `#DBDBDB` | 219, 219, 219 | Substrate light  |

The blue endpoint `#5A9FD4` is visually the official `#599DD2`; keep the exact gradient stops when
reconstructing the emblem, and use `#599DD2` for flat brand fills.

### 2.3 Light-mode surfaces and text (source)

| Semantic name          | Hex       | RGB           | Source / role                              |
| ---------------------- | --------- | ------------- | ------------------------------------------ |
| `surface-page`         | `#EDF0F2` | 237, 240, 242 | Theme body background                      |
| `surface-content`      | `#FCFCFC` | 252, 252, 252 | Content column, default light artboard     |
| `surface-paper`        | `#FFFFFF` | 255, 255, 255 | Cards, code blocks, max-contrast artboards |
| `surface-elevated`     | `#F8F9FA` | 248, 249, 250 | `--our-lightgrey`; raised panels           |
| `surface-subtle`       | `#F9F9F9` | 249, 249, 249 | Dropdowns                                  |
| `surface-table-stripe` | `#F3F6F6` | 243, 246, 246 | Table zebra rows                           |
| `surface-code`         | `#FFFFFF` | 255, 255, 255 | Code block background                      |
| `border-default`       | `#E1E4E5` | 225, 228, 229 | Hairlines, tables, connectors              |
| `border-strong`        | `#CCCCCC` | 204, 204, 204 | Strong dividers                            |
| `text-primary`         | `#404040` | 64, 64, 64    | Body copy                                  |
| `text-heading`         | `#1F1D1D` | 31, 29, 29    | Display ink (derived from theme chrome)    |
| `text-link`            | `#1C5E89` | 28, 94, 137   | Accessible site link blue                  |
| `text-link-hover`      | `#3091D1` | 48, 145, 209  | Hover only                                 |
| `accent-visited`       | `#9B59B6` | 155, 89, 182  | Visited links only                         |

### 2.4 Proposed dark palette - **TODO-001, review-only**

Anchored to the existing dark chrome, but **new and not approved**. Produce review artwork only; do
not publish or use it on the site yet.

| Semantic name              | Hex       | RGB           | Status                 |
| -------------------------- | --------- | ------------- | ---------------------- |
| `surface-dark`             | `#1F1D1D` | 31, 29, 29    | Source (theme chrome)  |
| `surface-dark-elevated`    | `#2A2727` | 42, 39, 39    | Derived                |
| `surface-dark-chrome`      | `#343131` | 52, 49, 49    | Source (theme sidebar) |
| `surface-dark-code`        | `#171515` | 23, 21, 21    | Derived                |
| `border-dark`              | `#3E3A3A` | 62, 58, 58    | Derived                |
| `border-dark-strong`       | `#565151` | 86, 81, 81    | Derived                |
| `text-on-dark`             | `#FCFCFC` | 252, 252, 252 | Source                 |
| `text-muted-on-dark`       | `#B3B3B3` | 179, 179, 179 | Source                 |
| `nuitka-primary-on-dark`   | `#7AB8E4` | 122, 184, 228 | Derived                |
| `nuitka-secondary-on-dark` | `#8E9BE8` | 142, 155, 232 | Derived                |
| `nuitka-green-on-dark`     | `#4FD1AC` | 79, 209, 172  | Derived                |
| `logo-grey-dark-start`     | `#2A2727` | 42, 39, 39    | Derived                |
| `logo-grey-dark-end`       | `#4A4545` | 74, 69, 69    | Derived                |

### 2.5 Commercial and tier colours - **approved 2026-11-18**

The live pricing grid still uses the legacy flat tier colours:

| Semantic name       | Hex       | RGB          | Existing class               |
| ------------------- | --------- | ------------ | ---------------------------- |
| `tier-commercial`   | `#78C933` | 120, 201, 51 | `.nuitka-offer-commercial`   |
| `tier-full-package` | `#403472` | 64, 52, 114  | `.nuitka-offer-full-package` |
| `tier-sponsor`      | `#B45F06` | 180, 95, 6   | `.nuitka-offer-sponsor`      |
| `tier-priority`     | `#007DD6` | 0, 125, 214  | `.nuitka-offer-priority`     |

The approved commercial palette extends these with a metallic ramp derived from sponsor amber
`#B45F06` and brand yellow `#FFD43B`:

| Semantic name                 | Hex       | RGB           | Approved role               |
| ----------------------------- | --------- | ------------- | --------------------------- |
| `nuitka-commercial-bronze`    | `#8C5A1B` | 140, 90, 27   | Shadow, outline, lower stop |
| `nuitka-commercial-gold`      | `#D99A2B` | 217, 154, 43  | Primary metal               |
| `nuitka-commercial-champagne` | `#F7D98B` | 247, 217, 139 | Specular highlight          |
| `nuitka-commercial-ink`       | `#2A1A08` | 42, 26, 8     | Text on gold/champagne      |

The approved commercial asset lives in `_static/brand/` and is gitignored until the site uses it.
The gold outer-arm inlay is part of the approved commercial emblem treatment.

### 2.6 Action / CI sub-brand colours

| Semantic name    | Hex       | RGB          | Use                        |
| ---------------- | --------- | ------------ | -------------------------- |
| `nuitka-ci`      | `#00916E` | 0, 145, 110  | Actions/CI badge           |
| `nuitka-watch`   | `#2A3990` | 42, 57, 144  | Watch/benchmarking badge   |
| `nuitka-docs`    | `#599DD2` | 89, 157, 210 | Documentation badge        |
| `nuitka-tooling` | `#1C5E89` | 28, 94, 137  | Tooling badge text/outline |

### 2.7 Contrast rules that matter - **TODO-003, target WCAG 2.2 AA**

The current site is **not audited as WCAG 2.2 AA compliant**. The rules below keep new artwork
compliant; the site-wide audit and remediation remain open. Measured WCAG 2.x contrast:

- `#1C5E89` on `#FCFCFC`: **6.80:1** - safe for body text.
- `#404040` on `#FCFCFC`: **10.4:1** - safe for body text.
- `#599DD2` on white: **2.93:1** - graphics and large display only; not body text.
- `#00916E` on white: **3.88:1** - large text only.
- `#78C933` on white: **2.06:1** - never text on white.
- `#FFD43B` on `#1F1D1D`: **11.77:1** - excellent on dark.
- `#7AB8E4` on `#1F1D1D`: **7.83:1** - safe body text on dark.
- `#B45F06` on white: **4.58:1** - just passes for body text.

Never place thin gold text directly on white. Use `commercial-ink` text inside a gold pill, or place
gold on `surface-dark`. The commercial palette was approved on 2026-11-18.

**Remediation checklist for TODO-003:**

1. Audit small text currently set in `#599DD2`, `#78C933`, or `#00916E` and replace it with
   `text-link`, `text-primary`, or a darker accessible token.
2. Keep brand fills for graphics, large display type, and non-text accents.
3. Add an automated contrast check to the artwork export pipeline.
4. Re-audit when the dark theme is approved; the commercial palette was approved on 2026-11-18.
5. Do not claim site-wide WCAG compliance until this checklist is complete.

______________________________________________________________________

## 3. Gradients

Full machine-readable stops are in `style-spec.json`. Summary:

| Name                      | Type   | Direction        | Stops                                                                 | Use                                                  |
| ------------------------- | ------ | ---------------- | --------------------------------------------------------------------- | ---------------------------------------------------- |
| `logo-blue`               | Linear | 135°             | `#5A9FD4` → `#306998`                                                 | Blue ribbon arms                                     |
| `logo-yellow`             | Linear | 135°             | `#FFD43B` → `#FFE873`                                                 | Yellow ribbon arms                                   |
| `logo-grey`               | Linear | 180°             | `#DBDBDB` → `#ADADAD`                                                 | Emblem substrate                                     |
| `logo-grey-dark`          | Linear | 180°             | `#4A4545` → `#2A2727`                                                 | Dark emblem substrate **(TODO-001, review-only)**    |
| `nuitka-signature`        | Linear | 120°             | `#2A3990` → `#599DD2` → `#7FC4EC`                                     | Hero bands, CTA panels                               |
| `nuitka-signature-deep`   | Linear | 135°             | `#1F1D1D` → `#232A44` → `#2A3990` → `#599DD2`                         | Dark hero / OG field                                 |
| `hero-radial-glow`        | Radial | centre 50% / 15% | white 16% → 5% → 0%                                                   | Optional vignette                                    |
| `commercial-metal`        | Linear | 135°             | `#6E3F0A` → `#8C5A1B` → `#D99A2B` → `#F7D98B` → `#E3B04B` → `#B9791F` | Approved commercial frame, pill, and outer-arm inlay |
| `commercial-metal-radial` | Radial | top centre       | `#FFE8A3` → `#F7D98B` → `#D99A2B` → `#8C5A1B` → `#6E3F0A`             | Approved commercial highlight                        |
| `action-ci`               | Linear | 135°             | `#00916E` → `#2A3990`                                                 | CI/Actions badge                                     |
| `action-watch`            | Linear | 135°             | `#2A3990` → `#599DD2`                                                 | Watch/benchmarking badge                             |
| `docs-header`             | Linear | 90°              | `#599DD2` → `#1C5E89`                                                 | Documentation bands                                  |

Angles are CSS-style clockwise from “to top”: 0° up, 90° right, 135° down-right, 180° down. All
gradient stops are opaque unless the JSON explicitly gives an opacity.

______________________________________________________________________

## 4. Typography and outlining

### 4.1 Active stacks

The site’s **source** stacks and the **built** stacks differ because `postcss.config.js` removes the
Lato and Roboto Slab `@font-face` declarations and rewrites their family references.

| Role     | Source stack (Sphinx theme)                                                                     | Built stack (what users actually get)                                            |
| -------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Body     | `Lato, proxima-nova, "Helvetica Neue", Arial, sans-serif`                                       | `ui-sans-serif, proxima-nova, "Helvetica Neue", Arial, sans-serif`               |
| Headings | `Roboto Slab, ff-tisa-web-pro, Georgia, Arial, sans-serif`                                      | `Rockwell, "Rockwell Nova", "Roboto Slab", "DejaVu Serif", "Sitka Small", serif` |
| Mono     | `SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", Courier, monospace` | Same (no rewrite)                                                                |
| Wordmark | `Inter SemiBold 600` (current); `NanumGothic 120` previous                                      | Outlined geometry on export                                                      |

For artwork that ships to the built site, use the **built stack**; do not design around a Lato or
Roboto Slab webfont that the build strips.

**VectorCraft 0.24.1 substitutes** (the headless runtime does not have Lato, Roboto Slab, Rockwell,
or Noto Sans):

| Role                   | Use in VectorCraft                       | Maps to                              |
| ---------------------- | ---------------------------------------- | ------------------------------------ |
| Headings               | `DejaVu Serif` (or `Source Serif 4`)     | Built heading stack’s serif fallback |
| Body / labels / badges | `Inter` (or `Source Sans 3`)             | Built `ui-sans-serif` body stack     |
| Code / terminals       | `DejaVu Sans Mono` (or `JetBrains Mono`) | Built mono stack                     |
| Nuitka wordmark        | `Inter SemiBold 600`                     | Current approved wordmark            |

The current wordmark is **Inter SemiBold 600** at an effective **216 px** in the 1200×260 lockup,
with **−27/1000 em** kerning on the `u` (equivalent to −3 px at the 112 px comparison size).
NanumGothic 120 was the previous original; it is not retained during development and must not be
used for new artwork. Do not retype the current wordmark in another face, and do not separate the
N-u kerning from the wordmark when resizing.

### 4.2 Type rules

- Headlines: serif slab stack, weight 700, line-height 1.15, tracking `-0.01em`.
- Body, captions, diagram labels, badges: sans stack, weight 400; bold is 700.
- Code, terminal, benchmark readouts: mono stack.
- Hero headlines: 64-96 px, 24-38 characters per line, never more than 42.
- OpenGraph subhead: 28-36 px.
- Documentation diagram title: 36-56 px; labels 18-24 px.
- Badge titles: 40-72 px; kickers 12-16 px uppercase with `0.12em` tracking.
- Never use faux bold/italic, scripts, novelty faces, or a substitute for the Nuitka wordmark.

### 4.3 Outlining policy (strict)

**Master `.vectorcraft` files keep editable text.** Exported copies do not.

- Apply `type.createOutlines` to a duplicate/export copy, never to the saved master.
- Export standalone SVGs with `outlineText: true` and `preserveEditing: false`.
- Verify: the exported file must contain **no** `<text>` and **no** `<image>` elements.
- Text for `<img>` tags, CSS backgrounds, favicons, social cards, and downloads is always outlined.
- Live effects that would bake a raster `<image>` into the SVG are forbidden unless a manifest
  explicitly marks the asset as intentionally raster-backed with source and licence recorded.
- Raster companions are rendered from the outlined vector master, never from a UI screenshot.

______________________________________________________________________

## 5. Artboard presets

| Preset                     | Size           | Safe area | Default background      | Purpose                      |
| -------------------------- | -------------- | --------- | ----------------------- | ---------------------------- |
| OpenGraph / Hero           | **1200 × 630** | 64 px     | `nuitka-signature-deep` | Social cards, release heroes |
| Documentation architecture | **1000 × 560** | 48 px     | `surface-content`       | Compiler pipelines, diagrams |
| Product / feature badge    | **400 × 400**  | 32 px     | transparent             | Square badges, tiles         |
| Horizontal lockup          | **1200 × 300** | 40 px     | transparent             | Sub-brand lockups            |
| Logo horizontal            | **1200 × 260** | 40 px     | transparent             | Primary logo lockup          |
| Logo vertical              | **640 × 760**  | 48 px     | transparent             | Vertical / print placements  |
| Favicon                    | **512 × 512**  | 48 px     | transparent             | Favicon and touch icons      |

OpenGraph raster companions are produced at 1200 × 630 PNG, 2400 × 1260 PNG (`@2x`), and 1200 × 630
WebP (quality 88). `document.exportSettings` should carry the `nuitka-opengraph` preset defined in
the JSON so the raster pair is never re-invented per session.

______________________________________________________________________

## 6. Logo geometry and construction

### 6.1 Emblem

- Master viewBox: **`0 0 198.073 198.53`** (essentially square, ratio **0.9977**).
- Rounded-square substrate: **198.073 × 198.53**, corner radius **18.216** = **9.2%** of width.
- Four interlocking ribbon paths, thickness **25.52** = **12.9%** of width.
- Folds are **45°**; arms meet at **90°**.
- The negative space forms a geometric **N**. Blue occupies the upper-left vertical and lower-left
  inner arm; yellow occupies the upper-right inner arm and lower-left outer arm.
- The grey substrate must remain visible as a thin channel between the ribbon arms. Do not merge
  blue and yellow into touching shapes.
- Gradients: blue 135° `#5A9FD4 → #306998`; yellow 135° `#FFD43B → #FFE873`; grey 180°
  `#DBDBDB → #ADADAD`.
- Clear space: **0.25 × symbol height** on all sides (≈ 49.6 px at master size).
- Minimum digital size: **16 × 16 px** for the symbol; **120 px wide** for the horizontal lockup.

### 6.2 Horizontal lockup

- Master size: **478.2 × 96.991** (ratio **4.93:1**).
- Symbol height: 92.475; wordmark baseline: 91.172; wordmark start x: 101.735.
- Gap between symbol and wordmark: **9.3 px** at master size (≈ 9.6% of symbol width).
- Wordmark: **Inter SemiBold 600**, effective **216 px**, black, tracking 0, with **−27/1000 em**
  kerning on the `u` (the N-u pair). Outline it on export.
- The wordmark cap height sits under the symbol height; the baseline stays at the original optical
  position. Do not vertically centre by naive bounding box, and do not increase the wordmark above
  the emblem height.

### 6.3 Vertical lockup

- Master size: **340.684 × 318.732** (ratio **1.069:1**).
- Symbol above, wordmark centred beneath, ≈ 24 px optical gap at master size.
- Keep the same emblem and wordmark proportions; the wordmark is Inter SemiBold 600 with the same
  −27/1000 em N-u kerning. Only the composition changes.

### 6.4 Background variants

| Variant          | Emblem                                     | Wordmark / ink         |
| ---------------- | ------------------------------------------ | ---------------------- |
| Standard light   | Full colour, `logo-grey` substrate         | Black / `text-heading` |
| Standard dark    | Full colour, `logo-grey-dark` substrate    | `text-on-dark`         |
| Monochrome light | Black substrate, white ribbon N (knockout) | Black / `text-heading` |
| Monochrome dark  | White substrate, black ribbon N (knockout) | White / `text-on-dark` |

The implemented monochrome assets are **two-tone knockouts**, not single-ink silhouettes. The
substrate and the ribbon N use two inks so the negative-space N remains legible; the wordmark uses
the substrate ink. Do not merge the substrate and ribbons into one flat ink, and do not thin or
thicken the arms to compensate for the loss of colour.

______________________________________________________________________

## 7. Commercial lockup - **approved 2026-11-18**

The commercial palette and lockup are approved. The asset lives in `_static/brand/` and is
gitignored until the site references it.

- Core emblem and wordmark proportions are unchanged.
- The commercial emblem uses a **gold outer-arm inlay**: the two large outer N arms are filled with
  `commercial-metal`; the two inner arms keep the brand blue/yellow. This is the tier signal inside
  the mark itself.
- Default variant is **light**: `surface-content`, dark Inter wordmark, the inlaid emblem,
  `commercial-bronze` frame/divider, and an approved gold pill. A dark-surface commercial variant is
  deferred to TODO-001.
- Add a **precision geometric frame**: 1.5 px `commercial-bronze` rule on light (or
  `commercial-metal` on dark), 8 px radius, 12 px inset.
- Add a **COMMERCIAL pill** to the right of the wordmark, separated by a 24 px rule segment:
  uppercase, 0.12em tracking, bold sans, 28-36 px height at 1200 px lockup width.
- Pill fill: `commercial-metal` or `commercial-metal-radial`. Pill text: `commercial-ink` on
  champagne/gold, or `commercial-champagne` on bronze.
- No crowns, laurels, shields, bevels, or faux-3D gloss. The signal is engineering precision, not
  luxury clip-art.

______________________________________________________________________

## 8. Action / CI / tooling sub-brands

All three are modular horizontal lockups on the 1200 × 300 preset.

| Sub-brand          | Label   | Gradient / accent                    | Extra geometry                                |
| ------------------ | ------- | ------------------------------------ | --------------------------------------------- |
| CI / Actions       | `CI`    | `action-ci` (`#00916E → #2A3990`)    | Squared terminal frame + chevron prompt glyph |
| Watch / benchmarks | `WATCH` | `action-watch` (`#2A3990 → #599DD2`) | Benchmark grid or stopwatch tick ring         |
| Docs               | `DOCS`  | `docs-header` (`#599DD2 → #1C5E89`)  | Open documentation bracket frame              |

Keep the emblem at the same optical size as the core lockup. The label sits to the right, followed
by the sub-brand word; the emblem is never replaced by a generic icon.

______________________________________________________________________

## 9. Naming and output

- Art source root: `_art/vectorcraft/`
- Masters: `_art/vectorcraft/src/{asset}.vectorcraft`
- Manifest: `_art/vectorcraft/manifests/brand-assets.yaml`
- SVG: `_static/brand/{asset}-{theme}.svg`
- PNG: `_static/brand/{asset}-{theme}{suffix}.png`
- WebP: `_static/brand/{asset}-{theme}.webp`
- Review-only: `_art/vectorcraft/review/{asset}-{theme}-review.{svg,png,webp}`

Use lowercase kebab-case. Theme suffixes are `-light`, `-dark`, `-mono`, `-mono-dark`; omit `-light`
when there is only one default light variant. Never overwrite the historical files in `images/svg/`
or `Nuitka-develop/doc/Logo/`.

**Never copy `_art/` into `_static/`.** The source folder contains editable masters and review work.
Only post-processed, approved derivatives belong in `_static/brand/`.

______________________________________________________________________

## 10. Definition of done for an export

1. `doc_inspect` shows no clipped or out-of-bounds geometry.
2. `render_preview` at `max_side: 1024` has been visually checked for alignment, kerning, optical
   balance, and dark/light contrast.
3. The SVG contains no `<text>`, `<tspan>`, `<image>`, or `<foreignObject>`.
4. The SVG has `viewBox`, `role="img"`, `<title>`, and `<desc>` (or a manifest-provided alt text).
5. File size is under 512 KB; paths are clean and not a traced bitmap.
6. PNG/WebP companions, where required, are rendered from the outlined master at the specified
   dimensions.
7. The manifest entry and the source master are both updated, and the output path matches the naming
   convention above.
8. **TODO gate:** if the asset is a dark variant, its TODO is still open, or the asset is otherwise
   review-only, it stays in `_art/vectorcraft/review/` and is **not** written to `_static/`. The
   commercial palette is approved; the commercial lockup is an approved asset.

______________________________________________________________________

## 11. Open decisions and TODOs

The compiled list is [`TODO.md`](./TODO.md). The items that affect artwork production are:

| ID       | Topic                         | Effect on artwork                                                                          |
| -------- | ----------------------------- | ------------------------------------------------------------------------------------------ |
| TODO-001 | Dark theme                    | Dark variants are review-only; do not publish them yet.                                    |
| TODO-002 | Commercial palette            | **Done:** palette approved 2026-11-18; gold outer-arm inlay selected.                      |
| TODO-003 | WCAG 2.2 AA compliance        | Keep failing brand colours out of small text; site audit is open.                          |
| TODO-004 | Footer symbol SVG             | **Done:** `_static/Nuitka-Logo-Symbol.svg` is a clean outlined selection.                  |
| TODO-005 | `_art/` → `_static/` pipeline | **Done:** `scripts/export-approved.sh` and `scripts/verify-exports.sh`.                    |
| TODO-006 | OpenGraph meta tags           | OG raster companions are unused until the head tags exist.                                 |
| TODO-007 | MCP roots                     | **Done:** headless MCP configured and verified; read `_art/`, write `_static/` and review. |

### Current approved outputs

- `_static/brand/nuitka-logo-horizontal-light.svg` + PNG/@2x
- `_static/brand/nuitka-logo-horizontal-mono.svg` + PNG
- `_static/brand/nuitka-symbol-light.svg` + PNG/@2x
- `_static/Nuitka-Logo-Symbol.svg` (tight footer symbol)
- `_static/brand/nuitka-ci-lockup.svg` + PNG
- `_static/brand/nuitka-watch-lockup.svg` + PNG
- `_static/brand/nuitka-docs-lockup.svg` + PNG
- `_static/brand/nuitka-commercial-lockup.svg` + PNG

Review-only outputs live in `_art/vectorcraft/review/` for the dark and mono-dark variants. They are
not referenced by the site.

Regenerate the approved set with `_art/vectorcraft/scripts/export-approved.sh`; it ends by running
`_art/vectorcraft/scripts/verify-exports.sh`.
