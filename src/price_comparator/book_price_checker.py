# src/price_comparator/book_price_checker.py

from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from src.price_comparator.price_utils import parse_price_to_float


# 3 different book pages, treated as 3 different "sites" for comparison.
BOOK_SITES: List[Dict[str, str]] = [
    {
        "name": "BooksToScrape - Book 1",
        "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    },
    {
        "name": "BooksToScrape - Book 2",
        "url": "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
    },
    {
        "name": "BooksToScrape - Book 3",
        "url": "https://books.toscrape.com/catalogue/soumission_998/index.html",
    },
]


def create_driver() -> webdriver.Chrome:
    """Creates a plain Chrome WebDriver instance."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )
    return driver


def get_price_for_site(driver: webdriver.Chrome, site: Dict[str, str]) -> Dict:
    """
    Visits a single book page, finds the price element and parses it.
    """
    driver.get(site["url"])

    # On BooksToScrape product pages, the price is rendered as:
    # <p class="price_color">£51.77</p>
    price_element = driver.find_element(By.CSS_SELECTOR, "p.price_color")
    raw_price = price_element.text.strip()

    try:
        price = parse_price_to_float(raw_price)
    except Exception:
        price = None

    return {
        "site": site["name"],
        "url": site["url"],
        "raw_price": raw_price,
        "price": price,
    }


def collect_book_prices() -> List[Dict]:
    """
    Collects prices for every site listed in BOOK_SITES.
    """
    driver = create_driver()
    results: List[Dict] = []

    try:
        for site in BOOK_SITES:
            item = get_price_for_site(driver, site)
            results.append(item)
    finally:
        driver.quit()

    return results
