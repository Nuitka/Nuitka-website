# Obtain shared config values
import sys
from pathlib import Path

DOC_ROOT = Path(__file__).parent.absolute()
sys.path.extend([DOC_ROOT.as_posix(), DOC_ROOT.parent.as_posix()])

from shared_conf import *

language = 'en'  #'zh_CN'
locale_dirs = ['../locales/']  # path is example but recommended.
gettext_compact = False  # optional.

# Sitemap configuration
html_baseurl = f'{blog_baseurl}/zh_CN'
sitemap_locales = ['en', 'zh_CN']
sitemap_url_scheme = "{lang}/{link}"
extlinks = {
    'nuitka': (f'{html_baseurl}/%s', ''),
}

# extra_navbar = """<div>
# <button><a href="/nuitka-doc/">en</a></button>
# <button><a href="/nuitka-doc/zh_CN">zh_CN</a></button>
# </div>
# """

# html_sidebars = {
#     "posts/**": [
#         "postcard.html",
#         "recentposts.html",
#         "tagcloud.html",
#         "categories.html",
#         "archives.html",
#     ],
# }
