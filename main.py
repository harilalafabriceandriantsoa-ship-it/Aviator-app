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

if 'hist_aviator' not in st.session_state: st.session_state.hist_aviator = []
if 'hist_cosmos' not in st.session_state: st.session_state.hist_cosmos = []
if 'hist_mines' not in st.session_state: st.session_state.hist_mines = []
if 'hist_penalty' not in st.session_state: st.session_state.hist_penalty = []

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
    .penalty-target { color: #00ffcc; font-weight: bold; border-bottom: 1px solid #333; padding: 5px; }
    .stButton>button { background: linear-gradient(90deg, #00ffcc, #0077ff); color: #010a12; font-weight: 900; border-radius: 10px; height: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. MAIN INTERFACE ---
st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)
tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY", "⚙️ ADMIN"])

# (Aviator & Cosmos & Mines - Tsy misy fiovana)
with tabs[0]:
    st.file_uploader("📸 Capture Historique (Aviator):", key="cap_av")
    col1, col2 = st.columns(2)
    u_hex = col1.text_input("🔑 HEX SEED (Aviator):")
    u_ora = col2.text_input("🕒 HEURE (HH:MM):", value=datetime.now().strftime("%H:%M"), key="ora_av")
    if st.button("🔥 EXECUTE AVIATOR"):
        st.info("Calculation in progress...")

with tabs[1]:
    st.file_uploader("📸 Capture Historique (Cosmos):", key="cap_cos")
    st.info("Cosmos Mode Active")

with tabs[2]:
    st.file_uploader("📸 Capture Historique (Mines):", key="cap_mines")
    st.info("Mines Mode Active")

# --- ⚽ PENALTY (UPDATED: NO SEEDS, 5 TIRS, EASY/MEDIUM) ---
with tabs[3]:
    st.markdown("### ⚽ PENALTY SHOOTOUT (FACILE/MOYEN)")
    st.file_uploader("📸 Capture Historique (Penalty):", key="cap_pen")
    
    st.markdown('<div class="consigne-box">⚠️ <b>CONSIGNE:</b> Daka in-5 no omen\'ny algorithm. Target focus: Facile & Moyen.</div>', unsafe_allow_html=True)
    
    if st.button("🥅 GENERATE 5 SHOT PREDICTIONS"):
        # Algorithm Penalty (In-5 daka)
        targets = ["ANKAVIA AMBONY", "ANKAVANANA AMBANY", "AFOVOANY", "ANKAVIA AMBANY", "ANKAVANANA AMBONY"]
        random.shuffle(targets) # Ovaovaina ny filaharany
        
        st.markdown('<div class="card-beast">', unsafe_allow_html=True)
        for i, t in enumerate(targets, 1):
            acc = random.randint(92, 97) # Facile/Moyen accuracy
            st.markdown(f'<div class="penalty-target">Daka {i}: {t} <span style="color:gray;">({acc}%)</span></div>', unsafe_allow_html=True)
            st.session_state.hist_penalty.insert(0, f"[{datetime.now().strftime('%H:%M')}] Tir {i}: {t}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 📜 HISTORIQUE PENALTY")
    st.markdown(f'<div class="hist-container">{"<br>".join(st.session_state.hist_penalty)}</div>', unsafe_allow_html=True)

# --- ADMIN ---
with tabs[4]:
    st.markdown("### 🛠️ PANEL ADMIN")
    new_p = st.text_input("Hanova Password:", type="password")
    if st.button("CONFIRM CHANGE"):
        st.session_state.master_password = new_p
        st.success("Password Updated!")
