---
name: nuitka-changelog
description: Use when creating or updating Nuitka changelog entries (hotfix releases like 4.1.3 or upcoming releases) in the Nuitka website repository, by running update-changelog.py to generate the commit prompt and editing site/changelog/Changelog-next.rst.
---

# Nuitka Website Changelog Updates

This skill covers producing changelog entries in the Nuitka website repository for a hotfix release
(e.g. `4.1.3`) or a develop update, based on the git history of the Nuitka repository.

## Workflow

1. Generate the prompt:

   ```
   python3 update-changelog.py 4.1.3 --nuitka-repo ../Nuitka-develop   # hotfix
   python3 update-changelog.py 4.2 --nuitka-repo ../Nuitka-develop     # final release
   python3 update-changelog.py 4.2rc3 --nuitka-repo ../Nuitka-develop  # pre-release
   ```

   - `VERSION` is required and must be one of: hotfix `X.Y.Z` (e.g. `4.1.3`), final `X.Y` (e.g.
     `4.2`), or pre-release `X.YrcN` (e.g. `4.2rc3`). Anything else is rejected.
   - The line "It currently covers changes up to version **...**." tracks the last `VERSION`
     argument passed to the script and is updated by the script itself, never by hand.
   - Running with a `VERSION` that is already the documented state yields an empty range, that is
     expected.
   - `--website-repo PATH` allows running from outside the website repo.
   - `--output FILE` writes the prompt to a file instead of stdout.
   - This prints "Processing changelog for: ..." plus a technical writer prompt containing the raw
     commit data.

2. Process the prompt: turn every relevant commit into entries in
   `site/changelog/Changelog-next.rst`, following the content rules below. When done, verify
   coverage mechanically: extract every unique commit subject from the prompt and check each one
   against the changelog, so that no commit is missed by eyeballing.

3. When the entries are done, always run:

   ```
   ./auto-format site/changelog/Changelog-next.rst
   ```

   The user often edits the file themselves in between. Read the file again before each edit,
   preserve their edits, and learn from them.

## Pre-release (develop) updates

What differs from the hotfix workflow:

- The range starts at the commit that introduced the last documented version. It may contain commits
  already covered by earlier hotfix passes, so skip every commit whose change is already present in
  `Changelog-next.rst`, do not create duplicate entries.
- The script uses `git log --no-merges`, so merge commits never appear in the prompt, and skips
  release-cycle commits ("New stable release.", "New release cycle.", ...).
- New entries get no `(Fixed in X.Y.Z already.)` or `(Added in X.Y.Z already.)` suffix, and are
  appended at the end of their group in each section, keeping the prefix grouping.
- A develop update covers commits up to the release of the version being documented. Commits after a
  "New release cycle." commit belong to the next version and go to its changelog instead.
- Develop commits get their own entries even when related work was already announced in a hotfix
  entry.

## Researching commits

The raw commit data in the prompt includes diffs, but for anything unclear, inspect the actual code
in the Nuitka repository (default `../Nuitka-develop`):

```
git show <hash>                      # the commit itself
git log --all --oneline --grep=...   # related commits
git log --format="%h %ci %s" -1 <hash>
```

In particular:

- Check whether a changed feature is behind an experimental flag or is the default at the time of
  the hotfix, so entries do not claim a regression that is not one (e.g. new style code objects were
  `--experimental` until after 4.1.2).
- Get the actual semantics right, e.g. `_stdlib_module_raises` is the list of modules known to
  **never** raise on import.
- Name the actual helpers and options (e.g. `has_builtin_module`, `--disable-ccache`), not vague
  descriptions.

## Content rules

### Categorization

Use only the existing sections of `Changelog-next.rst`: Bug Fixes, Package Support, New Features,
Optimization, Anti-Bloat, Organizational, Tests, Cleanups. Never add new headings. A section that
stays empty keeps the placeholder `-  None yet.` (with trailing period).

- Fixes for Nuitka itself -> Bug Fixes.
- Package support additions and fixes -> Package Support.
- New abilities -> New Features (use "Added").
- Performance or import-time optimizations -> Optimization.
- Avoided package dependencies -> Anti-Bloat.
- Release process, packaging (RPM, Debian), license, project tooling -> Organizational.
- Test suite changes -> Tests.
- Code quality, tools, styling -> Cleanups.
- Adding new tooling or functional enhancements of quality tools (new checker tools, new autoformat
  behaviors, hook behavior changes) -> Organizational, not Cleanups.
- User visible warnings and handling of user options -> **UI:** prefix (e.g. duplicate data file
  warning), placed per its category, usually Organizational or Bug Fixes.
- Release/packaging fixes -> Organizational with **Release:**, **RPM:**, or **Debian:** prefix.

### Suffixes for hotfix entries

Since the commits are the hotfix itself, append:

- `(Fixed in X.Y.Z already.)` to fixes.
- `(Added in X.Y.Z already.)` to new features and package support additions, using "Added" rather
  than "Fixed".

