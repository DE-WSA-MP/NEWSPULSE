from apps.processing.integrator import integrate_records


def test_integrate_records():

    nasa_records = [
        {
            "id": "nasa-1",
            "title": "NASA News",
            "source": "NASA"
        }
    ]

    wikipedia_records = [
        {
            "id": "wiki-1",
            "title": "Wikipedia News",
            "source": "Wikipedia"
        }
    ]

    hackernews_records = [
        {
            "id": "hn-1",
            "title": "Hacker News",
            "source": "Hacker News"
        }
    ]

    result = integrate_records(
        nasa_records,
        wikipedia_records,
        hackernews_records
    )

    assert len(result) == 3

    assert result[0]["source"] == "NASA"
    assert result[1]["source"] == "Wikipedia"
    assert result[2]["source"] == "Hacker News"


def test_empty_source():

    nasa_records = [
        {
            "id": "nasa-1",
            "title": "NASA News",
            "source": "NASA"
        }
    ]

    result = integrate_records(
        nasa_records,
        [],
        []
    )

    assert len(result) == 1
    assert result[0]["source"] == "NASA"