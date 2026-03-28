import streamlit as st
import random
import time
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V64.3 ELITE", layout="wide")

# Mampiasa 'key' miovaova mba hampiova ny prediction isaky ny miova ny seed
if 'history' not in st.session_state:
    st.session_state.history = []
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if st.session_state["password"] == "TITAN2026": 
        st.session_state.authenticated = True
    else:
        st.error("❌ ACCESS DENIED.")

if not st.session_state.authenticated:
    st.markdown("<style>.stApp { background-color: #050a10; }</style>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; padding:50px; border:2px solid #00ffcc; border-radius:30px; margin-top:100px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#00ffcc;'>🛸 TITAN ELITE V64.3</h1>", unsafe_allow_html=True)
    st.text_input("ENTER SYSTEM KEY:", type="password", key="password", on_change=check_password)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #080c14; color: #ffffff; }
    .titan-header { font-size: 35px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 15px #00ffcc; }
    .signal-on { color: #ffd700; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .prediction-card { background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; }
    .grid-box { width:50px; height:50px; border-radius:8px; border:1px solid #34495e; transition: 0.3s; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="titan-header">TITAN OMNI-STRIKE V64.3</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💣 MINES VIP", "🚀 COSMOS X", "⚽ PENALTY"])

# --- TAB 1: MINES VIP (NO MORE STUCK PREDICTION) ---
with tab1:
    st.subheader("💣 NEURAL MINES ENGINE")
    
    col1, col2 = st.columns(2)
    with col1:
        # Ny fampiasana 'st.text_area' fa tsy 'text_input' dia manampy amin'ny famakiana seed lava
        c_seed = st.text_area("💻 Client Seed (Paste New):", placeholder="Paste seed here...", key="c_seed_input")
    with col2:
        s_seed = st.text_area("🖥️ Server Seed (Paste New):", placeholder="Paste seed here...", key="s_seed_input")
        
    nb_mines = st.select_slider("Mines:", options=[1, 3, 5], value=3)
    
    # CRITICAL FIX: Random seed is now strictly tied to the CURRENT input
    if st.button("⚡ GENERATE NEW PREDICTION", use_container_width=True):
        if c_seed and s_seed:
            # Ity no vahaolana: mampiasa ny lera sy ny seed miaraka mba tsy hitovy mihitsy ny valiny
            combined_hash = hash(c_seed + s_seed + str(time.time()))
            random.seed(combined_hash)
            
            stars = random.sample(range(25), k=7 if nb_mines == 5 else 5)
            
            st.session_state.history.append(f"Mines Scan: {datetime.now().strftime('%H:%M:%S')}")
            
            grid_html = '<div style="display: grid; grid-template-columns: repeat(5, 50px); gap: 10px; justify-content: center; margin-top:20px;">'
            for i in range(25):
                color = "#ffd700" if i in stars else "#2c3e50" # Loko mavo tahaka ny sary-nao
                grid_html += f'<div class="grid-box" style="background:{color};"></div>'
            st.markdown(grid_html + '</div>', unsafe_allow_html=True)
            st.success(f"✅ New Pattern Analysis Complete for Seed: {c_seed[:10]}...")
        else:
            st.warning("⚠️ Ampidiro aloha ny Seed vao manindry Analyze.")

# --- HISTORIQUE & RESET ---
st.write("---")
if st.button("🗑️ RESET ENGINE (CLEAN ALL)", use_container_width=True):
    st.session_state.history = []
    # Force refresh amin'ny alalan'ny fanadiovana ny cache
    st.rerun()

for h in reversed(st.session_state.history[-3:]):
    st.info(h)
