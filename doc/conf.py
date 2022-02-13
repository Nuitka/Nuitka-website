# Obtain shared config values
import os, sys

sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("../.."))

from shared_conf import *

# Sitemap configuration
sitemap_locales = [None]
sitemap_url_scheme = "{link}"
html_baseurl = blog_baseurl