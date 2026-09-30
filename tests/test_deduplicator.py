from apps.processing.deduplicator import deduplicate_records


def test_remove_duplicate_records():

    records = [
        {
            "id": "1",
            "title": "First News",
            "source": "NASA"
        },
        {
            "id": "2",
            "title": "Second News",
            "source": "Wikipedia"
        },
        {
            "id": "1",
            "title": "First News",
            "source": "NASA"
        }
    ]

    result = deduplicate_records(records)

    assert len(result) == 2
    assert result[0]["id"] == "1"
    assert result[1]["id"] == "2"


def test_no_duplicates():

    records = [
        {
            "id": "1",
            "title": "First News",
            "source": "NASA"
        },
        {
            "id": "2",
            "title": "Second News",
            "source": "Wikipedia"
        }
    ]

    result = deduplicate_records(records)

    assert len(result) == 2