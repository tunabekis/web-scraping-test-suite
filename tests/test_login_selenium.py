# tests/test_login_selenium.py
from pathlib import Path

from selenium.webdriver.common.by import By


def get_login_url() -> str:
    """
    Returns the file:// URL of login.html.
    """
    root = Path(__file__).resolve().parents[1]  # project root
    login_file = root / "src" / "login_app" / "static" / "login.html"
    return login_file.as_uri()


def test_login_success(driver):
    driver.get(get_login_url())

    driver.find_element(By.ID, "username").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "login-btn").click()

    assert "dashboard.html" in driver.current_url.lower()
    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Welcome, testuser!" in body_text


def test_login_failure(driver):
    driver.get(get_login_url())

    driver.find_element(By.ID, "username").send_keys("wronguser")
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.find_element(By.ID, "login-btn").click()

    assert "login" in driver.current_url.lower()
    msg = driver.find_element(By.ID, "message").text
    assert "Invalid username or password" in msg
