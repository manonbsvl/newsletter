from pathlib import Path
import sys
import yaml

from openai import OpenAI
from scored import render_scored_articles

from fetch import fetch_rss
from filter import filter_articles
from memory import load_sent_urls, save_sent_urls
from render import render
from fetched import render_fetched_articles
from summarize import summarize_article


# --------------------------------------------------
# Charger les sources par thème depuis config/sources.yaml
# --------------------------------------------------
def load_sources_by_theme() -> dict[str, list[str]]:
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
def main() -> str | None:
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
                print(f"⚠️ Erreur sur {url} : {e}")

    # ---------- LOG: articles fetchés (BRUTS) ----------
    render_fetched_articles(articles)

    # ---------- MEMORY: retirer les articles déjà envoyés ----------
    sent_urls = load_sent_urls()
    articles = [a for a in articles if a.url not in sent_urls]

    if not articles:
        print("ℹ️ Aucun nouvel article à envoyer aujourd’hui.")
        return None

    # ---------- FILTER ----------
    grouped_articles = filter_articles(articles)

    if not grouped_articles:
        print("ℹ️ Aucun article retenu après filtrage.")
        return None
    
    # ---------- LOG: articles scorés ----------
    render_scored_articles(grouped_articles)

    # ---------- SUMMARIZE ----------
    client = OpenAI()

    for theme_articles in grouped_articles.values():
        for article in theme_articles:
            article.summary = summarize_article(
                client,
                article,
                article.summary
            )

    # ---------- RENDER JOURNAL ----------
    md_path = render(grouped_articles)

    # ---------- MEMORY: marquer comme envoyés ----------
    new_urls = {
        article.url
        for articles in grouped_articles.values()
        for article in articles
    }
    sent_urls.update(new_urls)
    save_sent_urls(sent_urls)

    # ---------- FEEDBACK ----------
    print(f"📰 Articles fetchés : {len(articles)}")
    print(f"🧠 Rubriques publiées : {list(grouped_articles.keys())}")
    print(f"📄 Brief généré : {md_path}")

    return md_path


# --------------------------------------------------
# Lancement
# --------------------------------------------------
if __name__ == "__main__":
    send_email = "--send" in sys.argv

    md_path = main()

    if send_email and md_path:
        print(">>> Envoi de la newsletter")
        from send_mail import send_newsletter
        send_newsletter(md_path)
        print("✅ Newsletter envoyée")