'''It is best to work in an environment created by conda.
'''
from invoke import Collection, task
from _docs import intl, doc


@task
def download(c, branch='main'):
    origin = 'https://github.com/Nuitka/Nuitka.git'
    c.run(f'git clone {origin} -b {branch} Nuitka-{branch}')


@task
def init(c):
    '''Initialize reop.'''
    download(c, 'main')
    download(c, 'develop')
    download(c, 'factory')


@task
def virtualenv(c):
    '''create and install env'''
    c.run('pip install -U pipenv')
    c.run('pipenv install --dev')


@task
def update(c, target='update-docs'):
    '''
    :target: can be `update-docs`, `build-site`, `serve-site`
    '''
    cmd = 'pipenv run python update.py'
    c.run(f'{cmd} --{target}')

@task
def output(c):
    c.run('cp -rf doc/_build/html output/')
    c.run('cp -rf intl/_build/html/zh_CN output/zh_CN')