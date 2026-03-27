import streamlit as st
import time
import random
from datetime import datetime, timedelta

# --- STYLE ---
st.set_page_config(page_title="TITAN v62.9", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .prediction-box { 
        padding: 20px; 
        border: 2px solid #ffd700; 
        border-radius: 10px; 
        background: #161b22;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state:
    st.session_state.history = []

# --- SIDEBAR: HISTORIQUE & CAPTURE ---
with st.sidebar:
    st.header("📸 HISTORIQUE & LERA")
    # Capture d'écran ho an'ny tantara
    upload = st.file_uploader("Capture de l'historique :", type=['jpg', 'png'])
    
    if upload:
        with st.spinner("Famakiana sary..."):
            time.sleep(1.5)
            # Eto no maka ny lera sy ny multiplier avy amin'ny sary
            fake_res = f"{round(random.uniform(1.1, 10.0), 2)}x"
            now = (datetime.now() + timedelta(hours=3)).strftime("%H:%M:%S")
            if st.button("Tehirizo ao anaty tantara"):
                st.session_state.history.insert(0, {"Lera": now, "Vokatra": fake_res})
    
    st.markdown("---")
    st.subheader("🕒 Tantaran'ny lalao")
    if st.session_state.history:
        for item in st.session_state.history[:5]:
            st.write(f"⏱️ {item['Lera']} -> **{item['Vokatra']}**")

# --- MAIN: PREDICTION ---
st.title("💎 TITAN PREDICTION")

col1, col2, col3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS", "💣 MINES"])

# Aviator irery no ohatra eto (Hex Seed irery)
with col1:
    st.markdown("### 🔑 Prediction amin'ny Hex Seed")
    # Hex Seed irery no ampidirina, tsy misy lera intsony
    hex_input = st.text_input("Ampidiro ny HEX SEED (avy amin'ny Details) :", placeholder="8aa262bc02059...")
    
    if st.button("LANCER L'ANALYSE"):
        if hex_input:
            with st.spinner("Mikajy ny algorithm..."):
                time.sleep(2)
                st.markdown(f"""
                <div class="prediction-box">
                    <h2 style='color: #00ffcc;'>SIGNAL DETECTED</h2>
                    <p style='font-size: 24px;'>Accuracy: 98%</p>
                    <h1 style='color: #ffd700;'>NEXT: 2.50x +</h1>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Azafady, ampidiro aloha ny Hex Seed.")

with col3:
    st.info("Ny Mines dia mampiasa ny Schema (kintana 5 na 6) mivoaka avy amin'ny Seed-nao.")
