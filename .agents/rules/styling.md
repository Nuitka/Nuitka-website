# Styling

- Our CSS goes into `_static/my_theme.css`, indented with tabs. Use the site variables
  `--our-color-yellow`, `--our-color-blue`, `--our-color-dark-blue`, `--our-color-green`,
  `--our-carousel-light-blue`, and `--our-lightgrey`.
- `sphinx_design` is styled through its `--sd-*` variables rather than by overriding its rules.
- PurgeCSS in `postcss.config.js` only scans the built HTML. Classes and attributes that only
  JavaScript adds are removed from the CSS unless they are in its safelist. Prefer styling classes
  that are in the HTML, which directives in `_ext/` give you.
- The theme styles code blocks with `div[class^=highlight]`, i.e. only when the class attribute
  starts with `highlight`. Put own classes on a wrapping container, not on the code block itself.
- Text contrast follows WCAG AA, 4.5:1. White text only on `--our-color-dark-blue`, use dark text
  (`#404040` or `#111`) on yellow, blue, green, and the light blue.
- Check pages at a width of 390 pixels for horizontal scrolling, and with JavaScript disabled.

## Vertical spacing

- Gaps follow the theme: 24 pixels between blocks, 30 before a section heading, 10 below a heading.
  New elements keep to that, e.g. 24 pixels below an embedded recording.
- Containers made by directives get no bottom padding, so the bottom margin of their last block
  merges with the next one. Padding there doubles gaps.
- The site gives `.sd-col` a bottom margin for stacked cards. A single row of cards that is followed
  by more content needs a container class that removes it, like `step-cards` on the introduction
  page, and uses the grid `:gutter:` for spacing.
- Measure the gaps between neighboring blocks in a browser at desktop and phone width before
  pushing, screenshots hide differences of a few pixels.
