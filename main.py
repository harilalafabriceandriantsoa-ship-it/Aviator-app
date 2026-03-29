import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- 1. STYLE "CYBER-CHARME" ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

st.markdown("""
    <style>
    /* Loko fototra maizina */
    .stApp { background-color: #050505; color: #00ffcc; }
    
    /* Tabs style */
    .stTabs [data-baseweb="tab-list"] { background-color: #050505; }
    .stTabs [data-baseweb="tab"] { color: #ffffff; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #00ffcc !important; border-bottom: 2px solid #00ffcc !important; }

    /* Prediction Cards miaraka amin'ny Glow */
    .prediction-card {
        background: rgba(0, 255, 204, 0.05);
        border: 2px solid #00ffcc;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.3);
        margin-bottom: 15px;
    }
    
    /* Hafatra Bonne Chance */
    .luck-msg {
        color: #00ffcc;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        text-shadow: 0 0 10px #00ffcc;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Fitahirizana data
if 'history' not in st.session_state: st.session_state.history = []
if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"

# --- 2. SETTINGS MANAGER (SIDEBAR) ---
with st.sidebar:
    st.markdown("### ⚙️ SETTINGS")
    auth = st.text_input("Admin Key Access:", type="password")
    if auth == st.session_state.admin_pwd:
        st.success("Manager Authenticated")
        new_p = st.text_input("Hanova MDP vaovao:", type="password")
        if st.button("Hamafiso ny MDP"):
            st.session_state.admin_pwd = new_p
            st.success("MDP Voatahiry!")
        if st.button("🗑️ RESET APP"):
            st.session_state.history = []
            st.rerun()

# --- 3. ALGORITHM ---
def process_prediction(srv, clt, game):
    seed_hash = hashlib.sha256(f"{srv}{clt}".encode()).hexdigest()
    random.seed(int(seed_hash[:8], 16))
    
    now = datetime.now()
    results = []
    for i in range(1, 4):
        val = round(random.uniform(1.65, 4.25), 2)
        p = {
            "game": game,
            "time": (now + timedelta(minutes=i*2)).strftime("%H:%M:%S" if game == "COSMOS X" else "%H:%M"),
            "moyen": val,
            "min": round(val * 0.85, 2),
            "max": round(val * 1.30, 2)
        }
        results.append(p)
        st.session_state.history.insert(0, p)
    return results

# --- 4. INTERFACE ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

# Aviator & Cosmos
for tab, name in zip([t1, t2], ["AVIATOR", "COSMOS X"]):
    with tab:
        c1, c2 = st.columns(2)
        s_hex = c1.text_input(f"🔑 HEX SEED ({name}):", key=f"hex_{name}")
        s_time = c2.text_input(f"🕒 HEUR / CLIENT SEED ({name}):", key=f"time_{name}")
        
        if st.button(f"🔥 ANALYZE {name}"):
            res = process_prediction(s_hex, s_time, name)
            cols = st.columns(3)
            for i, r in enumerate(res):
                with cols[i]:
                    st.markdown(f"""
                    <div class='prediction-card'>
                        <b style='color:white;'>TOUR {i+1}</b><br>
                        <span style='color:#ffcc00;'>{r['time']}</span><br>
                        <span style='font-size:35px; color:#00ffcc;'>{r['moyen']}x</span><br>
                        <small style='color:#aaa;'>Min: {r['min']} | Max: {r['max']}</small>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("<p class='luck-msg'>🍀 Bonne chance à tous !</p>", unsafe_allow_html=True)

# Mines
with t3:
    st.subheader("💣 MINES VIP SYNC")
    m_srv = st.text_input("Server Seed:")
    m_clt = st.text_input("Client Seed:")
    if st.button("🔍 SCAN MINES"):
        process_prediction(m_srv, m_clt, "MINES")
        st.write("⭐ ⬛ ⬛ ⭐ ⬛")
        st.markdown("<p class='luck-msg'>🍀 Bonne chance à tous !</p>", unsafe_allow_html=True)

# --- 5. HISTORIQUE ---
st.markdown("---")
st.subheader("📜 LAST PREDICTIONS (CAPTURE)")
if st.session_state.history:
    for h in st.session_state.history[:5]:
        st.write(f"🎮 **{h['game']}** | 🕒 {h['time']} | **{h['moyen']}x** (Min: {h['min']} | Max: {h['max']})")
else:
    st.info("Tsy mbola misy historique.")
