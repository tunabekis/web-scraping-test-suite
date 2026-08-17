# src/config.py

import os
from dotenv import load_dotenv

# Load environment variables from a .env file in the project root, if present.
load_dotenv()

# Optional: enables real Gemini-powered summaries in src/google_report/summarizer.py.
# When it is not set, the summarizer transparently falls back to a local,
# dependency-free summarization strategy instead of failing.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
