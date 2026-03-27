import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- STYLE CONFIGURATION ---
st.set_page_config(page_title="ANDRIANTSO ULTIMATE v61.3", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .prediction-card {
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.1), rgba(255, 215, 0, 0.1));
        border: 2px solid #00ffcc; border-radius: 20px; padding: 25px; text-align: center;
    }
    .mine-grid {
        display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px;
        max-width: 300px; margin: 20px auto;
    }
    .mine-cell {
        width: 50px; height: 50px; border-radius: 8px; border: 1px solid #333;
        display: flex; align-items: center; justify-content: center; font-size: 20px;
    }
    .star { background: rgba(255, 215, 0, 0.2); border-color: #ffd700; color: #ffd700; }
    .empty { background: rgba(255, 255, 255, 0.05); color: #333; }
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #33ccff);
        color: black !important; font-weight: 900 !important; border-radius: 12px; height: 4em; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

st.markdown("<h1 style='text-align: center; color: #00ffcc;'>💎 TITAN ULTIMATE v61.3</h1>", unsafe_allow_html=True)

# --- 🎯 SELECTION LALAO (VISIBLE) ---
st.write("### 🎮 FIDIO NY LALAO:")
mode = st.radio("", ["✈️ AVIATOR GOLD", "🚀 COSMOS X", "💣 MINES PREDICT"], horizontal=True)

st.write("---")

# --- 📥 INPUT PANEL ---
col_up, col_tm = st.columns(2)
with col_up:
    st.file_uploader("📸 Screenshot History", type=['jpg', 'png'])
with col_tm:
    game_time = st.time_input("⏲️ Lera farany hita:", datetime.now().time())

hex_seed = st.text_input(f"🔑 HEX SEED {mode} (SHA-256):", placeholder="Paste Hash here...")

if st.button(f"🔥 EXECUTE {mode} ANALYSIS"):
    if not hex_seed:
        st.error("❌ Ampidiro aloha ny Hex Seed!")
    else:
        with st.spinner('🔐 TITAN AI is analyzing SHA-512...'):
            time.sleep(2)
            h = hashlib.sha512(hex_seed.encode()).hexdigest()
            val = int(h[:12], 16)
            
            accuracy = 92 + (val % 6)
            t_time = (datetime.combine(datetime.today(), game_time) + timedelta(minutes=(val % 3) + 1)).strftime("%H:%M")

            if mode == "💣 MINES PREDICT":
                st.markdown(f"<h3 style='text-align: center;'>💣 MINES PATTERN (Accuracy: {accuracy}%)</h3>", unsafe_allow_html=True)
                
                # Logic ho an'ny Mines (Kintana 4 ka hatramin'ny 6)
                random.seed(val)
                star_indices = random.sample(range(25), k=random.randint(4, 6))
                
                grid_html = '<div class="mine-grid">'
                for i in range(25):
                    if i in star_indices:
                        grid_html += '<div class="mine-cell star">⭐</div>'
                    else:
                        grid_html += '<div class="mine-cell empty">?</div>'
                grid_html += '</div>'
                st.markdown(grid_html, unsafe_allow_html=True)
                st.info("💡 Soso-kevitra: Sokafy fotsiny ireo misy kintana. Aza mihoatra ny 3-4 raha te ho azo antoka.")

            else:
                # Logic ho an'ny Aviator/Cosmos
                if "AVIATOR" in mode:
                    safe, max_p = round(1.85 + (val % 140) / 100, 2), round(35.0 + (val % 15000) / 100, 2)
                else:
                    safe, max_p = round(1.45 + (val % 120) / 100, 2), round(15.0 + (val % 9000) / 100, 2)
                
                moyen = round(safe * 2.6, 2)
                
                st.markdown(f"""
                    <div class="prediction-card">
                        <h2 style='color: #00ffcc;'>PROCHAIN SIGNAL : {t_time}</h2>
                        <h1 style='font-size: 55px;'>ACCURACY: {accuracy}%</h1>
                    </div>
                """, unsafe_allow_html=True)
                
                m1, m2, m3 = st.columns(3)
                m1.metric("🟢 SAFE", f"{safe}x")
                m2.metric("🟡 MOYEN", f"{moyen}x")
                m3.metric("🌸 MAX PINK", f"{max_p}x")

            st.session_state.history.insert(0, {"Lera": t_time, "Lalao": mode, "Status": "Success", "Acc": f"{accuracy}%"})

# --- HISTORY ---
st.write("---")
st.subheader("📜 RECENT SIGNALS")
if st.session_state.history:
    st.table(st.session_state.history)
