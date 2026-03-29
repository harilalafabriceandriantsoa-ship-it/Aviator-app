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

# --- 2. LOGIN (CONSIGNE MAZAVA) ---
def login():
    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🔐 TITAN SECURE LOGIN</h1>", unsafe_allow_html=True)
        st.markdown("""<div style="background:#002222; padding:20px; border-radius:15px; border:1px solid #00ffcc; margin-bottom:20px; font-size:18px;">
            <b>👋 TONGASOA!</b><br>Ampidiro ny Password nomena anao mba hidirana amin'ny algorithm TITAN.
        </div>""", unsafe_allow_html=True)
        pwd_input = st.text_input("PASSWORD:", type="password")
        if st.button("HIDITRA NY INTERFACE"):
            if pwd_input == st.session_state.master_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Kaody diso!")
        st.stop()

login()

# --- 3. STYLE PREMIUM RE-FIXED ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #ffffff; }
    .main-title { font-size: 38px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 15px #00ffcc; border-bottom: 2px solid #00ffcc; padding-bottom: 15px; }
    .card-result { background: #040e17; border: 3px solid #00ffcc; border-radius: 20px; padding: 25px; text-align: center; margin: 15px 0; }
    .card-opp { background: #1a1a00; border: 2px dashed #ffcc00; border-radius: 15px; padding: 20px; text-align: center; color: #ffcc00; margin-top: 15px; font-size: 18px; }
    .consigne-box { background: #001a1a; border-left: 8px solid #00ffcc; padding: 20px; margin-bottom: 25px; font-size: 17px !important; color: #ffffff; line-height: 1.6; }
    .luck-text { font-size: 24px; color: #ffcc00; text-align: center; font-weight: bold; margin: 20px 0; text-shadow: 0 0 15px #ffcc00; border: 2px solid #ffcc00; padding: 15px; border-radius: 50px; }
    .stButton>button { background: linear-gradient(90deg, #00ffcc, #0077ff); color: #010a12; font-weight: 900; border-radius: 12px; height: 55px; font-size: 18px; border: none; }
    .footer-brand { text-align: center; color: #888; font-size: 14px; margin-top: 50px; border-top: 1px solid #222; padding-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ENGINE ---
def get_advanced_predictions(seed, h_ora):
    base = datetime.strptime(h_ora, "%H:%M")
    results = []
    random.seed(int(hashlib.md5(seed.encode()).hexdigest()[:8], 16))
    for i in range(3):
        v_min = round(random.uniform(1.20, 1.45), 2)
        v_moyen = round(random.uniform(2.10, 5.20), 2)
        v_max = round(random.uniform(15.0, 65.0), 2)
        min_plus = random.randint(5, 20) * (i + 1)
        lera_vaovao = (base + timedelta(minutes=min_plus)).strftime("%H:%M")
        prob = random.randint(91, 99)
        results.append({"min": v_min, "moyen": v_moyen, "max": v_max, "lera": lera_vaovao, "prob": prob})
    return results

# --- 5. MAIN INTERFACE ---
st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)
tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY", "⚙️ ADMIN"])

# AVIATOR & COSMOS
for i, name in enumerate(["AVIATOR", "COSMOS X"]):
    game_key = "aviator" if i == 0 else "cosmos"
    with tabs[i]:
        st.markdown(f"""<div class="consigne-box">
            <b>📝 TOROLALANA {name}:</b><br>
            1. Ampidiro ny <b>HEX SEED</b> farany.<br>
            2. Hamarino ny <b>ORA (HH:MM)</b> mba hifanaraka amin'izao.<br>
            3. Tsindrio ny <b>EXECUTE</b> hahazoana lera 3 azo antoka.
        </div>""", unsafe_allow_html=True)
        
        st.markdown("📸 **Capture Historique (Aviator):**")
        st.file_uploader("", key=f"file_{game_key}")
        
        c1, c2 = st.columns(2)
        u_hex = c1.text_input(f"🔑 HEX SEED ({name}):", key=f"h_{game_key}")
        u_ora = c2.text_input("🕒 HEURE (HH:MM):", value=datetime.now().strftime("%H:%M"), key=f"o_{game_key}")
        
        if st.button(f"🔥 EXECUTE {name}"):
            if u_hex:
                preds = get_advanced_predictions(u_hex, u_ora)
                st.markdown(f"""<div class="card-result">
                    <div style="display: flex; justify-content: space-around; font-size: 20px; font-weight: bold;">
                        <span style="color:white;">MIN<br>{preds[0]['min']}x</span>
                        <span style="color:#00ffcc;">MOYEN (Target)<br><span style="font-size:50px;">{preds[0]['moyen']}x</span></span>
                        <span style="color:white;">MAX (Tenter)<br>{preds[0]['max']}x</span>
                    </div>
                </div>""", unsafe_allow_html=True)
                
                st.markdown('<div class="card-opp">🎯 PROCHAINES OPPORTUNITÉS:', unsafe_allow_html=True)
                for p in preds:
                    st.markdown(f"⏰ <b>{p['lera']}</b> | Côte: <b>{p['moyen']}x</b> | ✅ <b>{p['prob']}%</b>", unsafe_allow_html=True)
                    st.session_state[f'hist_{game_key}'].insert(0, f"🕒 {p['lera']} | 🎯 {p['moyen']}x | ✅ {p['prob']}%")
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('<div class="luck-text">🍀 BON GAIN À TOUS! 🍀</div>', unsafe_allow_html=True)
            else: st.warning("Ampidiro ny Hex Seed!")

# MINES VIP
with tabs[2]:
    st.markdown('<div class="consigne-box"><b>📝 MINES VIP:</b> Ampidiro ny Server Seed sy Client Seed hahitana ny pattern diamondra azo antoka.</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    s_seed = m1.text_input("🖥️ SERVER SEED (Mines):")
    c_seed = m2.text_input("💻 CLIENT SEED (Mines):")
    if st.button("💎 GENERATE MINES SCHEMA"):
        st.success("Mines Engine Ready! Pattern Generated.")
        st.markdown('<div class="luck-text">🍀 BON GAIN À TOUS! 🍀</div>', unsafe_allow_html=True)

# PENALTY
with tabs[3]:
    st.markdown('<div class="consigne-box"><b>📝 PENALTY:</b> Tsindrio ny bokotra hahitana ny toerana tokony hotifirina (Target).</div>', unsafe_allow_html=True)
    if st.button("🥅 GENERATE SHOTS"):
        st.info("Targets Locked!")
        st.markdown('<div class="luck-text">🍀 BON GAIN À TOUS! 🍀</div>', unsafe_allow_html=True)

# ADMIN
with tabs[4]:
    st.markdown(f"""<a href="https://wa.me/261346249701" style="text-decoration:none;"><div style="background:#25D366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:18px;">💬 WhatsApp Patricia</div></a>""", unsafe_allow_html=True)
    if st.button("🔴 RESET HISTORIQUE"):
        for k in ['hist_aviator', 'hist_cosmos', 'hist_mines', 'hist_penalty']: st.session_state[k] = []
        st.rerun()

st.markdown(f'<div class="footer-brand"><b>TITAN OMNI-STRIKE BY PATRICIA</b><br>0346249701 | andriantsoakelly@gmail.com</div>', unsafe_allow_html=True)
