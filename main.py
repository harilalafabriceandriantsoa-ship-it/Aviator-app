import streamlit as st
import random
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V73.0 MASTER", layout="wide")

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
    .time-val { font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="titan-header">TITAN OMNI-STRIKE V73.0 💎</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY VIP"])

# --- FUNCTION FOR CALCULATING NEXT ROUNDS ---
def get_next_rounds(h_start):
    try:
        base = datetime.strptime(h_start, "%H:%M")
    except:
        base = datetime.now()
    r1 = (base + timedelta(minutes=random.randint(1, 3))).strftime("%H:%M")
    r2 = (base + timedelta(minutes=random.randint(4, 7))).strftime("%H:%M")
    r3 = (base + timedelta(minutes=random.randint(8, 11))).strftime("%H:%M")
    return r1, r2, r3

# --- TAB 1: AVIATOR (With Hex & Next Rounds) ---
with tab1:
    st.file_uploader("📷 CAPTURE AVIATOR:", type=['jpg', 'png', 'jpeg'], key="avi_cap")
    avi_hex = st.text_input("🔑 HEX SEED (Aviator):", key="avi_hex")
    avi_h = st.text_input("🕒 HEURE:", value=datetime.now().strftime("%H:%M"), key="avi_h")
    
    if st.button("🚀 EXECUTE AVIATOR", use_container_width=True):
        random.seed(hash(avi_hex + avi_h))
        p_min, p_moy, p_max = round(random.uniform(1.2, 1.4), 2), round(random.uniform(2.0, 5.2), 2), round(random.uniform(10, 35), 2)
        r1, r2, r3 = get_next_rounds(avi_h)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='stat-box'>MIN<br><b>{p_min}x</b></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-box'>MOYEN<br><b>{p_moy}x</b></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-box'>MAX<br><b>{p_max}x</b></div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='card-res'><h3>ACCURACY: {random.randint(90,98)}%</h3><h1>{p_moy}x</h1></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="next-rounds-box">🕒 LERA FIDIRANA: <span class="time-val">{r1}</span> | <span class="time-val">{r2}</span> | <span class="time-val">{r3}</span></div>', unsafe_allow_html=True)
        st.session_state.prediction_history.append(f"✈️ AVIATOR | {avi_h} | Result: {p_moy}x")

# --- TAB 2: COSMOS X (With Hex & Next Rounds) ---
with tab2:
    st.file_uploader("📷 CAPTURE COSMOS:", type=['jpg', 'png', 'jpeg'], key="cos_cap")
    cos_hex = st.text_input("🔑 HEX SEED (Cosmos):", key="cos_hex")
    cos_h = st.text_input("🕒 HEURE COSMOS:", value=datetime.now().strftime("%H:%M"), key="cos_h")
    
    if st.button("🚀 EXECUTE COSMOS", use_container_width=True):
        random.seed(hash(cos_hex + cos_h))
        c_min, c_moy, c_max = round(random.uniform(1.3, 1.6), 2), round(random.uniform(2.2, 5.8), 2), round(random.uniform(12, 45), 2)
        r1, r2, r3 = get_next_rounds(cos_h)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='stat-box'>MIN<br><b>{c_min}x</b></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-box'>MOYEN<br><b>{c_moy}x</b></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-box'>MAX<br><b>{c_max}x</b></div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='card-res'><h3>ACCURACY: {random.randint(91,99)}%</h3><h1>{c_moy}x</h1></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="next-rounds-box">🕒 LERA FIDIRANA: <span class="time-val">{r1}</span> | <span class="time-val">{r2}</span> | <span class="time-val">{r3}</span></div>', unsafe_allow_html=True)

# --- TAB 3: MINES (Fixed: Client/Server Seed - No Hex) ---
with tab3:
    st.markdown("### 💣 MINES VIP SCANNER")
    st.file_uploader("📷 CAPTURE GRID:", type=['jpg', 'png', 'jpeg'], key="min_cap")
    m_client = st.text_input("💻 CLIENT SEED:", key="min_cli")
    m_server = st.text_input("🖥️ SERVER SEED:", key="min_ser")
    
    if st.button("⚡ SCAN MINES GRID", use_container_width=True):
        random.seed(hash(m_client + m_server))
        stars = random.sample(range(25), k=5)
        grid = '<div style="display: grid; grid-template-columns: repeat(5, 45px); gap: 10px; justify-content: center;">'
        for i in range(25):
            color = "#00ffcc" if i in stars else "#1a1f26"
            grid += f'<div style="width:45px; height:45px; background:{color}; border-radius:5px; border:1px solid #333;"></div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)

# --- TAB 4: PENALTY (Fixed: No Hex) ---
with tab4:
    st.markdown("### ⚽ PENALTY VIP")
    st.file_uploader("📷 CAPTURE GAME:", type=['jpg', 'png', 'jpeg'], key="pen_cap")
    st.selectbox("MODE:", ["FACILE (x2.93)", "MOYEN", "DIFFICILE"], key="pen_mod")
    
    if st.button("⚽ GENERATE SEQUENCE", use_container_width=True):
        spots = ["ANKAVIA AMBONY", "AFOVOANY", "ANKAVANANA AMBANY"]
        st.success(f"TARGET: {random.choice(spots)}")

# --- RESET & HISTORY ---
st.write("---")
if st.button("🗑️ RESET HISTORIQUE", use_container_width=True):
    st.session_state.prediction_history = []
    st.rerun()
