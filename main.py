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

# Fitahirizana Historique (Tsy miova)
for key in ['hist_aviator', 'hist_cosmos', 'hist_mines', 'hist_penalty']:
    if key not in st.session_state: st.session_state[key] = []

# --- 2. LOGIN (Nohajaina ny sary nalefanao) ---
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
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE BY PATRICIA", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #ffffff; }
    .main-title { font-size: 35px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 15px #00ffcc; border-bottom: 2px solid #00ffcc; padding-bottom: 10px; }
    .card-beast { background: #040e17; border: 2px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; box-shadow: 0 0 15px rgba(0,255,204,0.3); margin-bottom: 20px; }
    .hist-container { background: rgba(0,0,0,0.6); border-radius: 10px; padding: 15px; font-family: monospace; height: 180px; overflow-y: auto; border: 1px solid #333; color: #00ffcc; }
    .stButton>button { background: linear-gradient(90deg, #00ffcc, #0077ff); color: #010a12; font-weight: 900; border-radius: 10px; height: 50px; border: none; }
    .footer-brand { text-align: center; color: #555; font-size: 12px; margin-top: 50px; border-top: 1px solid #222; padding-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ENGINE (Tsy misy fiovana) ---
def get_prediction_engine(seed, h_ora):
    raw = f"{seed}{h_ora}{time.time()}".encode()
    hash_res = hashlib.sha512(raw).hexdigest()
    random.seed(int(hash_res[:16], 16))
    vmoy = round(random.uniform(2.10, 4.50), 2)
    base = datetime.strptime(h_ora, "%H:%M")
    lera = (base + timedelta(minutes=random.randint(2, 10))).strftime("%H:%M")
    return vmoy, lera

# --- 5. MAIN INTERFACE ---
st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)
tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY", "⚙️ ADMIN"])

# (Aviator & Cosmos & Mines - Mitovy amin'ny teo aloha foana)
with tabs[0]:
    st.file_uploader("📸 Capture Historique (Aviator):", key="cap_av")
    c1, c2 = st.columns(2)
    u_hex = c1.text_input("🔑 HEX SEED (Aviator):", key="hex_av")
    u_ora = c2.text_input("🕒 HEURE (HH:MM):", value=datetime.now().strftime("%H:%M"), key="ora_av")
    if st.button("🔥 EXECUTE AVIATOR"):
        vm, lr = get_prediction_engine(u_hex, u_ora)
        st.session_state.hist_aviator.insert(0, f"🕒 {lr} | 🎯 {vm}x")
        st.markdown(f'<div class="card-beast"><h2>{vm}x</h2><p>NEXT: {lr}</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_aviator)}</div>', unsafe_allow_html=True)

with tabs[1]:
    st.file_uploader("📸 Capture Historique (Cosmos):", key="cap_cos")
    cC1, cC2 = st.columns(2)
    c_hex = cC1.text_input("🔑 HEX SEED (Cosmos X):", key="hex_cos")
    c_ora = cC2.text_input("🕒 HEURE (HH:MM):", value=datetime.now().strftime("%H:%M"), key="ora_cos")
    if st.button("🚀 EXECUTE COSMOS"):
        vm, lr = get_prediction_engine(c_hex, c_ora)
        st.session_state.hist_cosmos.insert(0, f"🕒 {lr} | 🎯 {vm}x")
        st.markdown(f'<div class="card-beast"><h2>{vm}x</h2><p>NEXT: {lr}</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_cosmos)}</div>', unsafe_allow_html=True)

with tabs[2]:
    m1, m2 = st.columns(2)
    m_serv = m1.text_input("🖥️ SERVER SEED (Mines):")
    m_clie = m2.text_input("💻 CLIENT SEED (Mines):")
    if st.button("💎 GENERATE SCHEMA"):
        st.session_state.hist_mines.insert(0, f"🕒 {datetime.now().strftime('%H:%M')} | Schema OK")
        st.success("Schema Ready!")
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_mines)}</div>', unsafe_allow_html=True)

with tabs[3]:
    if st.button("🥅 GENERATE 5 SHOT PREDICTIONS"):
        targets = ["ANKAVIA AMBONY", "ANKAVANANA AMBANY", "AFOVOANY", "ANKAVIA AMBANY", "ANKAVANANA AMBONY"]
        random.shuffle(targets)
        st.markdown('<div class="card-beast">', unsafe_allow_html=True)
        for i, t in enumerate(targets, 1):
            st.markdown(f'<div>Daka {i}: <b>{t}</b></div>', unsafe_allow_html=True)
            st.session_state.hist_penalty.insert(0, f"[{datetime.now().strftime('%H:%M')}] Daka {i}: {t}")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_penalty)}</div>', unsafe_allow_html=True)

# --- ⚙️ ADMIN (BRAND & CONTACT) ---
with tabs[4]:
    st.markdown("### 🛠️ PANEL ADMIN & BRANDING")
    st.info(f"Developed by: Patricia | Contact: andriantsoakelly@gmail.com")
    
    new_p = st.text_input("Password vaovao:", type="password")
    if st.button("OK"):
        st.session_state.master_password = new_p
        st.success("Updated!")
    
    if st.button("🔴 EFFACER TOUT L'HISTORIQUE"):
        for k in ['hist_aviator', 'hist_cosmos', 'hist_mines', 'hist_penalty']: st.session_state[k] = []
        st.rerun()

# --- FOOTER BRAND ---
st.markdown(f"""
    <div class="footer-brand">
        © 2026 TITAN OMNI-STRIKE | Propriété de Patricia | Support: andriantsoakelly@gmail.com
    </div>
""", unsafe_allow_html=True)
