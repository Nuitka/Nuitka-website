#!/usr/bin/env python3.12

import argparse
import sys
import subprocess
import re
from typing import List, Optional
from packaging.version import parse as parse_version

class ChangelogGenerator:
    def __init__(self, repo_dir: str, hotfix_version: str):
        self.repo_dir = repo_dir
        self.hotfix_version = hotfix_version
        self.delimiter = "PCT_DELIMITER"

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
            sys.exit(f"Error: Command '{args[0]}' not found. Please ensure it is in your PATH.")
        except subprocess.CalledProcessError as e:
            # Handle specific git errors if needed, otherwise re-raise or exit
            if "fatal: No names found" in e.stderr:
                return None
            sys.exit(f"Error executing command '{' '.join(args)}':\n{e.stderr}")

    def getCommitVersion(self, commit_hash: str) -> Optional[str]:
        """Get the release version for a given commit hash."""
        return self._runGitCommand(
            ["git", "describe", "--tags", "--abbrev=0", commit_hash]
        )

    def getGitRange(self) -> str:
        """Calculate the git log range based on the hotfix version."""
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", self.hotfix_version)
        if not match:
            sys.exit(f"Error: Version '{self.hotfix_version}' is not in the required X.Y.Z format.")

        major, minor, patch = map(int, match.groups())
        previous_version = f"{major}.{minor}.{patch - 1}".rstrip(".0")
        return f"{previous_version}..{self.hotfix_version}"

    def getRawCommits(self, git_range: str) -> List[str]:
        """Get raw commits using a custom format to avoid parsing issues."""
        # Format: Hash%nSubject%nBody%nDelimiter
        cmd = [
            "git",
            "log",
            f"--format=%H%n%s%n%b%n{self.delimiter}",
            git_range,
        ]
        output = self._runGitCommand(cmd)
        if not output:
            return []
        return output.split(f"\n{self.delimiter}\n")

    def processCommits(self) -> List[str]:
        git_range = self.getGitRange()
        print(f"Processing changelog for Nuitka hotfix version: {self.hotfix_version}")
        print(f"Querying git log for range: {git_range}")

        raw_commits = self.getRawCommits(git_range)
        if not raw_commits:
            print("No commits found in the specified range.")
            return []

        actions_to_take = []
        current_version_obj = parse_version(self.hotfix_version)

        for commit_block in raw_commits:
            if not commit_block.strip():
                continue

            lines = commit_block.splitlines()
            if not lines:
                continue

            commit_hash = lines[0].strip()
            subject_line = lines[1].strip() if len(lines) > 1 else ""
            body = "\n".join(lines[2:]).strip() if len(lines) > 2 else ""

            # Filter out irrelevant infrastructure commits
            if not subject_line:
                continue

            if subject_line.startswith("Merge branch 'hotfix/"):
                continue
            if subject_line == "New hotfix release.":
                continue
            lower_subject = subject_line.lower()
            if "minor cleanup" in lower_subject or "minor spelling" in lower_subject:
                continue

            # Handle fixups
            if subject_line.startswith("fixup! "):
                original_subject = subject_line[len("fixup! ") :].strip()
                # Find the hash of the commit being fixed up
                # We still use grep here as it's the most reliable way to find by subject
                original_hash = self._runGitCommand([
                    "git", "log", "--all", "--grep", f"^{re.escape(original_subject)}$",
                    "--format=%H", "-1"
                ])

                if original_hash:
                    original_version_str = self.getCommitVersion(original_hash)
                    if original_version_str and parse_version(original_version_str) < current_version_obj:
                         action = (
                            f"Fixup for '{original_subject}' (from version {original_version_str}) is in this hotfix.\n"
                            f"Consider adding its details to the changelog.\n"
                            f"Fixup commit details ({commit_hash}):\n---\n{subject_line}\n\n{body}\n---"
                        )
                         actions_to_take.append(action)
            else:
                action = (
                    f"Non-fixup commit '{subject_line}' is in this hotfix.\n"
                    f"Consider adding its details to the changelog.\n"
                    f"Commit details ({commit_hash}):\n---\n{subject_line}\n\n{body}\n---"
                )
                actions_to_take.append(action)

        return actions_to_take

    def generate(self):
        actions = self.processCommits()
        if actions:
            print(f"\n--- Found {len(actions)} relevant commits, preparing prompt for Gemini ---")
            commit_data = "\n\n".join(actions)
            prompt = f"""
You are a technical writer writing an update for the changelog information of the Nuitka Python compiler on the Website. Your task is to
integrate a changelog entries in ReStructuredText (RST) format for the hotfix release version {self.hotfix_version} into the existing
document under "site/changelog/Changelog-next.rst".

Use the following git commit information to draft the changelog. Analyze each commit message to determine its category (e.g.,
Bug Fixes, Optimization, New Features, Cleanups) and write a clear, concise summary for it.

Follow these style guidelines precisely:
- The output must be valid ReStructuredText and be in the style of other Changelog files in this repo.
- Group related changes under appropriate existing headings like "Bug Fixes", "Optimization", etc.
- Put new changelog items at the end of the section where they are added.
- For each item, write in the past tense, ending with "(Fixed in {self.hotfix_version} already.)".
- For new features, "Added" should be used rather than "Fixed".

Here is the raw commit information for version {self.hotfix_version}:

--- RAW COMMIT DATA START ---
{commit_data}
--- RAW COMMIT DATA END ---

Generate only the ReStructuredText for the changelog section. Do not include any other explanatory text or headers.
"""
            print(prompt)
        else:
            print("\nNo relevant commits found to generate a changelog.")

def main():
    parser = argparse.ArgumentParser(description="Update changelog for a Nuitka hotfix release.")
    parser.add_argument(
        "hotfix_version",
        metavar="VERSION",
        type=str,
        help="The hotfix version number to process (e.g., '2.8.5').",
    )
    parser.add_argument(
        "--nuitka-repo",
        dest="nuitka_repo",
        default="../Nuitka-develop",
        help="Path to the Nuitka repository (default: ../Nuitka-develop)",
    )

    args = parser.parse_args()

    generator = ChangelogGenerator(args.nuitka_repo, args.hotfix_version)
    generator.generate()

if __name__ == "__main__":
    main()
