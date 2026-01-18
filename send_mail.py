import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

from dotenv import load_dotenv
import markdown

# -------------------------------------------------------------------
# Chargement des variables d'environnement
# -------------------------------------------------------------------

load_dotenv()

EMAIL_FROM = os.getenv("NEWSLETTER_EMAIL")
EMAIL_PASSWORD = os.getenv("NEWSLETTER_EMAIL_PASSWORD")
EMAIL_TO = os.getenv("NEWSLETTER_EMAIL_TO", EMAIL_FROM)

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# -------------------------------------------------------------------
# Fonction principale
# -------------------------------------------------------------------

def send_newsletter(md_path: str):
    """
    Envoie la newsletter Markdown par email (texte + HTML)
    """

    if not EMAIL_FROM or not EMAIL_PASSWORD:
        raise RuntimeError("❌ Variables EMAIL manquantes (.env)")

    if not os.path.exists(md_path):
        raise FileNotFoundError(f"❌ Fichier introuvable : {md_path}")

    # ----------------------------------------------------------------
    # Lecture du Markdown
    # ----------------------------------------------------------------

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        print("⛔ Newsletter vide, envoi annulé")
        return

    # ----------------------------------------------------------------
    # Création du message email
    # ----------------------------------------------------------------

    today = date.today().strftime("%d/%m/%Y")

    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = f"🗞️ Newsletter – {today}"

    # Version texte brut (fallback)
    text_part = MIMEText(content, "plain", "utf-8")
    msg.attach(text_part)

    # Version HTML (principale)
    html = markdown.markdown(
        content,
        extensions=["extra"]
    )

    html_part = MIMEText(html, "html", "utf-8")
    msg.attach(html_part)

    # ----------------------------------------------------------------
    # Envoi SMTP
    # ----------------------------------------------------------------

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

    print("✅ Newsletter envoyée avec succès")


# -------------------------------------------------------------------
# Mode exécution directe (debug)
# -------------------------------------------------------------------

if __name__ == "__main__":
    today = date.today().isoformat()
    md_file = f"output/brief_{today}.md"
    send_newsletter(md_file)
