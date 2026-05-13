import streamlit as st
import json
import random
from pathlib import Path

# ─── CONFIG ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🔮 Oracle Tarot Professionnel",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Cinzel:wght@400;600&display=swap');

  .stApp { background: #0a0a0f; }
  .main .block-container { padding-top: 1rem; }

  h1, h2, h3 { font-family: 'Cinzel', serif !important; color: #e8d5a3 !important; }

  .header-box {
    background: linear-gradient(135deg, #1a0f2e, #0a0a0f);
    border: 1px solid rgba(201,168,76,0.4);
    border-radius: 12px;
    padding: 25px 30px;
    text-align: center;
    margin-bottom: 20px;
  }
  .header-box h1 { font-size: 1.8rem; margin: 0; color: #e8d5a3 !important; }
  .header-box p { color: rgba(201,168,76,0.6); font-family: 'Cormorant Garamond', serif; font-style: italic; margin-top: 5px; }

  .stat-box {
    background: rgba(201,168,76,0.05);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 8px;
    padding: 12px;
    text-align: center;
  }
  .stat-box .num { color: #c9a84c; font-family: 'Cinzel', serif; font-size: 1.5rem; display: block; }
  .stat-box .lbl { color: rgba(201,168,76,0.5); font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase; }

  .section-label {
    font-family: 'Cinzel', serif;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #c9a84c;
    margin-bottom: 8px;
    padding-bottom: 5px;
    border-bottom: 1px solid rgba(201,168,76,0.2);
  }

  .carte-mini {
    background: linear-gradient(135deg, #2d1b4e, #1a0f2e);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 6px;
    padding: 10px;
    text-align: center;
    margin: 5px 0;
  }
  .carte-mini .emoji { font-size: 1.4rem; display: block; }
  .carte-mini .nom { color: #e8d5a3; font-family: 'Cinzel', serif; font-size: 0.75rem; }

  .discours-container {
    background: #0f0f1a;
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 12px;
    padding: 25px;
  }

  .bloc-carte {
    border-left: 2px solid rgba(201,168,76,0.3);
    padding: 12px 18px;
    margin: 15px 0;
    background: rgba(255,255,255,0.02);
    border-radius: 0 6px 6px 0;
  }
  .bloc-titre {
    color: #e8d5a3;
    font-family: 'Cinzel', serif;
    font-size: 0.8rem;
    letter-spacing: 2px;
    margin-bottom: 8px;
  }
  .bloc-texte {
    color: rgba(232,213,163,0.85);
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.05rem;
    font-style: italic;
    line-height: 1.8;
  }

  .badge-pos {
    background: rgba(201,168,76,0.15);
    border: 1px solid rgba(201,168,76,0.3);
    color: #c9a84c;
    padding: 2px 8px;
    border-radius: 20px;
    font-size: 0.6rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-family: 'Cinzel', serif;
    margin-left: 8px;
  }

  .message-final {
    background: linear-gradient(135deg, rgba(45,27,78,0.5), rgba(26,15,46,0.8));
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    margin-top: 15px;
  }
  .message-final p {
    color: #e8d5a3;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    font-style: italic;
    line-height: 1.8;
    margin: 0;
  }

  .stButton > button {
    background: linear-gradient(135deg, #c9a84c, #a07830) !important;
    color: #0a0a0f !important;
    font-family: 'Cinzel', serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    border: none !important;
    padding: 12px 20px !important;
    border-radius: 4px !important;
    width: 100% !important;
    font-weight: 600 !important;
    margin-top: 8px !important;
  }

  .stSelectbox > div > div {
    background: rgba(45,27,78,0.5) !important;
    border: 1px solid rgba(201,168,76,0.3) !important;
    color: #e8d5a3 !important;
  }

  div[data-testid="stSelectbox"] label,
  div[data-testid="stTextInput"] label,
  div[data-testid="stTextArea"] label {
    color: #c9a84c !important;
    font-family: 'Cinzel', serif !important;
    font-size: 0.65rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
  }

  div[data-testid="stRadio"] label { color: #e8d5a3 !important; }
  div[data-testid="stRadio"] p { color: #e8d5a3 !important; }
  div[data-testid="stCheckbox"] label { color: rgba(232,168,76,0.7) !important; font-size: 0.8rem !important; }

  .sidebar-section {
    background: rgba(201,168,76,0.04);
    border: 1px solid rgba(201,168,76,0.15);
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 12px;
  }

  .stTextArea textarea {
    background: rgba(45,27,78,0.3) !important;
    border: 1px solid rgba(201,168,76,0.2) !important;
    color: #e8d5a3 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 0.95rem !important;
  }

  hr { border-color: rgba(201,168,76,0.15) !important; }

  [data-testid="stSidebar"] {
    background: #0a0a12 !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── CHARGEMENT ────────────────────────────────────────────────────────────────
@st.cache_data
def charger_banque():
    # Chercher banque_complete.json d'abord, sinon banque.json
    for nom in ['banque_complete.json', 'banque.json']:
        chemin = Path(__file__).parent.parent / "data" / nom
        if chemin.exists():
            with open(chemin, 'r', encoding='utf-8') as f:
                return json.load(f)
    return {"arcanes": {}}

banque = charger_banque()
arcanes = banque["arcanes"]
noms_cartes = sorted(list(arcanes.keys()))

# Grouper par type
majeurs = [c for c in noms_cartes if arcanes[c].get('couleur') is None]
coupes = [c for c in noms_cartes if arcanes[c].get('couleur') == 'Coupes']
batons = [c for c in noms_cartes if arcanes[c].get('couleur') == 'Bâtons']
epees = [c for c in noms_cartes if arcanes[c].get('couleur') == 'Épées']
pentacles = [c for c in noms_cartes if arcanes[c].get('couleur') == 'Pentacles']

secteurs_labels = {
    "amour": "❤️ Amour & Relations",
    "travail": "💼 Travail & Carrière",
    "argent": "💰 Argent & Abondance",
    "famille": "👨‍👩‍👧 Famille & Entourage",
    "spirituel": "🌙 Spiritualité"
}

positions_5 = ["La situation actuelle", "Ce qui est caché", "Le blocage", "Ce qui s'ouvre", "La réponse finale"]
positions_3 = ["Passé", "Présent", "Futur"]
positions_1 = ["Message du jour"]
positions_celtic = ["Situation", "Défi", "Fondation", "Passé récent", "Potentiel", "Avenir proche", "Toi", "Environnement", "Espoirs/Peurs", "Résultat final"]

# ─── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
  <h1>🔮 Oracle Tarot Professionnel</h1>
  <p>Banque de lectures · Arcanes Majeurs & Mineurs · 5 secteurs</p>
</div>
""", unsafe_allow_html=True)

# Stats
nb_cartes = len(arcanes)
nb_blocs = sum(len(v) for c in arcanes.values() for v in c['secteurs'].values())
c1,c2,c3,c4 = st.columns(4)
with c1: st.markdown(f'<div class="stat-box"><span class="num">{nb_cartes}</span><span class="lbl">Cartes</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat-box"><span class="num">{nb_blocs}</span><span class="lbl">Blocs</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="stat-box"><span class="num">5</span><span class="lbl">Secteurs</span></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="stat-box"><span class="num">4</span><span class="lbl">Tirages</span></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-label">✦ Paramètres Client</div>', unsafe_allow_html=True)

    prenom = st.text_input("Prénom", placeholder="ex: Sophie", key="prenom")
    question = st.text_area("Question posée", placeholder="ex: Est-ce que cette relation peut évoluer ?", height=70, key="question")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">✦ Secteur</div>', unsafe_allow_html=True)
    secteur = st.radio("", options=list(secteurs_labels.keys()), format_func=lambda x: secteurs_labels[x], key="secteur")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">✦ Type de tirage</div>', unsafe_allow_html=True)
    tirage_type = st.radio("", ["5 cartes — Lecture complète", "3 cartes — Passé/Présent/Futur", "1 carte — Carte du jour", "10 cartes — Croix Celtique"], key="tirage")

# ─── SÉLECTION DES CARTES ──────────────────────────────────────────────────────
if "5 cartes" in tirage_type:
    positions = positions_5
    nb = 5
elif "3 cartes" in tirage_type:
    positions = positions_3
    nb = 3
elif "1 carte" in tirage_type:
    positions = positions_1
    nb = 1
else:
    positions = positions_celtic
    nb = 10

col_left, col_right = st.columns([1, 1.6], gap="large")

with col_left:
    st.markdown(f'<div class="section-label">✦ Sélection des {nb} cartes</div>', unsafe_allow_html=True)

    cartes_sel = []
    renversees = []

    # Grouper les cartes par catégorie pour la sélection
    toutes_cartes = majeurs + coupes + batons + epees + pentacles
    groupes = {
        "── Arcanes Majeurs ──": majeurs,
        "── Coupes ──": coupes,
        "── Bâtons ──": batons,
        "── Épées ──": epees,
        "── Pentacles ──": pentacles
    }

    # Créer liste avec séparateurs
    options_flat = []
    for groupe, cartes in groupes.items():
        options_flat.append(groupe)
        options_flat.extend(cartes)

    for i in range(nb):
        with st.expander(f"Position {i+1} — {positions[i]}", expanded=(i < 3)):
            # Filtre par groupe
            groupe_choix = st.selectbox(
                "Famille",
                ["Arcanes Majeurs", "Coupes", "Bâtons", "Épées", "Pentacles"],
                key=f"groupe_{i}"
            )
            mapping = {
                "Arcanes Majeurs": majeurs,
                "Coupes": coupes,
                "Bâtons": batons,
                "Épées": epees,
                "Pentacles": pentacles
            }
            cartes_du_groupe = mapping.get(groupe_choix, majeurs)
            if not cartes_du_groupe:
                cartes_du_groupe = majeurs

            carte = st.selectbox(
                "Carte",
                options=cartes_du_groupe,
                key=f"carte_{i}",
                index=i % len(cartes_du_groupe)
            )
            rev = st.checkbox("↩ Renversée", key=f"rev_{i}")

            cartes_sel.append(carte)
            renversees.append(rev)

            if carte in arcanes:
                emoji = arcanes[carte].get("emoji", "🃏")
                num = arcanes[carte].get("numero", "")
                couleur = arcanes[carte].get("couleur", "")
                info = f"{num}" + (f" • {couleur}" if couleur else "")
                st.markdown(f'<div class="carte-mini"><span class="emoji">{emoji}</span><span class="nom">{info} — {carte}{"  ↩" if rev else ""}</span></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    generer = st.button("✦ GÉNÉRER LE DISCOURS", key="gen")
    if st.button("🔄 NOUVELLES VARIANTES", key="regen"):
        if "blocs" in st.session_state:
            del st.session_state["blocs"]
        st.rerun()

# ─── GÉNÉRATION ET AFFICHAGE ───────────────────────────────────────────────────
with col_right:
    st.markdown('<div class="section-label">✦ Lecture générée</div>', unsafe_allow_html=True)

    if generer:
        blocs = []
        for i, (carte, rev) in enumerate(zip(cartes_sel, renversees)):
            if carte in arcanes and secteur in arcanes[carte]["secteurs"]:
                variantes = arcanes[carte]["secteurs"][secteur]
                idx = random.randint(0, len(variantes)-1)
                blocs.append({
                    "position": positions[i],
                    "carte": carte,
                    "emoji": arcanes[carte].get("emoji", "🃏"),
                    "numero": arcanes[carte].get("numero", ""),
                    "couleur": arcanes[carte].get("couleur", ""),
                    "renversee": rev,
                    "texte": variantes[idx],
                    "variante": idx+1
                })
        st.session_state["blocs"] = blocs
        st.session_state["meta"] = {
            "prenom": prenom or "chère âme",
            "question": question,
            "secteur": secteurs_labels[secteur],
            "tirage": tirage_type
        }

    if "blocs" in st.session_state:
        blocs = st.session_state["blocs"]
        meta = st.session_state.get("meta", {})
        prenom_a = meta.get("prenom", "chère âme")
        question_a = meta.get("question", "")
        secteur_a = meta.get("secteur", "")
        tirage_a = meta.get("tirage", "")

        with st.container():
            st.markdown('<div class="discours-container">', unsafe_allow_html=True)

            # En-tête
            st.markdown(f"""
            <div style="margin-bottom:15px; padding-bottom:12px; border-bottom:1px solid rgba(201,168,76,0.15);">
              <div style="color:#c9a84c;font-family:'Cinzel',serif;font-size:0.65rem;letter-spacing:3px;text-transform:uppercase;">
                {tirage_a} · {secteur_a}
              </div>
              <div style="color:#e8d5a3;font-family:'Cormorant Garamond',serif;font-size:1.2rem;margin-top:4px;">
                Lecture pour <strong>{prenom_a}</strong>
              </div>
              {"<div style='color:rgba(232,213,163,0.55);font-family:Cormorant Garamond,serif;font-style:italic;font-size:0.9rem;'>\"" + question_a + "\"</div>" if question_a else ""}
            </div>
            """, unsafe_allow_html=True)

            # Introduction
            intro = f"{prenom_a}… j'ai pris le temps de me connecter à ton énergie avant de tirer ces cartes. Ce que j'ai reçu est fort et clair. Voici ce que les cartes ont à te dire."
            st.markdown(f"""
            <div style="background:rgba(201,168,76,0.06);border-left:2px solid #c9a84c;padding:12px 18px;margin-bottom:15px;border-radius:0 6px 6px 0;">
              <p style="color:rgba(232,213,163,0.85);font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1rem;margin:0;">{intro}</p>
            </div>
            """, unsafe_allow_html=True)

            # Blocs par carte
            discours_txt = f"LECTURE — {prenom_a.upper()}\n{secteur_a} · {tirage_a}\n"
            if question_a: discours_txt += f"Question : {question_a}\n"
            discours_txt += "\n" + "─"*50 + "\n\n"
            discours_txt += intro + "\n\n"

            for bloc in blocs:
                rev_tag = " ↩" if bloc["renversee"] else ""
                couleur_info = f" • {bloc['couleur']}" if bloc['couleur'] else ""
                titre = f"{bloc['emoji']} {bloc['numero']}{couleur_info} — {bloc['carte']}{rev_tag}"
                pos = bloc['position']

                st.markdown(f"""
                <div class="bloc-carte">
                  <div class="bloc-titre">{titre}<span class="badge-pos">{pos}</span></div>
                  <div class="bloc-texte">{bloc['texte']}</div>
                  <div style="color:rgba(201,168,76,0.2);font-size:0.6rem;margin-top:6px;">variante #{bloc['variante']}</div>
                </div>
                """, unsafe_allow_html=True)

                discours_txt += f"[{pos.upper()}] {titre}\n{bloc['texte']}\n\n"

            # Message final
            final = f"{prenom_a}, les cartes ont parlé avec clarté et bienveillance. Ce qui se déploie dans ta vie mérite toute ton attention et ta confiance. Tu as les ressources pour traverser ce moment — les cartes ne font que te le rappeler. ✦"
            st.markdown(f"""
            <div class="message-final">
              <div style="font-size:1.2rem;color:#c9a84c;margin-bottom:10px;letter-spacing:6px;">✦ ☽ ✦</div>
              <p>{final}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            discours_txt += "─"*50 + "\n" + final

            # Zone copie
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-label">📋 Texte complet — Copier/Envoyer</div>', unsafe_allow_html=True)
            st.text_area("", value=discours_txt, height=250, key="txt_copie", label_visibility="collapsed")

    else:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:rgba(201,168,76,0.25);">
          <div style="font-size:3rem;margin-bottom:12px;">🔮</div>
          <p style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1rem;">
            Sélectionne les cartes et génère la lecture
          </p>
        </div>
        """, unsafe_allow_html=True)

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:30px;color:rgba(201,168,76,0.15);font-family:'Cinzel',serif;font-size:0.6rem;letter-spacing:3px;">
  ORACLE TAROT PROFESSIONNEL · BANQUE PRIVÉE · USAGE PERSONNEL
</div>
""", unsafe_allow_html=True)
