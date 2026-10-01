import json
from collections import Counter
import re

DATA_FILE = "data/processed/news_data.json"


def load_data():
    """Load processed news records from JSON."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def analyze_sources(records):
    """Count records by source."""

    source_counts = Counter(
        record.get("source", "")
        for record in records
        if record.get("source")
    )

    return dict(source_counts)


def analyze_categories(records):
    """Count records by category."""

    category_counts = Counter(
        record.get("category", "")
        for record in records
        if record.get("category")
    )

    return dict(category_counts)


def analyze_dates(records):
    """Count records by publication date."""

    date_counts = Counter()

    for record in records:
        published_at = record.get("published_at", "")

        if published_at:
            date = published_at[:10]
            date_counts[date] += 1

    return dict(date_counts)

def analyze_keywords(records, top_n=15):
    """Find frequent meaningful words and phrases."""

    stopwords = {
        "the", "a", "an", "and", "or", "but",
        "of", "to", "in", "on", "for", "with",
        "from", "by", "at", "as", "is", "are",
        "was", "were", "be", "been", "being",
        "this", "that", "these", "those",
        "it", "its", "into", "after", "over",
        "about", "their", "they", "them",
        "has", "have", "had", "will", "would",
        "can", "could", "may", "might",
        "more", "than", "also",
        "first", "one", "two", "three",
        "people", "during", "says", "said"
    }

    ignored_words = {
        "nasa",
        "wikipedia",
        "hacker",
        "news"
    }

    word_counts = Counter()
    phrase_counts = Counter()

    for record in records:

        text = (
            record.get("title", "")
            + " "
            + record.get("description", "")
        )

        words = re.findall(
            r"\b[a-zA-Z]{3,}\b",
            text.lower()
        )

        filtered_words = [
            word
            for word in words
            if word not in stopwords
            and word not in ignored_words
        ]

        # Single-word frequencies
        for word in filtered_words:
            word_counts[word] += 1

        # Two-word phrases
        for i in range(len(filtered_words) - 1):
            phrase = (
                filtered_words[i]
                + " "
                + filtered_words[i + 1]
            )

            phrase_counts[phrase] += 1

    # Combine words and phrases
    combined = []

    for word, count in word_counts.items():
        combined.append((word, count))

    for phrase, count in phrase_counts.items():
        combined.append((phrase, count))

    combined.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return combined[:top_n]

def analyze_keywords_by_source(records, top_n=10):
    """Find meaningful keywords and phrases for each source."""

    stopwords = {
        "the", "a", "an", "and", "or", "but",
        "of", "to", "in", "on", "for", "with",
        "from", "by", "at", "as", "is", "are",
        "was", "were", "be", "been", "being",
        "this", "that", "these", "those",
        "it", "its", "into", "after", "over",
        "about", "their", "they", "them",
        "has", "have", "had", "will", "would",
        "can", "could", "may", "might",
        "more", "than", "also",
        "first", "one", "two", "three",
        "people", "during", "says", "said"
    }

    ignored_words = {
        "nasa",
        "wikipedia",
        "hacker",
        "news"
    }

    source_counts = {}

    for record in records:

        source = record.get("source", "")

        if not source:
            continue

        if source not in source_counts:
            source_counts[source] = Counter()

        text = (
            record.get("title", "")
            + " "
            + record.get("description", "")
        )

        words = re.findall(
            r"\b[a-zA-Z]{3,}\b",
            text.lower()
        )

        filtered_words = [
            word
            for word in words
            if word not in stopwords
            and word not in ignored_words
        ]

        # Single words
        for word in filtered_words:
            source_counts[source][word] += 1

        # Two-word phrases
        for i in range(len(filtered_words) - 1):

            phrase = (
                filtered_words[i]
                + " "
                + filtered_words[i + 1]
            )

            source_counts[source][phrase] += 1

    result = {}

    for source, counts in source_counts.items():
        result[source] = counts.most_common(top_n)

    return result

def save_analysis(results):
    """Save trend analysis results to JSON."""

    output_file = "data/processed/trend_analysis.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nTrend analysis saved to {output_file}")

def main():

    print("Starting NewsPulse trend analysis...")

    records = load_data()

    print(f"\nTotal records loaded: {len(records)}")

    source_counts = analyze_sources(records)
    category_counts = analyze_categories(records)
    date_counts = analyze_dates(records)
    keyword_counts = analyze_keywords(records)
    source_keyword_counts = analyze_keywords_by_source(records)

    print("\nRecords by source:")

    for source, count in source_counts.items():
        print(f"{source}: {count}")

    print("\nRecords by category:")

    for category, count in category_counts.items():
        print(f"{category}: {count}")

    print("\nRecords by date:")

    for date, count in sorted(date_counts.items()):
        print(f"{date}: {count}")

    print("\nTop keywords:")

    for keyword, count in keyword_counts:
        print(f"{keyword}: {count}")

    print("\nTop keywords by source:")

    for source, keywords in source_keyword_counts.items():
        print(f"\n{source}:")

        for keyword, count in keywords:
            print(f"  {keyword}: {count}")

    analysis_results = {
        "total_records": len(records),
        "records_by_source": source_counts,
        "records_by_category": category_counts,
        "records_by_date": date_counts,
        "top_keywords": keyword_counts,
        "top_keywords_by_source": source_keyword_counts
    }

    save_analysis(analysis_results)
if __name__ == "__main__":
    main()