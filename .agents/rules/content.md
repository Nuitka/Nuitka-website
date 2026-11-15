# Content

## Pages are reST only

- Pages are reST files in `site/`. Do not add HTML files, and do not include HTML with
  `.. raw:: html` and `:file:`. HTML files are not reviewed.
- Do not add JavaScript files unless there is no other way, and ask first. Interactive parts come
  from Sphinx extensions that work without our own scripts.
- Small HTML snippets, such as icons, are substitutions in `site/variables.inc`, e.g.
  `|DOWNLOAD_SYMBOL|`. `update.py` expands the `|..._SYMBOL|` ones after the build. Text
  substitutions like `|SUPPORTED_PYTHONS|` and `|NUITKA_VERSION|` are used instead of writing
  versions into pages.

## Building blocks

- Layout and interaction use `sphinx_design`: `grid` with `grid-item-card`, `tab-set` with
  `tab-item`, `dropdown`, and buttons. These work without JavaScript.
- Structures that repeat get a directive in `_ext/`, registered in `extensions` of `shared_conf.py`.
  Directives create normal docutils nodes with CSS classes. Existing ones are `carousel.py`, and
  `examples.py` with `tour-step` (numbered steps), `example-part` (input, command, output, run of an
  example), and `program-output` (text a program prints).
- Every new directive also needs to be listed in `extra_rst_keywords` of
  `nuitka/tools/release/Documentation.py` in Nuitka, otherwise `rstfmt` fails on it during
  formatting. Directives nested inside a listed one need no entry.
- Code blocks use `.. code:: <language>`. Program output uses `program-output`, so it gets no copy
  button.

## Terminal recordings

- Recordings use `.. asciinema:: ./casts/<name>.cast` from `sphinxcontrib.asciinema`.
- Casts are recorded with `make-casts.sh`, never written by hand. The steps are in `casts/<name>.sh`
  for `asciinema-automation` (`#$ delay`, `#$ expect \$`). Files a cast works with go into
  `casts/<name>/`, the recording runs in a copy of that folder.
- Do not give the directive options with a hyphen, like `idle-time-limit` or `start-at`, it writes
  them as invalid JavaScript and the player does not show. The idle time limit is stored in the cast
  by `make-casts.sh`.

## Page conventions

- Pages outside a toctree start with `:orphan:`. Pages have a `.. meta::` block with `:description:`
  and `:keywords:`, and end with `.. include:: variables.inc` (with `../` from sub folders) when
  they use substitutions.
- Getting started material belongs to the tours in `site/tours/`, e.g. the beginner tour.
- Class names containing `carousel` make `update.py` load `carousel.js` for that page, only use them
  for carousels.

## Facts

- Options, plugin names, and log messages of Nuitka are checked against the Nuitka source.
- Shown outputs come from real runs. Where a value is illustrative, like a version number, the pull
  request says so.
