import os
import shutil
import subprocess
import sys

# Which branches were already done.
updated_branches = set()


def _updateCheckout(branch, update):
    # We cannot use Nuitka directory change yet here.
    old_cwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))

    try:
        if os.path.exists(f"Nuitka-{branch}") and not update:
            return

        if branch in updated_branches:
            return

        if os.path.exists(f"Nuitka-{branch}"):
            shutil.rmtree(f"Nuitka-{branch}")

        print(f"Updating {branch} checkout...")
        sys.stdout.flush()

        # Using git is better than zip files for preserving x-bits.
        subprocess.run(
            [
                "git",
                "clone",
                "https://github.com/Nuitka/Nuitka.git",
                "--depth",
                "1",
                "--branch",
                branch,
                "--single-branch",
                f"Nuitka-{branch}",
            ],
            check=True,
        )

        # Install the commit hooks
        subprocess.run(["./Nuitka-develop/misc/install-git-hooks.py"], check=True)
        shutil.copy("./Nuitka-develop/.git/hooks/pre-commit", ".git/hooks/pre-commit")

        # Now we can drop the .git to make sure it doesn't confuse anything.
        shutil.rmtree("./Nuitka-develop/.git")
    finally:
        os.chdir(old_cwd)

    updated_branches.add(branch)


def updateNuitkaMain(update):
    _updateCheckout("main", update=update)


def updateNuitkaDevelop(update):
    _updateCheckout("develop", update=update)


def importNuitka():
    # TODO: Add an option to use other branches.
    updateNuitkaDevelop(update=False)

    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "Nuitka-develop"))
    )
    import nuitka.containers.OrderedSets

    del sys.path[0]

    return nuitka
