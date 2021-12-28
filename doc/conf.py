import os
import sys
import time

# Configuration file for the Sphinx documentation builder.

# -- Project information


project = "Nuitka the Python Compiler"
copyright = "%s, Kay Hayen and Nuitka Contributors" % time.gmtime().tm_year
author = "Kay Hayen"

sys.path.insert(0, os.path.abspath("../Nuitka-master"))
from nuitka.Version import getNuitkaVersion
del sys.path[0]

release = version = getNuitkaVersion()

del sys.modules["nuitka.Version"]
del sys.modules["nuitka"]

sys.path.insert(0, os.path.abspath("../Nuitka-develop"))
import nuitka
del sys.path[0]

# -- General configuration

extensions = [
    # Sphinx's own extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    # "sphinx.ext.viewcode",
    # External extensions
    'ablog',
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_inline_tabs",
    "sphinxcontrib.youtube",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output
html_theme = "sphinx_rtd_theme"
html_logo = "Nuitka-Logo-Symbol.png"
html_copy_source = False
html_show_sourcelink = False
html_show_sphinx = False

# -- Options for EPUB output
epub_show_urls = "footnote"

autodoc_member_order = 'bysource'

# Enable our own CSS to be used.
def setup(app):
    app.add_css_file('my_theme.css')

html_static_path = ['_static']

# Configure theme
html_theme_options = {
    "prev_next_buttons_location" : 'none',
    'analytics_id': 'G-V73VK1T804',
    'analytics_anonymize_ip': True,
}