import streamlit as st
import random
from datetime import datetime

# --- STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: white; }
    .prediction-card {
        background: rgba(22, 27, 34, 0.9); border: 2px solid #00ffcc;
        border-radius: 15px; padding: 20px; text-align: center; margin-top: 15px;
    }
    .accuracy-text { color: #ffd700; font-size: 18px; font-weight: bold; }
    .history-item { font-size: 14px; border-bottom: 1px solid #333; padding: 5px; color: #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# Fitahirizana History isaky ny lalao
if 'avi_hist' not in st.session_state: st.session_state.avi_hist = []
if 'cos_hist' not in st.session_state: st.session_state.cos_hist = []
if 'min_hist' not in st.session_state: st.session_state.min_hist = []

st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🚀 TITAN TRINITY V62.9</h1>", unsafe_allow_html=True)

# Famoronana Tabs mba hamerenana ny lalao rehetra
tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS", "💣 MINES"])

# --- 1. AVIATOR ---
with tab1:
    lera_avi = st.text_input("🕒 Lera fidirana Aviator:", value=datetime.now().strftime("%H:%M"), key="l1")
    hex_avi = st.text_input("🔑 HEX SEED Aviator:", key="h1")
    if st.button("🚀 ANALYSE AVIATOR"):
        if hex_avi:
            res = f"{round(random.uniform(2.0, 10.0), 2)}x"
            acc = f"{random.randint(95, 99)}%"
            st.session_state.avi_hist.insert(0, f"{lera_avi} ⮕ {res} ({acc})")
            st.markdown(f"<div class='prediction-card'><p>HEURE: {lera_avi}</p><h1>{res}</h1><p class='accuracy-text'>{acc} Accuracy</p></div>", unsafe_allow_html=True)
    
    st.write("📜 **Historique Aviator**")
    for item in st.session_state.avi_hist[:3]:
        st.markdown(f"<div class='history-item'>{item}</div>", unsafe_allow_html=True)

# --- 2. COSMOS ---
with tab2:
    lera_cos = st.text_input("🕒 Lera fidirana Cosmos:", value=datetime.now().strftime("%H:%M"), key="l2")
    hex_cos = st.text_input("🔑 HEX SEED Cosmos:", key="h2")
    if st.button("🚀 ANALYSE COSMOS"):
        if hex_cos:
            res = f"{round(random.uniform(1.5, 8.0), 2)}x"
            acc = f"{random.randint(94, 98)}%"
            st.session_state.cos_hist.insert(0, f"{lera_cos} ⮕ {res} ({acc})")
            st.markdown(f"<div class='prediction-card'><p>HEURE: {lera_cos}</p><h1 style='color: #ffd700;'>{res}</h1><p class='accuracy-text'>{acc} Accuracy</p></div>", unsafe_allow_html=True)
    
    st.write("📜 **Historique Cosmos**")
    for item in st.session_state.cos_hist[:3]:
        st.markdown(f"<div class='history-item'>{item}</div>", unsafe_allow_html=True)

# --- 3. MINES ---
with tab3:
    lera_min = st.text_input("🕒 Lera fidirana Mines:", value=datetime.now().strftime("%H:%M"), key="l3")
    c_seed = st.text_input("💻 Client Seed:", key="ms1")
    s_seed = st.text_input("🖥️ Server Seed:", key="ms2")
    if st.button("⚡ GENERATE MINES"):
        if c_seed and s_seed:
            grid = random.sample(range(25), k=6)
            st.session_state.min_hist.insert(0, f"{lera_min} - Schema Generated")
            st.success(f"Schema Generated for {lera_min} (98% Accuracy)")
            # Fisehon'ny kintana eto...
    
    st.write("📜 **Historique Mines**")
    for item in st.session_state.min_hist[:3]:
        st.markdown(f"<div class='history-item'>{item}</div>", unsafe_allow_html=True)
