import sys
from pathlib import Path

DOC_ROOT = Path(__file__).parent.absolute()
sys.path.extend([DOC_ROOT.as_posix(), DOC_ROOT.parent.as_posix()])

from shared_conf import *

# Offline bundle setup
html_baseurl = "./"
master_doc = "index_bundle"


# Keep only the bundle content, everything else is excluded
# note: Sphinx requires index files to be explicitly included to construct the TOC
include_patterns = [
    "index_bundle.rst",
    "variables.inc",
    "dynamic.inc",

    "user-documentation/index.rst",
    "doc/index.rst",
    "commercial/index.rst",

    "user-documentation/**",
    "doc/**",
    "commercial/**",
]

# Remove online only or site only extensions
excluded_extensions = {
	"ablog",
	"sphinx_sitemap",
	"carousel",
}

extensions = [ext for ext in extensions if ext not in excluded_extensions]