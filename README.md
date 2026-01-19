# 🗞️ Le Brief — Newsletter automatisée

Projet personnel de **newsletter quotidienne automatisée** à partir de flux RSS.  
Le script :

- récupère des articles depuis plusieurs sources (RSS)
- filtre, score et dédoublonne les contenus
- génère un brief éditorial en Markdown
- transforme ce brief en email HTML (style journal)
- envoie la newsletter par email (clair + sombre)
- évite d’envoyer deux fois le même article

Le tout est pensé pour être **simple, lisible et reproductible**.

---

## ✨ Fonctionnalités

- 📡 Fetch de flux RSS (économie, politique, climat, etc.)
- 🧠 Filtrage + scoring des articles
- 🔁 Mémoire des articles déjà envoyés (anti-doublons)
- 📝 Génération d’un brief Markdown
- 📰 Mise en page “journal” (articles alignés horizontalement)
- 🌙 Compatible mode clair / mode sombre (email)
- ✉️ Envoi automatique par email
- ⚙️ Compatible GitHub Actions

---

## 🧱 Structure du projet

```text
newsletter/
├── main.py                 # Pipeline principal
├── fetch.py                # Récupération RSS
├── filter.py               # Filtrage & scoring
├── memory.py               # Mémoire des articles envoyés
├── render.py               # Génération du brief Markdown (layout journal)
├── send_mail.py            # Envoi email (HTML + dark mode)
├── models.py               # Modèle Article
├── config/
│   └── sources.yaml        # Sources RSS par thème
├── data/
│   └── sent_articles.txt   # Historique des articles envoyés
├── output/                 # Briefs générés (non versionnés)
├── requirements.txt
├── .env.example
└── README.md
```
## 🚀 Installation

### 1️⃣ Cloner le dépôt

```bash
git clone https://github.com/manonbsvl/newsletter.git
cd newsletter
```
### 2️⃣ Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # macOS / Linux
```
### 3️⃣ Installer les dépendances

```bash
python -m venv venv
source venv/bin/activate  # macOS / Linux
```
## ⚙️ Configuration

### 1️⃣ Créer le fichier .env
```bash
cp .env.example .env
```
Puis remplir le fichier .env :

```env
NEWSLETTER_EMAIL=ton_email@gmail.com
NEWSLETTER_EMAIL_PASSWORD=mot_de_passe_application
NEWSLETTER_EMAIL_TO=destinataire@gmail.com

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

OPENAI_API_KEY=sk-xxxx
```
**⚠️ Important**
Pour Gmail, utiliser un mot de passe d’application, pas le mot de passe du compte.

### 2️⃣ Configurer les sources RSS

Modifier le fichier :
```
config/sources.yaml
```
Par exemple : 
```yaml
themes:
  economie:
    - https://feeds.reuters.com/reuters/businessNews
    - https://www.alternatives-economiques.fr/rss.xml

  politique:
    - https://www.politico.eu/rss/

  climat:
    - https://www.carbonbrief.org/feed/
```

### ▶️ Utilisation
Générer le brief (sans envoi) : 

```bash
python main.py
```

```text
output/brief_YYYY-MM-DD.md
```

Générer + envoyer la newsletter par email : 

```bash
python main.py --send
```

## ⏱️ Automatisation (optionnel)

Le projet est compatible avec GitHub Actions pour un envoi automatique quotidien (ex. tous les jours à 8h).
Cela permet :
	•	exécution même si ton ordinateur est éteint
	•	envoi fiable et régulier


## 🔐 Sécurité

Le fichier .env ne doit jamais être versionné
Il est volontairement ignoré par .gitignore
Utiliser uniquement des mots de passe d’application
