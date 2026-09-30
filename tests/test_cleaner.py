from apps.processing.cleaner import clean_text, clean_record


def test_clean_text():

    text = "  Hamas 's   armed wing .  "

    result = clean_text(text)

    assert result == "Hamas's armed wing."


def test_clean_record():

    record = {
        "id": "123",
        "title": "  Example   News Title  ",
        "description": " Some   description. ",
        "source": " Wikipedia ",
        "published_at": "2026-09-29",
        "url": " https://example.com ",
        "category": " World News "
    }

    result = clean_record(record)

    assert result["title"] == "Example News Title"
    assert result["description"] == "Some description."
    assert result["source"] == "Wikipedia"
    assert result["published_at"] == "2026-09-29"
    assert result["url"] == "https://example.com"
    assert result["category"] == "World News"