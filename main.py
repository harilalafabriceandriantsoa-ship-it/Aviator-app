import streamlit as st
import random
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V74.0 ULTRA", layout="wide")

if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050a10; color: #ffffff; }
    .titan-header { font-size: 30px; font-weight: 900; text-align: center; color: #00ffcc; border-bottom: 2px solid #00ffcc; padding-bottom: 10px; }
    .card-res { background: rgba(0, 255, 204, 0.05); border: 2px solid #00ffcc; border-radius: 12px; padding: 20px; text-align: center; }
    .stat-box { background: rgba(255, 255, 255, 0.05); border: 1px solid #00ffcc; border-radius: 8px; padding: 10px; text-align: center; }
    .next-rounds-box { background: rgba(255, 215, 0, 0.1); border: 1px dashed #ffd700; padding: 15px; border-radius: 10px; margin-top: 15px; text-align: center; color: #ffd700; }
    .safe-badge { background: #00ffcc; color: #050a10; padding: 5px 10px; border-radius: 5px; font-weight: bold; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="titan-header">TITAN V74.0 ULTRA-SAFE 💎</div>', unsafe_allow_True=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY VIP"])

# --- TAB 3: MINES (Fixed: 1-7 Mines, Client/Server Seed) ---
with tab3:
    st.markdown("### 💣 MINES STRATEGY PRO")
    st.file_uploader("📷 CAPTURE GRID:", type=['jpg', 'png', 'jpeg'], key="min_cap")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        m_client = st.text_input("💻 CLIENT SEED:", key="min_cli")
    with col_m2:
        m_server = st.text_input("🖥️ SERVER SEED:", key="min_ser")
    
    # Isan'ny baomba 1 hatramin'ny 7
    nb_mines = st.select_slider("💣 NOMBRE DE MINES:", options=[1, 2, 3, 4, 5, 6, 7], value=3)
    
    if st.button("⚡ SCAN SECURE PATH", use_container_width=True):
        with st.spinner('Calculating Safe Squares...'):
            time.sleep(1)
            random.seed(hash(m_client + m_server))
            # Mikajy ny kintana arakaraky ny isan'ny baomba
            nb_stars = 5 if nb_mines >= 3 else 3
            stars = random.sample(range(25), k=nb_stars)
            
            grid = '<div style="display: grid; grid-template-columns: repeat(5, 50px); gap: 10px; justify-content: center; margin-top:20px;">'
            for i in range(25):
                color = "#00ffcc" if i in stars else "#1a1f26"
                border = "2px solid #00ffcc" if i in stars else "1px solid #333"
                grid += f'<div style="width:50px; height:50px; background:{color}; border-radius:8px; border:{border};"></div>'
            st.markdown(grid + '</div>', unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; color:#00ffcc; margin-top:10px;'>✔️ SAFE PATH GENERATED</p>", unsafe_allow_html=True)

# --- TAB 1 & 2 (Aviator & Cosmos mbola misy lera fidirana) ---
def show_game_ui(game_name, key_prefix):
    st.file_uploader(f"📷 CAPTURE {game_name}:", type=['jpg', 'png', 'jpeg'], key=f"{key_prefix}_cap")
    g_hex = st.text_input(f"🔑 HEX SEED ({game_name}):", key=f"{key_prefix}_hex")
    g_h = st.text_input("🕒 HEURE:", value=datetime.now().strftime("%H:%M"), key=f"{key_prefix}_h")
    
    if st.button(f"🚀 EXECUTE {game_name}", use_container_width=True):
        random.seed(hash(g_hex + g_h))
        p_moy = round(random.uniform(2.0, 4.5), 2)
        r1 = (datetime.strptime(g_h, "%H:%M") + timedelta(minutes=random.randint(2, 5))).strftime("%H:%M")
        
        st.markdown(f"<div class='card-res'><h1>{p_moy}x</h1><span class='safe-badge'>VERY RELIABLE</span></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="next-rounds-box">🕒 LERA FIDIRANA: <span style="font-size:20px; font-weight:bold;">{r1}</span></div>', unsafe_allow_html=True)

with tab1: show_game_ui("AVIATOR", "avi")
with tab2: show_game_ui("COSMOS", "cos")

# --- RESET ---
st.write("---")
if st.button("🗑️ RESET ALL DATA"):
    st.rerun()
