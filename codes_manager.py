# ═══════════════════════════════════════════════════════════
# ORACLE TAROT — CODES MANAGER
# Génération, validation, révocation des codes d'accès
# ═══════════════════════════════════════════════════════════

import json
import random
import string
from datetime import datetime, timedelta
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))
from config import DB_CODES_PATH, CODE_PREFIXES, CODE_SUFFIXES, NIVEAUX

# ─── INITIALISATION BASE ────────────────────────────────────
def init_db():
    """Crée la base JSON si elle n'existe pas."""
    db_path = Path(DB_CODES_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if not db_path.exists():
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump({"codes": {}}, f, indent=2)
    return db_path

def charger_db():
    """Charge la base de codes."""
    db_path = init_db()
    with open(db_path, "r", encoding="utf-8") as f:
        return json.load(f)

def sauvegarder_db(data):
    """Sauvegarde la base de codes."""
    db_path = Path(DB_CODES_PATH)
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ─── GÉNÉRATION CODE ────────────────────────────────────────
def generer_code(niveau: str) -> str:
    """
    Génère un code unique au format :
    LUNE-7842-OR  (PRO)
    ETOILE-3341-ARG (STARTER)
    CERCLE-9901-DIA (CERCLE)
    """
    if niveau not in CODE_PREFIXES:
        raise ValueError(f"Niveau inconnu : {niveau}")

    prefix  = CODE_PREFIXES[niveau]
    suffix  = CODE_SUFFIXES.get(niveau, "XX")
    chiffres = "".join(random.choices(string.digits, k=4))
    code    = f"{prefix}-{chiffres}-{suffix}"

    # Vérifier unicité
    db = charger_db()
    while code in db["codes"]:
        chiffres = "".join(random.choices(string.digits, k=4))
        code = f"{prefix}-{chiffres}-{suffix}"

    return code

# ─── CRÉER UN CODE ──────────────────────────────────────────
def creer_code(
    niveau: str,
    email: str = "",
    prenom: str = "",
    duree_jours: int = 30,
    note: str = ""
) -> dict:
    """
    Crée et enregistre un nouveau code d'accès.
    Retourne le dict du code créé.
    """
    if niveau == "FREE":
        raise ValueError("Le niveau FREE n'a pas de code — accès direct.")

    code = generer_code(niveau)
    maintenant = datetime.now()
    expiration = maintenant + timedelta(days=duree_jours)

    entree = {
        "code":       code,
        "niveau":     niveau,
        "email":      email,
        "prenom":     prenom,
        "cree_le":    maintenant.strftime("%Y-%m-%d %H:%M"),
        "expire_le":  expiration.strftime("%Y-%m-%d"),
        "actif":      True,
        "note":       note,
        "nb_connexions": 0,
        "derniere_connexion": None,
    }

    db = charger_db()
    db["codes"][code] = entree
    sauvegarder_db(db)

    return entree

# ─── VALIDER UN CODE ────────────────────────────────────────
def valider_code(code: str) -> dict:
    """
    Valide un code d'accès.
    Retourne : {"valide": True/False, "niveau": str, "message": str, "data": dict}
    """
    code = code.strip().upper()
    db   = charger_db()

    # Code inexistant
    if code not in db["codes"]:
        return {
            "valide":  False,
            "niveau":  "FREE",
            "message": "Code introuvable. Vérifiez votre saisie.",
            "data":    {}
        }

    entree = db["codes"][code]

    # Code révoqué
    if not entree.get("actif", True):
        return {
            "valide":  False,
            "niveau":  "FREE",
            "message": "Ce code a été désactivé. Contactez le support.",
            "data":    {}
        }

    # Code expiré
    expire_le = datetime.strptime(entree["expire_le"], "%Y-%m-%d")
    if datetime.now() > expire_le:
        return {
            "valide":  False,
            "niveau":  "FREE",
            "message": f"Code expiré le {entree['expire_le']}. Renouvelez votre abonnement.",
            "data":    entree
        }

    # Enregistrer la connexion
    entree["nb_connexions"] += 1
    entree["derniere_connexion"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    db["codes"][code] = entree
    sauvegarder_db(db)

    niveau = entree["niveau"]
    infos  = NIVEAUX.get(niveau, NIVEAUX["FREE"])

    return {
        "valide":  True,
        "niveau":  niveau,
        "message": f"Bienvenue {entree.get('prenom', '')} ✦ Accès {infos['nom']} activé.",
        "data":    entree
    }

# ─── RÉVOQUER UN CODE ───────────────────────────────────────
def revoquer_code(code: str) -> bool:
    """Désactive un code sans le supprimer."""
    db = charger_db()
    if code in db["codes"]:
        db["codes"][code]["actif"] = False
        sauvegarder_db(db)
        return True
    return False

# ─── RENOUVELER UN CODE ─────────────────────────────────────
def renouveler_code(code: str, duree_jours: int = 30) -> bool:
    """Prolonge la durée d'un code existant."""
    db = charger_db()
    if code not in db["codes"]:
        return False
    entree = db["codes"][code]
    # Partir de la date d'expiration actuelle si pas encore expiré
    try:
        base = datetime.strptime(entree["expire_le"], "%Y-%m-%d")
        if base < datetime.now():
            base = datetime.now()
    except Exception:
        base = datetime.now()
    entree["expire_le"] = (base + timedelta(days=duree_jours)).strftime("%Y-%m-%d")
    entree["actif"] = True
    db["codes"][code] = entree
    sauvegarder_db(db)
    return True

# ─── LISTER TOUS LES CODES ──────────────────────────────────
def lister_codes(filtre_niveau: str = None, actifs_seulement: bool = False) -> list:
    """Retourne la liste des codes avec filtres optionnels."""
    db     = charger_db()
    codes  = list(db["codes"].values())
    if filtre_niveau:
        codes = [c for c in codes if c["niveau"] == filtre_niveau]
    if actifs_seulement:
        codes = [c for c in codes if c.get("actif", True)]
    return sorted(codes, key=lambda x: x.get("cree_le", ""), reverse=True)

# ─── STATS RAPIDES ──────────────────────────────────────────
def stats_db() -> dict:
    """Retourne des stats globales sur la base."""
    db    = charger_db()
    codes = list(db["codes"].values())
    maintenant = datetime.now()

    actifs  = [c for c in codes if c.get("actif", True) and
               datetime.strptime(c["expire_le"], "%Y-%m-%d") > maintenant]
    expires = [c for c in codes if datetime.strptime(c["expire_le"], "%Y-%m-%d") <= maintenant]
    revoques= [c for c in codes if not c.get("actif", True)]

    par_niveau = {}
    for niveau in ["STARTER", "PRO", "CERCLE", "ADMIN"]:
        par_niveau[niveau] = len([c for c in actifs if c["niveau"] == niveau])

    return {
        "total":       len(codes),
        "actifs":      len(actifs),
        "expires":     len(expires),
        "revoques":    len(revoques),
        "par_niveau":  par_niveau,
    }

# ─── TEST RAPIDE ────────────────────────────────────────────
if __name__ == "__main__":
    print("=== TEST CODES MANAGER ===")

    # Créer codes de test
    c1 = creer_code("STARTER", email="test1@email.com", prenom="Sophie", duree_jours=30)
    c2 = creer_code("PRO",     email="test2@email.com", prenom="Marie",  duree_jours=30)
    c3 = creer_code("CERCLE",  email="test3@email.com", prenom="Laura",  duree_jours=30)

    print(f"\nCodes créés :")
    print(f"  STARTER : {c1['code']}")
    print(f"  PRO     : {c2['code']}")
    print(f"  CERCLE  : {c3['code']}")

    # Valider
    print(f"\nValidation STARTER : {valider_code(c1['code'])['message']}")
    print(f"Validation invalide : {valider_code('FAUX-0000-XX')['message']}")

    # Stats
    s = stats_db()
    print(f"\nStats : {s['actifs']} actifs / {s['total']} total")
    print(f"Par niveau : {s['par_niveau']}")
