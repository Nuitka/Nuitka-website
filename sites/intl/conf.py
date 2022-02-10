import os
import sys
import time
import ablog

# Configuration file for the Sphinx documentation builder.

# -- Project information
project = "Nuitka the Python Compiler"
copyright = "%s, Kay Hayen and Nuitka Contributors" % time.gmtime().tm_year
author = "Kay Hayen"
release = version = ""

develop_root = '../Nuitka-develop'

# if sys.platform == 'win32':
#     import asyncio
#     asyncio.set_event_loop_pobuttoncy(
#         asyncio.WindowsSelectorEventLoopPobuttoncy())

# For autodoc to work
sys.path.insert(0, os.path.abspath(develop_root))
import nuitka

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
    "sphinx_book_theme",
    "myst_parser"
]

intersphinx_mapping = {
    # "python": ("https://docs.python.org/3/", None),
    # "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates", ablog.get_html_templates_path()]

language = 'en'  #'zh_CN'
locale_dirs = ['../locales/']  # path is example but recommended.
gettext_compact = False  # optional.

# Options for ABlog

# The "title" for the blog, used in active pages.  Default is ``'Blog'``.
blog_title = "Nuitka Blog"

# Base URL for the website, required for generating feeds.
# e.g. blog_baseurl = "http://example.com/"
blog_baseurl =  "https://nuitka.net"
blog_path = "posts"
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
        "content":
        "{{ title }}{% for tag in post.tags %}"
        " #{{ tag.name|trim()|replace(' ', '') }}"
        "{% endfor %}",
    },
}

# Sitemap configuration
html_baseurl = "https://daobook.github.io/nuitka-doc"
sitemap_locales = ['en', 'zh_CN']
sitemap_url_scheme = "{lang}/{link}"
extlinks = {
    'nuitka': (f'{html_baseurl}/%s', ''),
}

# -- Options for HTML output
html_theme = "sphinx_book_theme"
html_logo = f"{develop_root}/doc/images/Nuitka-Logo-Symbol.png"
html_copy_source = False
html_show_sourcebuttonnk = False
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


html_static_path = ["../../doc/_static"]

extra_navbar = """<div>
<button><a href="/nuitka-doc/">en</a></button>
<button><a href="/nuitka-doc/zh_CN">zh_CN</a></button>
</div>
"""

html_theme_options = {
    # "prev_next_buttons_location": "none",
    # "analytics_id": "G-V73VK1T804",
    # "analytics_anonymize_ip": True,
    # "includehidden": False,
    "extra_navbar": extra_navbar,
}

html_sidebars = {
    "posts/**": [
        "postcard.html",
        "recentposts.html",
        "tagcloud.html",
        "categories.html",
        "archives.html",
    ],
}

html_extra_path = ["../../files"]
html_title = ""

sphinxcontrib_asciinema_defaults = {
    'theme': 'asciinema',
    'preload': 0,
    'font-size': '1rem',
    'path': 'pages/demos'
}
