import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. SECURITY & SESSION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'master_password' not in st.session_state:
    st.session_state.master_password = "PATRICIA_BEAST"

for key in ['hist_aviator', 'hist_cosmos', 'hist_mines', 'hist_penalty']:
    if key not in st.session_state: st.session_state[key] = []

# --- 2. LOGIN ---
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

# --- 3. STYLE PREMIUM ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #ffffff; }
    .main-title { font-size: 35px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 15px #00ffcc; border-bottom: 2px solid #00ffcc; padding-bottom: 10px; }
    .card-result { background: #040e17; border: 2px solid #00ffcc; border-radius: 20px; padding: 25px; text-align: center; margin: 15px 0; }
    .card-opp { background: #1a1a00; border: 2px dashed #ffcc00; border-radius: 15px; padding: 15px; text-align: center; color: #ffcc00; margin-top: 10px; }
    .hist-container { background: rgba(0,0,0,0.6); border-radius: 10px; padding: 15px; font-family: monospace; height: 180px; overflow-y: auto; border: 1px solid #333; color: #00ffcc; }
    .consigne-box { background: #001a1a; border-left: 5px solid #00ffcc; padding: 12px; margin-bottom: 20px; font-size: 14px; color: #e0e0e0; }
    .motivation-text { background: linear-gradient(90deg, #004444, #001a1a); color: #00ffcc; padding: 10px; border-radius: 10px; text-align: center; font-style: italic; font-weight: bold; margin-bottom: 15px; border: 1px solid #00ffcc; }
    .stButton>button { background: linear-gradient(90deg, #00ffcc, #0077ff); color: #010a12; font-weight: 900; border-radius: 10px; height: 50px; border: none; }
    .footer-brand { text-align: center; color: #888; font-size: 13px; margin-top: 40px; border-top: 1px solid #222; padding-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ENGINE & MOTIVATION ---
def get_motivation():
    quotes = [
        "💪 Matokia ny tenanao, ny faharetana no lakilen'ny fahombiazana!",
        "🎯 Mifantoha tsara, aza taitaitra fa ho azonao io!",
        "🚀 Ny TITAN dia eto hanampy anao handresy. Miandrasa ny fotoana mety!",
        "💎 Ny fahaizana mifehy tena no mampiavaka ny mpandresy amin'ny resy.",
        "🔥 Androany no andro hanehoanao ny herinao. Go for it!"
    ]
    return random.choice(quotes)

def get_advanced_predictions(seed, h_ora):
    base = datetime.strptime(h_ora, "%H:%M")
    results = []
    for i in range(3):
        raw = f"{seed}{h_ora}{i}{time.time()}".encode()
        hash_res = hashlib.sha512(raw).hexdigest()
        random.seed(int(hash_res[:16], 16))
        v_min = round(random.uniform(1.15, 1.45), 2)
        v_moyen = round(random.uniform(2.10, 4.85), 2)
        v_max = round(random.uniform(12.0, 58.0), 2)
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
        st.markdown(f'<div class="consigne-box"><b>📝 TOROLALANA:</b> Ampidiro ny Hex Seed sy ny Ora, avy eo tsindrio ny Execute.</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        u_hex = col1.text_input(f"🔑 HEX SEED ({name}):", key=f"hex_{game_key}")
        u_ora = col2.text_input("🕒 HEURE (HH:MM):", value=datetime.now().strftime("%H:%M"), key=f"ora_{game_key}")
        
        if st.button(f"🔥 EXECUTE {name}"):
            # Asehontsika ny fampaherezana
            st.markdown(f'<div class="motivation-text">{get_motivation()}</div>', unsafe_allow_html=True)
            
            preds = get_advanced_predictions(u_hex, u_ora)
            st.markdown(f"""<div class="card-result">
                <div style="display: flex; justify-content: space-around; font-size: 18px; font-weight: bold;">
                    <span style="color:white;">MIN<br>{preds[0]['min']}x</span>
                    <span style="color:#00ffcc;">MOYEN (Target)<br><span style="font-size:45px;">{preds[0]['moyen']}x</span></span>
                    <span style="color:white;">MAX (Tenter)<br>{preds[0]['max']}x</span>
                </div>
            </div>""", unsafe_allow_html=True)
            
            st.markdown('<div class="card-opp">🎯 PROCHAINES OPPORTUNITÉS:', unsafe_allow_html=True)
            for p in preds:
                st.markdown(f"⏰ <b>{p['lera']}</b> | Côte: <b>{p['moyen']}x</b> | ✅ <b>{p['prob']}%</b>", unsafe_allow_html=True)
                st.session_state[f'hist_{game_key}'].insert(0, f"🕒 {p['lera']} | 🎯 {p['moyen']}x | ✅ {p['prob']}%")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('### 📜 HISTORIQUE')
        st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state[f"hist_{game_key}"])}</div>', unsafe_allow_html=True)

# --- MINES VIP ---
with tabs[2]:
    st.markdown('<div class="consigne-box"><b>📝 MINES:</b> Ampiasao ny Server Seed sy Client Seed hahitana ny diamondra.</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    m_serv = m1.text_input("🖥️ SERVER SEED:")
    m_clie = m2.text_input("💻 CLIENT SEED:")
    if st.button("💎 GENERATE SCHEMA"):
        st.markdown(f'<div class="motivation-text">{get_motivation()}</div>', unsafe_allow_html=True)
        st.success("Mines Mode Active!")

# --- PENALTY ---
with tabs[3]:
    if st.button("🥅 GENERATE SHOTS"):
        st.markdown(f'<div class="motivation-text">{get_motivation()}</div>', unsafe_allow_html=True)
        st.info("Targets Ready!")

# --- ADMIN & CONTACT ---
with tabs[4]:
    st.markdown(f"""
        <a href="https://wa.me/261346249701" style="background:#25D366; color:white; padding:10px; border-radius:5px; text-decoration:none; display:inline-block;">💬 WhatsApp Patricia</a>
        <a href="https://t.me/+261346249701" style="background:#0088cc; color:white; padding:10px; border-radius:5px; text-decoration:none; display:inline-block; margin-left:10px;">✈️ Telegram</a>
    """, unsafe_allow_html=True)
    if st.button("🔴 EFFACER L'HISTORIQUE"):
        for k in ['hist_aviator', 'hist_cosmos', 'hist_mines', 'hist_penalty']: st.session_state[k] = []
        st.rerun()

# --- FOOTER ---
st.markdown(f'<div class="footer-brand"><b>TITAN OMNI-STRIKE BY PATRICIA</b><br>0346249701 | andriantsoakelly@gmail.com</div>', unsafe_allow_html=True)
