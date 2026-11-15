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
  `examples.py` with `nuitka-example`, `nuitka-example-cast`, `tour-step` (numbered steps), and
  `program-output` (text a program prints).
- Every new directive also needs to be listed in `extra_rst_keywords` of
  `nuitka/tools/release/Documentation.py` in Nuitka, otherwise `rstfmt` fails on it during
  formatting. Directives nested inside a listed one need no entry.
- Code blocks use `.. code:: <language>`. Program output uses `program-output`, so it gets no copy
  button.

## Examples

- Do not write down what can be computed. Examples of compiling with Nuitka are
  `.. nuitka-example:: <main file>` blocks, their content is the program, the options say how to
  compile and run it. The extension compiles and runs it during the build and shows the command, the
  created files, the important log lines, and what the program prints. The module docstring of
  `_ext/examples.py` lists the options.
- Files an example works with go into `site/examples/<name>/`. Results are stored in
  `site/examples/<name>.json` and only made again when the example changes, commit them.
- Recording needs Nuitka in `Nuitka-develop`, a C compiler, and for `:requires:` network access to
  install packages. `NUITKA_EXAMPLES_RECORD=no` skips recording, `force` records everything again,
  e.g. for a new Nuitka release. `NUITKA_EXAMPLES_PYTHON` selects the Python to compile with.
- Record with a regularly installed Python. The Python shows in the results, e.g. with
  python-build-standalone the accelerated mode creates an extra launcher script next to the program,
  which users of normal installations do not get.
- Examples that cannot run unattended, like GUI programs, leave out `:run:`. Servers use
  `:timeout:`, and print with `flush=True` so the output is kept.

## Terminal recordings

- Recordings of examples come from `:cast:` of a `nuitka-example`, which records the same steps with
  `asciinema-automation` into `site/casts/<name>.cast`. `.. nuitka-example-cast:: <name>` shows it
  on any page, pages with it are read after the others so the cast exists.
- Other recordings use `.. asciinema:: ./casts/<name>.cast`, made with `make-casts.sh` from
  `casts/<name>.sh`. Casts are never written by hand.
- Do not give the `asciinema` directive options with a hyphen, like `idle-time-limit` or `start-at`,
  it writes them as invalid JavaScript and the player does not show. Example casts store their idle
  time limit in the cast instead.

## Page conventions

- Pages outside a toctree start with `:orphan:`. Pages have a `.. meta::` block with `:description:`
  and `:keywords:`, and end with `.. include:: variables.inc` (with `../` from sub folders) when
  they use substitutions.
- Getting started material belongs to the tours in `site/tours/`, e.g. the beginner tour.
- Class names containing `carousel` make `update.py` load `carousel.js` for that page, only use them
  for carousels.

## Facts

- Options, plugin names, and log messages of Nuitka are checked against the Nuitka source.
- Shown outputs come from real runs, for compilation through `nuitka-example`. Where a value is
  illustrative, the pull request says so.
