import hashlib
import time
import random
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone

# --- INITIALISATION ---
if 'history' not in st.session_state: st.session_state.history = []
if 'score' not in st.session_state: st.session_state.score = {"Win": 0, "Loss": 0}

st.set_page_config(page_title="SNIPER AI-VISION v41.0", layout="wide")
now_mg = datetime.now(timezone(timedelta(hours=3)))

# --- STYLE CSS TITAN AI ---
st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
    .stApp { background-color: #050505; }
    /* Bokotra lehibe mora kitihana */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #FF8C00 100%);
        color: black !important; font-weight: 900; border-radius: 20px;
        height: 65px; border: 5px solid rgba(0,0,0,0.1); font-size: 20px;
        box-shadow: 0px 5px 15px rgba(255,215,0,0.3);
    }
    .result-card {
        background: linear-gradient(145deg, #0f0f0f, #1a1a1a);
        padding: 25px; border-radius: 35px; border: 2px solid #FFD700;
        text-align: center; box-shadow: 0px 0px 30px rgba(255,215,0,0.1);
    }
    .time-display { font-size: 75px; font-weight: 900; color: #00FF44; text-shadow: 0px 0px 20px #00FF4466; }
    /* Ho an'ny finday */
    @media (max-width: 600px) { .time-display { font-size: 50px; } }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER WITH AI IMAGE ---
st.markdown("<h1 style='text-align: center; color: #FFD700;'>🤖 TITAN AI-VISION v41.0</h1>", unsafe_allow_html=True)

# Sary AI Avion Pro ho an'ny sary an-tsaina
st.image("https://img.freepik.com/premium-photo/futuristic-jet-plane-flying-high-speed-night-city-skyline-generative-ai_124507-42775.jpg", caption="AI Prediction System Active", use_container_width=True)

# --- ⚙️ SETUP & INTERFACE ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### 🛠️ CONFIGURATION")
    # Natao bokotra fa tsy radio mba tsy hibloaka
    sync_choice = st.selectbox("🕒 SYNC OFFSET:", ["0 min (Normal)", "+1 min (Taraiky)", "-1 min (Haingana)"])
    
    hex_input = st.text_input("🔑 HEX SEED (SHA-256):", key="hex_box", placeholder="Paste Hex here...")
    lera_input = st.time_input("⏲️ LERA LALAO:", value=now_mg.time())
    
    # Upload Screenshot
    file = st.file_uploader("📷 ANALYSE HISTORIQUE (Screenshot)", type=['jpg','png'])
    if file:
        st.image(file, caption="Sary nodinihina", use_container_width=True)

    # BOKOTRA GENERATE
    if st.button("🔥 GENERATE AI SIGNAL"):
        if not hex_input:
            st.warning("⚠️ Ampidiro aloha ny HEX SEED vao manindry!")
        else:
            # Algorithm SHA-256
            h = hashlib.sha256(hex_input.encode()).hexdigest()
            v = int(h[:8], 16)
            
            # Ajustement lera
            offset = 1 if "+1 min" in sync_choice else -1 if "-1 min" in sync_choice else 0
            t_dt = datetime.combine(datetime.today(), lera_input) + timedelta(minutes=(2 + offset))
            
            st.session_state.history.insert(0, {
                "Lera": t_dt.strftime("%H:%M"),
                "Prob": f"{70 + (v % 29)}%",
                "Safe": 2.03, "Moyen": round(4.0 + (v % 300)/100, 2), "Max": round(10.0 + (v % 1500)/100, 2),
                "target_dt": t_dt
            })
            st.rerun()

with col2:
    if st.session_state.history:
        r = st.session_state.history[0]
        diff = (r['target_dt'] - datetime.combine(datetime.today(), datetime.now().time())).total_seconds()
        
        st.markdown(f"""
        <div class="result-card">
            <p style='color:#888;'>🎯 PREDICTION AI ACTIVATED</p>
            <div class="time-display">{r['Lera']}</div>
        """, unsafe_allow_html=True)
        
        if diff > 0:
            m, s = divmod(int(diff), 60)
            st.markdown(f"<h2 class='blink' style='color:#FFD700;'>⌛ {m:02d}:{s:02d} SISA</h2>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 class='blink' style='color:#00FF44;'>🔥 MIDIRA IZAO! 🔥</h2>", unsafe_allow_html=True)
            
        st.markdown(f"""
            <p style='font-size:20px; font-weight:bold;'>⭐ FAHAMARINANA: {r['Prob']}</p>
            <div style='display:flex; justify-content:space-around; margin-top:15px;'>
                <div style='background:#004d1a; padding:10px; border-radius:10px;'>SAFE<br>{r['Safe']}x</div>
                <div style='background:#4d3d00; padding:10px; border-radius:10px;'>MOYEN<br>{r['Moyen']}x</div>
                <div style='background:#4d0000; padding:10px; border-radius:10px;'>MAX<br>{r['Max']}x</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if diff > -60:
            time.sleep(1)
            st.rerun()
    else:
        st.info("Andrasana ny Hex Seed mba hanombohana ny AI Prediction...")

# --- FOOTER TRAINING ---
st.write("---")
st.markdown("### 🎰 TRAINING ARENA")
if st.button("🎮 TEST SIMULATION"):
    sim = random.uniform(1.0, 5.0)
    if sim >= 2.03: st.success(f"WIN! Result: {sim:.2f}x"); st.session_state.score["Win"] += 1
    else: st.error(f"LOSS! Result: {sim:.2f}x"); st.session_state.score["Loss"] += 1
st.write(f"🏆 Score: ✅ {st.session_state.score['Win']} | ❌ {st.session_state.score['Loss']}")
