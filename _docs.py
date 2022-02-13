import sys, os
from pathlib import Path
from shutil import rmtree
from invoke import Collection, task


@task(name='clean')
def _clean(c):
    output = Path(c.sphinx.target)
    if output.exists():
        print(f'delete {output}')
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
def build(c,
          opts=None,
          language=None,
          source=None,
          target=None,
          nitpick=False):
    """
    Build the project's Sphinx docs.
    """
    if opts is None:
        opts = ""
    source = source or c.sphinx.source
    target = target or c.sphinx.target
    if language:
        opts = f'-D language={language}'
        target = f'{target}/{language}'
    if nitpick:
        opts += " -n -W -T"
    cmd = f"python3 -m pipenv run sphinx-build {opts} {source} {target}"
    c.run(cmd)


@task
def update(c, language='en'):
    '''Update the POT file and invoke the `sphinx-intl` `update` command

    Only used with `invoke intl.update`
    '''
    opts = "-b gettext"
    target = Path(c.sphinx.target).parent / 'output/gettext'
    if language == 'en':
        _clean(c)
        build(c, target=target, opts=opts)
    else:
        if not Path(target).exists():
            build(c, target=target, opts=opts)
        c.run(
            f'python3 -m pipenv run sphinx-intl update -p {target} -l {language}'
        )
        # for DIR in ['pages', 'posts', 'shop']:
        #     rmtree(f'locales/{language}/LC_MESSAGES/{DIR}/')


def _site(name, help_part):
    self = sys.modules[__name__]
    coll = Collection.from_module(
        self,
        name=name,
        config={"sphinx": {
            "source": name,
            "target": "output"
        }},
    )
    coll.__doc__ = f"Tasks for building {help_part}"
    coll["build"].__doc__ = f"Build {help_part}"
    return coll


# Usage doc/API site (published as e.g. docs.myproject.org)
intl = _site("intl", "the translations subsite.")
doc = _site("doc", "the main site.")

ns = Collection(intl, doc)
