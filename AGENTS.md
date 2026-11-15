# Agent Guidance

This repository builds https://nuitka.net with Sphinx from the reST sources in `site/`. Read
`site/pages/website-manual.rst` for the setup, the color palette, and the writing style guide.

Rules are split by topic, see `opencode.json` for the auto-loaded list:

- `.agents/rules/content.md`: how pages are written, what may not be added, and the building blocks
  to use instead.
- `.agents/rules/styling.md`: CSS, PurgeCSS, and color contrast.
- `.agents/rules/verification.md`: formatting and the checks to run before a pull request.

## AI Contribution Policy

The policy of Nuitka applies here as well, see `CONTRIBUTING.md` and the pull request template of
https://github.com/Nuitka/Nuitka. Pull requests state the model used, a summary of the prompts, how
the change was verified, and what the submitter checked by hand.
