# tests/test_login_factory.py
from pathlib import Path

import pytest
from selenium.webdriver.common.by import By

from src.factories.test_data_factory import login_scenarios


def get_login_url() -> str:
    """Returns the file:// URL of login.html, same as the other login tests."""
    root = Path(__file__).resolve().parents[1]  # project root
    login_file = root / "src" / "login_app" / "static" / "login.html"
    return login_file.as_uri()


@pytest.mark.parametrize(
    "scenario",
    login_scenarios(),
    ids=lambda s: s["id"],
)
def test_login_scenarios(driver, scenario):
    """
    A single test function that runs repeatedly against every scenario
    produced by the test data factory. This is the pytest equivalent of
    TestNG's @Factory approach.
    """
    driver.get(get_login_url())

    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "password").clear()

    driver.find_element(By.ID, "username").send_keys(scenario["username"])
    driver.find_element(By.ID, "password").send_keys(scenario["password"])
    driver.find_element(By.ID, "login-btn").click()

    if scenario["should_succeed"]:
        # Expect a successful login.
        assert "dashboard.html" in driver.current_url.lower()
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Welcome, testuser!" in body_text
    else:
        # Expect a failed login.
        assert "login" in driver.current_url.lower()
        msg = driver.find_element(By.ID, "message").text
        assert "Invalid username or password" in msg
