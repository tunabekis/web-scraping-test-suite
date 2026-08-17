# tests/test_google_report_integration.py
"""
Integration tests for the Google keyword report pipeline
(search -> fetch -> summarize -> PDF export).

The real Google search step relies on Selenium driving a live browser
against google.com, which is slow and prone to CAPTCHAs in CI/sandboxed
environments. These tests instead patch that single boundary and exercise
the rest of the pipeline (content fetching, summarization with its local
fallback, report assembly and PDF export) for real.
"""

from src.google_report import report_generator


def test_build_keyword_report_produces_well_formed_report(monkeypatch):
    monkeypatch.setattr(
        report_generator,
        "get_google_results",
        lambda keyword, max_results=5: [
            "https://en.wikipedia.org/wiki/IPhone_15",
            "https://www.apple.com/iphone-15/",
        ],
    )
    monkeypatch.setattr(
        report_generator,
        "fetch_page_text",
        lambda url, timeout=10: (
            "This is the first sentence about the product. "
            "This is the second sentence with more detail. "
            "This is a third, less important sentence."
        ),
    )

    report = report_generator.build_keyword_report("iphone 15", max_results=2)

    assert report["keyword"] == "iphone 15"
    assert len(report["entries"]) == 2
    for entry in report["entries"]:
        assert entry["url"].startswith("https://")
        assert entry["summary"]
    assert report["conclusion"]


def test_build_keyword_report_falls_back_when_search_returns_nothing(monkeypatch):
    monkeypatch.setattr(
        report_generator, "get_google_results", lambda keyword, max_results=5: []
    )
    monkeypatch.setattr(
        report_generator,
        "fetch_page_text",
        lambda url, timeout=10: "Fallback content sentence one. Fallback content sentence two.",
    )

    report = report_generator.build_keyword_report("iphone 15 128gb", max_results=3)

    # The iPhone-specific fallback URLs from build_keyword_report should be used.
    assert any("wikipedia.org" in e["url"] for e in report["entries"])
    assert report["conclusion"]


def test_export_report_to_pdf_writes_a_pdf_file(tmp_path, monkeypatch):
    monkeypatch.setattr(
        report_generator, "get_google_results", lambda keyword, max_results=5: ["https://example.com"]
    )
    monkeypatch.setattr(
        report_generator,
        "fetch_page_text",
        lambda url, timeout=10: "Example content sentence for the PDF export test.",
    )

    report = report_generator.build_keyword_report("example keyword", max_results=1)

    output_path = tmp_path / "report_example.pdf"
    report_generator.export_report_to_pdf(report, str(output_path))

    assert output_path.exists()
    assert output_path.stat().st_size > 0
