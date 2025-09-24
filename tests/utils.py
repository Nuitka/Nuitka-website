from nuitka.Tracing import my_print
import os
import re
from playwright.sync_api import Page, expect
from PIL import Image, ImageChops, ImageDraw
import math

GOLDEN_PAGES = [
    "/",
    "doc/developer-manual.html",
    "doc/download.html",
    "commercial/purchase.html",
    "changelog/index.html",
    "changelog/Changelog.html",
    "user-documentation/nuitka-package-config.html",
    "user-documentation/user-manual.html",
    "user-documentation/use-cases.html",
    "user-documentation/common-issue-solutions.html",
    "posts/nuitka-package-config-kickoff.html",
    "doc/api-doc.html",
    "doc/download.html",
    "changelog/Changelog-next.html",
    "posts/nuitka-shaping-up.html",
    "doc/commercial.html",
    "doc/commercial/protect-data-files.html",
    "posts/nuitka-package-config-part2.html",
    "user-documentation/tips.html",
    "posts/nuitka-package-config-part3.html",
    "pages/website-manual.html",
]

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
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)...",
    },
}

def sanitizeUrl(url: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]', '_', url)

def takeScreenshot(browser, url, mode, base_path="screenshots"):
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    context = browser.new_context(**VIEWPORTS[mode])
    page = context.new_page()
    page.goto(url)

    safe_url = sanitizeUrl(url)
    file_path = f"{base_path}/{mode}_{safe_url}.png"

    page.screenshot(path=file_path)
    context.close()

    return file_path

def updateGoldenImages(browser, base_path="screenshots"):
    for mode in VIEWPORTS:
        for url in GOLDEN_PAGES:
            path = takeScreenshot(browser, url, mode, base_path)
            
            if not path:
                my_print(f"Failed to take screenshot for {url} in {mode} mode")
            else:
                my_print(f"Screenshot taken for {url} in {mode} mode")

def compareImages(golden_path, current_path, diff_path=None, threshold=5):
    golden = Image.open(golden_path).convert("RGB")
    current = Image.open(current_path).convert("RGB")

    if golden.size != current.size:
        return False

    diff = ImageChops.difference(golden, current)

    h = diff.histogram()
    sq = (value * ((idx % 256) ** 2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / float(golden.size[0] * golden.size[1]))

    if rms <= threshold:
        return True

    if diff_path:
        highlight = current.copy()
        draw = ImageDraw.Draw(highlight)
        for x in range(current.width):
            for y in range(current.height):
                if diff.getpixel((x, y)) != (0, 0, 0):
                    draw.point((x, y), fill=(255, 0, 0))
        highlight.save(diff_path)

    return False
