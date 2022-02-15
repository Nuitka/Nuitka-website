import os
import subprocess


import sphinx_autobuild.build
from sphinx_autobuild.build import show

def get_builder(watcher, sphinx_args, *, host, port, pre_build_commands):
    """Prepare the function that calls sphinx."""
    def build():
        """Generate the documentation using ``sphinx``."""
        if watcher.filepath:
            show(context=f"Detected change: {watcher.filepath}")

            show(context="python3 -m invoke doc")
            subprocess.run("python3 -m invoke doc".split(), check=False)

            for locale in "zh_CN", "de_DE":
                if os.path.isdir(f"output/{locale}"):
                    show(context="python3 -m invoke intl -l {locale}")
                    subprocess.run(f"python3 -m invoke intl -l {locale}".split(), check=False)

            show(context="python3 -m invoke run -t post-process")
            subprocess.run("python3 -m invoke run -t post-process".split(), check=False)

            show(context=f"Serving on http://{host}:{port}")

    return build

sphinx_autobuild.build.get_builder = get_builder

if __name__ == "__main__":
    from sphinx_autobuild.cli import main
    main()
