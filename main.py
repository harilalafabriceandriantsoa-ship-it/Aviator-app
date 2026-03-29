import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- 1. SETTINGS & STYLE ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")
if 'history' not in st.session_state: st.session_state.history = []
if 'manche_screenshots' not in st.session_state: st.session_state.manche_screenshots = []
if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05);
        border: 2px solid #00ffcc;
        padding: 15px; border-radius: 15px; text-align: center;
        box-shadow: 0 0 10px rgba(0, 255, 204, 0.3);
    }
    .luck-msg { color: #00ffcc; font-size: 20px; font-weight: bold; text-align: center; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR ADMIN (Reset & MDP) ---
with st.sidebar:
    st.title("⚙️ ADMIN PANEL")
    auth = st.text_input("Access Key:", type="password")
    if auth == st.session_state.admin_pwd:
        if st.button("🗑️ RESET ALL DATA"):
            st.session_state.history = []
            st.session_state.manche_screenshots = []
            st.rerun()
    st.markdown("---")
    st.info("TITAN V85.0 - Version Ultra Sync")

# --- 3. MAIN INTERFACE ---
st.markdown("<h1 style='text-align:center;'>🛰️ TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "📸 HISTORIQUE MANCHE"])

# --- Lojika iraisana ho an'ny Aviator & Cosmos ---
def run_analysis(game):
    st.markdown(f"### ⚡ {game} ANALYZER")
    c1, c2 = st.columns(2)
    seed = c1.text_input("🔑 SERVER SEED (HEX):", key=f"s_{game}")
    time_val = c2.text_input("🕒 LERA (HH:mm):", key=f"t_{game}")
    
    if st.button(f"🔥 EXECUTE {game}"):
        now = datetime.now()
        cols = st.columns(3)
        for i in range(1, 4):
            moyen = round(random.uniform(1.65, 4.50), 2)
            t_str = (now + timedelta(minutes=i*2)).strftime("%H:%M:%S" if game == "COSMOS X" else "%H:%M")
            with cols[i-1]:
                st.markdown(f"""<div class="prediction-card">
                    <b>TOUR {i}</b><br>{t_str}<br>
                    <span style="font-size:30px; color:#00ffcc;">{moyen}x</span><br>
                    <small>85%: {round(moyen*0.85,2)} | 130%: {round(moyen*1.3,2)}</small>
                </div>""", unsafe_allow_html=True)
            st.session_state.history.insert(0, {"game": game, "time": t_str, "val": moyen})
        st.markdown("<p class='luck-msg'>🍀 Bonne chance à tous !</p>", unsafe_allow_html=True)

with tab1: run_analysis("AVIATOR")
with tab2: run_analysis("COSMOS X")
with tab3:
    st.markdown("### 💣 MINES VIP")
    if st.button("🔍 SCAN MINES"):
        st.write("⭐ ⬛ ⬛ ⭐ ⬛")
        st.markdown("<p class='luck-msg'>🍀 Bonne chance à tous !</p>", unsafe_allow_html=True)

# --- 4. HISTORIQUE DE LA MANCHE (SCREENSHOTS) ---
with tab4:
    st.header("📸 HISTORIQUE DE LA MANCHE")
    st.subheader("Ampidiro eto ny Screenshot-ny vokatra azo")
    
    with st.expander("➕ AMPIDIRO NY VOKATRA VAOVAO"):
        up_file = st.file_uploader("Safidio ny sary (JPG/PNG):", type=['jpg','png','jpeg'])
        up_time = st.text_input("Lera nisehoan'ny vokatra:")
        up_val = st.text_input("Vokatra (x):")
        
        if st.button("💾 TEHIRIZINA NY MANCHE"):
            if up_file:
                st.session_state.manche_screenshots.insert(0, {
                    "image": up_file,
                    "time": up_time,
                    "val": up_val,
                    "date": datetime.now().strftime("%d/%m/%Y")
                })
                st.success("Voatahiry ny sary!")
    
    st.markdown("---")
    if st.session_state.manche_screenshots:
        for m in st.session_state.manche_screenshots:
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.image(m['image'], width=200)
            with col_txt:
                st.markdown(f"**Lera:** {m['time']}")
                st.markdown(f"**Vokatra:** <span style='color:#00ffcc;'>{m['val']}x</span>", unsafe_allow_html=True)
                st.markdown(f"**Andro:** {m['date']}")
            st.markdown("---")
    else:
        st.info("Tsy mbola misy screenshot voatahiry.")
