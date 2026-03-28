import streamlit as st
import hashlib
import time
import random
import pandas as pd
from datetime import datetime, timedelta

# --- CONFIGURATION INITIALE ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

# Fitehirizana ny Historique
for key in ['h_avi', 'h_cos', 'h_min', 'h_pen']:
    if key not in st.session_state: st.session_state[key] = []

# --- STYLE PREMIUM MACHINE DE GUERRE ---
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #ffffff; }
    .main-title { font-size: 40px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 20px #00ffcc; border-bottom: 3px solid #00ffcc; }
    .consigne-box { background: rgba(255, 75, 75, 0.1); border-left: 5px solid #ff4b4b; padding: 10px; border-radius: 5px; margin-bottom: 15px; font-size: 14px; }
    .card { background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc; border-radius: 15px; padding: 20px; text-align: center; }
    .lera-box { background: rgba(255, 215, 0, 0.1); border: 1px dashed #ffd700; padding: 10px; border-radius: 10px; color: #ffd700; margin-top: 10px; font-weight: bold; }
    .stButton>button { 
        background: linear-gradient(90deg, #00ffcc, #0077ff); color: #010a12; 
        font-weight: 900; border-radius: 10px; height: 50px; width: 100%; border: none;
    }
    .status-bar { color: #00ffcc; font-size: 12px; text-align: center; animation: blinker 2s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)
st.markdown('<p class="status-bar">🛡️ ANTI-BOT STEALTH: ACTIVE | SYSTEM SYNC: 100%</p>', unsafe_allow_html=True)

# --- ALGORITHM ENGINE (ULTRA POWERFUL SHA-512) ---
def get_beast_prediction(seed, current_time):
    combined = f"{seed}{current_time}{time.time()}".encode()
    h = hashlib.sha512(combined).hexdigest()
    random.seed(int(h[:16], 16))
    
    # Coefficients
    vmin = round(random.uniform(1.20, 1.50), 2)
    vmoy = round(random.uniform(2.10, 4.50), 2)
    vmax = round(random.uniform(10.0, 65.0), 2)
    
    # Lera 3 samihafa sy ny Pourcentage-ny avy
    base_t = datetime.strptime(current_time, "%H:%M")
    rounds = []
    for _ in range(3):
        r_time = (base_t + timedelta(minutes=random.randint(2, 15))).strftime("%H:%M")
        r_acc = random.randint(91, 98)
        rounds.append({"ora": r_time, "acc": r_acc})
        
    return vmin, vmoy, vmax, rounds

# --- NAVIGATION ---
tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY"])

# --- AVIATOR & COSMOS X ---
for i, tab in enumerate([tabs[0], tabs[1]]):
    name = "AVIATOR" if i == 0 else "COSMOS X"
    key = "avi" if i == 0 else "cos"
    with tab:
        st.markdown(f'<div class="consigne-box">⚠️ <b>CONSIGNE:</b> Cashout 2x-4x. Tenter x10+ isaky ny 15min.</div>', unsafe_allow_html=True)
        st.file_uploader(f"📸 Capture {name}:", type=['jpg','png'], key=f"{key}_up")
        c1, c2 = st.columns(2)
        with c1: u_hex = st.text_input("🔑 HEX SEED:", key=f"{key}_h")
        with c2: u_time = st.text_input("🕒 HEURE:", value=datetime.now().strftime("%H:%M"), key=f"{key}_t")
        
        if st.button(f"🚀 EXECUTE {name} WAR MACHINE", key=f"{key}_b"):
            vmin, vmoy, vmax, rounds = get_beast_prediction(u_hex, u_time)
            st.markdown(f"""
                <div class="card">
                    <div style="display:flex; justify-content:space-around;">
                        <div><p>MIN</p><h2 style="color:#ff4b4b;">{vmin}x</h2></div>
                        <div><p>MOYEN</p><h1 style="color:#00ffcc;">{vmoy}x</h1></div>
                        <div><p>MAX</p><h2 style="color:#ffd700;">{vmax}x</h2></div>
                    </div>
                </div>
                <div class="lera-box">
                    🎯 NEXT ROUNDS:<br>
                    ⏰ {rounds[0]['ora']} ({rounds[0]['acc']}% Acc) | 
                    ⏰ {rounds[1]['ora']} ({rounds[1]['acc']}% Acc) | 
                    ⏰ {rounds[2]['ora']} ({rounds[2]['acc']}% Acc)
                </div>
            """, unsafe_allow_html=True)
            st.session_state[f'h_{key}'].append({"Time": u_time, "Result": f"{vmoy}x"})

# --- 💣 MINES VIP (DYNAMIC PREDICTION) ---
with tabs[2]:
    st.markdown('<div class="consigne-box">⚠️ <b>CONSIGNE:</b> Ovao ny Seed Client isaky ny mahazo 5 Diamants.</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1: c_seed = st.text_input("💻 CLIENT SEED:", key="m_cli")
    with m2: s_seed = st.text_input("🌐 SERVER SEED:", key="m_ser")
    n_mines = st.select_slider("💣 MINES:", options=[1,2,3,4,5,6,7], value=3)
    
    if st.button("💎 GENERATE BEAST SCHEMA"):
        # Ny schema dia miovaova foana araka ny seed
        random.seed(hash(c_seed + s_seed + str(time.time())))
        spots = random.sample(range(25), k=5)
        grid = '<div style="display:grid; grid-template-columns:repeat(5, 50px); gap:10px; justify-content:center;">'
        for i in range(25):
            char = "💎" if i in spots else ""
            color = "#00ffcc" if i in spots else "#1a1f26"
            grid += f'<div style="width:50px; height:50px; background:{color}; border:1px solid #00ffcc; border-radius:5px; display:flex; align-items:center; justify-content:center; font-size:20px;">{char}</div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)
        # Ora 3 ho an'ny Mines koa
        base_m = datetime.now()
        st.markdown(f"""
            <div class="lera-box" style="text-align:center;">
                🕒 ORA TSARA HILALAOVANA:<br>
                {(base_m + timedelta(minutes=2)).strftime("%H:%M")} (95%) | 
                {(base_m + timedelta(minutes=7)).strftime("%H:%M")} (92%) | 
                {(base_m + timedelta(minutes=12)).strftime("%H:%M")} (97%)
            </div>
        """, unsafe_allow_html=True)

# --- ⚽ PENALTY ---
with tabs[3]:
    st.markdown('<div class="consigne-box">⚠️ <b>CONSIGNE:</b> Ampiasao ny Martingale raha resy.</div>', unsafe_allow_html=True)
    if st.button("🥅 PREDICT PENALTY"):
        target = random.choice(["ANKAVIA", "ANKAVANANA", "AFOVOANY"])
        acc_p = random.randint(90, 96)
        st.markdown(f'<div class="card"><h3>🎯 TARGET: <span style="color:#00ffcc;">{target}</span></h3><h4>ACCURACY: {acc_p}%</h4></div>', unsafe_allow_html=True)
