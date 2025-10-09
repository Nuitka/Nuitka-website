import re
import os
import sys
from PIL import Image, ImageChops, ImageDraw
import math
from urllib.parse import urlparse

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../Nuitka-develop")
    )
)
from nuitka.Tracing import my_print

from const import VIEWPORTS, GOLDEN_PAGES, BASE_URL, GOLDEN_DIR, CURRENT_DIR, DIFF_DIR, BROWSERS, COMPARISON_THRESHOLD, DEFAULT_WAIT_TIME

def sanitizeUrl(url):
    path = urlparse(url).path
    path = "home" if path in ("", "/") else path.lstrip("/")
    return re.sub(r'[^a-zA-Z0-9_-]', '_', path)

def get_context_options(browser_name, mode):
    options = VIEWPORTS[mode].copy()
    if browser_name == "firefox":
        options.pop("is_mobile", None)
        options.pop("has_touch", None)
    return options

def build_url(page_path):
    if not page_path:
        return BASE_URL
    if page_path.startswith('/') and BASE_URL.endswith('/'):
        return f"{BASE_URL}{page_path[1:]}"
    if not page_path.startswith('/') and not BASE_URL.endswith('/'):
        return f"{BASE_URL}/{page_path}"
    return f"{BASE_URL}{page_path}"

def takeScreenshot(browser, url, mode, base_path=CURRENT_DIR, wait_time=DEFAULT_WAIT_TIME):
    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)

    browser_name = browser.browser_type.name
    context_options = get_context_options(browser_name, mode)
    context = browser.new_context(**context_options)
    page = context.new_page()

    page.goto(url, timeout=20000)
    my_print(f"  Taking screenshot of {url} ({browser_name}, {mode})")

    if wait_time > 0:
        page.wait_for_timeout(wait_time)

    safe_url = sanitizeUrl(url.replace(BASE_URL, "") or "home")
    file_path = f"{base_path}/{browser_name}_{mode}_{safe_url}.png"

    page.screenshot(path=file_path, timeout=20000)
    context.close()
    return file_path

def compareImages(golden_path, current_path, diff_path = None, threshold=COMPARISON_THRESHOLD):
    golden = Image.open(golden_path).convert("RGB")
    current = Image.open(current_path).convert("RGB")

    if golden.size != current.size:
        my_print(f"  Size mismatch: Golden {golden.size} vs Current {current.size}")
        if diff_path:
            error_img = Image.new('RGB', (400, 100), color=(255, 0, 0))
            ImageDraw.Draw(error_img).text(
                (10, 40),
                f"Size mismatch: Golden {golden.size} vs Current {current.size}",
                fill=(255, 255, 255)
            )
            error_img.save(diff_path)
        return False

    diff = ImageChops.difference(golden, current)
    h = diff.histogram()
    sum_of_squares = sum(value * ((idx % 256) ** 2) for idx, value in enumerate(h))
    rms = math.sqrt(sum_of_squares / float(golden.size[0] * golden.size[1]))

    if rms <= threshold:
        return True

    if diff_path:
        highlight = current.copy()
        draw = ImageDraw.Draw(highlight)
        for x in range(current.width):
            for y in range(current.height):
                pixel_diff = diff.getpixel((x, y))
                diff_sum = sum(pixel_diff[:3]) if isinstance(pixel_diff, tuple) else pixel_diff
                if diff_sum > 30:
                    draw.point((x, y), fill=(255, 0, 0))
        highlight.save(diff_path)

    return False

def update_golden_images(browsers_to_use=None, modes_to_use=None, pages_to_update=None, wait_time=DEFAULT_WAIT_TIME):
    from playwright.sync_api import sync_playwright

    browsers_to_use = browsers_to_use or BROWSERS
    modes_to_use = modes_to_use or list(VIEWPORTS.keys())
    pages_to_update = pages_to_update or GOLDEN_PAGES

    if not os.path.exists(GOLDEN_DIR):
        os.makedirs(GOLDEN_DIR, exist_ok=True)

    total = len(browsers_to_use) * len(modes_to_use) * len(pages_to_update)
    count = 0
    errors = []
    successes = 0

    my_print(f"\nStarting to update {total} golden images across {len(browsers_to_use)} browsers")

    with sync_playwright() as p:
        for browser_name in browsers_to_use:
            my_print(f"\nLaunching {browser_name}...")
            browser = getattr(p, browser_name).launch(timeout=120000)

            for mode in modes_to_use:
                for page_path in pages_to_update:
                    count += 1
                    my_print(f"\n[{count}/{total}] Processing: {browser_name} / {mode} / {page_path}")
                    url = build_url(page_path)
                    try:
                        file_path = takeScreenshot(browser, url, mode, base_path=GOLDEN_DIR, wait_time=wait_time)
                        my_print(f"✓ Completed: {os.path.basename(file_path)}")
                        successes += 1
                    except Exception as e:
                        my_print(f"✗ Failed: {browser_name} / {mode} / {page_path}")
                        my_print(f"  Error: {str(e)}")
                        errors.append(f"{browser_name} / {mode} / {page_path}: {str(e)}")
                        continue

            browser.close()

    my_print(f"\nSummary: {successes} successful, {len(errors)} failed out of {total} total")
    if errors:
        my_print("\nThe following errors occurred:")
        for error in errors:
            my_print(f"- {error}")
