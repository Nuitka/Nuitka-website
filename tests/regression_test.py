import os
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright

from regression_utils import (
    my_print,
    build_url,
    sanitizeUrl,
    compareImages,
    GOLDEN_DIR,
    CURRENT_DIR,
    DIFF_DIR,
    DESKTOP_DEVICES,
    MOBILE_DEVICES,
    GOLDEN_PAGES,
    DEFAULT_WAIT_TIME,
)
from settings import comparison_threshold


def run_visual_test(browser_name, viewport_mode, page_path, wait_time=DEFAULT_WAIT_TIME):
    if viewport_mode == "desktop":
        device_config = DESKTOP_DEVICES[browser_name]
    elif viewport_mode == "mobile":
        device_config = MOBILE_DEVICES[browser_name]
    else:
        raise ValueError(f"Unknown viewport mode: {viewport_mode}")

    url = build_url(page_path)
    safe_name = sanitizeUrl(page_path.lstrip('/') or "home")

    golden_path = f"{GOLDEN_DIR}/{browser_name}_{viewport_mode}_{safe_name}.png"
    current_path = f"{CURRENT_DIR}/{browser_name}_{viewport_mode}_{safe_name}.png"
    diff_path = f"{DIFF_DIR}/{browser_name}_{viewport_mode}_{safe_name}.png"

    os.makedirs(os.path.dirname(current_path), exist_ok=True)
    os.makedirs(os.path.dirname(diff_path), exist_ok=True)

    my_print(f"Testing {browser_name} / {viewport_mode} / {page_path}")
    my_print(f"Using device settings: {device_config}")

    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=True)
        context = browser.new_context(**device_config)
        page = context.new_page()

        my_print(f"  Navigating to {url}")
        page.goto(url, timeout=20000)
        if wait_time > 0:
            page.wait_for_timeout(wait_time)

        page.add_style_tag(content="""
            * {
                font-family: Arial, Helvetica, sans-serif !important;
                -webkit-font-smoothing: none !important;
                -moz-osx-font-smoothing: grayscale !important;
            }
        """)
        page.wait_for_function("document.fonts.ready")
        page.screenshot(path=current_path, full_page=True, timeout=20000)

        context.close()
        browser.close()

    if not os.path.exists(golden_path):
        pytest.fail(f"Reference image not found: {golden_path}. Run update_golden_images first.")

    is_same = compareImages(golden_path, current_path, diff_path, comparison_threshold)
    result = "✓ Passed" if is_same else "✗ Failed"
    my_print(f"{result}: {browser_name} / {viewport_mode} / {page_path}")

    assert is_same, (
        f"Visual regression detected in {url} ({browser_name}-{viewport_mode}).\n"
        f"Difference saved to {diff_path}"
    )


@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
@pytest.mark.desktop
@pytest.mark.chromium
def test_visual_desktop_chromium(page_path):
    run_visual_test("chromium", "desktop", page_path, wait_time=DEFAULT_WAIT_TIME)


@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
@pytest.mark.desktop
@pytest.mark.firefox
def test_visual_desktop_firefox(page_path):
    run_visual_test("firefox", "desktop", page_path, wait_time=DEFAULT_WAIT_TIME)


@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
@pytest.mark.desktop
@pytest.mark.webkit
def test_visual_desktop_webkit(page_path):
    run_visual_test("webkit", "desktop", page_path, wait_time=DEFAULT_WAIT_TIME)


@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
@pytest.mark.mobile
@pytest.mark.chromium
def test_visual_mobile_chromium(page_path):
    run_visual_test("chromium", "mobile", page_path, wait_time=DEFAULT_WAIT_TIME)


@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
@pytest.mark.mobile
@pytest.mark.firefox
def test_visual_mobile_firefox(page_path):
    run_visual_test("firefox", "mobile", page_path, wait_time=DEFAULT_WAIT_TIME)


@pytest.mark.parametrize("page_path", GOLDEN_PAGES)
@pytest.mark.mobile
@pytest.mark.webkit
def test_visual_mobile_webkit(page_path):
    run_visual_test("webkit", "mobile", page_path, wait_time=DEFAULT_WAIT_TIME)


if __name__ == "__main__":
    my_print("This file is meant to be run with pytest.")
    my_print("Run all tests: pytest tests/regression.py")
    my_print("Examples:")
    my_print("  Only desktop Chromium: pytest tests/regression.py -m 'desktop and chromium' -v")
    my_print("  Only mobile: pytest tests/regression.py -m 'mobile' -v")