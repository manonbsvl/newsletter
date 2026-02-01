# ══════════════════════════════════════════════════════════
# CONFIGURATION VEILLE AUTOMOBILE & ÉCONOMIE
# ══════════════════════════════════════════════════════════

# Seuil minimal pour garder un article
MIN_SCORE = 1

# Nombre max d'articles par thème
MAX_PER_THEME = 8

# ──────────────────────────────────────────────────────────
# SCORING PAR SOURCE (sources premium = bonus)
# ──────────────────────────────────────────────────────────
SOURCE_SCORE = {
    # Think tanks & institutions (haute valeur)
    "IEA": 3,
    "IFRI": 3,
    "Bruegel": 3,
    "CSIS": 3,
    "Carnegie": 2,
    "NBER": 3,
    "VoxEU": 2,
    "Peterson Institute": 2,

    # Rapports stratégie
    "McKinsey": 2,
    "BCG": 2,
    "OICA": 2,
    "ACEA": 2,

    # Presse spécialisée auto
    "Automotive News": 2,
    "Just Auto": 2,
    "Electrek": 1,
    "InsideEVs": 1,

    # Presse généraliste (neutre)
    "Reuters": 0,
    "Financial Times": 0,
    "Les Échos": 0,
    "La Tribune": 0,
    "Bloomberg": 0,
    "Politico": 0,
    "Alternatives Économiques": 0,
    "Le Monde": 0,

    # Académique
    "ScienceDirect": 2,
    "SSRN": 2,

    # Tech & ingénierie
    "SAE": 3,
    "IEEE": 3,
    "MIT Technology Review": 2,
    "Nature": 3,
    "SIA": 2,
    "Green Car Congress": 2,
}

# ──────────────────────────────────────────────────────────
# MOTS-CLÉS FORTS (déclenchent un bonus de score)
# ──────────────────────────────────────────────────────────
STRONG_KEYWORDS = {
    # Géopolitique & commerce
    "tarif": 2,
    "tariff": 2,
    "sanctions": 2,
    "guerre commerciale": 3,
    "trade war": 3,
    "protectionnisme": 2,
    "souverainete": 2,
    "sovereignty": 2,
    "decoupling": 2,
    "decouplage": 2,
    "reshoring": 2,
    "nearshoring": 2,
    "friendshoring": 2,

    # Supply chain & batteries
    "supply chain": 2,
    "chaine approvisionnement": 2,
    "batterie": 2,
    "battery": 2,
    "lithium": 2,
    "cobalt": 2,
    "terres rares": 3,
    "rare earth": 3,
    "gigafactory": 2,
    "catl": 2,
    "byd": 2,
    "northvolt": 2,

    # Constructeurs & stratégie
    "stellantis": 2,
    "volkswagen": 1,
    "renault": 1,
    "tesla": 1,
    "toyota": 1,
    "bmw": 1,
    "mercedes": 1,
    "ford": 1,
    "gm": 1,
    "hyundai": 1,

    # Électrification
    "electrification": 2,
    "vehicule electrique": 2,
    "electric vehicle": 2,
    "ev": 1,
    "hybride": 1,
    "hybrid": 1,
    "borne recharge": 2,
    "charging": 1,

    # Politique industrielle
    "subvention": 2,
    "subsidy": 2,
    "ira": 2,  # Inflation Reduction Act
    "fit for 55": 2,
    "green deal": 2,
    "norme euro": 2,
    "emission": 1,
    "co2": 1,
    "cafe": 2,  # Corporate Average Fuel Economy

    # Économie générale
    "rapport": 1,
    "etude": 1,
    "study": 1,
    "crise": 1,
    "recession": 2,
    "inflation": 1,
    "taux": 1,
    "bce": 1,
    "fed": 1,

    # Pays clés
    "chine": 1,
    "china": 1,
    "etats unis": 1,
    "united states": 1,
    "allemagne": 1,
    "germany": 1,
    "japon": 1,
    "japan": 1,
    "coree": 1,
    "korea": 1,
}

# ──────────────────────────────────────────────────────────
# BLACKLIST (articles à exclure)
# ──────────────────────────────────────────────────────────
BLACKLIST = [
    # Sport
    "football", "tennis", "sport", "rugby", "basket",
    "jeux olympiques", "olympics", "coupe du monde",

    # People & divertissement
    "people", "celebrite", "star", "cinema", "film",
    "serie", "musique", "concert",

    # Faits divers
    "fait divers", "accident mortel", "agression",
    "cambriolage", "incendie criminel",

    # Contenu léger
    "horoscope", "meteo", "recette", "cuisine",
    "mode", "beaute", "lifestyle",

    # Spam/clickbait
    "vous ne croirez pas", "incroyable", "choquant",
    "viral", "buzz",
]

