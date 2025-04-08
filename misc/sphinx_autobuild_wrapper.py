import os
import signal
import subprocess
import sys

import psutil
import setproctitle
import sphinx_autobuild.build
from sphinx_autobuild.build import show


def mySignalHandler(signal, frame):
    process = psutil.Process(os.getpid())
    for proc in process.children(recursive=True):
        proc.kill()

    print("Exiting for rebuild of whole site", file=sys.stderr)
    sys.exit(27)


def get_builder(watcher, sphinx_args, *, host, port, pre_build_commands):
    """Prepare the function that calls sphinx."""

    def build():
        """Generate the documentation using ``sphinx``."""
        if not watcher.filepath:
            return
        if watcher.filepath.endswith(".cast"):
            return

        show(context=f"Detected change: {watcher.filepath}")

        show(context="python3 -m invoke site")
        subprocess.run("python3 -m invoke site".split(), check=False)

        for locale in "zh_CN", "de_DE":
            if os.path.isdir(f"output/{locale}"):
                show(context=f"python3 -m invoke intl -l {locale}")
                subprocess.run(
                    f"python3 -m invoke intl -l {locale}".split(), check=False
                )

        show(context="python3 -m invoke post-process")
        subprocess.run("python3 -m invoke post-process".split(), check=False)

        show(context=f"Serving on http://{host}:{port}")

    signal.signal(signal.SIGUSR2, mySignalHandler)

    return build


sphinx_autobuild.build.get_builder = get_builder

if __name__ == "__main__":
    setproctitle.setproctitle("sphinx-autobuild")
    from sphinx_autobuild.cli import main

    main()
