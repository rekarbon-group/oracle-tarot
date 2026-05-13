#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════
# ORACLE TAROT — GÉNÉRATEUR DE CODES (CLI Admin)
# Usage : python generate_code.py
# ═══════════════════════════════════════════════════════════

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from auth.codes_manager import creer_code, valider_code, revoquer_code, renouveler_code, lister_codes, stats_db
from config import NIVEAUX, LIEN_ETSY, LIEN_SKOOL

# ─── COULEURS TERMINAL ──────────────────────────────────────
OR     = "\033[93m"
VIOLET = "\033[95m"
VERT   = "\033[92m"
ROUGE  = "\033[91m"
GRIS   = "\033[90m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def banner():
    print(f"""
{OR}╔══════════════════════════════════════════════════════╗
║        🔮  ORACLE TAROT — ADMIN CLI  🔮              ║
║             Gestionnaire de codes d'accès            ║
╚══════════════════════════════════════════════════════╝{RESET}
""")

def menu():
    print(f"""
{BOLD}Que veux-tu faire ?{RESET}

  {OR}1{RESET}  →  Générer un nouveau code
  {OR}2{RESET}  →  Valider un code existant
  {OR}3{RESET}  →  Révoquer un code
  {OR}4{RESET}  →  Renouveler un code
  {OR}5{RESET}  →  Lister tous les codes actifs
  {OR}6{RESET}  →  Stats globales
  {OR}0{RESET}  →  Quitter
""")

def choisir_niveau():
    print(f"\n{BOLD}Choisis le niveau :{RESET}")
    niveaux = ["STARTER", "PRO", "CERCLE", "ADMIN"]
    for i, n in enumerate(niveaux, 1):
        infos = NIVEAUX[n]
        print(f"  {OR}{i}{RESET}  →  {infos['emoji']} {n} — {infos['nom']} ({infos['prix']})")
    choix = input(f"\n{GRIS}Niveau (1-4) : {RESET}").strip()
    try:
        return niveaux[int(choix) - 1]
    except Exception:
        print(f"{ROUGE}Choix invalide.{RESET}")
        return None

def action_generer():
    print(f"\n{BOLD}═══ GÉNÉRER UN CODE ═══{RESET}")
    niveau = choisir_niveau()
    if not niveau:
        return

    prenom    = input(f"{GRIS}Prénom du client (optionnel) : {RESET}").strip()
    email     = input(f"{GRIS}Email du client (optionnel) : {RESET}").strip()
    duree_str = input(f"{GRIS}Durée en jours (défaut: 30) : {RESET}").strip()
    note      = input(f"{GRIS}Note interne (optionnel) : {RESET}").strip()

    try:
        duree = int(duree_str) if duree_str else 30
    except ValueError:
        duree = 30

    entree = creer_code(niveau=niveau, email=email, prenom=prenom, duree_jours=duree, note=note)
    infos  = NIVEAUX[niveau]

    print(f"""
{VERT}╔══════════════════════════════════════════════════════╗
║  ✓  CODE CRÉÉ AVEC SUCCÈS                           ║
╚══════════════════════════════════════════════════════╝{RESET}

  Code      : {OR}{BOLD}{entree['code']}{RESET}
  Niveau    : {infos['emoji']} {infos['nom']}
  Client    : {prenom or '—'} ({email or '—'})
  Expire le : {entree['expire_le']}
  Durée     : {duree} jours

{BOLD}📧 Email à envoyer au client :{RESET}
{GRIS}─────────────────────────────────────────{RESET}
Bonjour {prenom or 'cher·e membre'} ✨

Votre code d'accès à l'Oracle Tarot Professionnel est prêt.

🔮 Votre code : {OR}{BOLD}{entree['code']}{RESET}

Rendez-vous sur notre application pour l'activer :
→ [LIEN APP STREAMLIT]

Niveau débloqué : {infos['emoji']} {infos['nom']} ({infos['prix']})
Valable jusqu'au : {entree['expire_le']}

Bienvenue dans Le Cercle des Étoiles ✦
{GRIS}─────────────────────────────────────────{RESET}
""")

