import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

from dotenv import load_dotenv
import markdown


# --------------------------------------------------
# Chargement des variables d'environnement
# --------------------------------------------------

load_dotenv()

EMAIL_FROM = os.getenv("NEWSLETTER_EMAIL")
EMAIL_PASSWORD = os.getenv("NEWSLETTER_EMAIL_PASSWORD")
EMAIL_TO = [
    email.strip()
    for email in os.getenv("NEWSLETTER_EMAIL_TO", EMAIL_FROM).split(",")
    if email.strip()
]

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))


# --------------------------------------------------
# Fonction principale
# --------------------------------------------------

def send_newsletter(md_path: str):
    """
    Envoie la newsletter Markdown par email (texte + HTML),
    avec titre, rendu journal et compatibilité mode clair / sombre.
    """

    if not EMAIL_FROM or not EMAIL_PASSWORD:
        raise RuntimeError("❌ Variables EMAIL manquantes (.env)")

    if not os.path.exists(md_path):
        raise FileNotFoundError(f"❌ Fichier introuvable : {md_path}")

    # --------------------------------------------------
    # Lecture du Markdown
    # --------------------------------------------------

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        print("⛔ Newsletter vide, envoi annulé")
        return

    # --------------------------------------------------
    # Création du message email
    # --------------------------------------------------

    today = date.today().strftime("%d/%m/%Y")
    today_human = date.today().strftime("%A %d %B %Y").capitalize()

    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(EMAIL_TO)
    msg["Subject"] = f"🗞️ Le Brief — {today}"

    # -------- Texte brut (fallback) --------

    text_part = MIMEText(content, "plain", "utf-8")
    msg.attach(text_part)

    # -------- HTML --------

    html_body = f"""
<h1 style="text-align:center; margin-bottom: 4px;">
  Le Brief
</h1>

<p style="text-align:center; color:#777; margin-top:0; margin-bottom:32px;">
  {today_human}
</p>

{markdown.markdown(content, extensions=["extra"])}
"""

    html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="color-scheme" content="light dark">
<meta name="supported-color-schemes" content="light dark">

<style>
  :root {{
    color-scheme: light dark;
  }}

  body {{
    font-family: Avenir, "Avenir Next", "Helvetica Neue", Helvetica, Arial, sans-serif;
    max-width: 700px;
    margin: auto;
    line-height: 1.6;
    color: #222;
  }}

  h1, h2, h3 {{
    color: #222;
  }}

  p {{
    color: #333;
  }}

  a {{
    color: #3366cc;
    text-decoration: none;
  }}

  strong {{
    color: #444;
  }}

  img {{
    display: block;
    width: 100%;
    max-height: 180px;
    object-fit: cover;
    border-radius: 6px;
    margin: 8px 0;
  }}

  /* 🌙 Dark mode — clients compatibles (Apple Mail, etc.) */
  @media (prefers-color-scheme: dark) {{
    body {{
      color: #e6e6e6;
    }}

    h1, h2, h3 {{
      color: #ffffff;
    }}

    p {{
      color: #dddddd;
    }}

    a {{
      color: #8ab4f8;
    }}

    strong {{
      color: #f0f0f0;
    }}
  }}
</style>
</head>

<body>
{html_body}
</body>
</html>
"""

    html_part = MIMEText(html, "html", "utf-8")
    msg.attach(html_part)

    # --------------------------------------------------
    # Envoi SMTP
    # --------------------------------------------------

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        print("📧 Destinataires utilisés :", EMAIL_TO)
    print("✅ Newsletter envoyée avec succès")


# --------------------------------------------------
# Exécution directe (debug local)
# --------------------------------------------------

if __name__ == "__main__":
    today = date.today().isoformat()
    md_file = f"output/brief_{today}.md"
    send_newsletter(md_file)