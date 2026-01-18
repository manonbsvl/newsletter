from datetime import date
from models import Article
import os


def render_markdown(grouped: dict[str, list[Article]]) -> str:
    """
    Génère le Markdown, l'écrit dans output/, et retourne le chemin du fichier.
    """
    lines = []
    EXCLUDED_TAGS = {"fr", "en"}

    for theme, articles in grouped.items():
        if theme in EXCLUDED_TAGS:
            continue

        lines.append(f"## {theme.replace('_', ' ').capitalize()}\n")

        for a in articles:
            lines.append(
                f"- **{a.source}** — [{a.title}]({a.url})\n"
                f"  > {a.summary}"
            )

        lines.append("")

    content = "\n".join(lines)

    # 🔹 Chemin du fichier
    os.makedirs("output", exist_ok=True)
    path = f"output/brief_{date.today().isoformat()}.md"

    # 🔹 Écriture du fichier
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Brief généré : {path}")

    # 🔹 RETOUR CRUCIAL
    return path