# seuil minimal pour garder un article
MIN_SCORE = 1

# nombre max d’articles par thème
MAX_PER_THEME = 3

# scoring par source
SOURCE_SCORE = {
    "Reuters": 0,
    "Financial Times": 0,
    "Alternatives Économiques": 0,
    "Le Monde": 0, 
    'Politico': 0,
}

# mots-clés forts
STRONG_KEYWORDS = {
    "crise": 2,
    "rapport": 2,
    "accord": 2,
    "record": 1,
    "scandale": 1
}

# blacklist bruit
BLACKLIST = [
    "football", "tennis", "sport",
    "people", "celebrite", "star",
    "fait divers", "accident", "mort de"
]

THEMES = {
    "economie": [
        # FR
        "inflation", "croissance", "taux", "banque",
        "budget", "deficit", "marche",
        # EN
        "inflation", "growth", "rates", "bank",
        "economy", "budget", "deficit", "market"
    ],
    "politique": [
        # FR
        "gouvernement", "election", "parlement",
        "commission", "reforme",
        # EN
        "government", "election", "parliament",
        "policy", "minister"
    ],
    "climat": [
        # FR
        "climat", "co2", "emissions", "energie",
        "carbone", "transition",
        # EN
        "climate", "carbon", "emissions",
        "energy", "transition"
    ],
    "industrie": [
        # FR
        "industrie", "usine", "production",
        "automobile", "constructeur",
        # EN
        "industry", "factory", "manufacturing",
        "automotive", "production"
    ]
}

