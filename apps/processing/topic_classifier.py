import re


TOPIC_KEYWORDS = {
    "Artificial Intelligence": [
        "artificial intelligence",
        "ai",
        "llm",
        "large language model",
        "machine learning",
        "deep learning",
        "neural network",
        "generative ai",
        "generative",
        "language model",
        "ai agent",
        "agents"
    ],

    "Space": [
        "nasa",
        "space",
        "astronaut",
        "rocket",
        "launch",
        "orbit",
        "spacecraft",
        "spacex",
        "satellite",
        "moon",
        "mars",
        "crew",
        "mission",
        "iss",
        "space station"
    ],

    "Software Development": [
        "programming",
        "programmer",
        "developer",
        "software development",
        "coding",
        "github",
        "git",
        "python",
        "javascript",
        "typescript",
        "rust",
        "java",
        "api",
        "framework",
        "library",
        "open source"
    ],

    "Web": [
        "website",
        "web",
        "browser",
        "html",
        "css",
        "domain",
        "internet",
        "frontend",
        "backend"
    ],

    "Cybersecurity": [
        "cybersecurity",
        "cyber security",
        "security",
        "malware",
        "ransomware",
        "phishing",
        "vulnerability",
        "exploit",
        "privacy",
        "encryption"
    ],

    "Hardware": [
        "hardware",
        "cpu",
        "gpu",
        "processor",
        "chip",
        "semiconductor",
        "computer",
        "laptop",
        "device",
        "microprocessor"
    ],

    "Databases": [
        "database",
        "sql",
        "postgresql",
        "mysql",
        "mongodb",
        "sqlite",
        "redis",
        "data warehouse"
    ],

    "Business and Finance": [
        "business",
        "startup",
        "company",
        "funding",
        "investment",
        "investor",
        "finance",
        "financial",
        "market",
        "revenue",
        "stock",
        "bank"
    ],

    "Science": [
        "science",
        "research",
        "study",
        "scientist",
        "experiment",
        "physics",
        "chemistry",
        "biology",
        "climate",
        "weather"
    ],

    "Sports": [
        "football",
        "soccer",
        "cricket",
        "basketball",
        "baseball",
        "tennis",
        "nfl",
        "nba",
        "athlete",
        "sports"
    ]
}


def normalize_text(text):
    """Normalize text before topic matching."""

    if not text:
        return ""

    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def detect_topic(title="", description=""):

    text = normalize_text(
        f"{title} {description}"
    )

    if not text:
        return "Other"

    topic_scores = {}

    for topic, keywords in TOPIC_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        if score > 0:
            topic_scores[topic] = score

    if not topic_scores:
        return "Other"

    # Select the topic with the highest score.
    return max(
        topic_scores,
        key=topic_scores.get
    )


def add_topics(records):
    """Add a topic to every record."""

    processed_records = []

    for record in records:

        updated_record = record.copy()

        # Keep an already extracted Wikipedia topic.
        existing_topic = str(
            updated_record.get("topic", "")
        ).strip()

        if existing_topic:
            updated_record["topic"] = existing_topic

        else:
            updated_record["topic"] = detect_topic(
                updated_record.get("title", ""),
                updated_record.get("description", "")
            )

        processed_records.append(
            updated_record
        )

    return processed_records