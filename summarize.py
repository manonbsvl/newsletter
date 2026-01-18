from models import Article
from cache import get_cached_summary, save_summary

SUMMARY_PROMPT = """
Résume l'article suivant en 3 phrases maximum.
Va à l'essentiel. Ton neutre.

TITRE:
{title}

CONTENU:
{content}
"""

def summarize_article(client, article: Article, content: str) -> str:
    # 1️⃣ cache
    cached = get_cached_summary(article.url)
    if cached:
        return cached

    # 2️⃣ appel LLM
    prompt = SUMMARY_PROMPT.format(
        title=article.title,
        content=content[:6000]
    )

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    summary = response.output_text.strip()

    # 3️⃣ sauvegarde
    save_summary(article.url, summary)

    return summary
