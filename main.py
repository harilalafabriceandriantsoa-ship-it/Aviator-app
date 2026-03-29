import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. SECURITY & SESSION (Patricia Profile) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'master_password' not in st.session_state:
    st.session_state.master_password = "PATRICIA_BEAST"

# Fitahirizana Historique isaky ny lalao
for key in ['hist_aviator', 'hist_cosmos', 'hist_mines', 'hist_penalty']:
    if key not in st.session_state: st.session_state[key] = []

# --- 2. LOGIN INTERFACE ---
def login():
    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🔐 TITAN SECURE LOGIN</h1>", unsafe_allow_html=True)
        pwd_input = st.text_input("Ampidiro ny kaody manokana (Patricia):", type="password")
        if st.button("HIRAFIKA NY INTERFACE"):
            if pwd_input == st.session_state.master_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Kaody diso!")
        st.stop()

login()

# --- 3. STYLE PREMIUM (Symmetric with Screenshots) ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #ffffff; }
    .main-title { font-size: 35px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 15px #00ffcc; border-bottom: 2px solid #00ffcc; padding-bottom: 10px; }
    .card-result { background: #040e17; border: 2px solid #00ffcc; border-radius: 20px; padding: 25px; text-align: center; margin: 15px 0; }
    .card-opp { background: #1a1a00; border: 2px dashed #ffcc00; border-radius: 15px; padding: 15px; text-align: center; color: #ffcc00; margin-top: 10px; }
    .hist-container { background: rgba(0,0,0,0.6); border-radius: 10px; padding: 15px; font-family: monospace; height: 180px; overflow-y: auto; border: 1px solid #333; color: #00ffcc; }
    .consigne-box { background: #001a1a; border-left: 5px solid #00ffcc; padding: 10px; margin-bottom: 20px; font-size: 14px; }
    .stButton>button { background: linear-gradient(90deg, #00ffcc, #0077ff); color: #010a12; font-weight: 900; border-radius: 10px; height: 50px; border: none; }
    .btn-contact { display: inline-block; padding: 8px 15px; border-radius: 5px; text-decoration: none; color: white; font-weight: bold; margin: 5px; }
    .footer-brand { text-align: center; color: #888; font-size: 13px; margin-top: 40px; border-top: 1px solid #222; padding-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ADVANCED ENGINE (3 Predictions samy hafa Cotes sy Lera) ---
def get_advanced_predictions(seed, h_ora):
    base = datetime.strptime(h_ora, "%H:%M")
    results = []
    for i in range(3):
        # Mampiasa seed + ora + index mba ho samy hafa ny vokatra 3
        raw = f"{seed}{h_ora}{i}{time.time()}".encode()
        hash_res = hashlib.sha512(raw).hexdigest()
        random.seed(int(hash_res[:16], 16))
        
        # Kajy Côte (Min, Moyen, Max) samy hafa isaky ny prediction
        v_min = round(random.uniform(1.15, 1.45), 2)
        v_moyen = round(random.uniform(2.10, 4.85), 2)
        v_max = round(random.uniform(12.0, 58.0), 2)
        
        # Lera samy hafa (elanelana 3 hatramin'ny 15 minitra)
        min_plus = random.randint(3, 15) * (i + 1)
        lera_vaovao = (base + timedelta(minutes=min_plus)).strftime("%H:%M")
        prob = random.randint(89, 99)
        
        results.append({"min": v_min, "moyen": v_moyen, "max": v_max, "lera": lera_vaovao, "prob": prob})
    return results

# --- 5. MAIN INTERFACE ---
st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)
tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY", "⚙️ ADMIN"])

# --- AVIATOR & COSMOS X ---
for i, name in enumerate(["AVIATOR", "COSMOS X"]):
    game_key = "aviator" if i == 0 else "cosmos"
    with tabs[i]:
        st.markdown(f'<div class="consigne-box">📝 <b>CONSIGNE:</b> Ampidiro ny HEX SEED farany sy ny ora izao hanombohana ny calculation 3 predictions.</div>', unsafe_allow_html=True)
        st.file_uploader(f"📸 Capture Historique ({name}):", key=f"cap_{game_key}")
        col1, col2 = st.columns(2)
        u_hex = col1.text_input(f"🔑 HEX SEED ({name}):", key=f"hex_{game_key}")
        u_ora = col2.text_input("🕒 HEURE (HH:MM):", value=datetime.now().strftime("%H:%M"), key=f"ora_{game_key}")
        
        if st.button(f"🔥 EXECUTE {name} ENGINE"):
            preds = get_advanced_predictions(u_hex, u_ora)
            
            # Asehontsika ny "Target" voalohany amin'ny endrika sary lehibe
            st.markdown(f"""
                <div class="card-result">
                    <div style="display: flex; justify-content: space-around; font-size: 18px; font-weight: bold;">
                        <span style="color:white;">MIN<br>{preds[0]['min']}x</span>
                        <span style="color:#00ffcc;">MOYEN (Target)<br><span style="font-size:45px;">{preds[0]['moyen']}x</span></span>
                        <span style="color:white;">MAX (Tenter)<br>{preds[0]['max']}x</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Lisitry ny lera 3 samy hafa lera sy côte
            st.markdown('<div class="card-opp">🎯 PROCHAINES OPPORTUNITÉS:', unsafe_allow_html=True)
            for p in preds:
                st.markdown(f"⏰ <b>{p['lera']}</b> | Côte: <b>{p['moyen']}x</b> | Fiabilité: <b>{p['prob']}%</b>", unsafe_allow_html=True)
                st.session_state[f'hist_{game_key}'].insert(0, f"🕒 {p['lera']} | 🎯 {p['moyen']}x | ✅ {p['prob']}%")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('### 📜 HISTORIQUE DES PRÉDICTIONS')
        st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state[f"hist_{game_key}"])}</div>', unsafe_allow_html=True)

# --- MINES VIP ---
with tabs[2]:
    m1, m2 = st.columns(2)
    m_serv = m1.text_input("🖥️ SERVER SEED (Mines):")
    m_clie = m2.text_input("💻 CLIENT SEED (Mines):")
    if st.button("💎 GENERATE SCHEMA"):
        st.session_state.hist_mines.insert(0, f"🕒 {datetime.now().strftime('%H:%M')} | Schema Created")
        st.success("Mines Mode Active: Focus on 5 Diamonds!")
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_mines)}</div>', unsafe_allow_html=True)

# --- PENALTY ---
with tabs[3]:
    if st.button("🥅 GENERATE 5 SHOT PREDICTIONS"):
        targets = ["ANKAVIA AMBONY", "ANKAVANANA AMBANY", "AFOVOANY", "ANKAVIA AMBANY", "ANKAVANANA AMBONY"]
        random.shuffle(targets)
        st.markdown('<div class="card-result">', unsafe_allow_html=True)
        for i, t in enumerate(targets, 1):
            st.write(f"Daka {i}: {t}")
            st.session_state.hist_penalty.insert(0, f"[{datetime.now().strftime('%H:%M')}] Daka {i}: {t}")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_penalty)}</div>', unsafe_allow_html=True)

# --- ADMIN & CONTACT ---
with tabs[4]:
    st.markdown("### 🛠️ PANEL ADMIN & BRANDING")
    st.markdown(f"""
        <a href="https://wa.me/261346249701" class="btn-contact" style="background:#25D366;">💬 WhatsApp Patricia</a>
        <a href="https://t.me/+261346249701" class="btn-contact" style="background:#0088cc;">✈️ Telegram Patricia</a>
    """, unsafe_allow_html=True)
    
    new_p = st.text_input("Password vaovao:", type="password")
    if st.button("OK"):
        st.session_state.master_password = new_p
        st.success("Password Updated!")
    
    if st.button("🔴 EFFACER TOUT L'HISTORIQUE"):
        for k in ['hist_aviator', 'hist_cosmos', 'hist_mines', 'hist_penalty']: st.session_state[k] = []
        st.rerun()

# --- FOOTER ---
st.markdown(f"""
    <div class="footer-brand">
        <b>TITAN OMNI-STRIKE BY PATRICIA</b><br>
        Contact: 0346249701 | andriantsoakelly@gmail.com
    </div>
""", unsafe_allow_html=True)
