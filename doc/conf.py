import os
import subprocess
import sys
import time

# Configuration file for the Sphinx documentation builder.

# -- Project information


project = "Nuitka the Python Compiler"
copyright = "%s, Kay Hayen and Nuitka Contributors" % time.gmtime().tm_year
author = "Kay Hayen"

release = version = "0.6.17.5"

# -- General configuration

extensions = [
    # Sphinx's own extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    # External stuff
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_inline_tabs",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = "footnote"

if os.environ.get("READTHEDOCS") == "True":
    subprocess.call(
        [
            "python",
            "update.py",
            "--update-docs",
        ],
        cwd="..",
    )
