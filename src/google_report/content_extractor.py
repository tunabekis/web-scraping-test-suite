# src/google_report/content_extractor.py

from typing import List
import re

import requests
from bs4 import BeautifulSoup


def fetch_page_text(url: str, timeout: int = 10) -> str:
    """
    Downloads the HTML of a page and returns cleaned text content.
    """

    try:
        response = requests.get(url, timeout=timeout, headers={
            "User-Agent": "Mozilla/5.0 (compatible; HomeworkBot/1.0)"
        })
        response.raise_for_status()
    except Exception as e:
        return f"Error fetching {url}: {e}"

    soup = BeautifulSoup(response.text, "lxml")

    # Extract text from all <p> tags as a reasonable approximation of the
    # page's main readable content.
    texts: List[str] = []

    for p in soup.find_all("p"):
        text = p.get_text(separator=" ", strip=True)
        if text:
            texts.append(text)

    raw_text = "\n".join(texts)

    # Collapse repeated whitespace produced by the extraction above.
    cleaned = re.sub(r"\s+", " ", raw_text)
    return cleaned.strip()
