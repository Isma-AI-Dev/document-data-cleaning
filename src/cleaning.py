from __future__ import annotations

import html
import re
from typing import Any

import pandas as pd
from ftfy import fix_text


# Finds links such as https://example.com or www.example.com
URL_PATTERN = re.compile(
    r"https?://\S+|www\.\S+",
    flags=re.IGNORECASE,
)

# Finds hidden control characters that may appear in damaged text
CONTROL_CHARACTER_PATTERN = re.compile(
    r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]"
)

# Finds repeated spaces, tabs, and line breaks
WHITESPACE_PATTERN = re.compile(r"\s+")


def is_missing_value(value: Any) -> bool:
    """
    Return True when a value is None, NaN, or another pandas missing value.
    """

    if value is None:
        return True

    try:
        return bool(pd.isna(value))
    except (TypeError, ValueError):
        return False


def remove_urls(text: str) -> str:
    """
    Remove website links from text.
    """

    return URL_PATTERN.sub(" ", text)


def normalize_whitespace(text: str) -> str:
    """
    Replace repeated spaces, tabs, and line breaks with one space.
    """

    return WHITESPACE_PATTERN.sub(" ", text).strip()


def clean_text(value: Any, remove_web_links: bool = True) -> str:
    """
    Clean one review while preserving valid languages, punctuation, and emojis.

    The function handles:
    - None and missing values
    - Empty text
    - Broken encoding characters
    - HTML characters such as &amp;
    - Hidden control characters
    - URLs
    - Repeated spaces and line breaks
    - English, Urdu, Arabic, and other languages
    """

    if is_missing_value(value):
        return ""

    text = str(value)

    # Repair broken characters such as Ã, Â, and similar encoding problems.
    text = fix_text(text)

    # Convert HTML characters, for example &amp; into &.
    text = html.unescape(text)

    # Remove invisible control characters.
    text = CONTROL_CHARACTER_PATTERN.sub(" ", text)

    # Remove zero-width spaces that may be hidden inside text.
    text = text.replace("\u200b", "")
    text = text.replace("\ufeff", "")

    if remove_web_links:
        text = remove_urls(text)

    text = normalize_whitespace(text)

    return text


def is_empty_text(value: Any) -> bool:
    """
    Return True when a value becomes empty after cleaning.
    """

    return clean_text(value) == ""


def is_valid_review(value: Any, minimum_length: int = 3) -> bool:
    """
    Return True when the cleaned review contains enough characters.
    """

    cleaned_text = clean_text(value)

    return len(cleaned_text) >= minimum_length
if __name__ == "__main__":
    sample_text = "   Great food and service!   "
    print(clean_text(sample_text))