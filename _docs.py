import sys
from pathlib import Path
from shutil import rmtree
import os

from invoke import Collection, task
from builder_config import *


@task(name="clean")
def _clean(c):
    output = Path(c.sphinx.target)
    if output.exists():
        print(f"delete {output}")
        rmtree(output)


@task(
    default=True,
    help={
        "opts": "Extra sphinx-build options/args",
        "nitpick": "Build with stricter warnings/errors enabled",
        "source": "Source directory; overrides config setting",
        "target": "Output directory; overrides config setting",
    },
)
def build(c, opts=None, language=None, source=None, target=None, nitpick=False):
    """
    Build the project's Sphinx docs.
    """
    if opts is None:
        opts = ""
    source = source or c.sphinx.source
    target = target or c.sphinx.target
    conf = c.sphinx.conf

    if language:
        opts = f"-D language={language}"
        target = f"{target}/{language}"
    if nitpick:
        opts += " -n -W -T"

    conf_flag = ""
    if conf != "conf.py":
        conf_dir = os.path.dirname(conf) if conf else source
        conf_flag = f"-c {conf_dir}"

    cmd = f"pipenv run sphinx-build -W --keep-going {conf_flag} {opts} {source} {target}"
    c.run(cmd)


@task
def update(c, language="en"):
    """Update the POT file and invoke the `sphinx-intl` `update` command

    Only used with `invoke intl.update`
    """
    opts = "-b gettext"
    target = Path(c.sphinx.target).parent / "output/gettext"
    if language == "en":
        _clean(c)
        build(c, target=target, opts=opts)
    else:
        if not Path(target).exists():
            build(c, target=target, opts=opts)
        c.run(f"pipenv run sphinx-intl update -p {target} -l {language}")


def _site(name, help_part, *, source, target, conf):
    self = sys.modules[__name__]
    coll = Collection.from_module(
        self,
        name=name,
        config={
            "sphinx": {
                "source": source,
                "target": target,
                "conf": conf,
            }
        },
    )
    coll.__doc__ = f"Tasks for building {help_part}"
    coll["build"].__doc__ = f"Build {help_part}"
    return coll


site = _site(
    "site",
    "the website",
    source="site",
    target=MAIN_TARGET,
    conf=MAIN_CONF
)

intl = _site(
    "intl",
    "the translations sub-site",
    source="intl",
    target=MAIN_TARGET,
    conf="intl/conf.py"
)

bundle = _site(
    "bundle",
    "package documentation bundle",
    source=BUNDLE_DIR,
    target=BUNDLE_HTML_DIR,
    conf=BUNDLE_CONF
)

ns = Collection(site, intl, bundle)
