import streamlit as st
import json
import random
from pathlib import Path
from datetime import datetime, timedelta

NIVEAUX = {
    "FREE":    {"nom":"Explorateur","emoji":"🌑","prix":"Gratuit","tirages_max":1,"types_tirage":["1 carte"],"secteurs":["amour"],"familles_cartes":["Arcanes Majeurs"],"export_pdf":False,"boutique_remise":0,"lives":False},
    "STARTER": {"nom":"Initié·e","emoji":"⭐","prix":"€9,99/mois","tirages_max":3,"types_tirage":["1 carte","3 cartes — Passé/Présent/Futur"],"secteurs":["amour","travail","argent","famille","spirituel"],"familles_cartes":["Arcanes Majeurs"],"export_pdf":False,"boutique_remise":0,"lives":False},
    "PRO":     {"nom":"Praticien·ne","emoji":"🌙","prix":"€27/mois","tirages_max":10,"types_tirage":["1 carte","3 cartes — Passé/Présent/Futur","5 cartes — Lecture complète","10 cartes — Croix Celtique"],"secteurs":["amour","travail","argent","famille","spirituel"],"familles_cartes":["Arcanes Majeurs","Coupes","Bâtons","Épées","Pentacles"],"export_pdf":True,"boutique_remise":0,"lives":False},
    "CERCLE":  {"nom":"Maître·sse","emoji":"🔮","prix":"€47/mois","tirages_max":10,"types_tirage":["1 carte","3 cartes — Passé/Présent/Futur","5 cartes — Lecture complète","10 cartes — Croix Celtique"],"secteurs":["amour","travail","argent","famille","spirituel"],"familles_cartes":["Arcanes Majeurs","Coupes","Bâtons","Épées","Pentacles"],"export_pdf":True,"boutique_remise":20,"lives":True,"code_promo_boutique":"CERCLE20"},
    "ADMIN":   {"nom":"Admin","emoji":"👁️","prix":"—","tirages_max":999,"types_tirage":["1 carte","3 cartes — Passé/Présent/Futur","5 cartes — Lecture complète","10 cartes — Croix Celtique"],"secteurs":["amour","travail","argent","famille","spirituel"],"familles_cartes":["Arcanes Majeurs","Coupes","Bâtons","Épées","Pentacles"],"export_pdf":True,"boutique_remise":100,"lives":True},
}
SECTEURS_LABELS = {"amour":"❤️ Amour & Relations","travail":"💼 Travail & Carrière","argent":"💰 Argent & Abondance","famille":"👨‍👩‍👧 Famille & Entourage","spirituel":"🌙 Spiritualité"}
POSITIONS_TIRAGE = {
    "1 carte":["Message du jour"],
    "3 cartes — Passé/Présent/Futur":["Passé","Présent","Futur"],
    "5 cartes — Lecture complète":["La situation actuelle","Ce qui est caché","Le blocage","Ce qui s'ouvre","La réponse finale"],
    "10 cartes — Croix Celtique":["Situation","Défi","Fondation","Passé récent","Potentiel","Avenir proche","Toi","Environnement","Espoirs/Peurs","Résultat final"],
}
LIEN_ETSY = "https://www.etsy.com/fr/shop/TON_SHOP"
CADENAS = {
    "cartes_mineures":{"titre":"🔒 Arcanes Mineurs verrouillés","texte":"Accessibles au niveau PRO (€27/mois).","cta":"→ Passer PRO"},
    "export":{"titre":"🔒 Export verrouillé","texte":"Export PDF disponible au niveau PRO (€27/mois).","cta":"→ Passer PRO"},
    "boutique":{"titre":"🔒 Remise boutique réservée","texte":"La remise -20% est réservée au Cercle (€47/mois).","cta":"→ Rejoindre le Cercle"},
}
DB_PATH = Path("codes_db.json")

def init_db():
    if not DB_PATH.exists():
        DB_PATH.write_text(json.dumps({"codes":{}},indent=2))

def charger_db():
    init_db()
    return json.loads(DB_PATH.read_text(encoding="utf-8"))

def sauvegarder_db(data):
    DB_PATH.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8")

