from apps.scrapers.nasa_scraper import (
    fetch_nasa_page,
    parse_nasa_articles
)
from apps.scrapers.wikipedia_scraper import (
    fetch_wikipedia_page,
    parse_wikipedia_events
)
from apps.api.hackernews_api import get_new_stories
from apps.processing.cleaner import clean_records
from apps.processing.validator import validate_records
from apps.processing.deduplicator import deduplicate_records
from apps.processing.integrator import integrate_records
from apps.processing.data_writer import save_json
from apps.processing.topic_classifier import add_topics

def main():

    print("Starting NewsPulse pipeline...")

    # NASA

    print("\n[1] Fetching NASA data...")

    html = fetch_nasa_page()

    nasa_records = parse_nasa_articles(html)

    print(
        f"NASA records acquired: {len(nasa_records)}"
    )

    print("\nNASA sample records:\n")

    for i, record in enumerate(
        nasa_records[:5],
        start=1
    ):
        print(f"{i}. {record['title']}")
        print(f"   Source: {record['source']}")
        print(f"   Content Type: {record['content_type']}")
        print(f"   Topic: {record.get('topic', '')}")
        print(f"   Date: {record['published_at']}")
        print(f"   URL: {record['url']}")
        print()

    # Wikipedia

    print("\n[2] Fetching Wikipedia data...")

    wikipedia_html = fetch_wikipedia_page()

    wikipedia_records = parse_wikipedia_events(
        wikipedia_html
    )

    print(
        f"Wikipedia records acquired: "
        f"{len(wikipedia_records)}"
    )

    print("\nWikipedia sample records:\n")

    for i, record in enumerate(
        wikipedia_records[:5],
        start=1
    ):
        print(f"{i}. {record['title']}")
        print(f"   Source: {record['source']}")
        print(f"   Content Type: {record['content_type']}")
        print(f"   Topic: {record.get('topic', '')}")
        print(f"   Date: {record['published_at']}")
        print(f"   URL: {record['url']}")
        print()

    # Hacker News

    print("\n[3] Fetching Hacker News data...")

    hackernews_records = get_new_stories(
        limit=50
    )

    print(
        f"Hacker News records acquired: "
        f"{len(hackernews_records)}"
    )

    print("\nHacker News sample records:\n")

    for i, record in enumerate(
        hackernews_records[:5],
        start=1
    ):
        print(f"{i}. {record['title']}")
        print(f"   Source: {record['source']}")
        print(f"   Content Type: {record['content_type']}")
        print(f"   Topic: {record.get('topic', '')}")
        print(f"   Date: {record['published_at']}")
        print(f"   URL: {record['url']}")
        print()

    # Combine all acquired records

    print("\n[4] Combining acquired records...")

    all_records = (
        nasa_records
        + wikipedia_records
        + hackernews_records
    )

    print(
        f"Total raw records: {len(all_records)}"
    )

    # Cleaning

    print("\n[5] Cleaning records...")

    cleaned_records = clean_records(
        all_records
    )

    print(
        f"Records after cleaning: "
        f"{len(cleaned_records)}"
    )

    # Topic Classification

    print("\n[5.5] Detecting topics...")

    topic_records = add_topics(
        cleaned_records
    )

    print(
        f"Topics assigned to "
        f"{len(topic_records)} records"
    )

    # Validation

    print("\n[6] Validating records...")

    valid_records, invalid_records = validate_records(
        topic_records
    )

    print(
        f"Valid records: {len(valid_records)}"
    )

    print(
        f"Invalid records: {len(invalid_records)}"
    )

    if invalid_records:

        print("\nInvalid records:")

        for item in invalid_records:

            record = item["record"]
            reasons = item["reasons"]

            print(
                f"\nTitle: {record.get('title', '')}"
            )

            print(
                f"Source: {record.get('source', '')}"
            )

            print(
                f"URL: {record.get('url', '')}"
            )

            print(
                f"Reasons: {', '.join(reasons)}"
            )

    else:

        print("No invalid records.")

    # Deduplication

    print("\n[7] Removing duplicate records...")

    deduplicated_records = deduplicate_records(
        valid_records
    )

    print(
        f"Records after deduplication: "
        f"{len(deduplicated_records)}"
    )

    # Integration

    print("\n[8] Integrating final records...")

    integrated_records = integrate_records(
        deduplicated_records
    )

    print(
        f"Final integrated records: "
        f"{len(integrated_records)}"
    )

    # Source summary

    print("\nSource summary:")

    nasa_count = sum(
        1
        for record in integrated_records
        if record["source"] == "NASA"
    )

    wikipedia_count = sum(
        1
        for record in integrated_records
        if record["source"] == "Wikipedia"
    )

    hackernews_count = sum(
        1
        for record in integrated_records
        if record["source"] == "Hacker News"
    )

    print(f"NASA: {nasa_count}")
    print(f"Wikipedia: {wikipedia_count}")
    print(f"Hacker News: {hackernews_count}")

    # Save processed dataset

    output_file = "data/processed/news_data.json"

    save_json(
        integrated_records,
        output_file
    )

    print(
        f"\nProcessed dataset saved to: {output_file}"
    )


if __name__ == "__main__":
    main()