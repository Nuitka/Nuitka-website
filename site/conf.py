# Obtain shared config values
import sys
from pathlib import Path

DOC_ROOT = Path(__file__).parent.absolute()
sys.path.extend([DOC_ROOT.as_posix(), DOC_ROOT.parent.as_posix()])

# isort:start

# -- General configuration
from shared_conf import *

# For autodoc to work we need to import Nuitka
from nuitka_import import importNuitka  # isort:skip

nuitka = importNuitka()

extensions += [
    # Blog extension
    "ablog",
]

# Options for ABlog

# The "title" for the blog, used in active pages.  Default is ``'Blog'``.
blog_title = "Nuitka Blog"

# Base URL for the website, required for generating feeds.
# e.g. blog_baseurl = "http://example.com/"
blog_baseurl = html_baseurl
blog_path = "blog"
blog_feed_fulltext = True  # spell-checker: ignore fulltext
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
sitemap_locales = [None]
sitemap_url_scheme = "{link}"

autodoc_member_order = "bysource"

# Sphinx intl configuration
gettext_compact = False
