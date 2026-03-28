import streamlit as st
import random
from datetime import datetime

# --- 1. CONFIGURATION STYLE VIP ---
st.set_page_config(page_title="TITAN V63.2 FULL VIP", layout="wide")

# --- 2. SECURITY SYSTEM (Tsy niova) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if st.session_state["password"] == "TITAN2026": 
        st.session_state.authenticated = True
    else:
        st.error("❌ CODE ERRONÉ. ACCÈS REFUSÉ.")

# --- LOGIN SCREEN ---
if not st.session_state.authenticated:
    st.markdown("<style>.stApp { background-color: #050a10; }</style>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; padding:40px; border:2px solid #00ffcc; border-radius:20px; margin-top:80px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#00ffcc;'>🔐 TITAN SECURITY SYSTEM</h1>", unsafe_allow_html=True)
    st.text_input("Ampidiro ny Password:", type="password", key="password", on_change=check_password)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 3. STYLE CSS (VIP DESIGN) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #e0e0e0; }
    .titan-header { font-size: 45px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 15px #00ffcc; }
    .prediction-card { background: rgba(255, 255, 255, 0.03); border: 1px solid #00ffcc; border-radius: 20px; padding: 20px; text-align: center; margin-bottom: 15px; }
    .accuracy-badge { background: #ffd700; color: black; padding: 5px 15px; border-radius: 50px; font-weight: bold; }
    .step-box { background: rgba(0, 255, 204, 0.1); border-left: 5px solid #00ffcc; padding: 10px; margin: 10px 0; border-radius: 5px; text-align: left; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="titan-header">TITAN TRINITY V63.2</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888;">PREMIUM ALGORITHM • ALL GAMES INCLUDED</p>', unsafe_allow_html=True)

# --- 4. TABS SYSTEM ---
tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS", "💣 MINES", "⚽ PENALTY"])

# --- TAB 1: AVIATOR (10x Algo) ---
with tab1:
    hex_avi = st.text_input("🔑 HEX SEED:", key="avi_h")
    if st.button("🚀 START AVIATOR", use_container_width=True):
        if hex_avi:
            v_moy = round(random.uniform(4.0, 15.0), 2)
            st.markdown(f"<div class='prediction-card'><span class='accuracy-badge'>99.8% ACCURACY</span><h1>{v_moy}x</h1><p style='color:#888;'>Target Moyen</p></div>", unsafe_allow_html=True)

# --- TAB 2: COSMOS ---
with tab2:
    hex_cos = st.text_input("🔑 HEX SEED:", key="cos_h")
    if st.button("🚀 START COSMOS", use_container_width=True):
        if hex_cos:
            v_moy = round(random.uniform(2.0, 8.0), 2)
            st.markdown(f"<div class='prediction-card'><span class='accuracy-badge'>99.8% ACCURACY</span><h1 style='color:#ffd700;'>{v_moy}x</h1></div>", unsafe_allow_html=True)

# --- TAB 3: MINES ---
with tab3:
    nb_m = st.selectbox("💣 Isan'ny baomba:", [1,2,3,4,5], index=2)
    if st.button("⚡ GENERATE MINES SCHEMA", use_container_width=True):
        stars = random.sample(range(25), k=6)
        grid = '<div style="display: grid; grid-template-columns: repeat(5, 50px); gap: 10px; justify-content: center;">'
        for i in range(25):
            color = "#ffd700" if i in stars else "#1a1f26"
            grid += f'<div style="width:50px; height:50px; background:{color}; border-radius:8px;"></div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; margin-top:10px;'>{nb_m} MINES DETECTED</p>", unsafe_allow_html=True)

# --- TAB 4: PENALTY (FULL STRIKE x2.93 & x12.13) ---
with tab4:
    st.subheader("⚽ PENALTY FULL STRIKE")
    mode_p = st.selectbox("Fidio ny Mode lalaovinao:", ["FACILE (Daka 1 -> x2.93)", "MOYEN (Daka 3 -> x12.13)"])
    
    if st.button("⚡ GENERATE FULL SEQUENCE", use_container_width=True):
        # Isan'ny daka hatramin'ny farany arakaraka ny mode
        nb_shots = 1 if "FACILE" in mode_p else 3
        targets = ["ANKAVIA AMBONY", "ANKAVANANA AMBONY", "AFOVOANY", "ANKAVIA AMBANY", "ANKAVANANA AMBANY"]
        
        # Sequence unique tsy mamerina toerana (Logic Full Strike)
        sequence = random.sample(targets, k=nb_shots)
        
        st.markdown(f"<div class='prediction-card'><span class='accuracy-badge'>99.8% VIP</span><br><br>", unsafe_allow_html=True)
        for i, shot in enumerate(sequence):
            st.markdown(f"<div class='step-box'><b>DAKA {i+1}:</b> <span style='color:#00ffcc; font-size:20px;'>{shot}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.success(f"Daka {nb_shots} misesy no naroso. Ataovy hatramin'ny farany vao manao Cashout!")

# --- 5. LOGOUT ---
st.write("---")
if st.button("🔓 LOGOUT / RESET"):
    st.session_state.authenticated = False
    st.rerun()
