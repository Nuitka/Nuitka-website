from pathlib import Path

BASE_URL = "http://localhost:8000"

ROOT = Path(__file__).parent.parent

GOLDEN_DIR = ROOT / "tests" / "golden"
CURRENT_DIR = ROOT / "tests" / "current"
DIFF_DIR = ROOT / "tests" / "diff"

BROWSERS = ["chromium", "firefox", "webkit"]

VIEWPORTS = {
    "desktop": {
        "viewport": {"width": 1920, "height": 1080},
        "device_scale_factor": 1,
        "is_mobile": False,
        "has_touch": False,
    },
    "mobile": {
        "viewport": {"width": 390, "height": 844},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    },
}

GOLDEN_PAGES = [
    "/",
    "doc/download.html",
    "commercial/purchase.html",
    "user-documentation/user-manual.html",
    "user-documentation/use-cases.html",
    "user-documentation/common-issue-solutions.html",
    "doc/commercial/protect-data-files.html",
    "user-documentation/tips.html",
    "pages/website-manual.html",
    "posts/nuitka-shaping-up.html"
]

DEFAULT_WAIT_TIME = 1000
COMPARISON_THRESHOLD = 5
