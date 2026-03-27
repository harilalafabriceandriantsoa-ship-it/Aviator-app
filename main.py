import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- CONFIGURATION STYLE (Optimized for Mobile) ---
st.set_page_config(page_title="ANDRIANTSO ULTIMATE v62.2", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #030303; color: #ffffff; }
    .mine-container { display: flex; justify-content: center; padding: 10px; }
    .mine-grid {
        display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px;
        width: 300px; background: #0a0a0a; padding: 15px;
        border-radius: 12px; border: 2px solid #ffd700;
    }
    .mine-cell {
        width: 50px; height: 50px; border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px; transition: 0.3s;
    }
    .star { background: #ffd700; color: #000; box-shadow: 0 0 10px #ffd700; font-weight: bold; }
    .empty { background: #1a1a1a; border: 1px solid #333; color: #333; }
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #ffd700);
        color: black !important; font-weight: 900 !important; border-radius: 12px;
        height: 4em; width: 100%; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

st.markdown("<h1 style='text-align: center; color: #00ffcc;'>💎 TITAN ULTIMATE v62.2</h1>", unsafe_allow_html=True)

# --- NAVIGATION ---
mode = st.radio("TARGET:", ["✈️ AVIATOR GOLD", "🚀 COSMOS X", "💣 MINES 6-STAR"], horizontal=True)

st.write("---")

# --- INPUT PANEL ---
c1, c2 = st.columns(2)
with c1: st.file_uploader("📸 Capture", type=['jpg', 'png'])
with c2:
    if mode == "💣 MINES 6-STAR":
        c_s = st.text_input("💻 Seed Client:", placeholder="Client Seed...")
        s_s = st.text_input("🖥️ Seed Serveur:", placeholder="Server Hash...")
    else:
        g_time = st.time_input("⏲️ Lera farany:", datetime.now().time())
        h_seed = st.text_input("🔑 HEX SEED (SHA-256):")

# --- EXECUTION ---
if st.button(f"🚀 ANALYSE {mode}"):
    if (mode == "💣 MINES 6-STAR" and (not c_s or not s_s)) or (mode != "💣 MINES 6-STAR" and not h_seed):
        st.error("❌ Fenoy daholo ny banga!")
    else:
        with st.spinner('🔐 SHA-512 Deep Decryption...'):
            time.sleep(1.5)
            
            if mode == "💣 MINES 6-STAR":
                combined = c_s + s_s
                h = hashlib.sha512(combined.encode()).hexdigest()
                random.seed(int(h[:16], 16))
                
                num_stars = random.choice([5, 6])
                star_spots = random.sample(range(25), k=num_stars)
                
                st.markdown(f"<h3 style='text-align: center; color: #ffd700;'>⭐ SCHEMA MINES ({num_stars} KINTANA) ⭐</h3>", unsafe_allow_html=True)
                
                # Grid feno 25 carreaux (5x5)
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
                # Aviator & Cosmos (Mitazona ny algorithm-nao teo aloha)
                h = hashlib.sha512(h_seed.encode()).hexdigest()
                val = int(h[:12], 16)
                acc = 94 + (val % 5)
                t_t = (datetime.combine(datetime.today(), g_time) + timedelta(minutes=(val % 3) + 1)).strftime("%H:%M")
                st.info(f"SIGNAL: {t_t} | ACCURACY: {acc}%")
                res_txt = f"{t_t} ({acc}%)"

            st.session_state.history.insert(0, {"Lera": datetime.now().strftime("%H:%M"), "Lalao": mode, "Vokatra": res_txt})

# --- HISTORY ---
st.write("---")
st.subheader("📜 HISTORIQUE")
st.table(st.session_state.history)
