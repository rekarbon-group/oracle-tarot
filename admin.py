import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import sys
sys.path.append(str(Path(__file__).parent.parent))
from auth.codes_manager import creer_code, valider_code, revoquer_code, renouveler_code, lister_codes, stats_db
from config import NIVEAUX, LIEN_ETSY

# ─── MOT DE PASSE ADMIN ─────────────────────────────────────
ADMIN_PASSWORD = "ORACLE-ADMIN-2026"  # ← à changer

st.set_page_config(page_title="🔐 Admin Oracle", page_icon="🔐", layout="wide")

st.markdown("""
<style>
  .stApp { background: #0a0a0f; }
  h1,h2,h3 { font-family: 'Cinzel', serif !important; color: #e8d5a3 !important; }
  .stButton > button {
    background: linear-gradient(135deg, #c9a84c, #a07830) !important;
    color: #0a0a0f !important; font-weight: 600 !important;
    border: none !important; border-radius: 4px !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── GUARD LOGIN ADMIN ──────────────────────────────────────
if not st.session_state.get("admin_ok"):
    st.markdown("## 🔐 Accès Administration")
    pwd = st.text_input("Mot de passe admin", type="password")
    if st.button("Connexion"):
        if pwd == ADMIN_PASSWORD:
            st.session_state["admin_ok"] = True
            st.rerun()
        else:
            st.error("Mot de passe incorrect.")
    st.stop()

# ─── DASHBOARD ADMIN ────────────────────────────────────────
st.markdown("## 👁️ Oracle Tarot — Dashboard Admin")

# Stats en haut
s = stats_db()
c1,c2,c3,c4,c5 = st.columns(5)
for col, label, val, color in [
    (c1, "Total codes",  s["total"],   "#888"),
    (c2, "Actifs",       s["actifs"],  "#2ecc71"),
    (c3, "⭐ STARTER",   s["par_niveau"].get("STARTER",0), "#c0c0c0"),
    (c4, "🌙 PRO",       s["par_niveau"].get("PRO",0),     "#c9a84c"),
    (c5, "🔮 CERCLE",    s["par_niveau"].get("CERCLE",0),  "#9b59b6"),
]:
    with col:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:12px;text-align:center;">
          <div style="color:{color};font-size:1.6rem;font-weight:bold;">{val}</div>
          <div style="color:#888;font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["➕ Créer un code", "📋 Liste des codes", "🔧 Gérer un code", "📊 Stats"])

# ─── TAB 1 : CRÉER ──────────────────────────────────────────
with tab1:
    st.markdown("### Générer un nouveau code d'accès")
    col_a, col_b = st.columns(2)
    with col_a:
        niveau_choix = st.selectbox("Niveau", ["STARTER","PRO","CERCLE","ADMIN"],
                                    format_func=lambda x: f"{NIVEAUX[x]['emoji']} {x} — {NIVEAUX[x]['nom']} ({NIVEAUX[x]['prix']})")
        prenom_client = st.text_input("Prénom client")
        email_client  = st.text_input("Email client")
    with col_b:
        duree = st.number_input("Durée (jours)", min_value=1, max_value=365, value=30)
        note  = st.text_area("Note interne", height=80)

    if st.button("✦ GÉNÉRER LE CODE"):
        entree = creer_code(niveau=niveau_choix, email=email_client, prenom=prenom_client, duree_jours=int(duree), note=note)
        infos_n = NIVEAUX[niveau_choix]
        st.success(f"Code créé : **{entree['code']}**")
        st.code(f"""
📧 Email à envoyer à {prenom_client or 'votre client'} :

Bonjour {prenom_client or ''} ✨

Votre code d'accès Oracle Tarot est prêt.

🔮 Code : {entree['code']}
Niveau  : {infos_n['emoji']} {infos_n['nom']}
Valable jusqu'au : {entree['expire_le']}

→ Activez votre code sur l'application :
[LIEN STREAMLIT ICI]

Bienvenue dans Le Cercle des Étoiles ✦
""", language="text")

# ─── TAB 2 : LISTE ──────────────────────────────────────────
with tab2:
    st.markdown("### Tous les codes")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filtre_n = st.selectbox("Filtrer par niveau", ["Tous","STARTER","PRO","CERCLE","ADMIN"])
    with col_f2:
        actifs_seul = st.checkbox("Actifs seulement", value=True)

    codes = lister_codes(
        filtre_niveau=None if filtre_n == "Tous" else filtre_n,
        actifs_seulement=actifs_seul
    )

    if not codes:
        st.info("Aucun code trouvé.")
    else:
        maintenant = datetime.now()
        rows = []
        for c in codes:
            expire = datetime.strptime(c["expire_le"], "%Y-%m-%d")
            jours_restants = (expire - maintenant).days
            statut = "✅ Actif" if c.get("actif") and jours_restants > 0 else ("⏰ Expiré" if jours_restants <= 0 else "❌ Révoqué")
            infos_n = NIVEAUX.get(c["niveau"], {})
            rows.append({
                "Code":        c["code"],
                "Niveau":      f"{infos_n.get('emoji','')} {c['niveau']}",
                "Prénom":      c.get("prenom","—"),
                "Email":       c.get("email","—"),
                "Expire":      c["expire_le"],
                "J. restants": jours_restants,
                "Connexions":  c.get("nb_connexions",0),
                "Statut":      statut,
            })
        st.dataframe(rows, use_container_width=True)
        st.caption(f"{len(rows)} code(s) trouvé(s).")

# ─── TAB 3 : GÉRER ──────────────────────────────────────────
with tab3:
    st.markdown("### Gérer un code existant")
    code_gere = st.text_input("Code à gérer", placeholder="LUNE-7842-OR").strip().upper()

    if code_gere:
        result = valider_code(code_gere)
        if result["data"]:
            d = result["data"]
            infos_n = NIVEAUX.get(d["niveau"], {})
            st.markdown(f"""
            **Code :** `{d['code']}`  
            **Niveau :** {infos_n.get('emoji','')} {d['niveau']} — {infos_n.get('nom','')}  
            **Client :** {d.get('prenom','—')} ({d.get('email','—')})  
            **Expire :** {d['expire_le']}  
            **Connexions :** {d.get('nb_connexions',0)}  
            **Actif :** {'✅ Oui' if d.get('actif') else '❌ Non'}
            """)
            col_x, col_y = st.columns(2)
            with col_x:
                duree_renouv = st.number_input("Renouveler (jours)", min_value=1, max_value=365, value=30, key="renouv")
                if st.button("🔄 Renouveler"):
                    ok = renouveler_code(code_gere, int(duree_renouv))
                    st.success("Code renouvelé.") if ok else st.error("Erreur.")
            with col_y:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("❌ Révoquer ce code", type="secondary"):
                    ok = revoquer_code(code_gere)
                    st.success("Code révoqué.") if ok else st.error("Erreur.")
        else:
            st.warning(f"Code introuvable : {code_gere}")

# ─── TAB 4 : STATS ──────────────────────────────────────────
with tab4:
    st.markdown("### Statistiques globales")
    s = stats_db()
    st.json(s)
    if st.button("🔄 Rafraîchir"):
        st.rerun()
    if st.button("🚪 Déconnexion admin"):
        st.session_state.pop("admin_ok", None)
        st.rerun()
