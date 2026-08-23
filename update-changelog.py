#!/usr/bin/env python3

import argparse
import os
import re
import subprocess
import sys
from contextlib import redirect_stdout
from typing import List, Optional

from packaging.version import parse as parse_version


class ChangelogGenerator:
    def __init__(
        self,
        repo_dir: str,
        target_version: Optional[str] = None,
        website_repo: str = ".",
    ):
        self.repo_dir = repo_dir
        self.target_version = target_version
        self.delimiter = "PCT_DELIMITER"
        self.changelog_file = os.path.join(
            website_repo, "site/changelog/Changelog-next.rst"
        )
        self.last_documented_version = self.parse_last_documented_version()

    def _runGitCommand(self, args: List[str]) -> Optional[str]:
        """Helper to run a git command and return its output."""
        try:
            result = subprocess.run(
                args,
                cwd=self.repo_dir,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
            )
            return result.stdout.strip()
        except FileNotFoundError:
            sys.exit(
                f"Error: Command '{args[0]}' not found. Please ensure it is in your PATH."
            )
        except subprocess.CalledProcessError as e:
            if "fatal: No names found" in e.stderr:
                return None
            sys.exit(f"Error executing command '{' '.join(args)}':\n{e.stderr}")

    def parse_last_documented_version(self) -> Optional[str]:
        """Parse the last documented version from the changelog file."""
        if not os.path.exists(self.changelog_file):
            return None

        with open(self.changelog_file, "r", encoding="utf-8") as f:
            content = f.read()
            # Match: It currently covers changes up to version **<VERSION>**.
            match = re.search(
                r"It currently covers changes up to version \*\*(.+)\*\*\.", content
            )
            if match:
                return match.group(1).strip()
        return None

    def find_commit_for_version(self, version_string: str) -> Optional[str]:
        """Find the commit hash that introduced a specific version string in nuitka/Version.py."""
        cmd = [
            "git",
            "log",
            "-p",
            "--format=COMMIT:%H",
            "-S",
            version_string,
            "nuitka/Version.py",
        ]

        output = self._runGitCommand(cmd)
        if not output:
            return None

        current_commit = None
        for line in output.splitlines():
            if line.startswith("COMMIT:"):
                current_commit = line.split(":", 1)[1]
            elif line.startswith("+") and version_string in line:
                return current_commit

        return None

    def getCommitVersion(self, commit_hash: str) -> Optional[str]:
        """Get the release version for a given commit hash."""
        return self._runGitCommand(
            ["git", "describe", "--tags", "--abbrev=0", commit_hash]
        )

    def is_hotfix_format(self, version: str) -> bool:
        return bool(re.match(r"^\d+\.\d+\.\d+$", version))

    def getHotfixRange(self) -> str:
        """Calculate the git log range based on the hotfix version."""
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", self.target_version)
        if not match:
            # Should not happen if is_hotfix_format checked
            sys.exit(
                f"Error: Version '{self.target_version}' is not in the required X.Y.Z format."
            )

        major, minor, patch = map(int, match.groups())
        if patch == 1:
            previous_version = f"{major}.{minor}"
        else:
            previous_version = f"{major}.{minor}.{patch - 1}"
        return f"{previous_version}..{self.target_version}"

    def getDevelopRange(self) -> str:
        """Calculate the git log range for develop/pre-release mode."""
        start_commit = "main"  # Default base

        if self.last_documented_version:
            print(
                f"Found last documented version state: {self.last_documented_version}"
            )
            found_commit = self.find_commit_for_version(self.last_documented_version)
            if found_commit:
                print(
                    f"Resolved version {self.last_documented_version} to commit {found_commit}"
                )
                start_commit = found_commit
            else:
                print(
                    f"Warning: Could not find commit for version {self.last_documented_version}, falling back to 'main'"
                )
        else:
            print("No previous documentation state found, starting from 'main'")

        end_commit = "HEAD"
        if self.target_version:
            found_end = self.find_commit_for_version(self.target_version)
            if found_end:
                print(
                    f"Resolved target version {self.target_version} to commit {found_end}"
                )
                end_commit = found_end
            else:
                sys.exit(
                    f"Error: Could not find commit for target version '{self.target_version}'"
                )

        return f"{start_commit}..{end_commit}"

    def getRawCommits(self, git_range: str) -> List[str]:
        """Get raw commits using a custom format."""
        cmd = [
            "git",
            "log",
            "-p",
            "--no-merges",
            f"--format=%n{self.delimiter}%n%H%n%s%n%b",
            "--reverse",
            git_range,
        ]

        output = self._runGitCommand(cmd)
        if not output:
            return []
        return output.split(f"\n{self.delimiter}\n")

    def processCommits(self) -> List[str]:
        # Determine mode
        is_hotfix = self.target_version and self.is_hotfix_format(self.target_version)

        if is_hotfix:
            git_range = self.getHotfixRange()
            version_label = f"hotfix {self.target_version}"
        else:
            git_range = self.getDevelopRange()
            version_label = (
                f"update to {self.target_version}"
                if self.target_version
                else "current develop"
            )

        print(f"Processing changelog for: {version_label}")
        print(f"Querying git log for range: {git_range}")

        raw_commits = self.getRawCommits(git_range)
        if not raw_commits:
            print("No commits found in the specified range.")
            return []

        actions_to_take = []
        seen_subjects = set()
        # Only parse version if it is a hotfix X.Y.Z
        current_version_obj = parse_version(self.target_version) if is_hotfix else None

        for commit_block in raw_commits:
            if not commit_block.strip():
                continue

            lines = commit_block.splitlines()
            if not lines:
                continue

            commit_hash = lines[0].strip()
            subject_line = lines[1].strip() if len(lines) > 1 else ""
            body = "\n".join(lines[2:]).strip() if len(lines) > 2 else ""

            if not subject_line:
                continue

            if subject_line in (
                "New hotfix release.",
                "New pre-release.",
                "New stable release.",
                "New release cycle.",
            ):
                continue
            if subject_line in seen_subjects:
                # The same change can appear multiple times in a range, e.g.
                # via a hotfix branch and its merge into develop, keep only
                # the first occurrence.
                continue
            seen_subjects.add(subject_line)

            lower_subject = subject_line.lower()
            if "minor cleanup" in lower_subject or "minor spelling" in lower_subject:
                continue

            # Handle fixups
            if subject_line.startswith("fixup! "):
                original_subject = subject_line[len("fixup! ") :].strip()
                original_hash = self._runGitCommand(
                    [
                        "git",
                        "log",
                        "--all",
                        "--grep",
                        f"^{re.escape(original_subject)}$",
                        "--format=%H",
                        "-1",
                    ]
                )

                if original_hash:
                    original_version_str = self.getCommitVersion(original_hash)

                    include_fixup = True
                    # In hotfix mode, exclude checks. In develop mode, we essentially include everything in range.
                    if is_hotfix and current_version_obj and original_version_str:
                        try:
                            if (
                                parse_version(original_version_str)
                                >= current_version_obj
                            ):
                                include_fixup = False
                        except:
                            pass

                    if include_fixup:
                        action = f"""Fixup for '{original_subject}' (from version {original_version_str}) is in this update.
Consider adding its details.
Fixup commit details ({commit_hash}):
---
{subject_line}

{body}
---"""
                        actions_to_take.append(action)
            else:
                action = f"""Non-fixup commit '{subject_line}' is in this update.
Consider adding its details.
Commit details ({commit_hash}):
---
{subject_line}

{body}
---"""
                actions_to_take.append(action)

        return actions_to_take

    def generate(self):
        actions = self.processCommits()
        is_hotfix = self.target_version and self.is_hotfix_format(self.target_version)

        if actions:
            print(f"\n--- Found {len(actions)} relevant commits, preparing prompt ---")
            commit_data = "\n\n".join(actions)

            target_str = (
                f"hotfix release version {self.target_version}"
                if is_hotfix
                else "upcoming release"
            )

            hotfix_suffix_hint = f"(Fixed in {self.target_version} already.)"
            added_suffix_hint = f"(Added in {self.target_version} already.)"

            if is_hotfix:
                suffix_rule = (
                    f'Append "{hotfix_suffix_hint}" to entries of fixes, and '
                    f'"{added_suffix_hint}" to new features and package support '
                    f"additions. For new features and package support additions, "
                    f'use "Added" rather than "Fixed".'
                )
            else:
                suffix_rule = (
                    'For develop changes, do not add a "Fixed in ... already." '
                    'suffix unless certain. For new features, use "Added" '
                    'rather than "Fixed".'
                )

            state_update_instruction = ""
            if not is_hotfix and self.target_version and self.last_documented_version:
                state_update_instruction = f"""
The document currently states: 'It currently covers changes up to version **{self.last_documented_version}**.'
Please update this line to: 'It currently covers changes up to version **{self.target_version}**.'
Include this updated line at the very beginning of your output.
"""

            prompt = f"""
You are a technical writer writing an update for the changelog information of
the Nuitka Python compiler on the Website. Your task is to integrate changelog
entries in ReStructuredText (RST) format for the {target_str} into the existing
document under "site/changelog/Changelog-next.rst".

Use the following git commit information to draft the changelog. Analyze each
commit message to determine its category and write a clear, concise summary
for it.

Follow these style guidelines precisely:

- The output must be valid ReStructuredText and be in the style of other
  Changelog files in this repo.
- Integrate the new entries into the existing sections of
  "site/changelog/Changelog-next.rst": Bug Fixes, Package Support, New
  Features, Optimization, Anti-Bloat, Organizational, Tests, Cleanups. Do
  not add new headings.
- Write in past tense. {suffix_rule}
- Skip fixup commits, they are folded into the entry of the commit they fix.
- Skip commits whose change is already present in the document from
  earlier hotfix passes, do not create duplicate entries.
- Skip trivial or internal changes without general relevance for users, e.g.
  fixes to features that are not yet the default.
- The audience is the experienced Nuitka and Python user, so explain the
  actual mechanism and the user visible consequence of a change, not just
  internal jargon. When in doubt, check the code to describe things
  correctly, and add a short code example when it clarifies a fix, showing
  the behavior before and after the fix.
- Within "Bug Fixes", each hotfix batch and the develop changes form
  their own group, and the develop group is appended after the hotfix
  groups. Within each group, keep entries grouped by their bold prefix
  in this order: generic Python fixes without a prefix, Python version
  fixes (**Python 3.x:** or **Python3:**), Standalone, Plugins, Windows,
  macOS, Linux, other non-platform prefixes, and other platforms last.
  Append new entries at the end of their prefix run.
- Use a bold prefix for the scope of an item, e.g. **Windows:**, **macOS:**,
  **Linux:**, **Plugins:**, **Standalone:**, **UI:**, **Debian:**, **RPM:**,
  **Debugging:**, **Quality:**, **Compatibility:**, **Release:**,
  **Project:**. Inside the "Tests" section, no prefix is needed for plain
  test changes.
- Release process and packaging changes (RPM, Debian, etc.) belong to
  "Organizational", user visible warnings and handling of user options use
  the **UI:** prefix.
- Quote in double backticks: option names (e.g. ``--disable-ccache``),
  module and package names, environment variables, exception, function,
  and attribute names, architecture names (e.g. ``x86_64``), and Python
  keywords (e.g. ``async``, ``await``, ``with``).
- Quote with double quotes only the flavor name "Python Build Standalone",
  since that name is highly misleading, and no other flavor names.
- Name the actual helpers and option names, e.g. ``has_builtin_module``.
- Avoid redundancy, do not repeat the topic word within an entry.
- State the mechanism neutrally, describe what was missing, rather than
  over-asserting the failure mode.
{state_update_instruction}
Here is the raw commit information:

--- RAW COMMIT DATA START --- {commit_data} --- RAW COMMIT DATA END ---

Integrate these changes to Changelog-next.rst document. Follow the style as
found in Changelog files found in general. After making the changes, run
`./auto-format site/changelog/Changelog-next.rst` so the final result matches
the repository formatting rules.
"""
            print(prompt)

        else:
            print("\nNo relevant commits found to generate a changelog.")
            # Update state if we explicitly asked for a target version in develop mode, even if empty?
            if not is_hotfix and self.target_version:
                print(
                    f"No content changes found, but updating state to {self.target_version} to avoid re-scanning."
                )


