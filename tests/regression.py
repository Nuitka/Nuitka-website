import pytest
import sys
import os
from playwright.sync_api import sync_playwright

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../Nuitka-develop")
    )
)

from nuitka.Tracing import my_print

from utils import *
from const import *

def run_visual_test(browser_name, viewport_mode, page_path, wait_time=DEFAULT_WAIT_TIME):
    url = build_url(page_path)
    safe_name = sanitizeUrl(page_path.lstrip('/') or "home")

    golden_path = f"{GOLDEN_DIR}/{browser_name}_{viewport_mode}_{safe_name}.png"
    current_path = f"{CURRENT_DIR}/{browser_name}_{viewport_mode}_{safe_name}.png"
    diff_path = f"{DIFF_DIR}/{browser_name}_{viewport_mode}_{safe_name}.png"

    os.makedirs(os.path.dirname(current_path), exist_ok=True)
    os.makedirs(os.path.dirname(diff_path), exist_ok=True)

    with sync_playwright() as p:
        browser = getattr(p, browser_name).launch()
        takeScreenshot(browser, url, viewport_mode, base_path=CURRENT_DIR, wait_time=wait_time)
        browser.close()

    if not os.path.exists(golden_path):
        pytest.fail(f"Reference image not found: {golden_path}. Run update_golden_images first.")

    my_print(f"Testing {browser_name} / {viewport_mode} / {page_path}")

    is_same = compareImages(golden_path, current_path, diff_path)
    result = "✓ Passed" if is_same else "✗ Failed"
    my_print(f"{result}: {browser_name} / {viewport_mode} / {page_path}")

    assert is_same, (f"Visual regression detected in {url} ({browser_name}-{viewport_mode}).\n"
                     f"Difference saved to {diff_path}")


def update_all_golden_images(wait_time=DEFAULT_WAIT_TIME):
    update_golden_images(wait_time=wait_time)


@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
def test_chrome_desktop(page_path):
    my_print(f"Running Chrome Desktop test for {page_path}")
    run_visual_test("chromium", "desktop", page_path, wait_time=DEFAULT_WAIT_TIME)

@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
def test_chrome_mobile(page_path):
    my_print(f"Running Chrome Mobile test for {page_path}")
    run_visual_test("chromium", "mobile", page_path, wait_time=DEFAULT_WAIT_TIME)

@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
def test_firefox_desktop(page_path):
    my_print(f"Running Firefox Desktop test for {page_path}")
    run_visual_test("firefox", "desktop", page_path, wait_time=DEFAULT_WAIT_TIME)

@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
def test_firefox_mobile(page_path):
    my_print(f"Running Firefox Mobile test for {page_path}")
    run_visual_test("firefox", "mobile", page_path, wait_time=DEFAULT_WAIT_TIME)

@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
def test_webkit_desktop(page_path):
    my_print(f"Running Webkit Desktop test for {page_path}")
    run_visual_test("webkit", "desktop", page_path, wait_time=DEFAULT_WAIT_TIME)

@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
def test_webkit_mobile(page_path):
    my_print(f"Running Webkit Mobile test for {page_path}")
    run_visual_test("webkit", "mobile", page_path, wait_time=DEFAULT_WAIT_TIME)


if __name__ == "__main__":
    my_print("This file is meant to be run with pytest.")
    my_print("Run all tests: pytest tests/browser_test.py")
    my_print("Update golden images: python tests/update_golden.py")