import feedparser
from models import Article
from datetime import datetime

def fetch_rss(url: str, source: str) -> list[Article]:
    feed = feedparser.parse(url)
    articles = []

    for entry in feed.entries:
        articles.append(
            Article(
                source=source,
                title=entry.get("title", ""),
                summary=entry.get("summary", ""),
                url=entry.get("link", ""),
                published_at=datetime(*entry.published_parsed[:6])
                if hasattr(entry, "published_parsed") else None
            )
        )

    return articles
