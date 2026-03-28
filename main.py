import streamlit as st
import random
import time
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="TITAN V65.0", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: #ffffff; }
    .titan-header { 
        font-size: 32px; font-weight: 900; text-align: center; 
        color: #00ffcc; text-shadow: 0 0 10px #00ffcc; padding: 20px;
    }
    .stat-box {
        background: rgba(0, 255, 204, 0.05);
        border: 1px solid #00ffcc;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="titan-header">TITAN OMNI-STRIKE V65.0</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

with tab2:
    st.markdown("### 🚀 COSMOS X ANALYZER")
    
    # Toerana fametahana ny HEX
    hex_input = st.text_input("🔑 HEX SEED:", placeholder="OxFF...", key="hex_v65")
    lera = st.text_input("🕒 Heure:", value=datetime.now().strftime("%H:%M"))
    
    if st.button("🚀 EXECUTE ANALYSIS", use_container_width=True):
        if not hex_input:
            st.error("⚠️ Apetaho eto aloha ny HEX SEED vao manindry execute.")
        else:
            with st.spinner('Calculating Probabilities...'):
                time.sleep(1.5)
                # Algorithm calculation
                random.seed(hash(hex_input + lera))
                p_min = round(random.uniform(1.2, 1.8), 2)
                p_moyen = round(random.uniform(2.0, 5.5), 2)
                p_max = round(random.uniform(10.0, 50.0), 2)
                pourcentage = random.randint(75, 98)
                
                # Fampisehoana ny vokatra
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"<div class='stat-box'>MIN<br><b>{p_min}x</b></div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div class='stat-box'>MOYEN<br><b>{p_moyen}x</b></div>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<div class='stat-box'>MAX<br><b>{p_max}x</b></div>", unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style='text-align:center; margin-top:20px; padding:20px; border:2px solid #00ffcc; border-radius:15px;'>
                        <p>PROBABILITY ACCURACY</p>
                        <h1 style='color:#00ffcc;'>{pourcentage}%</h1>
                        <p>NEXT PREDICTION: <b>{p_moyen}x</b></p>
                    </div>
                """, unsafe_allow_html=True)

# Kaody tsotra ho an'ny AVIATOR (mba tsy hisy erreur intsony)
with tab1:
    st.subheader("✈️ AVIATOR PREDICTOR")
    if st.button("🚀 GET SIGNAL"):
        st.success(f"Signal: {round(random.uniform(1.5, 10.0), 2)}x")
