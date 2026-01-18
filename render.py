from models import Article

def render_markdown(grouped: dict[str, list[Article]]) -> str:
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

    return "\n".join(lines)
