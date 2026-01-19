from datetime import date
from models import Article
from pathlib import Path


THEME_ORDER = [
    "economie",
    "politique",
    "industrie",
    "climat_environnement",
]

THEME_LABELS = {
    "economie": "💼 Économie",
    "politique": "🏛️ Politique",
    "industrie": "🏭 Industrie",
    "climat_environnement": "🌍 Climat & Environnement",
}


def render_markdown(grouped: dict[str, list[Article]]) -> str:
    """
    Génère un rendu type journal, écrit le Markdown dans output/,
    et retourne le chemin du fichier.
    """

    lines: list[str] = []

    # 🗞️ Titre du journal
    today = date.today().strftime("%d %B %Y")
    lines.append(f"# 🗞️ Le Brief — {today}\n")

    # Parcours des rubriques dans un ordre fixe
    for theme in THEME_ORDER:
        articles = grouped.get(theme)
        if not articles:
            continue

        label = THEME_LABELS.get(theme, theme.replace("_", " ").title())
        lines.append(f"## {label}\n")

        for a in articles:
            # Image si disponible
            if getattr(a, "image_url", None):
                lines.append(
                    f'<img src="{a.image_url}" '
                    f'style="width:100%; max-height:280px; '
                    f'object-fit:cover; border-radius:6px; margin:12px 0;" />'
                )

            # Source
            lines.append(f"**{a.source}**")

            # Titre
            lines.append(f"### [{a.title}]({a.url})")

            # Résumé
            if a.summary:
                lines.append(f"{a.summary}")

            lines.append("")  # espace entre articles

        lines.append("---\n")  # séparation entre rubriques

    content = "\n".join(lines)

    # 📁 Écriture du fichier
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    path = output_dir / f"brief_{date.today().isoformat()}.md"
    path.write_text(content, encoding="utf-8")

    print(f"✅ Brief généré : {path}")

    return str(path)
