from invoke import Collection, task
from _docs import intl, doc


@task
def download(c, branch='main'):
    origin = 'https://github.com/Nuitka/Nuitka.git'
    c.run(f'git clone {origin} -b {branch} Nuitka-{branch}')


@task
def init(c):
    c.run(f'pip install -r dev-requirements.txt')
    download(c, 'main')
    download(c, 'develop')
    download(c, 'factory')


@task
def preprocessing(c):
    # c.run('cp doc/pages/images/gitter-badge.svg'
    #       'docs/images/gitter-badge.svg')
    # c.run('mkdir intl/doc/ intl/doc/images/')
    # c.run('cp Nuitka-develop/doc/images/Nuitka-Logo-Symbol.png'
    #       'docs/doc/images/Nuitka-Logo-Symbol.png')
    c.run('cp -rf doc/posts intl/posts/')


ns = Collection(download, init, preprocessing, intl, doc)
