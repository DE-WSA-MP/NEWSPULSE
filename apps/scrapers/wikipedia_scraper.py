import requests
from bs4 import BeautifulSoup


WIKIPEDIA_URL = (
    "https://en.wikipedia.org/wiki/"
    "Portal:Current_events/"
    "2026_September_29"
)

HEADERS = {
    "User-Agent": "NewsPulse/1.0 (Academic Project)"
}


def fetch_wikipedia_page():
    response = requests.get(
        WIKIPEDIA_URL,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    return response.text


def parse_wikipedia_events(html):
    soup = BeautifulSoup(html, "html.parser")

    content = soup.select_one("#mw-content-text")

    if content is None:
        print("Could not find Wikipedia main content.")
        return []

    events = []

    lists = content.find_all("ul")

    for ul in lists:

        # Skip Wikipedia's navigation list
        if "current-events-navbar" in (ul.get("class") or []):
            continue

        # Only process top-level lists
        if ul.find_parent("li"):
            continue

        items = ul.find_all("li", recursive=False)

        for item in items:

            # -------------------------------------------------
            # Find the actual event content
            # -------------------------------------------------

            nested_list = item.find("ul", recursive=False)

            if nested_list is not None:

                # Some Wikipedia entries have a topic/category
                # followed by a nested list containing the event.
                event_item = nested_list.find(
                    "li",
                    recursive=False
                )

                if event_item is None:
                    continue

            else:

                # Some entries contain the event directly
                # in the outer <li>.
                event_item = item


            # -------------------------------------------------
            # Get category/topic
            # -------------------------------------------------

            category_link = item.find(
                "a",
                recursive=False
            )

            category = ""

            if category_link:
                category = category_link.get_text(
                    " ",
                    strip=True
                )


            # -------------------------------------------------
            # Collect external source links
            # -------------------------------------------------

            source_links = []

            for link in event_item.select(
                "a.external.text[href]"
            ):

                href = link.get("href")

                if href and href not in source_links:
                    source_links.append(href)


            # -------------------------------------------------
            # Create a copy for text cleaning
            # -------------------------------------------------

            event_copy = BeautifulSoup(
                str(event_item),
                "html.parser"
            ).find("li")


            # Remove source labels such as:
            # (Reuters)
            # (AFP via RFI)
            #
            # The actual URLs are already stored in
            # source_links.
            for link in event_copy.select(
                "a.external.text[href]"
            ):
                link.extract()


            # -------------------------------------------------
            # Extract complete event text
            # -------------------------------------------------

            event_text = event_copy.get_text(
                " ",
                strip=True
            )

            if not event_text:
                continue


            # -------------------------------------------------
            # Determine event URL
            # -------------------------------------------------

            if source_links:
                event_url = source_links[0]

            else:
                event_url = WIKIPEDIA_URL


            # -------------------------------------------------
            # Create common NewsPulse record
            # -------------------------------------------------

            event = {
                "id": event_url,
                "title": event_text,
                "description": event_text,
                "source": "Wikipedia",
                "published_at": "2026-09-29",
                "url": event_url,
                "content_type": "Current Event",
                "topic": category,
                "source_links": source_links
            }

            events.append(event)

    return events


def main():

    print("Fetching Wikipedia Current Events page...")

    html = fetch_wikipedia_page()

    print("Page fetched successfully.")
    print(f"Downloaded {len(html):,} characters.")

    events = parse_wikipedia_events(html)

    print(f"\nFound {len(events)} Wikipedia events.\n")

    for i, event in enumerate(events[:15], start=1):

        print(f"{i}. {event['title'][:200]}")
        print(f"   Category: {event['category']}")
        print(f"   Date: {event['published_at']}")
        print(f"   URL: {event['url']}")
        print()


if __name__ == "__main__":
    main()