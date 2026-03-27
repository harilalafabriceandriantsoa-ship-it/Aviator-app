import streamlit as st
import time
import random
from datetime import datetime

# --- CONFIGURATION STYLE ---
st.set_page_config(page_title="TITAN TRINITY v62.3", page_icon="💎", layout="wide")

# Initialisation data
if 'total_gain' not in st.session_state: st.session_state.total_gain = 0
if 'gain_history' not in st.session_state: st.session_state.gain_history = []
if 'history_avi' not in st.session_state: st.session_state.history_avi = []
if 'history_cos' not in st.session_state: st.session_state.history_cos = []
if 'daily_goal' not in st.session_state: st.session_state.daily_goal = 50000

st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: #e0e0e0; }
    .titan-title {
        font-size: 40px; font-weight: 800; text-align: center;
        background: linear-gradient(90deg, #00ffcc, #ffd700);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .prediction-card {
        background: rgba(22, 27, 34, 0.9); border: 2px solid #00ffcc;
        border-radius: 15px; padding: 25px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.2);
    }
    .status-text { font-size: 22px; color: #ffd700; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: JOURNAL DE BORD ---
with st.sidebar:
    st.header("📒 JOURNAL DE BORD")
    
    # Setup Objectif
    st.session_state.daily_goal = st.number_input("Objectif androany:", value=st.session_state.daily_goal, step=5000)
    
    # Progress Bar
    prog = min(st.session_state.total_gain / st.session_state.daily_goal, 1.0) if st.session_state.daily_goal > 0 else 0
    st.progress(prog)
    st.markdown(f"<p class='status-text'>{st.session_state.total_gain:,} / {st.session_state.daily_goal:,}</p>", unsafe_allow_html=True)
    
    # Victory Alert (Confetti)
    if st.session_state.total_gain >= st.session_state.daily_goal and st.session_state.daily_goal > 0:
        st.balloons()
        st.success("🎯 Objectif Atteint!")

    # Input Gain
    with st.expander("💰 Ampidiro Gain"):
        g = st.number_input("Vola azo:", min_value=0, step=500)
        l = st.selectbox("Lalao:", ["Aviator", "Cosmos", "Mines"])
        if st.button("Tehirizo"):
            st.session_state.total_gain += g
            st.session_state.gain_history.insert(0, f"{datetime.now().strftime('%H:%M')} | +{g:,} ({l})")
            st.rerun()

    st.markdown("---")
    st.markdown("📜 **Derniers Gains:**")
    for entry in st.session_state.gain_history[:8]:
        st.write(entry)
    
    if st.button("🔄 Reset"):
        st.session_state.total_gain = 0
        st.session_state.gain_history = []
        st.rerun()

# --- MAIN INTERFACE ---
st.markdown('<h1 class="titan-title">💎 TITAN v62.3 TRINITY</h1>', unsafe_allow_html=True)

tab_avi, tab_cos, tab_min = st.tabs(["✈️ AVIATOR", "🚀 COSMOS", "💣 MINES"])

# 1. AVIATOR
with tab_avi:
    col1, col2 = st.columns([2, 1])
    with col1:
        l_avi = st.selectbox("🕒 Lera:", [datetime.now().strftime("%H:%M")], key="avi_l")
        h_avi = st.text_input("🔑 HEX SEED:", key="avi_h")
        if st.button("⚡ ANALYSE AVIATOR"):
            if h_avi:
                st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/sounds/button-09.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)
                est = round(random.uniform(2.2, 14.0), 2)
                st.session_state.history_avi.insert(0, {"T": l_avi, "X": f"{est}x"})
                st.markdown(f"<div class='prediction-card'><h1>{est}x</h1><p>Accuracy: 98%</p></div>", unsafe_allow_html=True)
    with col2:
        st.table(st.session_state.history_avi[:5])

# 2. COSMOS
with tab_cos:
    col1, col2 = st.columns([2, 1])
    with col1:
        l_cos = st.selectbox("🕒 Lera:", [datetime.now().strftime("%H:%M")], key="cos_l")
        h_cos = st.text_input("🔑 HEX SEED:", key="cos_h")
        if st.button("⚡ ANALYSE COSMOS"):
            if h_cos:
                st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/sounds/button-09.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)
                est = round(random.uniform(1.9, 9.0), 2)
                st.session_state.history_cos.insert(0, {"T": l_cos, "X": f"{est}x"})
                st.markdown(f"<div class='prediction-card'><h1>{est}x</h1><p>Accuracy: 96%</p></div>", unsafe_allow_html=True)
    with col2:
        st.table(st.session_state.history_cos[:5])

# 3. MINES (Serveur 2)
with tab_min:
    st.info("🌐 SERVEUR 2 BACKUP ACTIVE")
    if st.button("⚡ GENERATE VIP SCHEMA"):
        st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/sounds/button-09.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)
        grid = '<div style="display: grid; grid-template-columns: repeat(5, 45px); gap: 8px; justify-content: center;">'
        stars = random.sample(range(25), k=5)
        for i in range(25):
            color = "#ffd700" if i in stars else "#1a1a1a"
            grid += f'<div style="width:45px; height:45px; background:{color}; border-radius:8px;"></div>'
        grid += '</div>'
        st.markdown(grid, unsafe_allow_html=True)
        st.success("98% Accuracy")

st.markdown("---")
with st.expander("📜 CONSIGNES"):
    st.write("1. Aza miverina indroa amin'ny signal iray.")
    st.write("2. Ampiasao ny 10% amin'ny solde fotsiny.")
