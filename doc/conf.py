# Obtain shared config values
import sys
from pathlib import Path

DOC_ROOT = Path(__file__).parent.absolute()
sys.path.extend([DOC_ROOT.as_posix(), DOC_ROOT.parent.as_posix()])

from shared_conf import *

# Sitemap configuration
sitemap_locales = [None]
sitemap_url_scheme = "{link}"
