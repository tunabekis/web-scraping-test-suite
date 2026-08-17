# tests/conftest.py
import sys
from pathlib import Path

# Add the project root to sys.path so "from src.xxx import yyy" style
# imports (used throughout src/ and tests/) resolve regardless of how
# pytest was invoked.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


import shutil
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        d = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options,
        )

    else:  # firefox
        # Skip Firefox-based tests if Firefox isn't installed on this machine.
        firefox_path = shutil.which("firefox") or shutil.which("firefox.exe")
        if firefox_path is None:
            pytest.skip("Firefox is not installed on this system, skipping Firefox tests.")

        options = webdriver.FirefoxOptions()
        d = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options,
        )

    yield d
    d.quit()
