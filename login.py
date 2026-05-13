import streamlit as st
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from auth.codes_manager import valider_code
from config import NIVEAUX, LIEN_ETSY, LIEN_SKOOL

# ─── CSS LOGIN ──────────────────────────────────────────────
def css_login():
    st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Cinzel:wght@400;600&display=swap');
  .stApp { background: #080810; }

  .login-container {
    max-width: 480px;
    margin: 0 auto;
    padding: 40px 20px;
    text-align: center;
  }
  .login-ornament {
    font-size: 50px;
    margin-bottom: 20px;
    letter-spacing: 10px;
    color: #c9a84c;
    opacity: 0.8;
  }
  .login-title {
    font-family: 'Cinzel', serif;
    font-size: 1.8rem;
    color: #e8d5a3;
    margin-bottom: 5px;
    letter-spacing: 3px;
  }
  .login-sub {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    color: rgba(201,168,76,0.6);
    font-size: 1rem;
    margin-bottom: 30px;
  }
  .niveau-card {
    background: rgba(201,168,76,0.05);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 10px;
    padding: 16px;
    margin: 8px 0;
    text-align: left;
  }
  .niveau-nom {
    font-family: 'Cinzel', serif;
    font-size: 0.85rem;
    color: #e8d5a3;
    letter-spacing: 2px;
  }
  .niveau-prix {
    color: #c9a84c;
    font-size: 0.8rem;
    float: right;
  }
  .niveau-desc {
    color: rgba(232,213,163,0.5);
    font-size: 0.75rem;
    margin-top: 4px;
    font-family: 'Cormorant Garamond', serif;
  }
  .free-badge {
    background: rgba(201,168,76,0.1);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 20px;
    padding: 4px 14px;
    font-family: 'Cinzel', serif;
    font-size: 0.65rem;
    color: #c9a84c;
    letter-spacing: 2px;
    text-transform: uppercase;
    display: inline-block;
    margin-bottom: 15px;
  }
  .divider {
    border: none;
    border-top: 1px solid rgba(201,168,76,0.15);
    margin: 20px 0;
  }
  .stButton > button {
    background: linear-gradient(135deg, #c9a84c, #a07830) !important;
    color: #0a0a0f !important;
    font-family: 'Cinzel', serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    border: none !important;
    padding: 12px 30px !important;
    border-radius: 4px !important;
    width: 100% !important;
  }
  .stTextInput input {
    background: rgba(45,27,78,0.4) !important;
    border: 1px solid rgba(201,168,76,0.3) !important;
    color: #e8d5a3 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.1rem !important;
    text-align: center !important;
    letter-spacing: 3px !important;
  }
  div[data-testid="stTextInput"] label {
    color: #c9a84c !important;
    font-family: 'Cinzel', serif !important;
    font-size: 0.65rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── PAGE LOGIN ─────────────────────────────────────────────
def page_login():
    css_login()
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # Header
    st.markdown('<div class="login-ornament">✦ ☽ ✦</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-title">ORACLE TAROT</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">Logiciel professionnel de lectures personnalisées</div>', unsafe_allow_html=True)

    # Bouton Explorateur GRATUIT
    st.markdown('<div class="free-badge">🌑 Accès Explorateur — Gratuit</div>', unsafe_allow_html=True)
    if st.button("✦ ENTRER EN MODE EXPLORATEUR", key="btn_free"):
        st.session_state["niveau"] = "FREE"
        st.session_state["connecte"] = True
        st.session_state["prenom_membre"] = "Explorateur·rice"
        st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Saisie code
    st.markdown("""
    <div style="font-family:'Cinzel',serif;font-size:0.7rem;letter-spacing:3px;color:rgba(201,168,76,0.7);margin-bottom:10px;">
      OU ENTREZ VOTRE CODE D'ACCÈS
    </div>
    """, unsafe_allow_html=True)

    code_input = st.text_input(
        "Code d'accès membre",
        placeholder="ex: LUNE-7842-OR",
        key="code_input"
    ).strip().upper()

    if st.button("✦ ACTIVER MON CODE", key="btn_code"):
        if not code_input:
            st.error("Veuillez saisir votre code.")
        else:
            result = valider_code(code_input)
            if result["valide"]:
                st.session_state["niveau"]          = result["niveau"]
                st.session_state["connecte"]        = True
                st.session_state["code_actif"]      = code_input
                st.session_state["prenom_membre"]   = result["data"].get("prenom", "")
                st.session_state["data_membre"]     = result["data"]
                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])

    # Grille des niveaux
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Cinzel',serif;font-size:0.65rem;letter-spacing:3px;color:rgba(201,168,76,0.5);margin-bottom:12px;">
      LES NIVEAUX D'ACCÈS
    </div>
    """, unsafe_allow_html=True)

    niveaux_affiches = [
        ("FREE",    "🌑", "Explorateur", "Gratuit",     "1 carte · Arcanes Majeurs · Amour"),
        ("STARTER", "⭐", "Initié·e",    "€9,99/mois",  "3 cartes · 5 secteurs · Majeurs"),
        ("PRO",     "🌙", "Praticien·ne","€27/mois",    "78 cartes · 4 tirages · Export PDF"),
        ("CERCLE",  "🔮", "Maître·sse",  "€47/mois",    "Tout PRO + boutique -20% + lives"),
    ]

    for niveau_id, emoji, nom, prix, desc in niveaux_affiches:
        st.markdown(f"""
        <div class="niveau-card">
          <span class="niveau-nom">{emoji} {nom}</span>
          <span class="niveau-prix">{prix}</span>
          <div class="niveau-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center;">
      <a href="{LIEN_ETSY}" target="_blank" style="
        color:#c9a84c;
        font-family:'Cinzel',serif;
        font-size:0.7rem;
        letter-spacing:2px;
        text-decoration:none;
      ">→ Obtenir mon code d'accès sur Etsy</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─── BANDEAU NIVEAU (affiché dans l'app après connexion) ────
def bandeau_niveau():
    """Affiche un petit bandeau en haut de l'app avec le niveau actif."""
    niveau  = st.session_state.get("niveau", "FREE")
    prenom  = st.session_state.get("prenom_membre", "")
    infos   = NIVEAUX.get(niveau, NIVEAUX["FREE"])

    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f"""
        <div style="font-family:'Cinzel',serif;font-size:0.7rem;color:rgba(201,168,76,0.6);letter-spacing:2px;">
          {infos['emoji']} {infos['nom'].upper()}
          {f" · {prenom}" if prenom else ""}
        </div>
        """, unsafe_allow_html=True)
    with col3:
        if st.button("Déconnexion", key="btn_deconnect"):
            for key in ["niveau", "connecte", "code_actif", "prenom_membre", "data_membre", "blocs"]:
                st.session_state.pop(key, None)
            st.rerun()

