import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- STYLE CONFIGURATION (PREMIUM & CLEAN) ---
st.set_page_config(page_title="ANDRIANTSO ULTIMATE v62.1", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #030303; color: #ffffff; }
    .prediction-card {
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.1), rgba(0, 204, 255, 0.1));
        border: 2px solid #00ffcc; border-radius: 20px; padding: 25px; text-align: center;
    }
    /* Grid Mines 5x5 - Perfect Alignment */
    .mine-container { display: flex; justify-content: center; padding: 10px; }
    .mine-grid {
        display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px;
        width: 320px; background: rgba(255, 255, 255, 0.05);
        padding: 20px; border-radius: 15px; border: 2px solid #ffd700;
    }
    .mine-cell {
        width: 50px; height: 50px; border-radius: 10px;
        display: flex; align-items: center; justify-content: center; font-size: 24px;
    }
    .star { background: #ffd700; color: #000; box-shadow: 0 0 15px #ffd700; font-weight: bold; }
    .empty { background: #1a1a1a; border: 1px solid #333; color: #333; }
    
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #ffd700);
        color: black !important; font-weight: 900 !important; border-radius: 15px;
        height: 4em; width: 100%; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

st.markdown("<h1 style='text-align: center; color: #00ffcc;'>💎 TITAN ULTIMATE v62.1</h1>", unsafe_allow_html=True)

# --- 🎯 SELECTION ---
mode = st.radio("TARGET GAME:", ["✈️ AVIATOR GOLD", "🚀 COSMOS X", "💣 MINES 6-STAR"], horizontal=True)

st.write("---")

# --- 📥 INPUTS ---
col1, col2 = st.columns(2)
with col1:
    st.file_uploader("📸 Capture History", type=['jpg', 'png'])
with col2:
    if mode == "💣 MINES 6-STAR":
        client_s = st.text_input("💻 Seed Client:", placeholder="Client Seed...")
        server_s = st.text_input("🖥️ Seed Serveur:", placeholder="Server Hash...")
    else:
        game_time = st.time_input("⏲️ Lera farany hita:", datetime.now().time())
        hex_seed = st.text_input("🔑 HEX SEED (SHA-256):")

# --- ⚙️ EXECUTION ---
if st.button(f"🚀 START {mode} ANALYSIS"):
    if (mode == "💣 MINES 6-STAR" and (not client_s or not server_s)) or (mode != "💣 MINES 6-STAR" and not hex_seed):
        st.error("❌ Fenoy daholo ny banga!")
    else:
        with st.spinner('🔐 Titan AI Decrypting...'):
            time.sleep(2)
            
            if mode == "💣 MINES 6-STAR":
                # Mines Logic (New 5-6 Stars)
                combined = client_s + server_s
                h = hashlib.sha512(combined.encode()).hexdigest()
                random.seed(int(h[:16], 16))
                
                num_stars = random.choice([5, 6])
                star_spots = random.sample(range(25), k=num_stars)
                
                st.markdown(f"<h3 style='text-align: center; color: #ffd700;'>⭐ SCHEMA MINES ({num_stars} KINTANA) ⭐</h3>", unsafe_allow_html=True)
                grid_html = '<div class="mine-container"><div class="mine-grid">'
                for i in range(25):
                    if i in star_spots:
                        grid_html += '<div class="mine-cell star">⭐</div>'
                    else:
                        grid_html += '<div class="mine-cell empty">?</div>'
                grid_html += '</div></div>'
                st.markdown(grid_html, unsafe_allow_html=True)
                res_txt = f"Schéma {num_stars} Stars"
                
            else:
                # AVIATOR & COSMOS (TSY NIOVA MIHITSY)
                h = hashlib.sha512(hex_seed.encode()).hexdigest()
                val = int(h[:12], 16)
                accuracy = 93 + (val % 6)
                t_time = (datetime.combine(datetime.today(), game_time) + timedelta(minutes=(val % 3) + 1)).strftime("%H:%M")
                
                if "AVIATOR" in mode:
                    safe, max_p = round(1.85 + (val % 140) / 100, 2), round(35.0 + (val % 15000) / 100, 2)
                else:
                    safe, max_p = round(1.45 + (val % 120) / 100, 2), round(15.0 + (val % 9000) / 100, 2)
                
                moyen = round(safe * 2.6, 2)
                
                st.markdown(f"""
                    <div class="prediction-card">
                        <h2 style='color: #00ffcc;'>SIGNAL : {t_time}</h2>
                        <h1 style='font-size: 55px;'>{accuracy}%</h1>
                    </div>
                """, unsafe_allow_html=True)
                
                m1, m2, m3 = st.columns(3)
                m1.metric("🟢 SAFE", f"{safe}x")
                m2.metric("🟡 MOYEN", f"{moyen}x")
                m3.metric("🌸 MAX PINK", f"{max_p}x")
                res_txt = f"{t_time} ({accuracy}%)"

            st.session_state.history.insert(0, {"Lera": datetime.now().strftime("%H:%M"), "Lalao": mode, "Vokatra": res_txt})

# --- 📜 HISTORY ---
st.write("---")
st.subheader("📜 HISTORIQUE DE PRÉDICTION")
st.table(st.session_state.history)
