from pathlib import Path
from datetime import datetime
import yaml
from summarize import summarize_article
from openai import OpenAI

from fetch import fetch_rss
from filter import filter_articles
from render import render_markdown


# --------------------------------------------------
# Charger les sources par thème depuis config/sources.yaml
# --------------------------------------------------
def load_sources_by_theme():
    base_dir = Path(__file__).resolve().parent
    sources_path = base_dir / "config" / "sources.yaml"

    with open(sources_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data["themes"]

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
# Point d’entrée principal
# --------------------------------------------------
def main():
    sources_by_theme = load_sources_by_theme()

    articles = []

    # --- FETCH ---
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


    # --- FILTER ---
    grouped_articles = filter_articles(articles)
    client = OpenAI()

    for theme, articles in grouped_articles.items():
        for article in articles:
            article.summary = summarize_article(
                client,
                article,
                article.summary  # ou contenu complet si tu l’as
            )


    # --- RENDER ---
    markdown_output = render_markdown(grouped_articles)

    # --- EXPORT ---
    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)

    filename = datetime.now().strftime("brief_%Y-%m-%d.md")
    output_path = output_dir / filename
    output_path.write_text(markdown_output, encoding="utf-8")

    # --- FEEDBACK ---
    print(f"✅ Brief généré : {output_path}")
    print(f"📰 Articles fetchés : {len(articles)}")
    print(f"🧠 Thèmes : {list(sources_by_theme.keys())}")


# --------------------------------------------------
# Lancement
# --------------------------------------------------
if __name__ == "__main__":
    main()