# ──────────────────────────────────────────────────────────
# THÈMES ET MOTS-CLÉS DE CLASSIFICATION
# ──────────────────────────────────────────────────────────
THEMES = {
    "auto_industrie": [
        # Constructeurs
        "automobile", "automotive", "constructeur", "automaker",
        "vehicule", "vehicle", "voiture", "car",
        "stellantis", "volkswagen", "renault", "peugeot", "citroen",
        "tesla", "toyota", "bmw", "mercedes", "audi", "ford", "gm",
        "hyundai", "kia", "nissan", "honda", "byd", "nio", "xpeng",

        # Électrification
        "electrique", "electric", "batterie", "battery",
        "ev", "bev", "phev", "hybride", "hybrid",
        "recharge", "charging", "autonomie", "range",

        # Supply chain
        "supply chain", "fournisseur", "supplier",
        "equipementier", "tier 1", "tier 2",
        "usine", "factory", "production", "manufacturing",

        # Composants
        "moteur", "engine", "transmission", "chassis",
        "semi conducteur", "semiconductor", "chip", "puce",
    ],

    "geopolitique": [
        # Commerce international
        "tarif", "tariff", "douane", "customs",
        "sanction", "embargo", "quota",
        "accord commercial", "trade deal", "trade agreement",
        "omc", "wto", "protectionnisme", "protectionism",

        # Tensions géopolitiques
        "guerre commerciale", "trade war",
        "tensions", "conflit", "dispute",
        "decoupling", "decouplage", "reshoring",
        "nearshoring", "friendshoring", "onshoring",

        # Souveraineté industrielle
        "souverainete", "sovereignty", "strategique", "strategic",
        "dependance", "dependency", "autonomie strategique",
        "politique industrielle", "industrial policy",

        # Pays/régions clés
        "chine", "china", "beijing", "pekin",
        "etats unis", "united states", "washington",
        "union europeenne", "european union", "bruxelles",
    ],

    "energie_climat": [
        # Énergie
        "energie", "energy", "petrole", "oil", "gaz", "gas",
        "renouvelable", "renewable", "solaire", "solar",
        "eolien", "wind", "nucleaire", "nuclear", "hydrogene", "hydrogen",

        # Climat
        "climat", "climate", "co2", "carbone", "carbon",
        "emission", "rechauffement", "warming",
        "transition", "decarbonation", "net zero",

        # Réglementation
        "cop", "accord paris", "paris agreement",
        "green deal", "fit for 55", "taxonomie",
        "marche carbone", "carbon market", "ets",
    ],

    "economie": [
        # Macro
        "inflation", "croissance", "growth", "pib", "gdp",
        "recession", "emploi", "chomage", "unemployment",

        # Politique monétaire
        "taux", "rate", "banque centrale", "central bank",
        "bce", "ecb", "fed", "reserve federale",

        # Finance
        "marche", "market", "bourse", "stock",
        "investissement", "investment", "dette", "debt",
        "budget", "deficit", "fiscal",
    ],

    "academique": [
        # Types de publications
        "working paper", "etude", "study", "research",
        "analyse", "analysis", "rapport", "report",
        "publication", "paper", "review",

        # Méthodologie
        "modele", "model", "simulation", "scenario",
        "projection", "forecast", "prevision",
        "donnees", "data", "statistiques", "statistics",
    ],

    "rapports": [
        # Documents institutionnels
        "rapport annuel", "annual report",
        "outlook", "perspectives", "forecast",
        "global", "mondial", "world",

        # Stratégie
        "strategie", "strategy", "tendance", "trend",
        "prospective", "foresight", "scenario",
        "recommandation", "recommendation",
    ],

    "tech_industrie": [
        # Semi-conducteurs
        "semi conducteur", "semiconductor", "chip", "puce",
        "wafer", "foundry", "tsmc", "intel", "samsung",
        "chips act", "shortage", "penurie",

        # Batteries & stockage
        "batterie", "battery", "lithium", "solid state",
        "cathode", "anode", "cell", "gigafactory",
        "catl", "lg", "panasonic", "northvolt", "acc",

        # Véhicule autonome & ADAS
        "autonome", "autonomous", "self driving",
        "adas", "lidar", "radar", "camera",
        "waymo", "cruise", "mobileye",

        # Connectivité
        "connecte", "connected", "v2x", "ota",
        "software defined vehicle", "sdv",

        # IA & computing
        "intelligence artificielle", "artificial intelligence",
        "machine learning", "neural network",
        "nvidia", "qualcomm",

        # Standards & ingénierie
        "standard", "norme", "regulation", "homologation",
        "sae", "iso", "unece",
    ],

    "politique": [
        # Institutions
        "gouvernement", "government", "parlement", "parliament",
        "commission", "conseil", "senat", "assemblee",

        # Actions politiques
        "election", "vote", "reforme", "reform",
        "loi", "law", "reglement", "regulation",
        "directive", "decret", "arrete",

        # Acteurs
        "ministre", "minister", "president", "premier ministre",
        "depute", "senateur", "commissaire",
    ],

    "tech": [
        # IA & software
        "intelligence artificielle", "artificial intelligence",
        "ia", "ai", "machine learning", "deep learning",
        "algorithme", "algorithm", "software", "logiciel",

        # Mobilité
        "autonome", "autonomous", "self driving",
        "connecte", "connected", "adas",
        "mobilite", "mobility", "maas",

        # Innovation
        "startup", "innovation", "disruption",
        "r&d", "recherche", "research", "brevet", "patent",
    ],
}
