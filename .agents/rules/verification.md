# Verification

## Formatting

- Format changed reST and Python files with `./auto-format <files>`. It runs
  `autoformat-nuitka-source` of a Nuitka checkout in `Nuitka-develop`.
- It downloads `rstfmt` and `black` with pip into a private folder of Nuitka. The Python running it
  needs `pip`, otherwise reST files are not formatted and only a warning about the download is
  given. Check `git diff` afterwards: a left over `.. raw:: <directive>` line means formatting did
  not complete and has to be undone.
- CSS, JavaScript, and HTML are not formatted by it.

## Checks before a pull request

- The site builds without warnings for the changed pages, `python update.py --update-docs` or a
  `sphinx-build -W` of them.
- `python update.py --post-process` runs PostCSS with PurgeCSS, check that new rules survive.
- After changing casts, run `make-casts.sh` and look at the result in the built page.
- Look at changed pages in a browser at desktop and phone width, see `styling.md`.
