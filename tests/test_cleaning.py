import numpy as np

from src.cleaning import clean_text, is_empty_text, is_valid_review


def test_normal_text():
    result = clean_text("Great food and service!")
    assert result == "Great food and service!"


def test_extra_spaces():
    result = clean_text("   Great     food and service!   ")
    assert result == "Great food and service!"


def test_line_breaks_and_tabs():
    result = clean_text("Great\nfood\tand service!")
    assert result == "Great food and service!"


def test_none_value():
    assert clean_text(None) == ""


def test_nan_value():
    assert clean_text(np.nan) == ""


def test_empty_string():
    assert clean_text("") == ""


def test_only_spaces():
    assert clean_text("      ") == ""


def test_url_removal():
    result = clean_text(
        "Read more at https://example.com about this restaurant."
    )
    assert result == "Read more at about this restaurant."


def test_html_characters():
    result = clean_text("Food &amp; service were excellent.")
    assert result == "Food & service were excellent."


def test_preserves_special_characters():
    result = clean_text("Excellent food! 😊 10/10.")
    assert result == "Excellent food! 😊 10/10."


def test_detects_empty_text():
    assert is_empty_text("    ") is True


def test_detects_non_empty_text():
    assert is_empty_text("Good food") is False


def test_valid_review():
    assert is_valid_review("Good food") is True


def test_review_below_minimum_length():
    assert is_valid_review("Hi", minimum_length=3) is False