import re


REQUIRED_FIELDS = [
    "id",
    "title",
    "description",
    "source",
    "published_at",
    "url",
    "category"
]


def clean_text(text):
    """
    Clean basic formatting issues from text.

    This function does not rewrite the meaning of the text.
    It only normalizes whitespace and common spacing issues.
    """

    if text is None:
        return ""

    text = str(text)

    # Replace multiple whitespace characters with one space
    text = re.sub(r"\s+", " ", text)

    # Fix spaces before punctuation
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)

    # Fix spacing around apostrophes
    text = text.replace(" 's", "'s")

    # Fix spacing before hyphens
    text = text.replace(" -linked", "-linked")

    return text.strip()


def clean_record(record):
    """
    Clean one NewsPulse record.
    """

    cleaned = record.copy()

    # Clean text fields
    cleaned["title"] = clean_text(
        cleaned.get("title", "")
    )

    cleaned["description"] = clean_text(
        cleaned.get("description", "")
    )

    cleaned["source"] = clean_text(
        cleaned.get("source", "")
    )

    cleaned["category"] = clean_text(
        cleaned.get("category", "")
    )

    cleaned["url"] = str(
        cleaned.get("url", "")
    ).strip()

    cleaned["id"] = str(
        cleaned.get("id", "")
    ).strip()

    cleaned["published_at"] = str(
        cleaned.get("published_at", "")
    ).strip()

    return cleaned


def clean_records(records):
    """
    Clean a list of NewsPulse records.
    """

    cleaned_records = []

    for record in records:

        if not isinstance(record, dict):
            continue

        cleaned_record_data = clean_record(record)

        cleaned_records.append(
            cleaned_record_data
        )

    return cleaned_records