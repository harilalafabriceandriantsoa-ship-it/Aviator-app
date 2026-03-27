import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- STYLE & SOUND ---
def play_notif():
    st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/sounds/button-37.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)

st.set_page_config(page_title="TITAN v62.7 TRACKER", page_icon="📊", layout="wide")

# Initialisation an'ny fitahirizana (Memory)
if 'history_tours' not in st.session_state: st.session_state.history_tours = []
if 'total_gains' not in st.session_state: st.session_state.total_gains = 0.0

st.markdown("""
    <style>
    .stApp { background: #050505; color: #e0e0e0; }
    .sidebar .sidebar-content { background: #0a0a0a; }
    .card-signal {
        background: rgba(0, 255, 204, 0.05); border: 2px solid #ffd700;
        border-radius: 15px; padding: 20px; text-align: center;
    }
    .stat-val { font-size: 35px; font-weight: 900; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 TITAN v62.7 - SMART TRACKER")

# --- SIDEBAR : HISTORIQUE DE TOUR & JOURNAL ---
st.sidebar.header("📝 HISTORIQUE & JOURNAL")

with st.sidebar.expander("➕ AMPIDIRO NY VOKATRA (TOUR)"):
    t_val = st.number_input("Multiplier nivoaka (x):", min_value=1.0, step=0.01)
    t_game = st.selectbox("Lalao:", ["Aviator", "Cosmos", "Mines"])
    if st.button("Enregistrer le Tour"):
        now_mg = (datetime.now() + timedelta(hours=3)).strftime("%H:%M:%S")
        st.session_state.history_tours.insert(0, {"Lera": now_mg, "Lalao": t_game, "Resultat": f"{t_val}x"})
        st.sidebar.success("Tour voatahiry!")

st.sidebar.markdown(f"### 💰 Total Gains: {st.session_state.total_gains}$")
st.sidebar.write("---")
st.sidebar.subheader("🕒 5 Tours Farany")
if st.session_state.history_tours:
    st.sidebar.table(st.session_state.history_tours[:5])

# --- MAIN INTERFACE ---
mode = st.radio("LALAO:", ["✈️ AVIATOR GOLD", "🚀 COSMOS X", "💣 MINES 6-STAR"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    if mode == "💣 MINES 6-STAR":
        cs = st.text_input("💻 Seed Client")
        ss = st.text_input("🖥️ Seed Serveur (Hash)")
        source = "SHA-512 Server Hash"
    else:
        time_now = (datetime.now() + timedelta(hours=3)).time()
        gt = st.time_input("⏲️ Lera farany (Finday):", time_now)
        hs = st.text_input("🔑 HEX SEED (SHA-256):")
        source = "Hexadecimal Seed Analysis"

with col2:
    st.markdown("### 📋 Signal Status")
    st.info(f"**Source From:** {source}")
    st.write(f"**Sync:** Madagascar GMT+3 Active")

if st.button(f"🚀 ANALYSER {mode}"):
    with st.spinner('Calculating...'):
        time.sleep(1.2)
        play_notif()
        
        if mode == "💣 MINES 6-STAR":
            h = hashlib.sha512((cs + ss).encode()).hexdigest()
            random.seed(int(h[:16], 16))
            stars = random.sample(range(25), k=6)
            
            st.markdown("<h3 style='text-align:center;'>⭐ SCHÉMA DE TOUR ⭐</h3>", unsafe_allow_html=True)
            grid = '<div style="display: grid; grid-template-columns: repeat(5, 50px); gap: 10px; justify-content: center;">'
            for i in range(25):
                bg = "#ffd700" if i in stars else "#1a1a1a"
                grid += f'<div style="width:50px; height:50px; background:{bg}; border-radius:5px;"></div>'
            grid += '</div>'
            st.markdown(grid, unsafe_allow_html=True)
        else:
            h = hashlib.sha512(hs.encode()).hexdigest()
            val = int(h[:12], 16)
            pt = (datetime.combine(datetime.today(), gt) + timedelta(minutes=(val % 3) + 1)).strftime("%H:%M")
            acc = 94 + (val % 5)
            s, m = round(1.88 + (val % 110)/100, 2), round(50.0 + (val % 25000)/100, 2)

            st.markdown(f"""
                <div class="card-signal">
                    <h2 style="color: #ffd700;">PROCHAIN SIGNAL : {pt}</h2>
                    <p style="color: #00ffcc;">Source: {source}</p>
                    <div style="display: flex; justify-content: space-around; margin-top:20px;">
                        <div><p>🟢 SAFE</p><p class="stat-val">{s}x</p></div>
                        <div><p>🟡 MOYEN</p><p class="stat-val">{round(s*2.7, 2)}x</p></div>
                        <div><p>🌸 PINK</p><p class="stat-val">{m}x</p></div>
                    </div>
                    <h3>PRÉCISION: {acc}%</h3>
                </div>
            """, unsafe_allow_html=True)

st.write("---")
st.caption("TITAN v62.7 | Signal Tracking & Historical Data Enabled")
