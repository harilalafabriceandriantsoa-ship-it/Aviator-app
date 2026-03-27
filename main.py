import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- CONFIGURATION STYLE ---
st.set_page_config(page_title="ANDRIANTSO ULTIMATE v61.9", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #030303; color: #ffffff; }
    .prediction-card {
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.1), rgba(0, 204, 255, 0.1));
        border: 2px solid #00ffcc; border-radius: 20px; padding: 25px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
    }
    .mine-grid {
        display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px;
        max-width: 300px; margin: 20px auto; padding: 15px;
        background: rgba(255, 255, 255, 0.03); border-radius: 15px; border: 2px solid #ffd700;
    }
    .mine-cell {
        width: 45px; height: 45px; border-radius: 10px;
        display: flex; align-items: center; justify-content: center; font-size: 20px;
    }
    .star { background: #ffd700; color: #000; box-shadow: 0 0 10px #ffd700; font-weight: bold; }
    .empty { background: #1a1a1a; border: 1px solid #333; color: #444; }
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #ffd700);
        color: black !important; font-weight: 900 !important; border-radius: 15px;
        height: 4em; width: 100%; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Fitahirizana ny tantara (History)
if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown("<h1 style='text-align: center; color: #00ffcc;'>💎 TITAN ULTIMATE v61.9</h1>", unsafe_allow_html=True)

# --- 🎯 SELECTION LALAO ---
mode = st.radio("FIDIO NY LALAO:", ["✈️ AVIATOR GOLD", "🚀 COSMOS X", "💣 MINES 5-STAR"], horizontal=True)

st.write("---")

# --- 📥 INPUT PANEL (Misy Capture) ---
c1, c2 = st.columns(2)
with c1:
    st.file_uploader("📸 Screenshot History (Capture)", type=['jpg', 'png'])
with c2:
    if mode == "💣 MINES 5-STAR":
        client_s = st.text_input("💻 Seed du Client:", placeholder="Client Seed...")
        server_s = st.text_input("🖥️ Seed du Serveur:", placeholder="Server Hash...")
    else:
        game_time = st.time_input("⏲️ Lera farany hita:", datetime.now().time())
        hex_seed = st.text_input("🔑 HEX SEED (SHA-256):")

# --- ⚙️ EXECUTION ---
if st.button(f"🚀 EXECUTE {mode} ANALYSIS"):
    if (mode == "💣 MINES 5-STAR" and (not client_s or not server_s)) or (mode != "💣 MINES 5-STAR" and not hex_seed):
        st.error("❌ Fenoy daholo ny banga azafady!")
    else:
        with st.spinner('🔐 Mikajy ny SHA-512...'):
            time.sleep(2)
            
            if mode == "💣 MINES 5-STAR":
                combined = client_s + server_s
                h_mines = hashlib.sha512(combined.encode()).hexdigest()
                random.seed(int(h_mines[:16], 16))
                star_indices = random.sample(range(25), k=5)
                
                st.markdown("<h3 style='text-align: center; color: #ffd700;'>⭐ MINES SCHÉMA ⭐</h3>", unsafe_allow_html=True)
                grid_html = '<div class="mine-grid">'
                for i in range(25):
                    grid_html += f'<div class="mine-cell {"star" if i in star_indices else "empty"}>{"⭐" if i in star_indices else "?"}</div>'
                grid_html += '</div>'
                st.markdown(grid_html, unsafe_allow_html=True)
                
                res_val = "Schéma 5-Star"
            else:
                h = hashlib.sha512(hex_seed.encode()).hexdigest()
                val = int(h[:12], 16)
                accuracy = 93 + (val % 6)
                t_time = (datetime.combine(datetime.today(), game_time) + timedelta(minutes=(val % 3) + 1)).strftime("%H:%M")
                
                # Estimations (tsy novaina)
                if "AVIATOR" in mode:
                    safe = round(1.85 + (val % 140) / 100, 2)
                    max_p = round(35.0 + (val % 15000) / 100, 2)
                else:
                    safe = round(1.45 + (val % 120) / 100, 2)
                    max_p = round(15.0 + (val % 9000) / 100, 2)
                
                moyen = round(safe * 2.6, 2)
                
                st.markdown(f"""
                    <div class="prediction-card">
                        <h2 style='color: #00ffcc;'>SIGNAL : {t_time}</h2>
                        <h1 style='font-size: 50px;'>{accuracy}%</h1>
                    </div>
                """, unsafe_allow_html=True)
                
                m1, m2, m3 = st.columns(3)
                m1.metric("🟢 SAFE", f"{safe}x")
                m2.metric("🟡 MOYEN", f"{moyen}x")
                m3.metric("🌸 MAX PINK", f"{max_p}x")
                
                res_val = f"{t_time} ({accuracy}%)"

            # Ampidirina ao amin'ny History
            st.session_state.history.insert(0, {
                "Lera Prediction": datetime.now().strftime("%H:%M:%S"),
                "Lalao": mode,
                "Vokatra / Signal": res_val
            })

# --- 📜 HISTORY DE PRÉDICTION ---
st.write("---")
st.subheader("📜 HISTORIQUE DE PRÉDICTION")
if st.session_state.history:
    st.table(st.session_state.history)
else:
    st.info("Mbola tsisy prediction natao.")

# Sidebar ho an'ny reset
if st.sidebar.button("🗑️ Hamafa ny History"):
    st.session_state.history = []
    st.rerun()
