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
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_inline_tabs",
    "sphinxcontrib.youtube",
    "sphinx-favicon",
    "sphinx_sitemap",
    # Blog extension
    "sphinxcontrib.asciinema",
    "ablog",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# Options for ABlog

# The "title" for the blog, used in active pages.  Default is ``'Blog'``.
blog_title = "Nuitka Blog"

# Base URL for the website, required for generating feeds.
# e.g. blog_baseurl = "http://example.com/"
blog_baseurl = "https://nuitka.net"
blog_path = "blog"
blog_feed_fulltext = True
blog_feed_archives = True
blog_feed_length = None

# TODO: Optimized feeds one day?
x_blog_feed_templates = {
    # Use defaults, no templates
    "atom": {},
    # Create content text suitable posting to social media
    "social": {
        # Format tags as hashtags and append to the content
        "content": "{{ title }}{% for tag in post.tags %}"
        " #{{ tag.name|trim()|replace(' ', '') }}"
        "{% endfor %}",
    },
}

# Sitemap configuration
html_baseurl = blog_baseurl
sitemap_locales = [None]
sitemap_url_scheme = "{link}"

# -- Options for HTML output
html_theme = "sphinx_rtd_theme"
html_logo = "Nuitka-Logo-Symbol.png"
html_copy_source = False
html_show_sourcelink = False
html_show_sphinx = False


favicons = favicons = [
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

autodoc_member_order = "bysource"

# Enable our own CSS to be used.
def setup(app):
    app.add_css_file("my_theme.css")


html_static_path = ["_static"]

# Configure theme
html_theme_options = {
    "prev_next_buttons_location": "none",
    "analytics_id": "G-V73VK1T804",
    "analytics_anonymize_ip": True,
}

html_extra_path = ["../files"]

sphinxcontrib_asciinema_defaults = {
    'theme': 'asciinema',
    'preload': 0,
    'font-size': '1rem',
    'path': 'pages/demos'
}

# TODO: social buttons
html_js_files = []
