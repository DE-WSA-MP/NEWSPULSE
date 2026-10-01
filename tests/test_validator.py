from apps.processing.validator import (
    validate_record,
    validate_records
)


def test_valid_record():

    record = {
        "id": "123",
        "title": "Example News",
        "description": "Example description.",
        "source": "Hacker News",
        "published_at": "2026-09-29 20:12:30",
        "url": "https://example.com",
        "category": "Technology"
    }

    is_valid, reasons = validate_record(record)

    assert is_valid is True
    assert reasons == []


def test_invalid_record_missing_title():

    record = {
        "id": "123",
        "title": "",
        "description": "Example description.",
        "source": "Hacker News",
        "published_at": "2026-09-29 20:12:30",
        "url": "https://example.com",
        "category": "Technology"
    }

    is_valid, reasons = validate_record(record)

    assert is_valid is False
    assert "Title is empty" in reasons


def test_validate_records():

    valid_record = {
        "id": "123",
        "title": "Valid News",
        "description": "",
        "source": "Hacker News",
        "published_at": "2026-09-29 20:12:30",
        "url": "https://example.com",
        "category": "Technology"
    }

    invalid_record = {
        "id": "",
        "title": "Invalid News",
        "description": "",
        "source": "Hacker News",
        "published_at": "2026-09-29 20:12:30",
        "url": "https://example.com",
        "category": "Technology"
    }

    valid, invalid = validate_records(
        [valid_record, invalid_record]
    )

    assert len(valid) == 1
    assert len(invalid) == 1

    assert "ID is empty" in invalid[0]["reasons"]