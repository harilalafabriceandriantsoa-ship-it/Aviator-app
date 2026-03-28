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

# Fitahirizana Historique
for key in ['hist_aviator', 'hist_cosmos', 'hist_mines', 'hist_penalty']:
    if key not in st.session_state: st.session_state[key] = []

# --- 2. LOGIN ---
def login():
    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛡️ TITAN SECURE LOGIN</h1>", unsafe_allow_html=True)
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
    .card-beast { background: #040e17; border: 2px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; box-shadow: 0 0 15px rgba(0,255,204,0.3); margin-bottom: 20px; }
    .hist-header { color: #00ffcc; font-weight: bold; margin-top: 20px; border-left: 3px solid #00ffcc; padding-left: 10px; }
    .hist-container { background: rgba(0,0,0,0.6); border-radius: 10px; padding: 15px; font-family: 'Courier New', monospace; height: 180px; overflow-y: auto; border: 1px solid #333; color: #00ffcc; }
    .stButton>button { background: linear-gradient(90deg, #00ffcc, #0077ff); color: #010a12; font-weight: 900; border-radius: 10px; height: 50px; border: none; }
    .btn-delete>button { background: #ff4b4b !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ENGINE ---
def get_prediction_engine(seed, h_ora):
    raw = f"{seed}{h_ora}{time.time()}".encode()
    hash_res = hashlib.sha512(raw).hexdigest()
    random.seed(int(hash_res[:16], 16))
    vmoy = round(random.uniform(2.10, 4.50), 2)
    base = datetime.strptime(h_ora, "%H:%M")
    lera = (base + timedelta(minutes=random.randint(2, 12))).strftime("%H:%M")
    return vmoy, lera

# --- 5. MAIN INTERFACE ---
st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)
tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY", "⚙️ ADMIN"])

# --- AVIATOR ---
with tabs[0]:
    st.file_uploader("📸 Capture Historique (Aviator):", key="cap_av")
    c1, c2 = st.columns(2)
    u_hex = c1.text_input("🔑 HEX SEED (Aviator):", key="hex_av")
    u_ora = c2.text_input("🕒 HEURE (HH:MM):", value=datetime.now().strftime("%H:%M"), key="ora_av")
    if st.button("🔥 EXECUTE AVIATOR ENGINE"):
        vm, lr = get_prediction_engine(u_hex, u_ora)
        st.session_state.hist_aviator.insert(0, f"🕒 {lr} | 🎯 {vm}x")
        st.markdown(f'<div class="card-beast"><h2>MOYEN: {vm}x</h2><p>NEXT: {lr}</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="hist-header">📜 HISTORIQUE AVIATOR</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_aviator)}</div>', unsafe_allow_html=True)

# --- COSMOS X ---
with tabs[1]:
    st.file_uploader("📸 Capture Historique (Cosmos):", key="cap_cos")
    cC1, cC2 = st.columns(2)
    c_hex = cC1.text_input("🔑 HEX SEED (Cosmos X):", key="hex_cos")
    c_ora = cC2.text_input("🕒 HEURE (HH:MM):", value=datetime.now().strftime("%H:%M"), key="ora_cos")
    if st.button("🚀 EXECUTE COSMOS ENGINE"):
        vm, lr = get_prediction_engine(c_hex, c_ora)
        st.session_state.hist_cosmos.insert(0, f"🕒 {lr} | 🎯 {vm}x")
        st.markdown(f'<div class="card-beast"><h2>MOYEN: {vm}x</h2><p>NEXT: {lr}</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="hist-header">📜 HISTORIQUE COSMOS</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_cosmos)}</div>', unsafe_allow_html=True)

# --- MINES VIP ---
with tabs[2]:
    m1, m2 = st.columns(2)
    m_serv = m1.text_input("🖥️ SERVER SEED (Mines):")
    m_clie = m2.text_input("💻 CLIENT SEED (Mines):")
    if st.button("💎 GENERATE SCHEMA"):
        now = datetime.now().strftime("%H:%M:%S")
        st.session_state.hist_mines.insert(0, f"🕒 {now} | Schema OK")
        st.success("Schema Ready!")
    st.markdown('<div class="hist-header">📜 HISTORIQUE MINES</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_mines)}</div>', unsafe_allow_html=True)

# --- PENALTY ---
with tabs[3]:
    if st.button("🥅 GENERATE 5 SHOT PREDICTIONS"):
        targets = ["ANKAVIA AMBONY", "ANKAVANANA AMBANY", "AFOVOANY", "ANKAVIA AMBANY", "ANKAVANANA AMBONY"]
        random.shuffle(targets)
        st.markdown('<div class="card-beast">', unsafe_allow_html=True)
        for i, t in enumerate(targets, 1):
            st.markdown(f'<div>Daka {i}: <b>{t}</b></div>', unsafe_allow_html=True)
            st.session_state.hist_penalty.insert(0, f"[{datetime.now().strftime('%H:%M')}] Daka {i}: {t}")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="hist-header">📜 HISTORIQUE PENALTY</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_penalty)}</div>', unsafe_allow_html=True)

# --- ⚙️ ADMIN (FAMAFANA HISTORIQUE) ---
with tabs[4]:
    st.markdown("### 🛠️ PANEL ADMIN")
    
    # 1. Hanova Password
    new_p = st.text_input("Password vaovao:", type="password")
    if st.button("OK (Update Password)"):
        st.session_state.master_password = new_p
        st.success("Updated!")
    
    st.write("---")
    
    # 2. Famafana Historique
    st.markdown("#### 🗑️ FITANTANANA NY HISTORIQUE")
    st.markdown('<div class="btn-delete">', unsafe_allow_html=True)
    if st.button("🔴 EFFACER TOUT L'HISTORIQUE"):
        st.session_state.hist_aviator = []
        st.session_state.hist_cosmos = []
        st.session_state.hist_mines = []
        st.session_state.hist_penalty = []
        st.success("✅ Voafafa avokoa ny historique rehetra!")
        time.sleep(1)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
