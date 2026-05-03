# Copyright (c) 2026 Kindleify
# MIT License - see LICENSE file

from langdetect import detect, LangDetectException
from langdetect import DetectorFactory

DetectorFactory.seed = 0


def detect_language(text: str) -> str:
    """
    Detect language from text.
    Returns ISO 639-1 language code.
    Falls back to 'en' if detection fails.
    """
    if not text or len(text.strip()) < 50:
        return "en"

    try:
        lang = detect(text)
        return lang if lang else "en"
    except LangDetectException:
        return "en"