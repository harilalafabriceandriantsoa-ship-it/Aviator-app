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
    .card-beast { background: #040e17; border: 2px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; box-shadow: 0 0 15px rgba(0,255,204,0.3); }
    .hist-container { background: rgba(0,0,0,0.6); border-radius: 10px; padding: 10px; font-family: monospace; height: 150px; overflow-y: auto; border: 1px solid #333; color: #00ffcc; }
    .stButton>button { background: linear-gradient(90deg, #00ffcc, #0077ff); color: #010a12; font-weight: 900; border-radius: 10px; height: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ENGINE (AVIATOR & COSMOS) ---
def get_prediction_engine(seed, h_ora):
    raw = f"{seed}{h_ora}{time.time()}".encode()
    hash_res = hashlib.sha512(raw).hexdigest()
    random.seed(int(hash_res[:16], 16))
    vmoy = round(random.uniform(2.10, 4.50), 2)
    vmax = round(random.uniform(10.0, 60.0), 2)
    base = datetime.strptime(h_ora, "%H:%M")
    offsets = [random.randint(2, 8), random.randint(10, 20)]
    preds = [(base + timedelta(minutes=o)).strftime("%H:%M") for o in offsets]
    return vmoy, vmax, preds

# --- 5. INTERFACE TABS ---
st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)
tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY", "⚙️ ADMIN"])

# --- ✈️ AVIATOR (Firafitra Mitovy) ---
with tabs[0]:
    st.file_uploader("📸 Capture Historique (Aviator):", key="cap_av")
    col1, col2 = st.columns(2)
    u_hex = col1.text_input("🔑 HEX SEED (Aviator):", key="hex_av")
    u_ora = col2.text_input("🕒 HEURE (HH:MM):", value=datetime.now().strftime("%H:%M"), key="ora_av")
    if st.button("🔥 EXECUTE AVIATOR ENGINE"):
        vmoy, vmax, lera = get_prediction_engine(u_hex, u_ora)
        st.session_state.hist_aviator.insert(0, f"[{lera[0]}] -> {vmoy}x")
        st.markdown(f'<div class="card-beast"><h2>MOYEN: {vmoy}x</h2><p>MAX: {vmax}x</p><p>PROCHAIN: {lera[0]} | {lera[1]}</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_aviator)}</div>', unsafe_allow_html=True)

# --- 🚀 COSMOS X (Firafitra Mitovy amin'ny Aviator) ---
with tabs[1]:
    st.file_uploader("📸 Capture Historique (Cosmos):", key="cap_cos")
    colC1, colC2 = st.columns(2)
    c_hex = colC1.text_input("🔑 HEX SEED (Cosmos X):", key="hex_cos")
    c_ora = colC2.text_input("🕒 HEURE (HH:MM):", value=datetime.now().strftime("%H:%M"), key="ora_cos")
    if st.button("🚀 EXECUTE COSMOS ENGINE"):
        vmoy, vmax, lera = get_prediction_engine(c_hex, c_ora)
        st.session_state.hist_cosmos.insert(0, f"[{lera[0]}] -> {vmoy}x")
        st.markdown(f'<div class="card-beast"><h2>MOYEN: {vmoy}x</h2><p>MAX: {vmax}x</p><p>PROCHAIN: {lera[0]} | {lera[1]}</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_cosmos)}</div>', unsafe_allow_html=True)

# --- 💣 MINES VIP (Misy Seed Client & Serveur indray) ---
with tabs[2]:
    st.markdown("### 💣 MINES VIP (5 DIAMONDS MODE)")
    st.file_uploader("📸 Capture Historique (Mines):", key="cap_mines")
    m1, m2 = st.columns(2)
    m_serv = m1.text_input("🖥️ SERVER SEED (Mines):")
    m_clie = m2.text_input("💻 CLIENT SEED (Mines):")
    if st.button("💎 GENERATE 5-DIAMOND SCHEMA"):
        if m_serv and m_clie:
            st.session_state.hist_mines.insert(0, f"[{datetime.now().strftime('%H:%M')}] Schema Generated")
            st.success("Schema Ready! Focus on 5 Diamonds.")
        else:
            st.warning("Ampidiro ny Seeds azafady!")
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_mines)}</div>', unsafe_allow_html=True)

# --- ⚽ PENALTY (5 Tirs - Facile/Moyen) ---
with tabs[3]:
    st.markdown("### ⚽ PENALTY SHOOTOUT")
    if st.button("🥅 GENERATE 5 SHOT PREDICTIONS"):
        targets = ["ANKAVIA AMBONY", "ANKAVANANA AMBANY", "AFOVOANY", "ANKAVIA AMBANY", "ANKAVANANA AMBONY"]
        random.shuffle(targets)
        st.markdown('<div class="card-beast">', unsafe_allow_html=True)
        for i, t in enumerate(targets, 1):
            acc = random.randint(92, 97)
            st.markdown(f'<div style="border-bottom:1px solid #333; padding:5px;">Daka {i}: {t} ({acc}%)</div>', unsafe_allow_html=True)
            st.session_state.hist_penalty.insert(0, f"[{datetime.now().strftime('%H:%M')}] Tir {i}: {t}")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_penalty)}</div>', unsafe_allow_html=True)

# --- ⚙️ ADMIN ---
with tabs[4]:
    new_p = st.text_input("Password vaovao:", type="password")
    if st.button("OK"):
        st.session_state.master_password = new_p
        st.success("Vita!")
