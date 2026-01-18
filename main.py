from pathlib import Path
from datetime import datetime
import sys
import yaml

from openai import OpenAI

from fetch import fetch_rss
from filter import filter_articles
from render import render_markdown
from summarize import summarize_article


# --------------------------------------------------
# Charger les sources par thème depuis config/sources.yaml
# --------------------------------------------------
def load_sources_by_theme():
    base_dir = Path(__file__).resolve().parent
    sources_path = base_dir / "config" / "sources.yaml"

    with open(sources_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data["themes"]


# --------------------------------------------------
# Déduire le nom de la source depuis l’URL
# --------------------------------------------------
def infer_source_name(url: str) -> str:
    if "reuters" in url:
        return "Reuters"
    if "lemonde" in url:
        return "Le Monde"
    if "alternatives-economiques" in url:
        return "Alternatives Économiques"
    if "politico" in url:
        return "Politico"
    if "carbonbrief" in url:
        return "Carbon Brief"
    if "theconversation" in url:
        return "The Conversation"
    if "iea.org" in url:
        return "IEA"
    if "ft.com" in url:
        return "Financial Times"
    if "bbc" in url:
        return "BBC News"
    return "Source inconnue"


# --------------------------------------------------
# Pipeline principal
# --------------------------------------------------
def main() -> str:
    sources_by_theme = load_sources_by_theme()
    articles = []

    # ---------- FETCH ----------
    for theme, urls in sources_by_theme.items():
        for url in urls:
            try:
                source_name = infer_source_name(url)
                fetched = fetch_rss(url, source=source_name)

                for article in fetched:
                    article.tags.append(theme)

                articles.extend(fetched)

            except Exception as e:
                print(f"⚠️  Erreur sur {url} : {e}")

    # ---------- FILTER ----------
    grouped_articles = filter_articles(articles)

    # ---------- SUMMARIZE ----------
    client = OpenAI()

    for theme, theme_articles in grouped_articles.items():
        for article in theme_articles:
            article.summary = summarize_article(
                client,
                article,
                article.summary
            )

    # ---------- RENDER ----------
    md_path = render_markdown(grouped_articles)

    # ---------- FEEDBACK ----------
    print(f"📰 Articles fetchés : {len(articles)}")
    print(f"🧠 Thèmes : {list(grouped_articles.keys())}")

    return md_path


# --------------------------------------------------
# Lancement
# --------------------------------------------------
if __name__ == "__main__":
    send_email = "--send" in sys.argv

    md_path = main()

    if send_email:
        print(">>> DEBUG: calling send_newsletter()")
        from send_mail import send_newsletter
        send_newsletter(md_path)
        print("✅ Newsletter envoyée !")