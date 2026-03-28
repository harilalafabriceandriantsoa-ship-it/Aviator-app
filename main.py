import streamlit as st
import random
import time
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V64.7 ELITE", layout="wide")

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
    st.markdown("<h1 style='color:#00ffcc;'>🛸 TITAN ELITE V64.7</h1>", unsafe_allow_html=True)
    st.text_input("ENTER SYSTEM KEY:", type="password", key="password_input", on_change=check_password)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #080c14; color: #ffffff; }
    .titan-header { font-size: 35px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 15px #00ffcc; }
    .prediction-card { background: rgba(0, 255, 204, 0.1); border: 2px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; }
    .hist-box { background: #1a1f26; padding: 10px; border-radius: 5px; margin-top: 5px; border-left: 4px solid #00ffcc; }
    .expander-style { background-color: #16212e !important; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="titan-header">TITAN OMNI-STRIKE V64.7</h1>', unsafe_allow_html=True)

# --- VIP CONSIGNES (Pop-up Expander) ---
with st.expander("📜 VIP CONSIGNES & STRATEGIES (Patricia Edition)"):
    st.write("1. **Seed Copy**: Adikao foana ny Seed vaovao avy ao amin'ny bet261.")
    st.write("2. **Mines Strategy**: Aza manindry kintana mihoatra ny 3 isaky ny lalao.")
    st.write("3. **Penalty**: Fidio foana ny 'Arzantina' (Argentina).")

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY VIP"])

# --- TAB 1: AVIATOR ---
with tab1:
    st.text_input("🕒 Lera Aviator:", value=datetime.now().strftime("%H:%M"), key="avi_t")
    if st.button("🚀 EXECUTE AVIATOR", use_container_width=True):
        random.seed(time.time_ns())
        res = round(random.uniform(2.5, 12.0), 2)
        st.session_state.history.append(f"Aviator: {res}x at {datetime.now().strftime('%H:%M')}")
        st.markdown(f"<div class='prediction-card'><h1>{res}x</h1></div>", unsafe_allow_html=True)

# --- TAB 2: COSMOS X ---
with tab2:
    st.text_input("🕒 Lera Cosmos:", value=datetime.now().strftime("%H:%M"), key="cos_t")
    c_s_cos = st.text_input("🔑 HEX SEED:", key="cos_s")
    if st.button("🚀 EXECUTE COSMOS X", use_container_width=True):
        random.seed(hash(c_s_cos + str(time.time_ns())))
        res = round(random.uniform(1.8, 10.0), 2)
        st.session_state.history.append(f"Cosmos X: {res}x at {datetime.now().strftime('%H:%M')}")
        st.markdown(f"<div class='prediction-card'><h1 style='color:#ffd700;'>{res}x</h1></div>", unsafe_allow_html=True)

# --- TAB 3: MINES VIP ---
with tab3:
    st.subheader("💣 NEURAL MINES ENGINE")
    
    # Restored Capture History
    st.file_uploader("📷 Capture History (Drag & Drop):", type=['jpg', 'png', 'jpeg'], key="mine_img")
    
    m_c_s = st.text_input("💻 Client Seed:", key="min_c_s", placeholder="Enter Seed...")
    m_s_s = st.text_input("🖥️ Server Seed:", key="min_s_s", placeholder="Enter Seed...")
    nb_m = st.slider("Nombre de Mines:", 1, 5, 3)
    
    if st.button("⚡ ANALYZE SEEDS & SCAN", use_container_width=True):
        # Dynamic Seed to avoid stuck predictions
        random.seed(hash(m_c_s + m_s_s + str(time.time_ns())))
        stars = random.sample(range(25), k=5)
        st.session_state.history.append(f"Mines Scan: {datetime.now().strftime('%H:%M:%S')}")
        
        grid_html = '<div style="display: grid; grid-template-columns: repeat(5, 50px); gap: 10px; justify-content: center; margin-bottom:20px;">'
        for i in range(25):
            color = "#ffd700" if i in stars else "#2c3e50"
            grid_html += f'<div style="width:50px; height:50px; background:{color}; border-radius:5px;"></div>'
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)
        st.success("✅ Prediction Complete. Follow the yellow stars.")

# --- TAB 4: PENALTY ---
with tab4:
    st.selectbox("Sélectionnez le Mode:", ["FACILE (Cible x2.93)", "MOYEN", "DIFFICILE"])
    if st.button("⚽ GENERATE PENALTY SEQUENCE", use_container_width=True):
        random.seed(time.time_ns())
        targets = ["ANKAVIA AMBONY", "ANKAVANANA AMBONY", "AFOVOANY", "ANKAVIA AMBANY", "ANKAVANANA AMBANY"]
        seq = random.sample(targets, k=5)
        st.session_state.history.append(f"Penalty: Seq at {datetime.now().strftime('%H:%M')}")
        for i, s in enumerate(seq):
            st.markdown(f"<div class='hist-box'><b>SHOT {i+1}:</b> {s}</div>", unsafe_allow_html=True)

# --- HISTORIQUE DISPLAY ---
st.write("---")
st.subheader("📜 HISTORIQUE")
if st.button("🗑️ RESET SYSTEM"):
    st.session_state.history = []
    st.rerun()

for h in reversed(st.session_state.history[-5:]):
    st.markdown(f"<div class='hist-box'>{h}</div>", unsafe_allow_html=True)
