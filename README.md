# Web Scraping Test Suite

A collection of small Python applications and their automated test suites,
built to demonstrate web scraping techniques together with different
software testing approaches (Selenium, Playwright, pytest parametrization
and a test-data factory pattern).

## Features

### 1. Book Price Comparator
Uses Selenium to open three book pages on [BooksToScrape](https://books.toscrape.com/),
extracts and parses their prices, and reports the minimum, maximum and
average price.

- Run: `python run_price_comparison.py`
- Test: `pytest tests/test_price_utils.py`
- Key files: `run_price_comparison.py`, `src/price_comparator/`

### 2. Login Page + Automated Login Tests
A static login page (`src/login_app/static/login.html`) that redirects to
`dashboard.html` on success or shows an error message on failure. Covered
by three parallel test strategies:

- **Selenium**: `pytest tests/test_login_selenium.py`
- **Playwright** (Chromium + Firefox): `pytest tests/test_login_playwright.py`
- **Factory-style parametrization** (pytest's take on TestNG's `@Factory`,
  scenarios sourced from `src/factories/test_data_factory.py`):
  `pytest tests/test_login_factory.py`

### 3. Google Keyword Web Report Generator
Searches Google for a keyword, opens the top results, extracts their text,
summarizes each source and produces a PDF report with an overall
conclusion.

- Run: `python run_google_report.py`
- Test: `pytest tests/test_google_report_integration.py`
- Key files: `run_google_report.py`, `src/google_report/`

Summaries are generated with the Gemini API when a key is configured, and
automatically fall back to a local, dependency-free summarizer otherwise
(see [Configuration](#configuration)).

## Tech Stack

- **Python 3**
- **Selenium** + **webdriver-manager** — browser automation
- **Playwright** — cross-browser automation (Chromium, Firefox)
- **pytest** — test runner, fixtures and parametrization
- **requests** + **BeautifulSoup4** (`lxml` parser) — HTML fetching/parsing
- **fpdf2** — PDF report generation
- **openai** SDK — used against Gemini's OpenAI-compatible endpoint
- **python-dotenv** — loads local configuration from `.env`

## Project Structure

```
run_price_comparison.py       # entry point: book price comparison
run_google_report.py          # entry point: keyword web report generator
src/
  config.py                   # environment configuration (e.g. GEMINI_API_KEY)
  price_comparator/           # price scraping + parsing logic
  login_app/static/           # login.html / dashboard.html under test
  google_report/              # search, extraction, summarization, PDF export
  factories/                  # reusable test-data factories
tests/                        # pytest suite (unit, integration and UI tests)
```

## Getting Started

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Install Playwright's browser binaries (only needed for the Playwright tests):
   ```
   playwright install
   ```
3. Run any of the entry points or test files listed above.

## Configuration

The Google report generator can optionally use the Gemini API for higher
quality summaries. Create a `.env` file in the project root with:

```
GEMINI_API_KEY=your-key-here
```

If this variable is not set, the summarizer automatically falls back to a
local heuristic (no API key required, no network calls).

## Testing Notes

- `tests/conftest.py` provides a `driver` fixture parametrized over Chrome
  and Firefox; Firefox-based tests are skipped automatically if Firefox is
  not installed on the machine.
- UI tests load `login.html` directly via a `file://` URL, so no local web
  server is required to run them.
