#!/usr/bin/env python3.12

import argparse
import os
import re
import shutil
import subprocess
import sys

from packaging.version import parse as parse_version

NUITKA_REPO_DIR = "../Nuitka-develop"


def main():
    def _run_command(command_args, cwd=None):
        """Helper to run a command and return its output."""
        try:
            result = subprocess.run(
                command_args,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
            )
            return result.stdout.strip()
        except FileNotFoundError:
            sys.exit(
                f"Error: Command '{command_args[0]}' not found. Please ensure it is in your PATH."
            )
        except subprocess.CalledProcessError as e:
            # It's common for git describe to fail if a commit is not tagged, so handle this gracefully.
            if "fatal: No names found" in e.stderr:
                return None
            sys.exit(f"Error executing command '{" ".join(command_args)}':\n{e.stderr}")

    def _get_commit_version(commit_hash):
        """Get the release version for a given commit hash."""
        version_tag = _run_command(
            ["git", "describe", "--tags", "--abbrev=0", commit_hash],
            cwd=NUITKA_REPO_DIR,
        )
        return version_tag

    parser = argparse.ArgumentParser(
        description="Update changelog for a Nuitka hotfix release."
    )
    parser.add_argument(
        "hotfix_version",
        metavar="VERSION",
        type=str,
        help="The hotfix version number to process (e.g., '2.8.5').",
    )

    args = parser.parse_args()
    hotfix_version = args.hotfix_version

    # 1. Validate the version format
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", hotfix_version)
    if not match:
        sys.exit(
            f"Error: Version '{hotfix_version}' is not in the required X.Y.Z format."
        )

    major, minor, patch = map(int, match.groups())

    # 2. Calculate the previous version for the git log range
    previous_version = f"{major}.{minor}.{patch - 1}".rstrip(".0")
    git_range = f"{previous_version}..{hotfix_version}"

    print(f"Processing changelog for Nuitka hotfix version: {hotfix_version}")
    print(f"Querying git log for range: {git_range}")

    # 3. Get the git log with full commit details
    git_log_output = _run_command(["git", "log", git_range], cwd=NUITKA_REPO_DIR)

    if not git_log_output:
        print("No commits found in the specified range. Exiting.")
        return

    # 4. Parse commits and check for fixups
    actions_to_take = []
    current_version_obj = parse_version(hotfix_version)

    for commit_block in git_log_output.split("\ncommit "):
        if not commit_block.strip():
            continue

        lines = commit_block.splitlines()
        # Handle the first commit which doesn't have the "commit " prefix
        commit_hash = (
            lines[0] if lines[0].startswith("commit ") else lines[0].split()[0]
        )
        if len(commit_hash) != 40:
            commit_hash = lines[0].split()[1]

        subject_line = next(
            (line.strip() for line in lines if line.startswith("    ")), None
        )

        # Filter out irrelevant infrastructure commits
        if subject_line:
            if subject_line.startswith("Merge branch 'hotfix/"):
                continue
            if subject_line == "New hotfix release.":
                continue
            if "minor cleanup" in subject_line.lower():
                continue
            if "minor spelling" in subject_line.lower():
                continue

        if subject_line and subject_line.startswith("fixup! "):
            original_subject = subject_line[len("fixup! ") :].strip()

            # Find the hash of the commit being fixed up
            original_hash = _run_command(
                [
                    "git",
                    "log",
                    "--all",
                    "--grep",
                    f"^{re.escape(original_subject)}$",
                    "--format=%H",
                    "-1",
                ],
                cwd=NUITKA_REPO_DIR,
            )

            if original_hash:
                original_version_str = _get_commit_version(original_hash)

                if (
                    original_version_str
                    and parse_version(original_version_str) < current_version_obj
                ):
                    fixup_details = _run_command(
                        ["git", "show", "--no-patch", "--format=%B", commit_hash],
                        cwd=NUITKA_REPO_DIR,
                    )
                    action = (
                        f"Fixup for '{original_subject}' (from version {original_version_str}) is in this hotfix.\n"
                        f"Consider adding its details to the changelog.\n"
                        f"Fixup commit details ({commit_hash}):\n---\n{fixup_details}\n---"
                    )
                    actions_to_take.append(action)
        elif subject_line:
            commit_details = _run_command(
                ["git", "show", "--no-patch", "--format=%B", commit_hash],
                cwd=NUITKA_REPO_DIR,
            )
            action = (
                f"Non-fixup commit '{subject_line}' is in this hotfix.\n"
                f"Consider adding its details to the changelog.\n"
                f"Commit details ({commit_hash}):\n---\n{commit_details}\n---"
            )
            actions_to_take.append(action)

    if actions_to_take:
        print(
            "\n--- Found %d relevant commits, preparing prompt for Gemini ---"
            % len(actions_to_take)
        )

        commit_data = "\n\n".join(actions_to_take)

        prompt = f"""
You are a technical writer an update for the changelog information of the Nuitka Python compiler on the Website. Your task is to
integrate a changelog entries in ReStructuredText (RST) format for the hotfix release version {hotfix_version} into the existing
document under "site/changelog/Changelog-next.rst".

Use the following git commit information to draft the changelog. Analyze each commit message to determine its category (e.g.,
Bug Fixes, Optimization, New Features, Cleanups) and write a clear, concise summary for it.

Follow these style guidelines precisely:
- The output must be valid ReStructuredText and be in the style of other Changelog files in this repo.
- Group related changes under appropriate existing headings like "Bug Fixes", "Optimization", etc.
- Put new changelog items at the end of the section where they are added.
- For each item, write a in the past tense, ending with "(Fixed in {hotfix_version} already.)", for
  new features, "Added" should be used rather than "Fixed".


Here is the raw commit information for version {hotfix_version}:

--- RAW COMMIT DATA START ---
{commit_data}
--- RAW COMMIT DATA END ---

Generate only the ReStructuredText for the changelog section. Do not include any other explanatory text or headers.
"""
    else:
        print("\nNo relevant commits found to generate a changelog.")


if __name__ == "__main__":
    main()
