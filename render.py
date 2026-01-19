from datetime import date
from models import Article
import os
from textwrap import shorten


def render(grouped: dict[str, list[Article]]) -> str:
    """
    Génère un Markdown avec HTML intégré (layout journal),
    écrit le fichier dans output/ et retourne le chemin.
    """

    EXCLUDED_TAGS = {"fr", "en"}
    lines = []

    for theme, articles in grouped.items():
        if theme in EXCLUDED_TAGS:
            continue

        # Titre de section
        lines.append(f"## {theme.replace('_', ' ').capitalize()}\n")

        # On limite à 3 articles par catégorie
        articles = articles[:3]

        # Début table (email-safe)
        lines.append('<table width="100%" cellpadding="0" cellspacing="0">')
        lines.append("<tr>")

        for article in articles:
            summary = article.summary or ""
            image_html = ""
            if article.image_url:
                image_html = f"""
<img src="{article.image_url}"
     style="width:100%; max-height:160px; object-fit:cover;
            border-radius:6px; margin-bottom:8px;" />
"""

            lines.append(
                f"""
<td width="33%" valign="top" style="padding: 8px;">
  {image_html}

  <p style="margin: 4px 0;">
    <a href="{article.url}">
      <strong>{article.title}</strong>
    </a>
  </p>

  <p style="font-size: 12px; color: #666; margin: 0;">
    {article.source}
  </p>

  <p style="font-size: 14px; margin-top: 6px;">
    {summary}
  </p>
</td>
"""
            )

        lines.append("</tr>")
        lines.append("</table>\n")

    content = "\n".join(lines)

    # Écriture fichier
    os.makedirs("output", exist_ok=True)
    path = f"output/brief_{date.today().isoformat()}.md"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Brief généré : {path}")
    return path