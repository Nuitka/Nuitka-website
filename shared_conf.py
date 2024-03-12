import sys
import time
from pathlib import Path

# Configuration file for the Sphinx documentation builder.

# -- Project information
project = "Nuitka the Python Compiler"
copyright = f"{time.gmtime().tm_year}, Kay Hayen and Nuitka Contributors"
author = "Kay Hayen"
release = version = ""

ROOT = Path(__file__).parent.absolute().as_posix()  # The root directory
# For autodoc to work
sys.path.append(ROOT)
from update import importNuitka  # isort:skip

importNuitka()
del sys.path[-1]

# -- General configuration

extensions = [
    # Sphinx's own extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    #    "sphinx.ext.viewcode",
    # External extensions
    "sphinx_copybutton",
    "sphinx_design",
    #    "sphinx_inline_tabs",
    "sphinxcontrib.youtube",
    "sphinx_favicon",
    "sphinx_sitemap",
    # Disabled, loads to slow and cannot be limited to needing pages.
    # "sphinxcontrib.asciinema",
    # Blog extension
    "ablog",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = [f"{ROOT}/_templates"]

# -- Options for HTML output
html_theme = "sphinx_rtd_theme"
html_logo = None
html_copy_source = False
html_show_sourcelink = False
html_show_sphinx = False
html_title = project

favicons = [
    {
        "rel": "icon",
        "static-file": "favicon.svg",
        "type": "image/svg+xml",
    },
    {
        "rel": "icon",
        "sizes": "32x32",
        "static-file": "favicon.png",
    },
    {
        "rel": "icon",
        "sizes": "32x32",
        "static-file": "favicon.ico",
    },
    {
        "rel": "icon",
        "sizes": "57x57",
        "static-file": "apple-touch-icon-iphone.png",
    },
    {
        "rel": "icon",
        "sizes": "72x72",
        "static-file": "apple-touch-icon-ipad.png",
    },
    {
        "rel": "icon",
        "sizes": "114x114",
        "static-file": "apple-touch-icon-iphone4.png",
    },
    {
        "rel": "icon",
        "sizes": "144x144",
        "static-file": "apple-touch-icon-ipad3.png",
    },
    {
        "rel": "apple-touch-icon",
        "sizes": "180x180",
        "static-file": "apple-touch-icon-180x180.png",
    },
]

# -- Options for EPUB output
epub_show_urls = "footnote"


# Enable our own CSS to be used.
def setup(app):
    app.add_css_file("my_theme.css")


# Configure theme
html_theme_options = {
    "prev_next_buttons_location": "none",
    "includehidden": True,
    "titles_only": True,
}

html_extra_path = [f"{ROOT}/files"]

html_baseurl = "https://nuitka.net/"

sitemap_locales = [None]
sitemap_url_scheme = "{lang}/{link}"

# TODO: Not sure if I really like that, we should use relative URLs on the inside,
# so this ought to be wrong anyway.
extlinks = {"nuitka": ("/%s", None)}

html_static_path = [f"{ROOT}/_static"]

gettext_compact = False  # optional.
