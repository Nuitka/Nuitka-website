import sys
from pathlib import Path

DOC_ROOT = Path(__file__).parent.absolute()
sys.path.extend([DOC_ROOT.as_posix(), DOC_ROOT.parent.as_posix()])

from shared_conf import *

# Offline bundle setup
html_baseurl = "./"
master_doc = "index_bundle"

# Keep only the bundle content, everything else is excluded
include_patterns = [
	"index_bundle.rst",
	"variables.inc",
	"dynamic.inc",
	"doc/**",
	"user-documentation/**",
]

# Remove online only or site only extensions
excluded_extensions = {
	"ablog",
	"sphinx_sitemap",
	"carousel",
}

extensions = [ext for ext in extensions if ext not in excluded_extensions]