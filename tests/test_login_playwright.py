# tests/test_login_playwright.py

from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright


def get_login_url() -> str:
    """
    Same as in the Selenium tests: returns the file:// URL of login.html.
    """
    root = Path(__file__).resolve().parents[1]  # project root
    login_file = root / "src" / "login_app" / "static" / "login.html"
    return login_file.as_uri()


@pytest.mark.parametrize("browser_name", ["chromium", "firefox"])
def test_login_success_playwright(browser_name):
    """
    Successful login test with valid credentials (Playwright).
    """
    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=True)
        page = browser.new_page()

        page.goto(get_login_url())

        page.fill("#username", "testuser")
        page.fill("#password", "password123")
        page.click("#login-btn")

        # Verify that navigation went to dashboard.html
        page.wait_for_timeout(500)  # give the page half a second to settle
        assert "dashboard.html" in page.url.lower()
        assert "Welcome, testuser!" in page.text_content("body")

        browser.close()


@pytest.mark.parametrize("browser_name", ["chromium", "firefox"])
def test_login_failure_playwright(browser_name):
    """
    Failed login test with invalid credentials (Playwright).
    """
    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=True)
        page = browser.new_page()

        page.goto(get_login_url())

        page.fill("#username", "wronguser")
        page.fill("#password", "wrongpass")
        page.click("#login-btn")

        page.wait_for_timeout(500)

        # Should remain on the login page and show an error message
        assert "login" in page.url.lower()
        msg = page.text_content("#message")
        assert "Invalid username or password" in msg

        browser.close()
