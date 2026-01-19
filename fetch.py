import feedparser
from models import Article
from datetime import datetime


def parse_date(entry) -> datetime | None:
    """
    Extrait une date depuis un entry RSS si disponible.
    """
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6])

    if hasattr(entry, "updated_parsed") and entry.updated_parsed:
        return datetime(*entry.updated_parsed[:6])

    return None


def extract_image(entry) -> str | None:
    """
    Extrait une image depuis un entry RSS si disponible.
    Priorité :
    1. media:content
    2. media:thumbnail
    3. enclosure image
    """
    # media:content
    if hasattr(entry, "media_content"):
        for media in entry.media_content:
            url = media.get("url")
            if url:
                return url

    # media:thumbnail
    if hasattr(entry, "media_thumbnail"):
        for media in entry.media_thumbnail:
            url = media.get("url")
            if url:
                return url

    # enclosure
    if hasattr(entry, "enclosures"):
        for enc in entry.enclosures:
            if enc.get("type", "").startswith("image/"):
                return enc.get("href")

    return None


def fetch_rss(url: str, source: str) -> list[Article]:
    feed = feedparser.parse(url)
    articles: list[Article] = []

    for entry in feed.entries:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()

        if not title or not link:
            continue

        summary = entry.get("summary", "") or entry.get("description", "")

        article = Article(
            source=source,
            title=title,
            summary=summary,
            url=link,
            published_at=parse_date(entry),
            tags=[],
            score=0,
            image_url=extract_image(entry),
        )

        articles.append(article)

    return articles