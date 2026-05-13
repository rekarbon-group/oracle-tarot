# ═══════════════════════════════════════════════════════════
# ORACLE TAROT — CONFIG CENTRALE
# Niveaux d'accès, règles freemium, messages cadenas
# ═══════════════════════════════════════════════════════════

# ─── NIVEAUX D'ACCÈS ────────────────────────────────────────
NIVEAUX = {
    "FREE": {
        "nom": "Explorateur",
        "emoji": "🌑",
        "couleur": "#888888",
        "prix": "Gratuit",
        "tirages_max": 1,           # nb cartes max par tirage
        "types_tirage": ["1 carte"],
        "secteurs": ["amour"],      # secteurs accessibles
        "familles_cartes": ["Arcanes Majeurs"],
        "export_pdf": False,
        "historique": False,
        "boutique_remise": 0,
        "lives": False,
    },
    "STARTER": {
        "nom": "Initié·e",
        "emoji": "⭐",
        "couleur": "#c0c0c0",
        "prix": "€9,99/mois",
        "tirages_max": 3,
        "types_tirage": ["1 carte", "3 cartes — Passé/Présent/Futur"],
        "secteurs": ["amour", "travail", "argent", "famille", "spirituel"],
        "familles_cartes": ["Arcanes Majeurs"],
        "export_pdf": False,
        "historique": False,
        "boutique_remise": 0,
        "lives": False,
    },
    "PRO": {
        "nom": "Praticien·ne",
        "emoji": "🌙",
        "couleur": "#c9a84c",
        "prix": "€27/mois",
        "tirages_max": 10,
        "types_tirage": [
            "1 carte",
            "3 cartes — Passé/Présent/Futur",
            "5 cartes — Lecture complète",
            "10 cartes — Croix Celtique"
        ],
        "secteurs": ["amour", "travail", "argent", "famille", "spirituel"],
        "familles_cartes": ["Arcanes Majeurs", "Coupes", "Bâtons", "Épées", "Pentacles"],
        "export_pdf": True,
        "historique": True,
        "boutique_remise": 0,
        "lives": False,
    },
    "CERCLE": {
        "nom": "Maître·sse",
        "emoji": "🔮",
        "couleur": "#9b59b6",
        "prix": "€47/mois",
        "tirages_max": 10,
        "types_tirage": [
            "1 carte",
            "3 cartes — Passé/Présent/Futur",
            "5 cartes — Lecture complète",
            "10 cartes — Croix Celtique"
        ],
        "secteurs": ["amour", "travail", "argent", "famille", "spirituel"],
        "familles_cartes": ["Arcanes Majeurs", "Coupes", "Bâtons", "Épées", "Pentacles"],
        "export_pdf": True,
        "historique": True,
        "boutique_remise": 20,      # % de remise boutique
        "lives": True,
        "code_promo_boutique": "CERCLE20",
    },
    "ADMIN": {
        "nom": "Admin",
        "emoji": "👁️",
        "couleur": "#e74c3c",
        "prix": "—",
        "tirages_max": 999,
        "types_tirage": ["*"],
        "secteurs": ["amour", "travail", "argent", "famille", "spirituel"],
        "familles_cartes": ["Arcanes Majeurs", "Coupes", "Bâtons", "Épées", "Pentacles"],
        "export_pdf": True,
        "historique": True,
        "boutique_remise": 100,
        "lives": True,
    }
}

# ─── SECTEURS ───────────────────────────────────────────────
SECTEURS_LABELS = {
    "amour":     "❤️ Amour & Relations",
    "travail":   "💼 Travail & Carrière",
    "argent":    "💰 Argent & Abondance",
    "famille":   "👨‍👩‍👧 Famille & Entourage",
    "spirituel": "🌙 Spiritualité",
}

# ─── FAMILLES DE CARTES ─────────────────────────────────────
FAMILLES_CARTES = ["Arcanes Majeurs", "Coupes", "Bâtons", "Épées", "Pentacles"]

# ─── POSITIONS PAR TYPE DE TIRAGE ───────────────────────────
POSITIONS_TIRAGE = {
    "1 carte": ["Message du jour"],
    "3 cartes — Passé/Présent/Futur": ["Passé", "Présent", "Futur"],
    "5 cartes — Lecture complète": [
        "La situation actuelle",
        "Ce qui est caché",
        "Le blocage",
        "Ce qui s'ouvre",
        "La réponse finale"
    ],
    "10 cartes — Croix Celtique": [
        "Situation", "Défi", "Fondation", "Passé récent",
        "Potentiel", "Avenir proche", "Toi", "Environnement",
        "Espoirs/Peurs", "Résultat final"
    ],
}

# ─── MESSAGES CADENAS ───────────────────────────────────────
CADENAS = {
    "secteur": {
        "titre": "🔒 Secteur verrouillé",
        "texte": "Ce secteur est disponible dès le niveau **Initié·e** (€9,99/mois).",
        "cta": "→ Obtenir mon code d'accès",
    },
    "tirage": {
        "titre": "🔒 Tirage verrouillé",
        "texte": "Ce type de tirage est disponible à partir du niveau **Initié·e**.",
        "cta": "→ Débloquer maintenant",
    },
    "cartes_mineures": {
        "titre": "🔒 Arcanes Mineurs verrouillés",
        "texte": "Les 56 Arcanes Mineurs sont accessibles au niveau **Praticien·ne PRO** (€27/mois).",
        "cta": "→ Passer PRO",
    },
    "export": {
        "titre": "🔒 Export verrouillé",
        "texte": "L'export PDF est disponible au niveau **Praticien·ne PRO** (€27/mois).",
        "cta": "→ Passer PRO",
    },
    "boutique": {
        "titre": "🔒 Remise boutique réservée",
        "texte": "La remise -20% sur notre boutique ésotérique est réservée au **Cercle** (€47/mois).",
        "cta": "→ Rejoindre le Cercle",
    },
    "historique": {
        "titre": "🔒 Historique verrouillé",
        "texte": "L'historique de vos lectures est disponible au niveau **PRO**.",
        "cta": "→ Passer PRO",
    },
}

# ─── LIEN BOUTIQUE / ETSY ───────────────────────────────────
LIEN_ETSY        = "https://www.etsy.com/fr/shop/TON_SHOP"  # ← à remplacer
LIEN_SKOOL       = "https://www.skool.com/TON_CERCLE"        # ← à remplacer
LIEN_TIKTOK      = "https://www.tiktok.com/@TON_COMPTE"      # ← à remplacer
LIEN_BOUTIQUE    = "https://TON_SITE_ESOTHERIQUE.com"        # ← à remplacer

# ─── FORMAT CODES D'ACCÈS ───────────────────────────────────
CODE_PREFIXES = {
    "FREE":    "EXPLORE",   # non utilisé (pas de code pour FREE)
    "STARTER": "ETOILE",
    "PRO":     "LUNE",
    "CERCLE":  "CERCLE",
    "ADMIN":   "ADMIN",
}

CODE_SUFFIXES = {
    "STARTER": "ARG",   # argent
    "PRO":     "OR",    # or
    "CERCLE":  "DIA",   # diamant
    "ADMIN":   "ROI",   # roi
}

# ─── BASE DE DONNÉES CODES (fichier JSON) ───────────────────
DB_CODES_PATH = "auth/codes_db.json"
DB_HISTORIQUE_PATH = "auth/historique_db.json"
