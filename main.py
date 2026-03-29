import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #00ffcc; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #161b22; border-radius: 10px 10px 0 0;
        padding: 10px 20px; color: white;
    }
    .stTabs [aria-selected="true"] { background-color: #00ffcc !important; color: black !important; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc;
        padding: 15px; border-radius: 15px; text-align: center; margin: 5px;
        box-shadow: 0 0 10px rgba(0, 255, 204, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. CORE ALGORITHM ---
def get_prediction(srv, clt, game):
    seed_combined = hashlib.sha256(f"{srv}{clt}".encode()).hexdigest()
    random.seed(int(seed_combined[:10], 16))
    
    results = []
    base_time = datetime.now()
    
    for i in range(1, 4):
        moyen = round(random.uniform(1.60, 4.80), 2)
        # Fanovana ny lera ho an'ny Cosmos (misy segondra)
        time_fmt = "%H:%M:%S" if game == "COSMOS X" else "%H:%M"
        
        p = {
            "game": game,
            "time": (base_time + timedelta(minutes=i*2)).strftime(time_fmt),
            "moyen": moyen,
            "min": round(moyen * 0.85, 2),
            "max": round(moyen * 1.30, 2)
        }
        results.append(p)
        st.session_state.history.insert(0, p)
    return results

# --- 3. INTERFACE ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

# --- AVIATOR ---
with tab1:
    st.subheader("⚡ AVIATOR SCANNER")
    st.file_uploader("📸 UPLOAD SCREENSHOT (HISTORIQUE)", type=['png','jpg'], key="img_avi")
    col1, col2 = st.columns(2)
    hex_seed = col1.text_input("🔑 HEX SEED:", key="hex_avi")
    heur = col2.text_input("🕒 HEUR (HH:mm):", value=datetime.now().strftime("%H:%M"), key="time_avi")
    
    if st.button("🔥 ANALYZE AVIATOR"):
        res = get_prediction(hex_seed, heur, "AVIATOR")
        c = st.columns(3)
        for i, p in enumerate(res):
            with c[i]:
                st.markdown(f"<div class='prediction-card'><b>TOUR {i+1}</b><br>{p['time']}<br><span style='font-size:30px;'>{p['moyen']}x</span></div>", unsafe_allow_html=True)

# --- COSMOS X (Misy Segondra) ---
with tab2:
    st.subheader("🚀 COSMOS X ULTRA-SYNC")
    st.file_uploader("📸 UPLOAD SCREENSHOT", type=['png','jpg'], key="img_cos")
    col1, col2 = st.columns(2)
    hex_c = col1.text_input("🔑 HEX SEED:", key="hex_cos")
    # Ny lera eto dia mampiasa segondra
    heur_c = col2.text_input("🕒 HEUR (HH:mm:ss):", value=datetime.now().strftime("%H:%M:%S"), key="time_cos")
    
    if st.button("🚀 EXECUTE COSMOS"):
        res = get_prediction(hex_c, heur_c, "COSMOS X")
        c = st.columns(3)
        for i, p in enumerate(res):
            with c[i]:
                st.markdown(f"<div class='prediction-card'><b>TOUR {i+1}</b><br><span style='color:#ff4444;'>{p['time']}</span><br><span style='font-size:30px;'>{p['moyen']}x</span></div>", unsafe_allow_html=True)

# --- MINES VIP (Server & Client Seed) ---
with tab3:
    st.subheader("💣 MINES VIP 8/10")
    col1, col2 = st.columns(2)
    s_srv = col1.text_input("🔑 SEED DU SERVEUR:", key="mines_srv")
    s_clt = col2.text_input("📱 SEED DU CLIENT:", key="mines_clt")
    
    if st.button("🔍 SCAN MINES"):
        get_prediction(s_srv, s_clt, "MINES")
        st.markdown("<div style='text-align:center; font-size:25px;'>⭐ ⬛ ⬛ ⭐ ⬛<br>⬛ ⭐ ⬛ ⬛ ⬛<br>⬛ ⬛ ⭐ ⬛ ⭐</div>", unsafe_allow_html=True)

# --- 4. HISTORIQUE ---
st.markdown("---")
st.markdown("### 📜 LAST PREDICTIONS (CAPTURE)")
if st.session_state.history:
    for h in st.session_state.history[:6]:
        # Miseho eto ny pourcentage Min/Moyen/Max
        st.write(f"🎮 **{h['game']}** | 🕒 {h['time']} | **Min(85%): {h['min']}x** | **Moyen: {h['moyen']}x** | **Max(130%): {h['max']}x**")
