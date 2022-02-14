# Obtain shared config values
import sys
from pathlib import Path

DOC_ROOT = Path(__file__).parent.absolute()
sys.path.extend([DOC_ROOT.as_posix(), DOC_ROOT.parent.as_posix()])

# isort:start

from shared_conf import *

language = 'en'  # We lie here, actually 'zh_CN' or 'de'
locale_dirs = ['../locales/']