For develop updates, no such suffix unless certain.

### Grouping inside Bug Fixes

Bug Fixes consists of groups that must stay separated: one group per hotfix batch (e.g. all 4.1.1
entries) and one group for all develop changes. The different rc versions of a develop cycle do
**not** form separate groups, they are one develop group. Groups are ordered by time: hotfix batches
first, the develop group last, appended after the existing hotfix groups.

Within each group, keep entries grouped by bold prefix in this order, appending new entries at the
end of their prefix run:

1. Generic Python fixes without a prefix.
2. Python version fixes: `**Python 3.x:**`, `**Python 3.x+:**`, `**Python3:**`.
3. `**Standalone:**`.
4. `**Plugins:**`.
5. `**Windows:**`.
6. `**macOS:**`.
7. `**Linux:**` (and `**Debian:**` as part of the Linux group).
8. Other non-platform prefixes (e.g. `**Distutils:**`, `**PGO:**`, `**Onefile:**`, `**Report:**`,
   `**Zig:**`, `**NoGil:**`, `**UI:**`).
9. Other platforms (e.g. `**AIX:**`) at the end.

Other sections are not grouped this way, but keep items of the same prefix together where it is
natural.

### Ordering inside New Features

- An entry that pronounces a Python version as officially supported (e.g. "**Python 3.14:**
  Pronounced Python 3.14 as officially supported.") is always the first entry of New Features.
- Hotfix entries are **not** grouped together in New Features. Place them by relevance among the
  develop entries, keeping their `(Added in X.Y.Z already.)` suffix.

### Skipping commits

- Skip `fixup!` commits entirely, they are folded into the entry of the commit they fix.
- Skip trivial or internal changes without general relevance for users, e.g. fixes to features that
  are not yet the default (unless the user says otherwise).
- Never drop a commit whose content is not understood. Instead, check the code, add an entry with
  the best possible description, and inform the user about it, so they can decide.

### Audience and wording

The audience is the experienced Nuitka and Python user:

- Explain the actual mechanism and the user visible consequence, not just commit-title jargon. E.g.
  prefer "compiled coroutines left the send slot result uninitialized when they finished by raising,
  so `asyncio` could observe garbage values" over "coroutine am_send could return wrong result
  values".
- State the mechanism neutrally: describe what was missing rather than over-asserting the failure
  mode (e.g. "the output was not used yet", not "was never obtained").
- For fixes, describe the wrong behavior in past tense and the corrected behavior in present tense
  ("was handling ... incorrectly, now ..."), avoid formulations like "handled X correctly" that put
  the fix itself in the past.
- Never state the corrected behavior in past tense: not "Enabled UTF-8 mode", "added handling for",
  "avoided permission issues", "no longer crashed", "solved the need", but "Enables UTF-8 mode",
  "now handles", "no longer runs into", "no longer crashes", "no longer needs". Past tense is only
  for the wrong behavior and for the change event itself ("Added support for", "Renamed").
- Avoid redundancy, do not repeat the topic word within an entry (e.g. "compiler binary was a
  symlink" after already naming ccache), and avoid filler phrases like "closing a gap".
- Name the actual helpers and options (e.g. `has_builtin_module`).
- Terminology: handlers for runtime situations where something is missing, failing to work (e.g.
  `certifi` not present) are called "non-deployment handler", not "deployment handling".
- For hotfix entries that describe a change of behavior, showing what it was and what it is now can
  be done in a code example comment, e.g. `# 4.1: None (bug), 4.1.1: KeyError (correct)`.

### Quoting

- Double backticks for: option names (`--disable-ccache`, `--mode=dll`), module and package names,
  environment variables (`PYTHON_FROZEN_MODULES`), exception, function, and attribute names
  (`sys.exc_info()`, `__qualname__`), experimental flag names
  (`--experimental=deferred-annotations`), architecture names (`x86_64`), and Python keywords
  (`async`, `await`, `with`).
- Double quotes only for the flavor name `"Python Build Standalone"`, since that name is highly
  misleading. No other flavor names get quoted.

### Code examples

When an entry benefits from a code example, place it inside the list item:

```
-  **Python3:** Fix, ... (Fixed in 4.1.1 already.)

   .. code:: python

      ...
```

`./auto-format` turns `.. code-block:: python` into `.. code:: python` and formats the Python code
inside (e.g. two blank lines between functions).

## Improving this skill and the workflow

- Watch for conventions the user applies by editing `Changelog-next.rst` themselves or by correcting
  entries in prompts during a session.
- When a pattern emerges (wording, grouping, quoting, categorization), infer the intention behind
  it, not the concrete case, and propose adding it to this skill and to the style guide embedded in
  `update-changelog.py`.
- Propose such changes to the user rather than silently rewriting rules, the user is the authority
  on the conventions.
- When the workflow itself is painful (script location, output handling, etc.), suggest improvements
  to `update-changelog.py` as well.
