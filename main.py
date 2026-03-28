import streamlit as st
import random
import time
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V64.9 PREMIUM", layout="wide")

if 'history' not in st.session_state:
    st.session_state.history = []
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if st.session_state.get("password_input") == "TITAN2026": 
        st.session_state.authenticated = True
    else:
        st.error("❌ ACCESS DENIED.")

# --- LOGIN ---
if not st.session_state.authenticated:
    st.markdown("<style>.stApp { background-color: #050a10; }</style>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; padding:50px; border:2px solid #00ffcc; border-radius:30px; margin-top:100px;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#00ffcc;'>🛸 TITAN PREMIUM V64.9</h1>", unsafe_allow_html=True)
    st.text_input("ENTER SYSTEM KEY:", type="password", key="password_input", on_change=check_password)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- STYLE CSS (FIXED) ---
st.markdown("""
    <style>
    .stApp { background-color: #080c14; color: #ffffff; }
    .titan-header { font-size: 35px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 15px #00ffcc; margin-bottom: 5px; }
    .signal-status { text-align: center; color: #00ffcc; font-size: 14px; margin-bottom: 25px; font-weight: bold; }
    .prediction-card { background: rgba(0, 255, 204, 0.1); border: 2px solid #00ffcc; border-radius: 15px; padding: 25px; text-align: center; margin: 15px 0; }
    .hist-box { background: #1a1f26; padding: 12px; border-radius: 8px; margin-top: 8px; border-left: 5px solid #00ffcc; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="titan-header">TITAN OMNI-STRIKE V64.9</h1>', unsafe_allow_html=True)
st.markdown('<p class="signal-status">● PREMIUM MODE ACTIVE | SYSTEM STABLE</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY VIP"])

# --- TAB 1: AVIATOR ---
with tab1:
    st.subheader("✈️ AVIATOR PREDICTOR")
    st.file_uploader("📷 Capture Aviator History:", type=['jpg', 'png', 'jpeg'], key="avi_img")
    st.text_input("🕒 Lera Aviator:", value=datetime.now().strftime("%H:%M"), key="avi_t")
    
    if st.button("🚀 GET SIGNAL", use_container_width=True):
        with st.spinner('Analyzing...'):
            time.sleep(1)
            random.seed(time.time_ns())
            res = round(random.uniform(2.1, 14.8), 2)
            st.session_state.history.append(f"Aviator: {res}x ({st.session_state.avi_t})")
            st.markdown(f"<div class='prediction-card'><h2 style='color:#00ffcc;'>PROCHAIN CRASH:</h2><h1>{res}x</h1></div>", unsafe_allow_html=True)

# --- TAB 2: COSMOS X (FIXED HEX) ---
with tab2:
    st.subheader("🚀 COSMOS X ANALYZER")
    st.file_uploader("📷 Capture Cosmos History:", type=['jpg', 'png', 'jpeg'], key="cos_img")
    # Tafaverina eto ilay HEX SEED
    st.text_input("🔑 HEX SEED (Paste from game):", placeholder="OxFF...", key="cos_hex")
    st.text_input("🕒 Lera Cosmos:", value=datetime.now().strftime("%H:%M"), key="cos_t")
    
    if st.button("🚀 EXECUTE COSMOS", use_container_width=True):
        seed_val = st.session_state.cos_hex if st.session_state.cos_hex else str(time.time_ns())
        random.seed(hash(seed_val + st.session_state.cos_t))
        res = round(random.uniform(1.8, 11.5), 2)
        st.session_state.history.append(f"Cosmos X: {res}x ({st.session_state.cos_t})")
        st.markdown(f"<div class='prediction-card'><h2 style='color:#ffd700;'>SIGNAL:</h2><h1>{res}x</h1></div>", unsafe_allow_html=True)

# --- TAB 3: MINES VIP ---
with tab3:
    st.subheader("💣 NEURAL MINES")
    st.file_uploader("📷 Grid Capture:", type=['jpg', 'png', 'jpeg'], key="mine_img")
    m_seed = st.text_input("💻 Current Seed:", key="min_seed")
    nb_m = st.slider("Nombre de Mines:", 1, 5, 3)
    
    if st.button("⚡ SCAN GRID", use_container_width=True):
        random.seed(hash(m_seed + str(time.time_ns())))
        stars = random.sample(range(25), k=5)
        st.session_state.history.append(f"Mines: Grid Generated")
        
        grid_html = '<div style="display: grid; grid-template-columns: repeat(5, 50px); gap: 10px; justify-content: center; padding: 20px;">'
        for i in range(25):
            color = "#ffd700" if i in stars else "#2c3e50"
            grid_html += f'<div style="width:50px; height:50px; background:{color}; border-radius:8px; border:1px solid #444;"></div>'
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)

# --- TAB 4: PENALTY ---
with tab4:
    st.subheader("⚽ PENALTY VIP")
    st.selectbox("Mode:", ["FACILE (x2.93)", "MOYEN", "DIFFICILE"], key="pen_mode")
    if st.button("⚽ GENERATE SEQUENCE", use_container_width=True):
        targets = ["ANKAVIA AMBONY", "ANKAVANANA AMBONY", "AFOVOANY", "ANKAVIA AMBANY", "ANKAVANANA AMBANY"]
        seq = random.sample(targets, k=5)
        for i, s in enumerate(seq):
            st.markdown(f"<div class='hist-box'><b>SHOT {i+1}:</b> {s}</div>", unsafe_allow_html=True)

# --- HISTORIQUE ---
st.write("---")
st.subheader("🕒 LAST SIGNALS")
if st.button("🗑️ CLEAR CACHE"):
    st.session_state.history = []
    st.rerun()

for h in reversed(st.session_state.history[-5:]):
    st.markdown(f"<div class='hist-box'>{h}</div>", unsafe_allow_html=True)
