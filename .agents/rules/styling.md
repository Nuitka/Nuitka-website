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
