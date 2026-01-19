import re
import unicodedata
from models import Article
from config import (
    BLACKLIST, THEMES,
    SOURCE_SCORE, STRONG_KEYWORDS,
    MIN_SCORE, MAX_PER_THEME
)

def is_english(text: str) -> bool:
    english_markers = [
        "the", "and", "with", "from", "will",
        "said", "says", "after", "over"
    ]
    text = normalize(text)
    return sum(1 for w in english_markers if f" {w} " in f" {text} ") >= 2

def deduplicate_articles(articles):
    seen = set()
    unique = []

    for article in articles:
        key = article.url.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(article)

    return unique

def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def is_blacklisted(article: Article) -> bool:
    text = normalize(article.title + " " + article.summary)
    return any(word in text for word in BLACKLIST)


def tag_article(article: Article):
    text = normalize(article.title + " " + article.summary)

    if is_english(text):
        article.tags.append("en")
    else:
        article.tags.append("fr")

    for theme, keywords in THEMES.items():
        if any(k in text for k in keywords):
            article.tags.append(theme)


def score_article(article: Article):
    article.score += SOURCE_SCORE.get(article.source, 1)

    text = normalize(article.title + " " + article.summary)


    for word, value in STRONG_KEYWORDS.items():
        if word in text:
            article.score += value


def filter_articles(articles: list[Article]) -> dict[str, list[Article]]:
    
    articles = deduplicate_articles(articles)
    grouped = {}

    for article in articles:
        article.tags = []
        if is_blacklisted(article):
            continue

        tag_article(article)
        if not article.tags:
            continue

        score_article(article)
        if article.score < MIN_SCORE:
            continue

        for tag in article.tags:
            if tag in ("fr", "en"):
                continue
            grouped.setdefault(tag, []).append(article)

    for tag in grouped:
        grouped[tag] = sorted(
            grouped[tag],
            key=lambda a: a.score,
            reverse=True
        )[:MAX_PER_THEME]

    return grouped

from pathlib import Path

SENT_FILE = Path("data/sent_articles.txt")


def load_sent_urls() -> set[str]:
    if not SENT_FILE.exists():
        return set()
    return set(
        line.strip()
        for line in SENT_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )


def save_sent_urls(urls: set[str]):
    SENT_FILE.write_text(
        "\n".join(sorted(urls)),
        encoding="utf-8"
    )
