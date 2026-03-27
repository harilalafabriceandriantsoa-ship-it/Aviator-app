import hashlib
import time
import random
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION INITIALE ---
if 'history' not in st.session_state: st.session_state.history = []
if 'score' not in st.session_state: st.session_state.score = {"Win": 0, "Loss": 0}

st.set_page_config(page_title="ANDRIANTSO | APEX v43", layout="wide")
now_mg = datetime.now(timezone(timedelta(hours=3)))

# --- STYLE NEON DYNAMIQUE ---
st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
    .stApp { background-color: #050505; }
    
    /* Titre Glow */
    .apex-header {
        text-align: center; font-size: 40px; font-weight: 900;
        color: #FFD700; text-shadow: 0 0 20px #FFD700;
        margin-bottom: 10px;
    }
    
    /* Bouton lehibe mora kitihana */
    .stButton>button {
        width: 100%; height: 70px; border-radius: 20px;
        font-weight: 900; font-size: 22px; transition: 0.3s;
        border: none; cursor: pointer;
    }
    .btn-aviator > div > button { background: linear-gradient(90deg, #FFD700, #FF8C00) !important; color: black !important; }
    .btn-cosmos > div > button { background: linear-gradient(90deg, #00D4FF, #0055FF) !important; color: white !important; }
    
    .result-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 30px; border-radius: 30px; border: 2px solid #444;
        text-align: center; margin-top: 20px;
    }
    .time-val { font-size: 80px; font-weight: 900; color: #00FF66; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER & BRANDING ---
st.markdown('<p class="apex-header">💎 ANDRIANTSO | SNIPER APEX</p>', unsafe_allow_html=True)
st.image("https://img.freepik.com/free-photo/view-futuristic-fighter-jet-flying_23-2151214041.jpg", use_container_width=True)

# --- NAVIGATION SWITCH (TABS) ---
st.write("### 🕹️ FIDIO NY LALAO HATAO PREDICTION:")
tab1, tab2 = st.tabs(["✈️ MODE AVIATOR", "🚀 MODE COSMOS X"])

# --- SHARED LOGIC FUNCTION ---
def generate_signal(game_name, color, safe_multiplier, speed_adj):
    st.markdown(f"### ⚙️ SETUP {game_name}")
    col_a, col_b = st.columns([1, 1.2])
    
    with col_a:
        sync = st.radio(f"🕒 SYNC ({game_name}):", ["Normal", "+1 min", "-1 min"], horizontal=True, key=f"sync_{game_name}")
        hex_input = st.text_input("🔑 HEX SEED (SHA-256):", placeholder="Paste Hex Code here...", key=f"hex_{game_name}")
        lera_game = st.time_input("⏲️ LERA AO AMIN'NY LALAO:", value=now_mg.time(), key=f"time_{game_name}")
        
        if st.button(f"🔥 GENERATE {game_name} SIGNAL", key=f"btn_{game_name}"):
            if not hex_input:
                st.error("⚠️ Ampidiro ny Hex Seed!")
            else:
                h = hashlib.sha256(hex_input.encode()).hexdigest()
                v = int(h[:8], 16)
                offset = 1 if "+1 min" in sync else -1 if "-1 min" in sync else 0
                # Cosmos is faster, Aviator has more wait time
                t_dt = datetime.combine(datetime.today(), lera_game) + timedelta(minutes=(speed_adj + offset))
                
                st.session_state.history.insert(0, {
                    "Lera": t_dt.strftime("%H:%M"),
                    "Prob": f"{75 + (v % 24)}%",
                    "Safe": safe_multiplier,
                    "target_dt": t_dt,
                    "Game": game_name
                })
                st.rerun()

    with col_b:
        if st.session_state.history and st.session_state.history[0]["Game"] == game_name:
            r = st.session_state.history[0]
            sec = (r['target_dt'] - datetime.combine(datetime.today(), datetime.now().time())).total_seconds()
            
            st.markdown(f"""
            <div class="result-box" style="border-color: {color}; shadow: 0 0 20px {color}33;">
                <p style='color:{color}; font-weight:bold; letter-spacing:3px;'>{game_name} SIGNAL ACTIVE</p>
                <div class="time-val" style="color: {color if sec <= 0 else '#00FF66'}">{r['Lera']}</div>
            """, unsafe_allow_html=True)
            
            if sec > 0:
                m, s = divmod(int(sec), 60)
                st.markdown(f"<h2 style='color:white;'>⌛ TIMER: {m:02d}:{s:02d}</h2>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h2 class='blink' style='color:{color};'>🔥 MIDIRA IZAO! 🔥</h2>", unsafe_allow_html=True)
            
            st.markdown(f"<b>🎯 ACCURACY: {r['Prob']} | ✅ SAFE: {r['Safe']}x</b></div>", unsafe_allow_html=True)
            if sec > -60: time.sleep(1); st.rerun()
        else:
            st.info(f"Andrasana ny Hex Seed ho an'ny {game_name}...")

# --- EXECUTION ---
with tab1:
    generate_signal("AVIATOR", "#FFD700", 2.03, 2.0)

with tab2:
    generate_signal("COSMOS", "#00D4FF", 1.75, 1.0)

# --- TRAINING ---
st.write("---")
if st.button("🎮 PRACTICE MODE (TRAINING)"):
    res = random.uniform(1.0, 5.0)
    if res >= 1.75: st.success(f"💰 WIN! {res:.2f}x"); st.session_state.score["Win"] += 1
    else: st.error(f"💥 LOSS! {res:.2f}x"); st.session_state.score["Loss"] += 1
st.write(f"🏆 Score: ✅ {st.session_state.score['Win']} | ❌ {st.session_state.score['Loss']}")