def action_valider():
    print(f"\n{BOLD}═══ VALIDER UN CODE ═══{RESET}")
    code   = input(f"{GRIS}Code à valider : {RESET}").strip()
    result = valider_code(code)

    if result["valide"]:
        infos = NIVEAUX.get(result["niveau"], {})
        print(f"""
{VERT}✓ CODE VALIDE{RESET}
  Niveau   : {infos.get('emoji','')} {result['niveau']} — {infos.get('nom','')}
  Message  : {result['message']}
  Expire   : {result['data'].get('expire_le', '—')}
  Connexions: {result['data'].get('nb_connexions', 0)}
""")
    else:
        print(f"\n{ROUGE}✗ CODE INVALIDE{RESET}\n  {result['message']}\n")

def action_revoquer():
    print(f"\n{BOLD}═══ RÉVOQUER UN CODE ═══{RESET}")
    code = input(f"{GRIS}Code à révoquer : {RESET}").strip()
    conf = input(f"{ROUGE}Confirmer la révocation de {code} ? (oui/non) : {RESET}").strip().lower()
    if conf == "oui":
        ok = revoquer_code(code)
        print(f"\n{VERT}✓ Code révoqué.{RESET}" if ok else f"\n{ROUGE}✗ Code introuvable.{RESET}")
    else:
        print(f"\n{GRIS}Révocation annulée.{RESET}")

def action_renouveler():
    print(f"\n{BOLD}═══ RENOUVELER UN CODE ═══{RESET}")
    code      = input(f"{GRIS}Code à renouveler : {RESET}").strip()
    duree_str = input(f"{GRIS}Durée supplémentaire en jours (défaut: 30) : {RESET}").strip()
    try:
        duree = int(duree_str) if duree_str else 30
    except ValueError:
        duree = 30
    ok = renouveler_code(code, duree_jours=duree)
    print(f"\n{VERT}✓ Code renouvelé pour {duree} jours.{RESET}" if ok else f"\n{ROUGE}✗ Code introuvable.{RESET}")

def action_lister():
    print(f"\n{BOLD}═══ CODES ACTIFS ═══{RESET}")
    niveau_f = input(f"{GRIS}Filtrer par niveau ? (STARTER/PRO/CERCLE ou Entrée pour tous) : {RESET}").strip().upper() or None
    codes    = lister_codes(filtre_niveau=niveau_f, actifs_seulement=True)

    if not codes:
        print(f"\n{GRIS}Aucun code trouvé.{RESET}")
        return

    print(f"\n{'Code':<22} {'Niveau':<10} {'Prénom':<15} {'Expire':<12} {'Connexions'}")
    print(f"{GRIS}{'─'*22} {'─'*10} {'─'*15} {'─'*12} {'─'*10}{RESET}")
    for c in codes:
        infos = NIVEAUX.get(c['niveau'], {})
        print(f"{OR}{c['code']:<22}{RESET} {infos.get('emoji','')} {c['niveau']:<8} {c.get('prenom','—'):<15} {c['expire_le']:<12} {c.get('nb_connexions',0)}")
    print(f"\n{GRIS}Total : {len(codes)} code(s).{RESET}")

def action_stats():
    print(f"\n{BOLD}═══ STATS GLOBALES ═══{RESET}")
    s = stats_db()
    print(f"""
  Total codes  : {s['total']}
  {VERT}Actifs       : {s['actifs']}{RESET}
  {ROUGE}Expirés      : {s['expires']}{RESET}
  {GRIS}Révoqués     : {s['revoques']}{RESET}

  Par niveau :
    ⭐ STARTER  : {s['par_niveau'].get('STARTER', 0)}
    🌙 PRO      : {s['par_niveau'].get('PRO', 0)}
    🔮 CERCLE   : {s['par_niveau'].get('CERCLE', 0)}
    👁️  ADMIN    : {s['par_niveau'].get('ADMIN', 0)}
""")

# ─── MAIN ───────────────────────────────────────────────────
def main():
    banner()
    while True:
        menu()
        choix = input(f"{GRIS}Choix : {RESET}").strip()
        if choix == "1": action_generer()
        elif choix == "2": action_valider()
        elif choix == "3": action_revoquer()
        elif choix == "4": action_renouveler()
        elif choix == "5": action_lister()
        elif choix == "6": action_stats()
        elif choix == "0":
            print(f"\n{OR}✦ À bientôt. ✦{RESET}\n")
            break
        else:
            print(f"\n{ROUGE}Choix invalide.{RESET}")

if __name__ == "__main__":
    main()
