import os
import sys
from pathlib import Path

import re
from urllib.parse import urlparse

import math
from PIL import Image, ImageChops, ImageDraw

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "./Nuitka-develop")
    )
)

from nuitka.Tracing import my_print

BASE_URL = "http://localhost:8000"

ROOT = Path(__file__).parent.resolve()

GOLDEN_DIR = ROOT / "tests" / "golden"
CURRENT_DIR = ROOT / "tests" / "current"
DIFF_DIR = ROOT / "tests" / "diff"

VIEWPORT_MODES = ["desktop", "mobile"]

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

DESKTOP_DEVICES = {
    "chromium": {"viewport": {"width": 1920, "height": 1080}, "is_mobile": False},
    "firefox": {"viewport": {"width": 1920, "height": 1080}, "is_mobile": False},
    "webkit": {"viewport": {"width": 1920, "height": 1080}, "is_mobile": False},
}

MOBILE_DEVICES = {
    "chromium": {"viewport": {"width": 390, "height": 844}, "is_mobile": True, "has_touch": True},
    "firefox": {"viewport": {"width": 390, "height": 844}, "is_mobile": True, "has_touch": True},
    "webkit": {"viewport": {"width": 390, "height": 844}, "is_mobile": True, "has_touch": True},
}


def sanitizeUrl(url):
    path = urlparse(url).path
    path = "home" if path in ("", "/") else path.lstrip("/")
    return re.sub(r'[^a-zA-Z0-9_-]', '_', path)

def build_url(page_path, base_url="http://localhost:8000"):
    if not page_path:
        return base_url
    if page_path.startswith('/') and base_url.endswith('/'):
        return f"{base_url}{page_path[1:]}"
    if not page_path.startswith('/') and not base_url.endswith('/'):
        return f"{base_url}/{page_path}"
    return f"{base_url}{page_path}"

def compareImages(golden_path, current_path, diff_path=None, threshold=5):
    golden = Image.open(golden_path).convert("RGB")
    current = Image.open(current_path).convert("RGB")

    max_width = max(golden.width, current.width)
    max_height = max(golden.height, current.height)
    canvas_golden = Image.new("RGB", (max_width, max_height), (0, 0, 0))
    canvas_current = Image.new("RGB", (max_width, max_height), (0, 0, 0))
    canvas_golden.paste(golden, (0, 0))
    canvas_current.paste(current, (0, 0))

    diff = ImageChops.difference(canvas_golden, canvas_current)
    h = diff.histogram()
    sum_of_squares = sum(value * ((idx % 256) ** 2) for idx, value in enumerate(h))
    rms = math.sqrt(sum_of_squares / float(max_width * max_height))

    if rms <= threshold:
        return True

    if diff_path:
        highlight = canvas_current.copy()
        draw = ImageDraw.Draw(highlight)
        for x in range(max_width):
            for y in range(max_height):
                pixel_diff = diff.getpixel((x, y))
                diff_sum = sum(pixel_diff[:3]) if isinstance(pixel_diff, tuple) else pixel_diff
                if diff_sum > 30:
                    draw.point((x, y), fill=(255, 0, 0))
        highlight.save(diff_path)
        print(f"  RMS difference: {rms:.2f}, diff saved to {diff_path}")

    return False