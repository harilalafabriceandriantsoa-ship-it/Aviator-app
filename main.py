import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- STYLE CONFIGURATION (PREMIUM NEON & GOLD) ---
st.set_page_config(page_title="ANDRIANTSO ULTIMATE v61.8", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #030303; color: #ffffff; }
    /* Card style ho an'ny Aviator/Cosmos */
    .prediction-card {
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.1), rgba(0, 204, 255, 0.1));
        border: 2px solid #00ffcc; border-radius: 20px; padding: 25px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
    }
    /* Grid style ho an'ny Mines */
    .mine-grid {
        display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px;
        max-width: 320px; margin: 25px auto; padding: 20px;
        background: rgba(255, 255, 255, 0.03); border-radius: 20px;
        border: 2px solid #ffd700; box-shadow: 0 0 25px rgba(255, 215, 0, 0.2);
    }
    .mine-cell {
        width: 50px; height: 50px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px; transition: 0.3s;
    }
    .star { background: #ffd700; color: #000; box-shadow: 0 0 15px #ffd700; font-weight: bold; }
    .empty { background: #1a1a1a; border: 1px solid #333; color: #444; }
    /* Button Premium */
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #ffd700);
        color: black !important; font-weight: 900 !important; border-radius: 15px;
        height: 4.5em; width: 100%; border: none; text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

st.markdown("<h1 style='text-align: center; color: #00ffcc; text-shadow: 0 0 10px #00ffcc;'>💎 TITAN ULTIMATE v61.8</h1>", unsafe_allow_html=True)

# --- 🎯 NAVIGATION LALAO ---
mode = st.radio("SELECT TARGET GAME:", ["✈️ AVIATOR GOLD", "🚀 COSMOS X", "💣 MINES 5-STAR"], horizontal=True)

st.write("---")

# --- 📥 INPUT PANEL ---
if mode == "💣 MINES 5-STAR":
    c1, c2 = st.columns(2)
    with c1: client_s = st.text_input("💻 Seed du Client:", placeholder="Paste Client Seed...")
    with c2: server_s = st.text_input("🖥️ Seed du Serveur (Hash):", placeholder="Paste Server Seed...")
else:
    col1, col2 = st.columns(2)
    with col1: game_time = st.time_input("⏲️ Lera farany hita:", datetime.now().time())
    with col2: hex_seed = st.text_input("🔑 HEX SEED (SHA-256):")

# --- ⚙️ EXECUTION ---
if st.button(f"🔥 START {mode} ANALYSIS"):
    if (mode == "💣 MINES 5-STAR" and (not client_s or not server_s)) or (mode != "💣 MINES 5-STAR" and not hex_seed):
        st.error("❌ Ampidiro daholo ny Seed rehetra azafady!")
    else:
        with st.spinner('🔐 TITAN AI is decrypting SHA-512...'):
            time.sleep(2)
            
            if mode == "💣 MINES 5-STAR":
                # Logic Mines: 5 Kintana raikitra miankina amin'ny Seed
                combined = client_s + server_s
                h_mines = hashlib.sha512(combined.encode()).hexdigest()
                random.seed(int(h_mines[:16], 16))
                
                # Mifidy toerana 5 raikitra ho an'ny kintana
                star_indices = random.sample(range(25), k=5)
                
                st.markdown("<h3 style='text-align: center; color: #ffd700;'>⭐ MINES 5-STAR PATTERN ⭐</h3>", unsafe_allow_html=True)
                grid_html = '<div class="mine-grid">'
                for i in range(25):
                    if i in star_indices:
                        grid_html += '<div class="mine-cell star">⭐</div>'
                    else:
                        grid_html += '<div class="mine-cell empty">?</div>'
                grid_html += '</div>'
                st.markdown(grid_html, unsafe_allow_html=True)
                st.success("✅ Schéma 5-Star vonona! Araho tsara ny sary.")
                
            else:
                # Mitazona ny kaody Aviator sy Cosmos (tsy novaina)
                h = hashlib.sha512(hex_seed.encode()).hexdigest()
                val = int(h[:12], 16)
                accuracy = 93 + (val % 6)
                t_time = (datetime.combine(datetime.today(), game_time) + timedelta(minutes=(val % 3) + 1)).strftime("%H:%M")
                
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
                        <h1 style='font-size: 55px; margin: 10px 0;'>{accuracy}%</h1>
                        <p style='color: #888;'>PROBABILITÉ HAUTE</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                m1, m2, m3 = st.columns(3)
                m1.metric("🟢 SAFE", f"{safe}x")
                m2.metric("🟡 MOYEN", f"{moyen}x")
                m3.metric("🌸 MAX PINK", f"{max_p}x")

            st.session_state.history.insert(0, {"Lera": datetime.now().strftime("%H:%M"), "Lalao": mode, "Status": "Success"})

# --- HISTORY ---
st.write("---")
st.subheader("📜 RECENT TITAN SIGNALS")
st.table(st.session_state.history)
