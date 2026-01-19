from datetime import date
from pathlib import Path
from models import Article


def render_fetched_articles(articles: list[Article]) -> str:
    """
    Génère un fichier Markdown listant TOUS les articles fetchés
    avec date, source, catégories et titre.
    """

    lines = []

    today = date.today().strftime("%d %B %Y")
    lines.append(f"# Articles fetchés — {today}\n")

    for a in articles:
        # --- Date ---
        published = getattr(a, "published", None)
        if published:
            try:
                published_str = published.strftime("%Y-%m-%d")
            except Exception:
                published_str = str(published)
        else:
            published_str = "?"

        # --- Catégories ---
        categories = [
            tag.replace("_", " ").capitalize()
            for tag in getattr(a, "tags", [])
            if tag not in {"fr", "en"}
        ]

        categories_str = ", ".join(categories) if categories else "—"

        # --- Ligne finale ---
        lines.append(
            f"- {published_str} — **{a.source}** — "
            f"[{categories_str}] {a.title}"
        )

    content = "\n".join(lines)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    path = output_dir / f"fetched_{date.today().isoformat()}.md"
    path.write_text(content, encoding="utf-8")

    print(f"📄 Fetched list générée : {path}")

    return str(path)