def valider_code(code):
    code = code.strip().upper()
    db = charger_db()
    if code not in db["codes"]:
        return {"valide":False,"niveau":"FREE","message":"Code introuvable. Vérifiez votre saisie.","data":{}}
    e = db["codes"][code]
    if not e.get("actif",True):
        return {"valide":False,"niveau":"FREE","message":"Code désactivé. Contactez le support.","data":{}}
    if datetime.now() > datetime.strptime(e["expire_le"],"%Y-%m-%d"):
        return {"valide":False,"niveau":"FREE","message":f"Code expiré le {e['expire_le']}.","data":e}
    e["nb_connexions"] = e.get("nb_connexions",0)+1
    e["derniere_connexion"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    db["codes"][code] = e
    sauvegarder_db(db)
    infos = NIVEAUX.get(e["niveau"],NIVEAUX["FREE"])
    return {"valide":True,"niveau":e["niveau"],"message":f"Bienvenue {e.get('prenom','')} ✦ Accès {infos['nom']} activé.","data":e}

def peut_acceder(f):
    niveau = st.session_state.get("niveau","FREE")
    infos  = NIVEAUX.get(niveau,NIVEAUX["FREE"])
    m = {
        "cartes_mineures": lambda i: "Coupes" in i.get("familles_cartes",[]),
        "export":          lambda i: i.get("export_pdf",False),
        "boutique":        lambda i: i.get("boutique_remise",0)>0,
    }
    check = m.get(f)
    return check(infos) if check else False

st.set_page_config(page_title="🔮 Oracle Tarot",page_icon="🔮",layout="wide",initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Cinzel:wght@400;600&display=swap');
.stApp{background:#080810}
.main .block-container{padding-top:1rem}
h1,h2,h3{font-family:'Cinzel',serif !important;color:#e8d5a3 !important}
.header-box{background:linear-gradient(135deg,#1a0f2e,#0a0a0f);border:1px solid rgba(201,168,76,0.4);border-radius:12px;padding:20px 30px;margin-bottom:15px}
.header-box h1{font-size:1.6rem;margin:0;color:#e8d5a3 !important}
.header-box p{color:rgba(201,168,76,0.5);font-family:'Cormorant Garamond',serif;font-style:italic;margin:3px 0 0}
.slabel{font-family:'Cinzel',serif;font-size:0.65rem;letter-spacing:3px;text-transform:uppercase;color:#c9a84c;margin-bottom:8px;padding-bottom:5px;border-bottom:1px solid rgba(201,168,76,0.2)}
.bloc-carte{border-left:2px solid rgba(201,168,76,0.3);padding:12px 18px;margin:12px 0;background:rgba(255,255,255,0.02);border-radius:0 6px 6px 0}
.bloc-titre{color:#e8d5a3;font-family:'Cinzel',serif;font-size:0.75rem;letter-spacing:2px;margin-bottom:6px}
.bloc-texte{color:rgba(232,213,163,0.85);font-family:'Cormorant Garamond',serif;font-size:1rem;font-style:italic;line-height:1.8}
.discours-box{background:#0f0f1a;border:1px solid rgba(201,168,76,0.2);border-radius:10px;padding:20px}
.message-final{background:linear-gradient(135deg,rgba(45,27,78,0.5),rgba(26,15,46,0.8));border:1px solid rgba(201,168,76,0.3);border-radius:10px;padding:18px;text-align:center;margin-top:12px}
.message-final p{color:#e8d5a3;font-family:'Cormorant Garamond',serif;font-size:1rem;font-style:italic;line-height:1.8;margin:0}
.cadenas-box{background:rgba(201,168,76,0.04);border:1px dashed rgba(201,168,76,0.25);border-radius:10px;padding:18px;text-align:center;margin:12px 0}
.cadenas-inline{background:rgba(201,168,76,0.04);border:1px dashed rgba(201,168,76,0.2);border-radius:6px;padding:10px;text-align:center;margin:5px 0;color:rgba(201,168,76,0.5);font-family:'Cinzel',serif;font-size:0.65rem;letter-spacing:2px}
.niveau-card{background:rgba(201,168,76,0.05);border:1px solid rgba(201,168,76,0.2);border-radius:8px;padding:12px;margin:6px 0}
.stButton>button{background:linear-gradient(135deg,#c9a84c,#a07830) !important;color:#0a0a0f !important;font-family:'Cinzel',serif !important;font-size:0.7rem !important;letter-spacing:3px !important;text-transform:uppercase !important;border:none !important;padding:10px 20px !important;border-radius:4px !important;width:100% !important}
.stTextInput input{background:rgba(45,27,78,0.4) !important;border:1px solid rgba(201,168,76,0.3) !important;color:#e8d5a3 !important}
div[data-testid="stSelectbox"] label,div[data-testid="stTextInput"] label,div[data-testid="stTextArea"] label,div[data-testid="stRadio"]>label{color:#c9a84c !important;font-family:'Cinzel',serif !important;font-size:0.65rem !important;letter-spacing:2px !important;text-transform:uppercase !important}
div[data-testid="stCheckbox"] label{color:rgba(232,213,163,0.7) !important;font-size:0.8rem !important}
[data-testid="stSidebar"]{background:#0a0a12 !important}
.stTextArea textarea{background:rgba(45,27,78,0.3) !important;border:1px solid rgba(201,168,76,0.2) !important;color:#e8d5a3 !important}
</style>
""",unsafe_allow_html=True)

def afficher_cadenas(t):
    c = CADENAS.get(t,{})
    st.markdown(f'<div class="cadenas-box"><div style="font-size:1.3rem;margin-bottom:6px;">🔒</div><div style="font-family:Cinzel,serif;font-size:0.75rem;color:#e8d5a3;margin-bottom:6px;">{c.get("titre","Verrouillé")}</div><div style="font-family:Cormorant Garamond,serif;color:rgba(232,213,163,0.6);font-size:0.9rem;margin-bottom:10px;">{c.get("texte","")}</div><a href="{LIEN_ETSY}" target="_blank" style="color:#c9a84c;font-family:Cinzel,serif;font-size:0.6rem;letter-spacing:2px;text-decoration:none;">{c.get("cta","→ En savoir plus")}</a></div>',unsafe_allow_html=True)

@st.cache_data
def charger_banque():
    for nom in ["banque_complete.json","banque.json"]:
        p = Path(nom)
        if p.exists():
            with open(p,"r",encoding="utf-8") as f:
                return json.load(f)
    return {"arcanes":{}}

if not st.session_state.get("connecte"):
    _,col,_ = st.columns([1,2,1])
    with col:
        st.markdown('<div style="font-size:40px;text-align:center;color:#c9a84c;letter-spacing:10px;margin-bottom:15px;">✦ ☽ ✦</div>',unsafe_allow_html=True)
        st.markdown('<div style="font-family:Cinzel,serif;font-size:1.5rem;color:#e8d5a3;text-align:center;letter-spacing:3px;margin-bottom:5px;">ORACLE TAROT</div>',unsafe_allow_html=True)
        st.markdown('<div style="font-family:Cormorant Garamond,serif;font-style:italic;color:rgba(201,168,76,0.6);text-align:center;margin-bottom:20px;">Logiciel professionnel de lectures personnalisées</div>',unsafe_allow_html=True)
        if st.button("🌑 ENTRER EN MODE EXPLORATEUR — Gratuit",key="btn_free"):
            st.session_state.update({"niveau":"FREE","connecte":True,"prenom_membre":"Explorateur·rice"})
            st.rerun()
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;font-family:Cinzel,serif;font-size:0.6rem;letter-spacing:3px;color:rgba(201,168,76,0.5);margin-bottom:8px;">OU ENTREZ VOTRE CODE D\'ACCÈS</div>',unsafe_allow_html=True)
        code_input = st.text_input("Code d'accès",placeholder="ex: LUNE-7842-OR",key="code_input").strip().upper()
        if st.button("✦ ACTIVER MON CODE",key="btn_code"):
            if not code_input:
                st.error("Veuillez saisir votre code.")
            else:
                result = valider_code(code_input)
                if result["valide"]:
                    st.session_state.update({"niveau":result["niveau"],"connecte":True,"code_actif":code_input,"prenom_membre":result["data"].get("prenom",""),"data_membre":result["data"]})
                    st.success(result["message"])
                    st.rerun()
                else:
                    st.error(result["message"])
        st.markdown("<br>",unsafe_allow_html=True)
        for emoji,nom,prix,desc in [("🌑","Explorateur","Gratuit","1 carte · Arcanes Majeurs · Amour"),("⭐","Initié·e","€9,99/mois","3 cartes · 5 secteurs · Majeurs"),("🌙","Praticien·ne","€27/mois","78 cartes · 4 tirages · Export PDF"),("🔮","Maître·sse","€47/mois","Tout PRO + boutique -20% + lives")]:
            st.markdown(f'<div class="niveau-card"><span style="font-family:Cinzel,serif;font-size:0.8rem;color:#e8d5a3;letter-spacing:2px;">{emoji} {nom}</span><span style="color:#c9a84c;font-size:0.75rem;float:right;">{prix}</span><div style="color:rgba(232,213,163,0.5);font-size:0.72rem;margin-top:3px;font-family:Cormorant Garamond,serif;">{desc}</div></div>',unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:center;margin-top:12px;"><a href="{LIEN_ETSY}" target="_blank" style="color:#c9a84c;font-family:Cinzel,serif;font-size:0.6rem;letter-spacing:2px;text-decoration:none;">→ Obtenir mon code sur Etsy</a></div>',unsafe_allow_html=True)
    st.stop()

banque  = charger_banque()
arcanes = banque.get("arcanes",{})
majeurs   = [c for c in arcanes if not arcanes[c].get("couleur")]
coupes    = [c for c in arcanes if arcanes[c].get("couleur")=="Coupes"]
batons    = [c for c in arcanes if arcanes[c].get("couleur")=="Bâtons"]
epees     = [c for c in arcanes if arcanes[c].get("couleur")=="Épées"]
pentacles = [c for c in arcanes if arcanes[c].get("couleur")=="Pentacles"]
FAMILLES  = {"Arcanes Majeurs":majeurs or ["Le Mat"],"Coupes":coupes or ["As de Coupes"],"Bâtons":batons or ["As de Bâtons"],"Épées":epees or ["As d'Épées"],"Pentacles":pentacles or ["As de Pentacles"]}

niveau  = st.session_state.get("niveau","FREE")
infos   = NIVEAUX.get(niveau,NIVEAUX["FREE"])
prenom_m= st.session_state.get("prenom_membre","")

st.markdown(f'<div class="header-box"><h1>🔮 Oracle Tarot Professionnel</h1><p>{infos["emoji"]} {infos["nom"]} · {infos["prix"]}{f" · {prenom_m}" if prenom_m else ""}</p></div>',unsafe_allow_html=True)
c1,c2 = st.columns([5,1])
with c2:
    if st.button("Déconnexion",key="deco"):
        for k in ["niveau","connecte","code_actif","prenom_membre","data_membre","blocs"]:
            st.session_state.pop(k,None)
        st.rerun()
st.markdown("---")

with st.sidebar:
    st.markdown('<div class="slabel">✦ Client</div>',unsafe_allow_html=True)
    prenom   = st.text_input("Prénom",placeholder="Sophie")
    question = st.text_area("Question",placeholder="Sur quoi porte la lecture ?",height=70)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown('<div class="slabel">✦ Secteur</div>',unsafe_allow_html=True)
    secteurs_dispo   = infos.get("secteurs",["amour"])
    secteurs_options = {k:v for k,v in SECTEURS_LABELS.items() if k in secteurs_dispo}
    secteur = st.radio("",list(secteurs_options.keys()),format_func=lambda x:secteurs_options[x])
    for s in [k for k in SECTEURS_LABELS if k not in secteurs_dispo]:
        st.markdown(f'<div class="cadenas-inline">🔒 {SECTEURS_LABELS[s]}</div>',unsafe_allow_html=True)
    if niveau=="FREE":
        st.markdown(f'<div style="text-align:center;margin-top:5px;"><a href="{LIEN_ETSY}" style="color:#c9a84c;font-family:Cinzel,serif;font-size:0.6rem;">→ Débloquer</a></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown('<div class="slabel">✦ Tirage</div>',unsafe_allow_html=True)
    tirages_dispo = infos.get("types_tirage",["1 carte"])
    tirage_type   = st.radio("",tirages_dispo)
    for t in [x for x in POSITIONS_TIRAGE if x not in tirages_dispo]:
        st.markdown(f'<div class="cadenas-inline">🔒 {t}</div>',unsafe_allow_html=True)

positions     = POSITIONS_TIRAGE.get(tirage_type,["Message du jour"])
nb            = len(positions)
familles_ok   = infos.get("familles_cartes",["Arcanes Majeurs"])
col_left,col_right = st.columns([1,1.6],gap="large")

with col_left:
    st.markdown(f'<div class="slabel">✦ Les {nb} carte{"s" if nb>1 else ""}</div>',unsafe_allow_html=True)
    cartes_sel,renversees = [],[]
    for i,pos in enumerate(positions):
        with st.expander(f"Position {i+1} — {pos}",expanded=(i<2)):
            famille_choix = st.selectbox("Famille",familles_ok,key=f"fam_{i}")
            groupe        = FAMILLES.get(famille_choix,majeurs)
            if not groupe: groupe = ["Le Mat"]
            carte = st.selectbox("Carte",groupe,index=i%len(groupe),key=f"carte_{i}")
            rev   = st.checkbox("↩ Renversée",key=f"rev_{i}")
            cartes_sel.append(carte); renversees.append(rev)
            if carte in arcanes:
                e2 = arcanes[carte].get("emoji","🃏"); n2 = arcanes[carte].get("numero","")
                st.markdown(f'<div style="background:linear-gradient(135deg,#2d1b4e,#1a0f2e);border:1px solid rgba(201,168,76,0.3);border-radius:6px;padding:8px;text-align:center;margin-top:5px;"><span style="font-size:1.2rem;">{e2}</span><span style="color:#e8d5a3;font-family:Cinzel,serif;font-size:0.65rem;display:block;margin-top:2px;">{n2} — {carte}{"  ↩" if rev else ""}</span></div>',unsafe_allow_html=True)
        if i==0 and not peut_acceder("cartes_mineures"):
            st.markdown('<div class="cadenas-inline">🔒 Arcanes Mineurs — niveau PRO</div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    generer = st.button("✦ GÉNÉRER LE DISCOURS",key="gen")
    if st.button("🔄 NOUVELLES VARIANTES",key="regen"):
        st.session_state.pop("blocs",None); st.rerun()

with col_right:
    st.markdown('<div class="slabel">✦ Lecture générée</div>',unsafe_allow_html=True)
    if generer:
        blocs = []
        for i,(carte,rev) in enumerate(zip(cartes_sel,renversees)):
            if carte in arcanes and secteur in arcanes[carte].get("secteurs",{}):
                variantes = arcanes[carte]["secteurs"][secteur]
                if variantes:
                    idx = random.randint(0,len(variantes)-1)
                    blocs.append({"position":positions[i],"carte":carte,"emoji":arcanes[carte].get("emoji","🃏"),"numero":arcanes[carte].get("numero",""),"couleur":arcanes[carte].get("couleur",""),"renversee":rev,"texte":variantes[idx],"variante":idx+1})
        st.session_state["blocs"] = blocs
        st.session_state["meta"]  = {"prenom":prenom or "chère âme","question":question,"secteur":SECTEURS_LABELS.get(secteur,""),"tirage":tirage_type}

    if "blocs" in st.session_state and st.session_state["blocs"]:
        blocs=st.session_state["blocs"]; meta=st.session_state.get("meta",{})
        pa=meta.get("prenom","chère âme"); qa=meta.get("question",""); sa=meta.get("secteur",""); ta=meta.get("tirage","")
        st.markdown('<div class="discours-box">',unsafe_allow_html=True)
        st.markdown(f'<div style="margin-bottom:12px;padding-bottom:10px;border-bottom:1px solid rgba(201,168,76,0.15);"><div style="color:#c9a84c;font-family:Cinzel,serif;font-size:0.6rem;letter-spacing:3px;">{ta} · {sa}</div><div style="color:#e8d5a3;font-family:Cormorant Garamond,serif;font-size:1.1rem;margin-top:3px;">Pour <strong>{pa}</strong></div>{"<div style=\'color:rgba(232,213,163,0.5);font-style:italic;font-size:0.85rem;\'>\"" + qa + "\"</div>" if qa else ""}</div>',unsafe_allow_html=True)
        intro = f"{pa}… j'ai pris le temps de me connecter à ton énergie avant de tirer ces cartes. Ce que j'ai reçu est fort et clair."
        st.markdown(f'<div style="background:rgba(201,168,76,0.06);border-left:2px solid #c9a84c;padding:10px 16px;margin-bottom:12px;border-radius:0 6px 6px 0;"><p style="color:rgba(232,213,163,0.85);font-family:Cormorant Garamond,serif;font-style:italic;font-size:0.95rem;margin:0;">{intro}</p></div>',unsafe_allow_html=True)
        txt = f"LECTURE — {pa.upper()}\n{sa} · {ta}\n" + (f"Question : {qa}\n" if qa else "") + "\n"+"─"*50+"\n\n"+intro+"\n\n"
        for b in blocs:
            rt=(" ↩" if b["renversee"] else ""); ci=(f" · {b['couleur']}" if b['couleur'] else ""); ti=f"{b['emoji']} {b['numero']}{ci} — {b['carte']}{rt}"
            st.markdown(f'<div class="bloc-carte"><div class="bloc-titre">{ti}<span style="background:rgba(201,168,76,0.15);border:1px solid rgba(201,168,76,0.3);color:#c9a84c;padding:1px 7px;border-radius:20px;font-size:0.55rem;letter-spacing:2px;margin-left:8px;">{b["position"]}</span></div><div class="bloc-texte">{b["texte"]}</div></div>',unsafe_allow_html=True)
            txt += f"[{b['position'].upper()}] {ti}\n{b['texte']}\n\n"
        final = f"{pa}, les cartes ont parlé avec clarté et bienveillance. Tu as les ressources pour traverser ce moment. ✦"
        st.markdown(f'<div class="message-final"><div style="font-size:1.1rem;color:#c9a84c;margin-bottom:8px;letter-spacing:6px;">✦ ☽ ✦</div><p>{final}</p></div>',unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
        txt += "─"*50+"\n"+final
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown('<div class="slabel">📋 Texte complet</div>',unsafe_allow_html=True)
        st.text_area("",value=txt,height=200,label_visibility="collapsed")
        if not peut_acceder("export"): afficher_cadenas("export")
    else:
        st.markdown('<div style="text-align:center;padding:50px 20px;color:rgba(201,168,76,0.2);"><div style="font-size:2.5rem;margin-bottom:10px;">🔮</div><p style="font-family:Cormorant Garamond,serif;font-style:italic;">Sélectionne tes cartes et génère la lecture</p></div>',unsafe_allow_html=True)

    st.markdown("---")
    if peut_acceder("boutique"):
        r=infos.get("boutique_remise",0); cp=infos.get("code_promo_boutique","")
        st.markdown(f'<div style="background:linear-gradient(135deg,rgba(155,89,182,0.15),rgba(45,27,78,0.3));border:1px solid rgba(155,89,182,0.3);border-radius:10px;padding:16px;text-align:center;"><div style="font-family:Cinzel,serif;font-size:0.75rem;color:#9b59b6;letter-spacing:3px;margin-bottom:6px;">🔮 BOUTIQUE CERCLE</div><div style="color:#e8d5a3;font-family:Cormorant Garamond,serif;font-size:1rem;margin-bottom:8px;">-{r}% sur toute la boutique ésotérique</div><div style="color:#c9a84c;font-family:Cinzel,serif;font-size:0.8rem;letter-spacing:3px;">Code : {cp}</div></div>',unsafe_allow_html=True)
    else:
        afficher_cadenas("boutique")

st.markdown('<div style="text-align:center;margin-top:20px;color:rgba(201,168,76,0.12);font-family:Cinzel,serif;font-size:0.55rem;letter-spacing:3px;">ORACLE TAROT PROFESSIONNEL · USAGE PRIVÉ</div>',unsafe_allow_html=True)
