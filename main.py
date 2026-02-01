from pathlib import Path
import sys
import yaml
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

from openai import OpenAI
from scored import render_scored_articles

from fetch import fetch_rss
from filter import filter_articles
from memory import load_sent_urls, save_sent_urls
from render import render
from fetched import render_fetched_articles
from summarize import summarize_article
from notion import send_articles_to_notion, check_notion_connection


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
def main(to_notion: bool = False, skip_summary: bool = False) -> dict | str | None:
    """
    Pipeline RSS → Filtrage → (Résumé) → Notion ou Markdown

    Args:
        to_notion: Si True, envoie vers Notion. Sinon, génère un Markdown.
        skip_summary: Si True, saute le résumé OpenAI (plus rapide).

    Returns:
        - dict avec stats Notion si to_notion=True
        - chemin du fichier .md sinon
        - None si aucun article
    """
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
        print("ℹ️ Aucun nouvel article à envoyer aujourd'hui.")
        return None

    # ---------- FILTER ----------
    grouped_articles = filter_articles(articles)

    if not grouped_articles:
        print("ℹ️ Aucun article retenu après filtrage.")
        return None

    # ---------- LOG: articles scorés ----------
    render_scored_articles(grouped_articles)

    # ---------- SUMMARIZE (optionnel) ----------
    if not skip_summary:
        client = OpenAI()
        for theme_articles in grouped_articles.values():
            for article in theme_articles:
                article.summary = summarize_article(
                    client,
                    article,
                    article.summary
                )

    # ---------- NOTION ou MARKDOWN ----------
    if to_notion:
        # Vérifier la connexion
        if not check_notion_connection():
            print("❌ Connexion Notion échouée. Vérifie .env")
            return None

        # Dédupliquer : un article peut être dans plusieurs thèmes
        # On fusionne tous les thèmes dans les tags de l'article
        unique_articles = {}  # url -> (article, [themes])
        for theme, theme_articles in grouped_articles.items():
            for article in theme_articles:
                if article.url not in unique_articles:
                    unique_articles[article.url] = (article, [theme])
                else:
                    # Article déjà vu, ajouter le thème
                    unique_articles[article.url][1].append(theme)

        # Fusionner les thèmes dans les tags de chaque article
        deduplicated = []
        for url, (article, themes) in unique_articles.items():
            # Ajouter tous les thèmes aux tags (sans doublons)
            for theme in themes:
                if theme not in article.tags:
                    article.tags.append(theme)
            deduplicated.append((article, themes[0]))  # On garde le 1er thème comme principal

        print(f"\n📊 {len(deduplicated)} articles uniques (dédupliqués)")

        # Envoyer vers Notion
        from notion import send_to_notion
        total_stats = {"success": 0, "failed": 0}
        for article, main_theme in deduplicated:
            result = send_to_notion(article, main_theme)
            if result:
                total_stats["success"] += 1
            else:
                total_stats["failed"] += 1

        # Marquer comme envoyés
        new_urls = {url for url in unique_articles.keys()}
        sent_urls.update(new_urls)
        save_sent_urls(sent_urls)

        # Feedback
        print(f"\n✅ Notion: {total_stats['success']} ajoutés, {total_stats['failed']} échoués")
        print(f"🧠 Thèmes: {list(grouped_articles.keys())}")

        return total_stats

    else:
        # Mode classique: générer Markdown
        md_path = render(grouped_articles)

        new_urls = {
            article.url
            for articles in grouped_articles.values()
            for article in articles
        }
        sent_urls.update(new_urls)
        save_sent_urls(sent_urls)

        print(f"📰 Articles fetchés : {len(articles)}")
        print(f"🧠 Rubriques publiées : {list(grouped_articles.keys())}")
        print(f"📄 Brief généré : {md_path}")

        return md_path


# --------------------------------------------------
# Lancement
# --------------------------------------------------
if __name__ == "__main__":
    to_notion = "--notion" in sys.argv
    send_email = "--send" in sys.argv
    skip_summary = "--no-summary" in sys.argv

    # Mode Notion (par défaut maintenant)
    if to_notion or (not send_email):
        print("🚀 Mode Notion activé")
        result = main(to_notion=True, skip_summary=skip_summary)
        if result:
            print(f"✅ Terminé: {result}")

    # Mode email (legacy)
    elif send_email:
        print("📧 Mode Email (legacy)")
        md_path = main(to_notion=False, skip_summary=skip_summary)
        if md_path:
            from send_mail import send_newsletter
            send_newsletter(md_path)
            print("✅ Newsletter envoyée")