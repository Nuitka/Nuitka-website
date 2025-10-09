import os
from pathlib import Path

import pytest

from .utils import *

BASE_URL = "http://localhost:8000"

ROOT = Path(__file__).parent.parent

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

def run_visual_test(page, browser_name, page_path, viewport_mode, wait_time=DEFAULT_WAIT_TIME):
    url = build_url(page_path)
    safe_name = sanitizeUrl(page_path.lstrip('/') or "home")

    golden_path = f"{GOLDEN_DIR}/{browser_name}_{viewport_mode}_{safe_name}.png"
    current_path = f"{CURRENT_DIR}/{browser_name}_{viewport_mode}_{safe_name}.png"
    diff_path = f"{DIFF_DIR}/{browser_name}_{viewport_mode}_{safe_name}.png"

    os.makedirs(os.path.dirname(current_path), exist_ok=True)
    os.makedirs(os.path.dirname(diff_path), exist_ok=True)

    my_print(f"  Navigating to {url} ({browser_name}, {viewport_mode})")
    page.goto(url, timeout=20000)

    if wait_time > 0:
        page.wait_for_timeout(wait_time)

    page.screenshot(path=current_path, full_page=True, timeout=20000)

    if not os.path.exists(golden_path):
        pytest.fail(f"Reference image not found: {golden_path}. Run update_golden_images first.")

    my_print(f"Testing {browser_name} / {viewport_mode} / {page_path}")

    is_same = compareImages(golden_path, current_path, diff_path)
    result = "✓ Passed" if is_same else "✗ Failed"
    my_print(f"{result}: {browser_name} / {viewport_mode} / {page_path}")

    assert is_same, (
        f"Visual regression detected in {url} ({browser_name}-{viewport_mode}).\n"
        f"Difference saved to {diff_path}"
    )

DESKTOP_DEVICES = {
    "chromium": {"viewport": {"width": 1280, "height": 720}, "is_mobile": False},
    "firefox": {"viewport": {"width": 1280, "height": 720}, "is_mobile": False},
    "webkit": {"viewport": {"width": 1280, "height": 720}, "is_mobile": False},
}

MOBILE_DEVICES = {
    "chromium": {"viewport": {"width": 375, "height": 667}, "is_mobile": True, "has_touch": True},
    "firefox": {"viewport": {"width": 375, "height": 667}, "is_mobile": True, "has_touch": True},
    "webkit": {"viewport": {"width": 375, "height": 667}, "is_mobile": True, "has_touch": True},
}

@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
@pytest.mark.desktop
@pytest.mark.chromium
def test_visual_desktop_chromium(page, page_path):
    browser_name = "chromium"
    viewport_mode = "desktop"
    device = DESKTOP_DEVICES[browser_name]

    my_print(f"Running {browser_name} {viewport_mode} test for {page_path}")
    my_print(f"Using device settings: {device}")

    context = page.context.browser.new_context(**device)
    emulated_page = context.new_page()

    run_visual_test(
        page=emulated_page,
        browser_name=browser_name,
        page_path=page_path,
        viewport_mode=viewport_mode,
        wait_time=DEFAULT_WAIT_TIME
    )

    context.close()

@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
@pytest.mark.desktop
@pytest.mark.firefox
def test_visual_desktop_firefox(page, page_path):
    browser_name = "firefox"
    viewport_mode = "desktop"
    device = DESKTOP_DEVICES[browser_name]

    my_print(f"Running {browser_name} {viewport_mode} test for {page_path}")
    my_print(f"Using device settings: {device}")

    context = page.context.browser.new_context(**device)
    emulated_page = context.new_page()

    run_visual_test(
        page=emulated_page,
        browser_name=browser_name,
        page_path=page_path,
        viewport_mode=viewport_mode,
        wait_time=DEFAULT_WAIT_TIME
    )

    context.close()

@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
@pytest.mark.desktop
@pytest.mark.webkit
def test_visual_desktop_webkit(page, page_path):
    browser_name = "webkit"
    viewport_mode = "desktop"
    device = DESKTOP_DEVICES[browser_name]

    my_print(f"Running {browser_name} {viewport_mode} test for {page_path}")
    my_print(f"Using device settings: {device}")

    context = page.context.browser.new_context(**device)
    emulated_page = context.new_page()

    run_visual_test(
        page=emulated_page,
        browser_name=browser_name,
        page_path=page_path,
        viewport_mode=viewport_mode,
        wait_time=DEFAULT_WAIT_TIME
    )

    context.close()

@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
@pytest.mark.mobile
@pytest.mark.chromium
def test_visual_mobile_chromium(page, page_path):
    browser_name = "chromium"
    viewport_mode = "mobile"
    device = MOBILE_DEVICES[browser_name]

    my_print(f"Running {browser_name} {viewport_mode} test for {page_path}")
    my_print(f"Using device settings: {device}")

    context = page.context.browser.new_context(**device)
    emulated_page = context.new_page()

    run_visual_test(
        page=emulated_page,
        browser_name=browser_name,
        page_path=page_path,
        viewport_mode=viewport_mode,
        wait_time=DEFAULT_WAIT_TIME
    )

    context.close()

@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
@pytest.mark.mobile
@pytest.mark.firefox
def test_visual_mobile_firefox(page, page_path):
    browser_name = "firefox"
    viewport_mode = "mobile"
    device = MOBILE_DEVICES[browser_name]

    my_print(f"Running {browser_name} {viewport_mode} test for {page_path}")
    my_print(f"Using device settings: {device}")

    context = page.context.browser.new_context(**device)
    emulated_page = context.new_page()

    run_visual_test(
        page=emulated_page,
        browser_name=browser_name,
        page_path=page_path,
        viewport_mode=viewport_mode,
        wait_time=DEFAULT_WAIT_TIME
    )

    context.close()

@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
@pytest.mark.mobile
@pytest.mark.webkit
def test_visual_mobile_webkit(page, page_path):
    browser_name = "webkit"
    viewport_mode = "mobile"
    device = MOBILE_DEVICES[browser_name]

    my_print(f"Running {browser_name} {viewport_mode} test for {page_path}")
    my_print(f"Using device settings: {device}")

    context = page.context.browser.new_context(**device)
    emulated_page = context.new_page()

    run_visual_test(
        page=emulated_page,
        browser_name=browser_name,
        page_path=page_path,
        viewport_mode=viewport_mode,
        wait_time=DEFAULT_WAIT_TIME
    )

    context.close()

if __name__ == "__main__":
    my_print("This file is meant to be run with pytest.")
    my_print("Run all tests: pytest tests/regression.py")
    my_print("Examples:")
    my_print("  Only desktop Chromium: pytest tests/regression.py -m 'desktop and chromium' -v")
    my_print("  Only mobile: pytest tests/regression.py -m 'mobile' -v")