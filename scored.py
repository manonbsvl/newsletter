from datetime import date
from pathlib import Path
from models import Article


def render_scored_articles(grouped: dict[str, list[Article]]) -> str:
    """
    Génère un fichier listant les articles retenus APRÈS filtrage,
    avec leur score.
    """

    lines = []

    today = date.today().strftime("%d %B %Y")
    lines.append(f"# Articles retenus (scorés) — {today}\n")

    for theme, articles in grouped.items():
        if theme in {"fr", "en"}:
            continue

        label = theme.replace("_", " ").capitalize()
        lines.append(f"## {label}\n")

        for a in articles:
            lines.append(
                f"- (score: {a.score}) **{a.source}** — {a.title}"
            )

        lines.append("")

    content = "\n".join(lines)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    path = output_dir / f"scored_{date.today().isoformat()}.md"
    path.write_text(content, encoding="utf-8")

    print(f"📊 Scored list générée : {path}")

    return str(path)