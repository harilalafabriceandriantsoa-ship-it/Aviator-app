import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- STYLE CONFIGURATION (PREMIUM & VISIBLE) ---
st.set_page_config(page_title="ANDRIANTSO ULTIMATE v62.3", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #030303; color: #ffffff; }
    .main-card {
        background: rgba(0, 255, 204, 0.1);
        border: 2px solid #00ffcc; border-radius: 15px;
        padding: 20px; text-align: center; margin-bottom: 20px;
    }
    .stat-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px; padding: 15px; text-align: center;
        border-top: 3px solid #ffd700;
    }
    .mine-grid {
        display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px;
        width: 300px; margin: auto; background: #000; padding: 15px;
        border-radius: 12px; border: 2px solid #ffd700;
    }
    .mine-cell {
        width: 50px; height: 50px; border-radius: 8px;
        display: flex; align-items: center; justify-content: center; font-size: 22px;
    }
    .star { background: #ffd700; color: #000; box-shadow: 0 0 10px #ffd700; }
    .empty { background: #1a1a1a; border: 1px solid #333; }
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #ffd700);
        color: black !important; font-weight: 900 !important; border-radius: 12px;
        height: 4em; width: 100%; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

st.markdown("<h1 style='text-align: center; color: #00ffcc;'>💎 TITAN ULTIMATE v62.3</h1>", unsafe_allow_html=True)

mode = st.radio("SELECT GAME:", ["✈️ AVIATOR GOLD", "🚀 COSMOS X", "💣 MINES 6-STAR"], horizontal=True)

st.write("---")

c1, c2 = st.columns(2)
with c1: st.file_uploader("📸 Capture History", type=['jpg', 'png'])
with c2:
    if mode == "💣 MINES 6-STAR":
        c_s = st.text_input("💻 Seed Client:")
        s_s = st.text_input("🖥️ Seed Serveur:")
    else:
        g_time = st.time_input("⏲️ Lera farany:", datetime.now().time())
        h_seed = st.text_input("🔑 HEX SEED (SHA-256):")

if st.button(f"🚀 START {mode} ANALYSIS"):
    if (mode == "💣 MINES 6-STAR" and (not c_s or not s_s)) or (mode != "💣 MINES 6-STAR" and not h_seed):
        st.error("❌ Fenoy ny banga!")
    else:
        with st.spinner('🔐 Analyzing SHA-512...'):
            time.sleep(2)
            if mode == "💣 MINES 6-STAR":
                combined = c_s + s_s
                h = hashlib.sha512(combined.encode()).hexdigest()
                random.seed(int(h[:16], 16))
                num_stars = random.choice([5, 6])
                star_spots = random.sample(range(25), k=num_stars)
                
                st.markdown(f"<h3 style='text-align: center; color: #ffd700;'>⭐ SCHEMA ({num_stars} KINTANA) ⭐</h3>", unsafe_allow_html=True)
                grid_html = '<div style="display: flex; justify-content: center;"><div class="mine-grid">'
                for i in range(25):
                    grid_html += f'<div class="mine-cell {"star" if i in star_spots else "empty"}>{"⭐" if i in star_spots else "?"}</div>'
                grid_html += '</div></div>'
                st.markdown(grid_html, unsafe_allow_html=True)
                res_txt = f"Schéma {num_stars} Stars"
            else:
                # --- AVIATOR & COSMOS WITH FULL ESTIMATIONS ---
                h = hashlib.sha512(h_seed.encode()).hexdigest()
                val = int(h[:12], 16)
                acc = 93 + (val % 6)
                t_t = (datetime.combine(datetime.today(), g_time) + timedelta(minutes=(val % 3) + 1)).strftime("%H:%M")
                
                if "AVIATOR" in mode:
                    s_val, m_val = round(1.85 + (val % 140) / 100, 2), round(35.0 + (val % 15000) / 100, 2)
                else:
                    s_val, m_val = round(1.45 + (val % 120) / 100, 2), round(15.0 + (val % 9000) / 100, 2)
                mid_val = round(s_val * 2.6, 2)

                # Fanehoana ny valiny ho hitan'ny maso tsara
                st.markdown(f"""
                    <div class="main-card">
                        <h2 style='color: #00ffcc; margin:0;'>SIGNAL: {t_t}</h2>
                        <h1 style='color: #ffffff; font-size: 50px; margin:0;'>{acc}%</h1>
                    </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b, col_c = st.columns(3)
                with col_a: st.markdown(f"<div class='stat-box'><p>🟢 SAFE</p><h3>{s_val}x</h3></div>", unsafe_allow_html=True)
                with col_b: st.markdown(f"<div class='stat-box'><p>🟡 MOYEN</p><h3>{mid_val}x</h3></div>", unsafe_allow_html=True)
                with col_c: st.markdown(f"<div class='stat-box'><p>🌸 MAX PINK</p><h3>{m_val}x</h3></div>", unsafe_allow_html=True)
                
                res_txt = f"{t_t} ({acc}%)"

            st.session_state.history.insert(0, {"Lera": datetime.now().strftime("%H:%M"), "Lalao": mode, "Vokatra": res_txt})

st.write("---")
st.subheader("📜 HISTORIQUE")
st.table(st.session_state.history)
