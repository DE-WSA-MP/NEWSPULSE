import requests
from apps.processing.date_utils import convert_unix_timestamp


BASE_URL = "https://hacker-news.firebaseio.com/v0"

HEADERS = {
    "User-Agent": "NewsPulse/1.0 (Academic Project)"
}


def fetch_story_ids():
    url = f"{BASE_URL}/newstories.json"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


def fetch_story(story_id):
    url = f"{BASE_URL}/item/{story_id}.json"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


def get_new_stories(limit=50):

    story_ids = fetch_story_ids()

    stories = []

    for story_id in story_ids[:limit]:

        story = fetch_story(story_id)

        if not story:
            continue

        # Only keep actual stories
        if story.get("type") != "story":
            continue

        # Skip stories without a title
        if not story.get("title"):
            continue

        record = {
            "id": str(story.get("id")),
            "title": story.get("title", ""),
            "description": "",
            "source": "Hacker News",
            "published_at": convert_unix_timestamp(
                story.get("time")
            ),
            "url": story.get(
                "url",
                f"https://news.ycombinator.com/item?id={story.get('id')}"
            ),
            "content_type": "Story",
            "topic": ""
        }

        stories.append(record)

    return stories


def main():

    print("Fetching Hacker News stories...")

    stories = get_new_stories(limit=50)

    print(f"\nFound {len(stories)} stories.\n")

    for i, story in enumerate(stories, start=1):

        print(f"{i}. {story['title']}")
        print(f"   Source: {story['source']}")
        print(f"   Content Type: {story['content_type']}")
        print(f"   Topic: {story.get('topic', '')}")
        print(f"   Date: {story['published_at']}")
        print(f"   URL: {story['url']}")
        print()


if __name__ == "__main__":
    main()