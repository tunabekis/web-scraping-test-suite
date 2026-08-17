# src/google_report/google_search.py

from typing import List
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


def get_google_results(keyword: str, max_results: int = 5) -> List[str]:
    """
    Uses Selenium + Chrome to search a keyword on Google
    and returns a list of first non-ad result URLs.
    """

    # Plain, non-headless Chrome driver.
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )

    try:
        driver.get("https://www.google.com")

        # NOTE: if a cookie consent banner appears, this selector may need
        # to be adjusted. For now we go straight for the search input.
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)  # simple wait for the results page to load

        # Collect the organic (non-ad) result links.
        links = []
        result_elements = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf > a")

        for el in result_elements:
            url = el.get_attribute("href")
            if url and "google.com" not in url:
                links.append(url)
            if len(links) >= max_results:
                break

        return links

    finally:
        driver.quit()
