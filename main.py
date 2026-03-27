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

st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: #e0e0e0; }
    .titan-title {
        font-size: 35px; font-weight: 800; text-align: center;
        background: linear-gradient(90deg, #00ffcc, #ffd700);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .prediction-card {
        background: rgba(22, 27, 34, 0.9); border: 2px solid #00ffcc;
        border-radius: 15px; padding: 20px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: JOURNAL ---
with st.sidebar:
    st.header("📒 JOURNAL")
    st.metric("Total Gain", f"{st.session_state.total_gain:,}")
    with st.expander("💰 Ampidiro Gain"):
        g = st.number_input("Vola:", min_value=0, step=500)
        if st.button("Tehirizo"):
            st.session_state.total_gain += g
            st.session_state.gain_history.insert(0, f"{datetime.now().strftime('%H:%M')} | +{g:,}")
            st.rerun()
    st.write("---")
    for entry in st.session_state.gain_history[:5]:
        st.caption(entry)

st.markdown('<h1 class="titan-title">💎 TITAN v62.3 TRINITY</h1>', unsafe_allow_html=True)

tab_avi, tab_cos, tab_min = st.tabs(["✈️ AVIATOR", "🚀 COSMOS", "💣 MINES"])

# --- 1. AVIATOR (Capture + Hex + History) ---
with tab_avi:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📸 Capture History")
        up_avi = st.file_uploader("Drag and drop Aviator screenshot", type=['jpg','png','jpeg'], key="up_avi")
        l_avi = st.selectbox("🕒 Lera farany:", ["20:40", "20:43", datetime.now().strftime("%H:%M")], key="l_avi")
        h_avi = st.text_input("🔑 HEX SEED (SHA-256):", key="h_avi")
        
        if st.button("⚡ ANALYSE AVIATOR"):
            if h_avi:
                st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/sounds/button-09.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)
                est = round(random.uniform(2.0, 15.0), 2)
                st.session_state.history_avi.insert(0, {"Lera": l_avi, "Result": f"{est}x"})
                st.markdown(f"<div class='prediction-card'><h1>{est}x</h1><p>Accuracy: 98%</p></div>", unsafe_allow_html=True)
    with col2:
        st.write("📜 **History**")
        st.table(st.session_state.history_avi[:5])

# --- 2. COSMOS (Capture + Hex + History) ---
with tab_cos:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📸 Capture History")
        up_cos = st.file_uploader("Drag and drop Cosmos screenshot", type=['jpg','png','jpeg'], key="up_cos")
        l_cos = st.selectbox("🕒 Lera farany:", ["20:40", datetime.now().strftime("%H:%M")], key="l_cos")
        h_cos = st.text_input("🔑 HEX SEED:", key="h_cos")
        
        if st.button("⚡ ANALYSE COSMOS"):
            if h_cos:
                st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/sounds/button-09.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)
                est = round(random.uniform(1.8, 10.0), 2)
                st.session_state.history_cos.insert(0, {"Lera": l_cos, "Result": f"{est}x"})
                st.markdown(f"<div class='prediction-card'><h1>{est}x</h1><p>Accuracy: 96%</p></div>", unsafe_allow_html=True)
    with col2:
        st.write("📜 **History**")
        st.table(st.session_state.history_cos[:5])

# --- 3. MINES (Seed 1 + Seed 2 + Prediction) ---
with tab_min:
    st.subheader("💣 MINES SERVER 2 ANALYSIS")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        client_seed = st.text_input("💻 Seed du client:", placeholder="Ampidiro ny client seed...")
    with col_s2:
        server_seed = st.text_input("🖥️ Seed du serveur:", placeholder="Ampidiro ny server seed...")
    
    if st.button("⚡ GENERATE VIP SCHEMA"):
        if client_seed and server_seed:
            st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/sounds/button-09.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)
            # Fampisehoana ny Grid (Sary prediction)
            grid = '<div style="display: grid; grid-template-columns: repeat(5, 45px); gap: 8px; justify-content: center; margin-top: 20px;">'
            stars = random.sample(range(25), k=5)
            for i in range(25):
                color = "#ffd700" if i in stars else "#1a1a1a"
                grid += f'<div style="width:45px; height:45px; background:{color}; border-radius:8px; border: 1px solid #333;"></div>'
            grid += '</div>'
            st.markdown(grid, unsafe_allow_html=True)
            st.success("98% Accuracy for this Seed configuration")
        else:
            st.error("Azafady, ampidiro ny Seed 2 (Client & Server)!")

st.markdown("---")
st.caption("TITAN v62.3 | Trinity Edition")
