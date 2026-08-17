# src/google_report/gemini_client.py

from typing import Optional

from src.config import GEMINI_API_KEY

# Gemini exposes an OpenAI-compatible endpoint, so the official `openai` SDK
# can talk to it directly by pointing base_url at Google's compatibility layer.
_GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
_GEMINI_MODEL = "gemini-2.0-flash"


def is_available() -> bool:
    """Whether a Gemini API key has been configured."""
    return bool(GEMINI_API_KEY)


def generate_summary(prompt: str) -> Optional[str]:
    """
    Sends a prompt to Gemini and returns the generated text.

    Returns None (instead of raising) whenever Gemini cannot be used, so
    callers can fall back to a local summarization strategy without needing
    their own try/except around every call site.
    """
    if not is_available():
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=GEMINI_API_KEY, base_url=_GEMINI_BASE_URL)
        response = client.chat.completions.create(
            model=_GEMINI_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.choices[0].message.content
        return text.strip() if text else None
    except Exception:
        # Network errors, invalid/expired keys, rate limits, etc. should
        # degrade to the local fallback rather than crash the report build.
        return None
