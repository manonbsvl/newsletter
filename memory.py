from pathlib import Path

# Fichier qui contient les URLs déjà envoyées
SENT_FILE = Path("data/sent_articles.txt")


def load_sent_urls() -> set[str]:
    """
    Charge les URLs des articles déjà envoyés.
    """
    if not SENT_FILE.exists():
        return set()

    return {
        line.strip()
        for line in SENT_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def save_sent_urls(urls: set[str]):
    """
    Sauvegarde les URLs envoyées (écrase le fichier).
    """
    SENT_FILE.parent.mkdir(exist_ok=True)

    SENT_FILE.write_text(
        "\n".join(sorted(urls)),
        encoding="utf-8"
    )