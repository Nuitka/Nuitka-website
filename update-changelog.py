#!/usr/bin/env python3

import argparse
import os
import re
import subprocess
import sys
from typing import List, Optional

from packaging.version import parse as parse_version


class ChangelogGenerator:
    def __init__(self, repo_dir: str, target_version: Optional[str] = None):
        self.repo_dir = repo_dir
        self.target_version = target_version
        self.delimiter = "PCT_DELIMITER"
        self.changelog_file = "site/changelog/Changelog-next.rst"
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
        previous_version = f"{major}.{minor}.{patch - 1}".rstrip(".0")
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

            if subject_line.startswith("Merge branch 'hotfix/"):
                continue
            if (
                subject_line == "New hotfix release."
                or subject_line == "New pre-release."
            ):
                continue
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
                        action = (
                            f"Fixup for '{original_subject}' (from version {original_version_str}) is in this update.\n"
                            f"Consider adding its details.\n"
                            f"Fixup commit details ({commit_hash}):\n---\n{subject_line}\n\n{body}\n---"
                        )
                        actions_to_take.append(action)
            else:
                action = (
                    f"Non-fixup commit '{subject_line}' is in this update.\n"
                    f"Consider adding its details.\n"
                    f"Commit details ({commit_hash}):\n---\n{subject_line}\n\n{body}\n---"
                )
                actions_to_take.append(action)

        return actions_to_take

    def generate(self):
        actions = self.processCommits()
        is_hotfix = self.target_version and self.is_hotfix_format(self.target_version)

        if actions:
            print(
                f"\n--- Found {len(actions)} relevant commits, preparing prompt for Gemini ---"
            )
            commit_data = "\n\n".join(actions)

            target_str = (
                f"hotfix release version {self.target_version}"
                if is_hotfix
                else "upcoming release"
            )
            hotfix_suffix_hint = (
                f"(Fixed in {self.target_version} already.)" if is_hotfix else "release"
            )

            state_update_instruction = ""
            if not is_hotfix and self.target_version and self.last_documented_version:
                state_update_instruction = (
                    f"\nThe document currently states: 'It currently covers changes up to version **{self.last_documented_version}**.'\n"
                    f"Please update this line to: 'It currently covers changes up to version **{self.target_version}**.'\n"
                    "Include this updated line at the very beginning of your output.\n"
                )

            prompt = f"""
You are a technical writer writing an update for the changelog information of the Nuitka Python compiler on the Website. Your task is to
integrate changelog entries in ReStructuredText (RST) format for the {target_str} into the existing
document under "site/changelog/Changelog-next.rst".

Use the following git commit information to draft the changelog. Analyze each commit message to determine its category (e.g.,
Bug Fixes, Optimization, New Features, Cleanups) and write a clear, concise summary for it.

Follow these style guidelines precisely:
- The output must be valid ReStructuredText and be in the style of other Changelog files in this repo.
- Group related changes under appropriate existing headings like "Bug Fixes", "Optimization", etc.
- Put new changelog items at the end of the section where they are added.
- For each item, write in the past tense, ending with "{hotfix_suffix_hint}" only if it matches a hotfix pattern. For general develop changes, do not add "Fixed in..." unless certain.
- For new features, "Added" should be used rather than "Fixed".{state_update_instruction}

Here is the raw commit information:

--- RAW COMMIT DATA START ---
{commit_data}
--- RAW COMMIT DATA END ---

Generate only the ReStructuredText for the changelog section. Do not include any other explanatory text or headers.
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
        nargs="?",
        help="The version to process. If format 'X.Y.Z' (e.g. 2.8.5), treats as Hotfix. Otherwise (e.g. 4.0rc5), treats as Pre-release update and updates changelog state. If omitted, performs a dry-run check of pending develop changes.",
    )
    parser.add_argument(
        "--nuitka-repo",
        dest="nuitka_repo",
        default="../Nuitka-develop",
        help="Path to the Nuitka repository (default: ../Nuitka-develop)",
    )

    args = parser.parse_args()

    generator = ChangelogGenerator(args.nuitka_repo, args.version)
    generator.generate()


if __name__ == "__main__":
    main()