# ─── CADENAS GÉNÉRIQUE ──────────────────────────────────────
def afficher_cadenas(type_cadenas: str):
    """Affiche un message de cadenas avec CTA."""
    from config import CADENAS
    c = CADENAS.get(type_cadenas, {})
    st.markdown(f"""
    <div style="
      background: rgba(201,168,76,0.04);
      border: 1px dashed rgba(201,168,76,0.25);
      border-radius: 10px;
      padding: 20px;
      text-align: center;
      margin: 15px 0;
    ">
      <div style="font-size:1.5rem;margin-bottom:8px;">🔒</div>
      <div style="font-family:'Cinzel',serif;font-size:0.8rem;color:#e8d5a3;margin-bottom:8px;">
        {c.get('titre','Fonctionnalité verrouillée')}
      </div>
      <div style="font-family:'Cormorant Garamond',serif;color:rgba(232,213,163,0.6);font-size:0.9rem;margin-bottom:12px;">
        {c.get('texte','')}
      </div>
      <a href="{LIEN_ETSY}" target="_blank" style="
        color:#c9a84c;
        font-family:'Cinzel',serif;
        font-size:0.65rem;
        letter-spacing:2px;
        text-decoration:none;
      ">{c.get('cta','→ En savoir plus')}</a>
    </div>
    """, unsafe_allow_html=True)

# ─── VÉRIFICATION ACCÈS ─────────────────────────────────────
def peut_acceder(fonctionnalite: str) -> bool:
    """
    Vérifie si le niveau actuel peut accéder à une fonctionnalité.
    fonctionnalite : "cartes_mineures" | "export" | "historique" | "boutique" | etc.
    """
    niveau = st.session_state.get("niveau", "FREE")
    infos  = NIVEAUX.get(niveau, NIVEAUX["FREE"])

    mapping = {
        "cartes_mineures": lambda i: "Coupes" in i.get("familles_cartes", []),
        "export":          lambda i: i.get("export_pdf", False),
        "historique":      lambda i: i.get("historique", False),
        "boutique":        lambda i: i.get("boutique_remise", 0) > 0,
        "lives":           lambda i: i.get("lives", False),
        "tirage_5":        lambda i: i.get("tirages_max", 0) >= 5,
        "tirage_10":       lambda i: i.get("tirages_max", 0) >= 10,
        "tous_secteurs":   lambda i: len(i.get("secteurs", [])) >= 5,
    }

    check = mapping.get(fonctionnalite)
    return check(infos) if check else False
