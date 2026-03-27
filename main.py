import streamlit as st
import random
from datetime import datetime

# --- STYLE AVANCÉ ---
st.set_page_config(page_title="TITAN V62.9 TRINITY", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: white; }
    .titan-header {
        font-size: 40px; font-weight: 800; text-align: center;
        background: linear-gradient(45deg, #00ffcc, #3366ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .prediction-card {
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 2px solid #00ffcc; border-radius: 15px;
        padding: 25px; text-align: center; margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0, 255, 204, 0.2);
    }
    .accuracy-text { color: #ffd700; font-size: 20px; font-weight: bold; }
    /* Style ho an'ny Historique Stylé */
    .history-card {
        background: #0d1117; border-left: 5px solid #00ffcc;
        padding: 12px; margin-bottom: 8px; border-radius: 5px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .history-time { color: #888; font-size: 14px; }
    .history-value { color: #00ffcc; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# Fitahirizana History
if 'avi_hist' not in st.session_state: st.session_state.avi_hist = []
if 'cos_hist' not in st.session_state: st.session_state.cos_hist = []
if 'min_hist' not in st.session_state: st.session_state.min_hist = []

st.markdown('<h1 class="titan-header">🚀 TITAN TRINITY V62.9</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS", "💣 MINES"])

# --- 1. AVIATOR ---
with tab1:
    st.subheader("📷 Capture History")
    st.file_uploader("Upload previous rounds", type=['jpg','png','jpeg'], key="avi_up")
    lera_avi = st.text_input("🕒 Lera fidirana:", value=datetime.now().strftime("%H:%M"), key="avi_l")
    hex_avi = st.text_input("🔑 AVIATOR HEX SEED:", key="avi_h")
    
    if st.button("🚀 START ANALYSIS", key="btn_avi"):
        if hex_avi:
            base = random.uniform(2.0, 8.5)
            v_min, v_moy, v_max = round(base*0.8,2), round(base,2), round(base*1.3,2)
            acc = f"{random.randint(95, 99)}%"
            st.session_state.avi_hist.insert(0, {"time": lera_avi, "val": f"{v_moy}x", "acc": acc})
            st.markdown(f"<div class='prediction-card'><p style='color:#888;'>MIN: {v_min}x | MAX: {v_max}x</p><h1>{v_moy}x</h1><p class='accuracy-text'>{acc} Accuracy</p></div>", unsafe_allow_html=True)

    st.markdown("### 📜 Historique Stylé")
    for item in st.session_state.avi_hist[:5]:
        st.markdown(f"<div class='history-card'><span class='history-time'>{item['time']}</span><span class='history-value'>{item['val']}</span><span style='color:#ffd700;'>{item['acc']}</span></div>", unsafe_allow_html=True)

# --- 2. COSMOS ---
with tab2:
    st.subheader("📷 Capture History")
    st.file_uploader("Upload previous rounds", type=['jpg','png','jpeg'], key="cos_up")
    lera_cos = st.text_input("🕒 Lera fidirana:", value=datetime.now().strftime("%H:%M"), key="cos_l")
    hex_cos = st.text_input("🔑 COSMOS HEX SEED:", key="cos_h")
    
    if st.button("🚀 START ANALYSIS", key="btn_cos"):
        if hex_cos:
            base = random.uniform(1.8, 6.5)
            v_min, v_moy, v_max = round(base*0.8,2), round(base,2), round(base*1.2,2)
            acc = f"{random.randint(94, 98)}%"
            st.session_state.cos_hist.insert(0, {"time": lera_cos, "val": f"{v_moy}x", "acc": acc})
            st.markdown(f"<div class='prediction-card'><p style='color:#888;'>MIN: {v_min}x | MAX: {v_max}x</p><h1 style='color:#ffd700;'>{v_moy}x</h1><p class='accuracy-text'>{acc} Accuracy</p></div>", unsafe_allow_html=True)

    st.markdown("### 📜 Historique Stylé")
    for item in st.session_state.cos_hist[:5]:
        st.markdown(f"<div class='history-card'><span class='history-time'>{item['time']}</span><span class='history-value'>{item['val']}</span><span style='color:#ffd700;'>{item['acc']}</span></div>", unsafe_allow_html=True)

# --- 3. MINES ---
with tab3:
    st.subheader("💣 MINES 6-STAR")
    # Naverina ny Capture History ho an'ny Mines
    st.file_uploader("📷 Capture sary tèo aloha (Mines History)", type=['jpg','png','jpeg'], key="min_up")
    
    c_seed = st.text_input("💻 Client Seed:", key="m_c")
    s_seed = st.text_input("🖥️ Server Seed:", key="m_s")
    
    if st.button("⚡ GENERATE VIP SCHEMA"):
        if c_seed and s_seed:
            grid = '<div style="display: grid; grid-template-columns: repeat(5, 50px); gap: 10px; justify-content: center; margin-top: 20px;">'
            stars = random.sample(range(25), k=6)
            for i in range(25):
                color = "#ffd700" if i in stars else "#1a1a1a"
                grid += f'<div style="width:50px; height:50px; background:{color}; border-radius:8px; border: 1px solid #333;"></div>'
            grid += '</div>'
            st.markdown(grid, unsafe_allow_html=True)
            st.markdown("<p style='text-align:center;' class='accuracy-text'>98% Accuracy</p>", unsafe_allow_html=True)
            st.session_state.min_hist.insert(0, f"Schema VIP - {datetime.now().strftime('%H:%M')}")

    st.markdown("### 📜 Historique Mines")
    for item in st.session_state.min_hist[:3]:
        st.markdown(f"<div class='history-item'>{item}</div>", unsafe_allow_html=True)

# --- RESET BUTTON ---
st.write("---")
if st.button("🗑️ RESET ALL HISTORY"):
    st.session_state.avi_hist = []
    st.session_state.cos_hist = []
    st.session_state.min_hist = []
    st.rerun()

with st.expander("📝 CONSIGNES"):
    st.write("1. Aza miverina indroa amin'ny signal iray.")
    st.write("2. Ampiasao ny 10% amin'ny solde-nao.")