def main():
    parser = argparse.ArgumentParser(description="Update changelog for Nuitka.")
    parser.add_argument(
        "version",
        metavar="VERSION",
        type=str,
        help="The version to process. Hotfix format 'X.Y.Z' (e.g. 4.1.3), final format 'X.Y' (e.g. 4.2), or pre-release format 'X.YrcN' (e.g. 4.2rc3).",
    )
    parser.add_argument(
        "--nuitka-repo",
        dest="nuitka_repo",
        default="../Nuitka-develop",
        help="Path to the Nuitka repository (default: ../Nuitka-develop)",
    )
    parser.add_argument(
        "--website-repo",
        dest="website_repo",
        default=".",
        help="Path to the Nuitka website repository (default: current directory)",
    )
    parser.add_argument(
        "--output",
        dest="output",
        default=None,
        help="Write the generated prompt to a file instead of stdout",
    )

    args = parser.parse_args()

    if not (
        re.match(r"^\d+\.\d+\.\d+$", args.version)
        or re.match(r"^\d+\.\d+(rc\d+)?$", args.version)
    ):
        sys.exit(
            """\
Error, version '%s' is not valid. Use hotfix format 'X.Y.Z' (e.g. 4.1.3), \
final format 'X.Y' (e.g. 4.2), or pre-release format 'X.YrcN' (e.g. 4.2rc3)."""
            % args.version
        )

    generator = ChangelogGenerator(
        args.nuitka_repo, args.version, website_repo=args.website_repo
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as output_file:
            with redirect_stdout(output_file):
                generator.generate()
    else:
        generator.generate()


if __name__ == "__main__":
    main()
