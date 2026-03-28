import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. RAFITRA FIAROVANA SY FITAHIRIZANA ---
# Izaho irery (Admin) no afaka manova ny teny miafina mandritra ny session
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'master_password' not in st.session_state:
    st.session_state.master_password = "PATRICIA_BEAST"

# Historique tsirairay isaky ny efitra
if 'hist_aviator' not in st.session_state: st.session_state.hist_aviator = []
if 'hist_cosmos' not in st.session_state: st.session_state.hist_cosmos = []
if 'hist_mines' not in st.session_state: st.session_state.hist_mines = []

# --- 2. LOGIN INTERFACE ---
def login():
    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛡️ TITAN ADMIN ACCESS</h1>", unsafe_allow_html=True)
        pwd_input = st.text_input("Ampidiro ny kaody manokana (Patricia):", type="password")
        if st.button("HIRAFIKA NY INTERFACE"):
            if pwd_input == st.session_state.master_password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Access Denied.")
        st.stop()

login()

# --- 3. CONFIGURATION SY STYLE "MACHINE DE GUERRE" ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #010a12; color: #ffffff; }
    .main-title { font-size: 40px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 20px #00ffcc; border-bottom: 3px solid #00ffcc; padding-bottom: 10px; }
    .card-beast { background: #040e17; border: 2px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; box-shadow: 0 0 15px rgba(0,255,204,0.2); }
    .hist-container { background: rgba(0,0,0,0.5); border-radius: 10px; padding: 10px; font-family: monospace; font-size: 12px; height: 150px; overflow-y: auto; border: 1px solid #333; }
    .stButton>button { background: linear-gradient(90deg, #00ffcc, #0077ff); color: #010a12; font-weight: 900; border-radius: 10px; border: none; width: 100%; transition: 0.3s; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ENGINE ALGO ---
def get_prediction(seed, h_ora):
    raw = f"{seed}{h_ora}{time.time()}".encode()
    hash_res = hashlib.sha512(raw).hexdigest()
    random.seed(int(hash_res[:16], 16))
    
    vmoy = round(random.uniform(2.10, 4.80), 2)
    vmax = round(random.uniform(10.0, 50.0), 2)
    
    # Ora 3 samihafa (Next Rounds)
    base = datetime.strptime(h_ora, "%H:%M")
    offsets = random.sample(range(2, 30), 3)
    offsets.sort()
    preds = [(base + timedelta(minutes=o)).strftime("%H:%M") for o in offsets]
    return vmoy, vmax, preds

# --- 5. INTERFACE TABS ---
st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)
tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY", "⚙️ ADMIN"])

# --- ✈️ AVIATOR ---
with tabs[0]:
    st.file_uploader("📸 Capture Historique (Aviator):", key="cap_av")
    col1, col2 = st.columns(2)
    u_hex = col1.text_input("🔑 HEX SEED (Aviator):")
    u_ora = col2.text_input("🕒 HEURE:", value=datetime.now().strftime("%H:%M"), key="ora_av")
    
    if st.button("🔥 EXECUTE AVIATOR"):
        vmoy, vmax, lera = get_prediction(u_hex, u_ora)
        st.session_state.hist_aviator.insert(0, f"[{lera[0]}] -> {vmoy}x | {vmax}x")
        st.markdown(f'<div class="card-beast"><h1>{vmoy}x</h1><p>TENTER: {vmax}x</p></div>', unsafe_allow_html=True)
    
    st.markdown("### 📜 HISTORIQUE AVIATOR")
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_aviator)}</div>', unsafe_allow_html=True)

# --- 🚀 COSMOS X ---
with tabs[1]:
    st.file_uploader("📸 Capture Historique (Cosmos):", key="cap_cos")
    u_hex_c = st.text_input("🔑 HEX SEED (Cosmos X):")
    if st.button("🔥 EXECUTE COSMOS"):
        vmoy, vmax, lera = get_prediction(u_hex_c, datetime.now().strftime("%H:%M"))
        st.session_state.hist_cosmos.insert(0, f"[{lera[0]}] -> {vmoy}x | {vmax}x")
        st.success(f"PREDICTION: {vmoy}x")
    
    st.markdown("### 📜 HISTORIQUE COSMOS")
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_cosmos)}</div>', unsafe_allow_html=True)

# --- 💣 MINES VIP ---
with tabs[2]:
    m_cli = st.text_input("💻 CLIENT SEED (Mines):")
    if st.button("💎 GENERATE SCHEMA"):
        random.seed(m_cli + str(time.time()))
        spots = random.sample(range(25), k=5)
        st.session_state.hist_mines.insert(0, f"[{datetime.now().strftime('%H:%M')}] Schema Generated")
        # Grid Display... (Simplified for brevity)
        st.write("Schema 5 Diamonds Ready")
    
    st.markdown("### 📜 HISTORIQUE MINES")
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_mines)}</div>', unsafe_allow_html=True)

# --- ⚙️ ADMIN SETTINGS (Ianao irery) ---
with tabs[4]:
    st.markdown("### 🛠️ PANEL ADMIN CONTROL")
    st.warning("Eto ianao irery no afaka manova ny fiarovana ny app.")
    
    new_pwd = st.text_input("Hanova Teny Miafina (Master):", type="password")
    if st.button("CONFIRM CHANGE"):
        if new_pwd:
            st.session_state.master_password = new_pwd
            st.success("✅ Voova soa aman-tsara ny Password Master!")

    if st.button("🧹 RESET ALL HISTORIES"):
        st.session_state.hist_aviator = []
        st.session_state.hist_cosmos = []
        st.session_state.hist_mines = []
        st.rerun()
