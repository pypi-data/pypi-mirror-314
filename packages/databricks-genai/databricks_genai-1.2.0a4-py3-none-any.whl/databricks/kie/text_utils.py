"""Utility functions for text processing."""

import difflib
import re

__all__ = [
    'clean_text',
    'normalize_text',
    'fuzzy_string_match',
]


def clean_text(text: str) -> str:
    # Replace common character that shows up in PDF parsed text
    text = text.replace('\xa0', ' ')

    # Strip off leading and trailing white spaces
    text = text.strip()

    # Lower case
    text = text.lower()

    # Replace consecutive white spaces with single ones
    text = re.sub(r'\s+', ' ', text)

    return text


def normalize_text(text: str) -> str:
    # Apply cleaning
    text = clean_text(text)

    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # Remove ordinal suffixes
    text = re.sub(r'\b(\d+)(st|nd|rd|th)\b', lambda x: x.group(1), text)

    return text


def fuzzy_string_match(
    text_1: str,
    text_2: str,
    long_ratio_threshold: float = 0.7,
    short_ratio_threshold: float = 0.5,
    similarity_threshold: float = 0.8,
    min_length_threshold: int = 3,
) -> bool:
    """Check if two strings are similar based on a combination of string similarity and ratio of longest match.

    Args:
        text_1 (str): The first text to compare.
        text_2 (str): The second text to compare.
        long_ratio_threshold (float, optional): Minimum threshold for the larger ratio of longest common substring
            to string length. Defaults to 0.7.
        short_ratio_threshold (float, optional): Minimum threshold for the smaller ratio of longest common substring
            to string length. Defaults to 0.5.
        similarity_threshold (float, optional): Minimum overall sequence similarity ratio required for strings
            to be considered matching. Defaults to 0.8.
        min_length_threshold (int, optional): Minimum length of input strings for fuzzy matching.
            Strings shorter than this will be compared exactly. Defaults to 3.

    Returns:
        bool: True if the strings are similar, False otherwise.
    """
    if len(text_1) <= min_length_threshold or len(text_2) <= min_length_threshold:
        return clean_text(text_1) == clean_text(text_2)

    sm = difflib.SequenceMatcher(None, clean_text(str(text_1)), clean_text(str(text_2)))
    similarity = sm.ratio()
    longest_match = sm.find_longest_match()
    ratio_a = longest_match.size / len(sm.a)  # type: ignore
    ratio_b = longest_match.size / len(sm.b)  # type: ignore
    longest_match_ratio = max(ratio_a, ratio_b)
    shortest_match_ratio = min(ratio_a, ratio_b)

    is_ratio_match = longest_match_ratio > long_ratio_threshold and shortest_match_ratio > short_ratio_threshold
    is_similarity_match = similarity > similarity_threshold

    return is_ratio_match or is_similarity_match
