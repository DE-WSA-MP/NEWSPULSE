import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


NASA_URL = "https://www.nasa.gov/news/recently-published/"

HEADERS = {
    "User-Agent": "NewsPulse/1.0 (Academic Project)"
}


def fetch_nasa_page():
    """Fetch the NASA Recently Published page."""

    response = requests.get(
        NASA_URL,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    return response.text


def extract_date_from_url(url):

    if not url:
        return ""

    match = re.search(
        r"/(20\d{2})/(\d{2})/(\d{2})/",
        url
    )

    if match:
        year, month, day = match.groups()

        try:
            date_object = datetime(
                int(year),
                int(month),
                int(day)
            )

            return date_object.strftime("%Y-%m-%d")

        except ValueError:
            return ""

    return ""


def parse_nasa_articles(html):
    """Extract article information from NASA's Recently Published page."""

    soup = BeautifulSoup(html, "html.parser")

    # Find the container containing the Recently Published articles
    article_container = soup.select_one(
        "div.hds-content-items.hds-content-items-list"
    )

    if article_container is None:
        print("Could not find NASA article container.")
        return []

    # Each article is represented by one hds-content-item
    article_cards = article_container.select(
        "div.hds-content-item"
    )

    articles = []

    for card in article_cards:

        # Title and URL

        title_link = card.select_one(
            "a.hds-content-item-heading"
        )

        if title_link is None:
            continue

        title = title_link.get_text(
            " ",
            strip=True
        )

        url = title_link.get("href")

        # Description
        description_element = card.select_one(
            "p.margin-top-0.margin-bottom-1"
        )

        description = ""

        if description_element:
            description = description_element.get_text(
                " ",
                strip=True
            )

        # Content type
        content_type = ""

        content_type_element = card.select_one(
            ".color-carbon-60 span"
        )

        if content_type_element:
            content_type = content_type_element.get_text(
                " ",
                strip=True
            )

        # Publication date

        published_at = ""

        # First try to extract the date from the page.
        date_element = card.select_one(
            "div.color-carbon-60.margin-bottom-1.margin-top-1"
        )

        if date_element:
            published_at = date_element.get_text(
                " ",
                strip=True
            )

        # If the page does not contain a visible date,
        # extract it from the NASA article URL.
        if not published_at:
            published_at = extract_date_from_url(url)

        # Store article
        article = {
            "id": url,
            "title": title,
            "description": description,
            "source": "NASA",
            "published_at": published_at,
            "url": url,
            "content_type": content_type,
            "topic": ""
        }

        articles.append(article)

    return articles


def main():

    print("Fetching NASA Recently Published page...")

    html = fetch_nasa_page()

    print("Page fetched successfully.")
    print(f"Downloaded {len(html):,} characters.")

    articles = parse_nasa_articles(html)

    print(f"\nFound {len(articles)} NASA articles.\n")

    for i, article in enumerate(
        articles[:10],
        start=1
    ):

        print(f"{i}. {article['title']}")
        print(f"   Content Type: {article['content_type']}")
        print(f"   Topic: {article.get('topic', '')}")
        print(f"   Date: {article['published_at']}")
        print(f"   URL: {article['url']}")
        print(
            f"   Description: "
            f"{article['description'][:150]}"
        )
        print()


if __name__ == "__main__":
    main()

