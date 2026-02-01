# ══════════════════════════════════════════════════════════
# CONFIGURATION VEILLE ÉCONOMIE & AUTOMOBILE
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
    "Brookings": 2,
    "CFR": 2,
    "Chatham House": 2,

    # Fédérations auto
    "OICA": 2,
    "ACEA": 2,
    "CCFA": 2,

    # Presse spécialisée auto
    "Automotive News": 2,
    "Just Auto": 2,

    # Presse généraliste (neutre)
    "Reuters": 0,
    "Financial Times": 0,
    "Les Échos": 0,
    "La Tribune": 0,
    "L'Usine Nouvelle": 1,
    "Politico": 0,
    "Alternatives Économiques": 0,
    "Le Monde": 0,
    "BBC": 0,

    # Académique
    "ScienceDirect": 2,
    "NBER": 3,

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
    "reshoring": 2,
    "nearshoring": 2,

    # Supply chain & batteries
    "supply chain": 2,
    "batterie": 2,
    "battery": 2,
    "lithium": 2,
    "terres rares": 3,
    "rare earth": 3,
    "gigafactory": 2,

    # Constructeurs
    "stellantis": 2,
    "volkswagen": 1,
    "renault": 1,
    "tesla": 1,
    "toyota": 1,
    "byd": 2,

    # Électrification
    "vehicule electrique": 2,
    "electric vehicle": 2,

    # Politique industrielle
    "subvention": 2,
    "subsidy": 2,
    "ira": 2,
    "fit for 55": 2,
    "green deal": 2,

    # Économie
    "crise": 1,
    "recession": 2,
    "inflation": 1,
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
    # ══════════════════════════════════════════════════════
    # AUTOMOBILE (spécifique auto)
    # ══════════════════════════════════════════════════════
    "automobile": [
        # Constructeurs
        "automobile", "automotive", "automaker",
        "stellantis", "volkswagen", "renault", "peugeot", "citroen",
        "tesla", "toyota", "bmw", "mercedes", "audi", "ford", "gm",
        "hyundai", "kia", "nissan", "honda", "byd", "nio", "xpeng",
        "volvo", "porsche", "ferrari", "lamborghini",

        # Véhicules
        "voiture", "car", "vehicule", "vehicle",
        "suv", "berline", "sedan", "pickup",

        # Électrification auto
        "ev", "bev", "phev", "hybride", "hybrid",
        "recharge", "charging", "autonomie",
        "borne", "supercharger",

        # Équipementiers
        "equipementier", "tier 1", "tier 2",
        "valeo", "faurecia", "forvia", "bosch", "continental",
        "denso", "magna", "lear", "aptiv",

        # Fédérations
        "acea", "oica", "ccfa",
    ],

    # ══════════════════════════════════════════════════════
    # INDUSTRIE GÉNÉRALE (hors auto spécifiquement)
    # ══════════════════════════════════════════════════════
    "industrie": [
        # Production
        "usine", "factory", "manufacturing", "production",
        "industriel", "industrial",

        # Supply chain générale
        "supply chain", "fournisseur", "supplier",
        "logistique", "logistics",

        # Secteurs industriels (hors auto)
        "aeronautique", "aerospace", "aviation",
        "siderurgie", "steel", "acier",
        "chimie", "chemical",
        "pharmacie", "pharmaceutical",
        "agroalimentaire", "food",
    ],

    # ══════════════════════════════════════════════════════
    # ÉCONOMIE & FINANCE
    # ══════════════════════════════════════════════════════
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

    # ══════════════════════════════════════════════════════
    # GÉOPOLITIQUE & COMMERCE
    # ══════════════════════════════════════════════════════
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
        "nearshoring", "friendshoring",

        # Souveraineté
        "souverainete", "sovereignty", "strategique", "strategic",
        "politique industrielle", "industrial policy",

        # Pays/régions
        "chine", "china", "beijing",
        "etats unis", "united states", "washington",
        "union europeenne", "european union", "bruxelles",
    ],

    # ══════════════════════════════════════════════════════
    # ÉNERGIE & CLIMAT
    # ══════════════════════════════════════════════════════
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

    # ══════════════════════════════════════════════════════
    # TECH & INNOVATION
    # ══════════════════════════════════════════════════════
    "tech": [
        # Semi-conducteurs
        "semi conducteur", "semiconductor", "chip", "puce",
        "wafer", "foundry", "tsmc", "intel", "samsung",
        "chips act",

        # Batteries
        "batterie", "battery", "lithium", "solid state",
        "cathode", "anode", "gigafactory",
        "catl", "northvolt", "acc",

        # Véhicule autonome
        "autonome", "autonomous", "self driving",
        "adas", "lidar", "radar",
        "waymo", "cruise", "mobileye",

        # IA
        "intelligence artificielle", "artificial intelligence",
        "ia", "ai", "machine learning",
        "nvidia", "qualcomm",

        # Standards
        "sae", "ieee", "iso",
    ],

    # ══════════════════════════════════════════════════════
    # ACADÉMIQUE
    # ══════════════════════════════════════════════════════
    "academique": [
        "working paper", "etude", "study", "research",
        "analyse", "analysis", "rapport", "report",
        "publication", "paper", "review",
        "modele", "model", "simulation", "scenario",
        "projection", "forecast",
    ],

    # ══════════════════════════════════════════════════════
    # RAPPORTS
    # ══════════════════════════════════════════════════════
    "rapports": [
        "rapport annuel", "annual report",
        "outlook", "perspectives", "forecast",
        "global", "mondial", "world",
        "strategie", "strategy", "tendance", "trend",
        "prospective", "foresight",
    ],

    # ══════════════════════════════════════════════════════
    # POLITIQUE
    # ══════════════════════════════════════════════════════
    "politique": [
        "gouvernement", "government", "parlement", "parliament",
        "commission", "conseil", "senat", "assemblee",
        "election", "vote", "reforme", "reform",
        "loi", "law", "reglement", "regulation",
        "directive", "decret",
        "ministre", "minister", "president",
    ],
}
