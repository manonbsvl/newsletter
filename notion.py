"""
notion.py — Intégration Notion pour la newsletter RSS
Envoie les articles collectés vers la base de données "Sources" dans Notion.
"""

import os
import requests
from datetime import datetime
from typing import List, Optional
from models import Article

# Configuration Notion
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")  # ID de ta base "Sources"

NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_VERSION = "2022-06-28"


def get_headers() -> dict:
    """Headers pour l'API Notion."""
    return {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }


def score_to_priority(score: int) -> str:
    """Convertit le score en niveau de priorité Notion."""
    if score >= 8:
        return "🔴 Urgent"
    elif score >= 5:
        return "🟠 Cette semaine"
    elif score >= 3:
        return "🟡 Ce mois"
    else:
        return "🟢 Veille longue"


def theme_to_thematique(theme: str) -> str:
    """Mappe les thèmes RSS vers les thématiques Notion."""
    mapping = {
        "economie": "Économie",
        "politique": "Géopolitique",
        "climat_environnement": "Environnement",
        "automobile_industrie": "Industrie Auto",
        "automobile_environnement": "Électrification",
    }
    return mapping.get(theme, theme.replace("_", " ").title())


def source_to_editeur(source: str) -> str:
    """Normalise le nom du média pour Notion."""
    # Mapping des sources connues
    mapping = {
        "alternatives-economiques": "Alternatives Économiques",
        "politico": "Politico",
        "bbc": "BBC",
        "lesechos": "Les Échos",
        "theconversation": "The Conversation",
        "iea": "IEA",
        "actu-environnement": "Actu-Environnement",
        "autoactu": "AutoActu",
        "usinenouvelle": "L'Usine Nouvelle",
        "auto-infos": "Auto Infos",
        "insideevs": "InsideEVs",
        "autorite-transports": "ART",
    }
    
    source_lower = source.lower()
    for key, value in mapping.items():
        if key in source_lower:
            return value
    return source


def article_to_notion_payload(article: Article, theme: str) -> dict:
    """Convertit un Article en payload Notion."""

    properties = {
        # Nom (Title - propriété principale de la page)
        "Nom": {
            "title": [{"text": {"content": article.title[:2000]}}]
        },

        # URL
        "URL": {
            "url": article.url
        },

        # Type (Select)
        "Type": {
            "select": {"name": "Article de presse"}
        },

        # Statut (Multi-select dans ta base)
        "Statut": {
            "multi_select": [{"name": "📥 À lire"}]
        },

        # Priorité (Select) — basé sur le score
        "Priorité": {
            "select": {"name": score_to_priority(article.score)}
        },

        # Éditeur/Média (Select)
        "Éditeur/Média": {
            "select": {"name": source_to_editeur(article.source)}
        },

        # Résumé rapide (Text)
        "Résumé rapide": {
            "rich_text": [{"text": {"content": article.summary[:2000] if article.summary else ""}}]
        },

        # Note: Thématiques est une Relation - on ne peut pas l'envoyer sans l'ID de la page liée
        # On utilise Tags à la place pour stocker le thème

        # Tags (Multi-select)
        "Tags": {
            "multi_select": [
                {"name": theme_to_thematique(theme)},
                *[{"name": tag} for tag in article.tags[:9]]  # +9 autres tags max
            ]
        },
    }

    # Date de publication (si disponible)
    if article.published_at:
        properties["Date de publication"] = {
            "date": {"start": article.published_at.isoformat()}
        }

    return {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": properties
    }


def send_to_notion(article: Article, theme: str) -> Optional[str]:
    """
    Envoie un article vers Notion.
    Retourne l'ID de la page créée, ou None en cas d'erreur.
    """
    if not NOTION_API_KEY or not NOTION_DATABASE_ID:
        print("⚠️  NOTION_API_KEY ou NOTION_DATABASE_ID non configuré")
        return None
    
    payload = article_to_notion_payload(article, theme)
    
    try:
        response = requests.post(
            NOTION_API_URL,
            headers=get_headers(),
            json=payload
        )
        
        if response.status_code == 200:
            page_id = response.json().get("id")
            print(f"✅ Notion: {article.title[:50]}...")
            return page_id
        else:
            print(f"❌ Notion error {response.status_code}: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Notion exception: {e}")
        return None


def send_articles_to_notion(articles: List[Article], theme: str) -> dict:
    """
    Envoie une liste d'articles vers Notion.
    Retourne un résumé {success: int, failed: int}.
    """
    results = {"success": 0, "failed": 0}
    
    for article in articles:
        page_id = send_to_notion(article, theme)
        if page_id:
            results["success"] += 1
        else:
            results["failed"] += 1
    
    return results


def check_notion_connection() -> bool:
    """Vérifie que la connexion Notion fonctionne."""
    if not NOTION_API_KEY or not NOTION_DATABASE_ID:
        return False
    
    try:
        response = requests.get(
            f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}",
            headers=get_headers()
        )
        return response.status_code == 200
    except:
        return False


# --- Pour tester ---
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    if check_notion_connection():
        print("✅ Connexion Notion OK")
    else:
        print("❌ Connexion Notion échouée")
        print("   Vérifie NOTION_API_KEY et NOTION_DATABASE_ID dans .env")