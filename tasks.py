import os
import sys

from invoke import Collection, task

from _docs import bundle, intl, site

# Disable pipenv warning, we run potentially inside the virtualenv already,
# Visual Code e.g. picks it up and there is no harm in that. This is only
# to not confuse people with a pipenv warning that it may not be working.
os.environ["PIPENV_VERBOSITY"] = "-1"
os.environ["PIPENV_IGNORE_VIRTUALENVS"] = "1"


@task
def virtualenv(c):
    """create and install env"""
    c.run(
        f"{sys.executable} -m pipenv 2>/dev/null >/dev/null || {sys.executable} -m pip install -U pipenv"
    )
    c.run(f"{sys.executable} -m pipenv install --dev")

    # Workaround pipenv failing to pin black version due to it being pre-release
    # always.
    c.run(f"{sys.executable} -m pipenv run python -m pip install black==24.10.0")

    # Install node while we are here, probably worth renaming the task
    c.run(f"npm install")


@task
def serve(c):
    c.run(f"{sys.executable} -m pipenv run python update.py --serve-site")


@task
def update_docs(c):
    c.run(f"{sys.executable} -m pipenv run python update.py --update-docs")


@task
def update_downloads(c):
    c.run(f"{sys.executable} -m pipenv run python update.py --update-downloads")


@task
def post_process(c):
    c.run(f"{sys.executable} -m pipenv run python update.py --post-process")


@task
def deploy(c):
    c.run(f"{sys.executable} -m pipenv run python update.py --deploy")


ns = Collection(
    intl,
    site,
    bundle,
    serve,
    update_docs,
    update_downloads,
    post_process,
    deploy,
    virtualenv,
)
