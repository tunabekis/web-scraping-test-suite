# src/google_report/summarizer.py

from typing import Dict, List
import re

from src.google_report import gemini_client


def _split_sentences(text: str) -> List[str]:
    """Naive sentence splitter: breaks after '.', '?' or '!' followed by whitespace."""
    text = text.strip()
    if not text:
        return []
    return re.split(r'(?<=[.!?])\s+', text)


def _local_summarize_page_text(page_text: str, url: str) -> str:
    """
    Dependency-free fallback summarizer: takes the first 2-3 sentences of the
    page text. Used whenever Gemini is unavailable or fails.
    """
    if not page_text or page_text.startswith("Error fetching"):
        return (
            f"Content for {url} could not be retrieved, "
            "so no detailed summary is available."
        )

    sentences = _split_sentences(page_text)
    if not sentences:
        return (
            f"Content for {url} does not contain enough readable text "
            "to generate a summary."
        )

    summary_sentences = sentences[:3]
    return " ".join(summary_sentences)


def summarize_page_text(page_text: str, url: str) -> str:
    """
    Summarizes a single page's text.

    Tries Gemini first (when GEMINI_API_KEY is configured) for a higher
    quality summary, and falls back to a local, purely rule-based summary
    otherwise. This mirrors the "Gemini API (or fallback)" behavior the
    report generator is expected to provide.
    """
    if not page_text or page_text.startswith("Error fetching"):
        return _local_summarize_page_text(page_text, url)

    prompt = (
        "Summarize the following web page content in 2-3 concise sentences "
        f"for a short research report about the source at {url}.\n\n{page_text[:4000]}"
    )
    gemini_summary = gemini_client.generate_summary(prompt)
    if gemini_summary:
        return gemini_summary

    return _local_summarize_page_text(page_text, url)


def summarize_overall(keyword: str, entries: List[Dict]) -> str:
    """
    Produces an overall conclusion from the per-source summaries.

    Tries Gemini first, then falls back to a local heuristic that stitches
    together the first few sentences collected from all source summaries.
    """
    if not entries:
        return (
            "No sources were available, so no overall conclusion can be drawn."
        )

    all_summaries_text = " ".join(e.get("summary", "") for e in entries)

    prompt = (
        f"Based on the following per-source summaries about '{keyword}', "
        "write a short overall conclusion (3-5 sentences):\n\n"
        f"{all_summaries_text[:4000]}"
    )
    gemini_conclusion = gemini_client.generate_summary(prompt)
    if gemini_conclusion:
        return gemini_conclusion

    sentences = _split_sentences(all_summaries_text)
    if not sentences:
        return (
            "The collected summaries did not contain enough information "
            "to produce a meaningful conclusion."
        )

    overall_sentences = sentences[:5]
    conclusion = (
        f"For the keyword '{keyword}', the collected web pages generally "
        "discuss similar key aspects. "
        + " ".join(overall_sentences)
    )
    return conclusion
