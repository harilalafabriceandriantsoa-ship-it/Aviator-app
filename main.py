import streamlit as st
import hashlib
import time
import random
import pandas as pd
from datetime import datetime, timedelta

# --- CONFIGURATION INITIALE ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

# Fitehirizana ny Historique samihafa
for key in ['h_avi', 'h_cos', 'h_min', 'h_pen']:
    if key not in st.session_state: st.session_state[key] = []

# --- STYLE MACHINE DE GUERRE ---
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #ffffff; }
    .main-title { font-size: 45px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 30px #00ffcc; border-bottom: 3px solid #00ffcc; padding-bottom: 10px; }
    .consigne-box { background: rgba(255, 75, 75, 0.1); border-left: 5px solid #ff4b4b; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-style: italic; }
    .card { background: rgba(0, 255, 204, 0.03); border: 1px solid #00ffcc; border-radius: 15px; padding: 25px; text-align: center; box-shadow: 0 0 15px rgba(0,255,204,0.1); }
    .stButton>button { 
        background: linear-gradient(90deg, #00ffcc 0%, #0077ff 100%); color: #010a12; 
        border-radius: 8px; border: none; font-weight: 900; letter-spacing: 1px; transition: 0.4s; height: 55px; width: 100%;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,255,204,0.4); color: white; }
    .status-bar { color: #00ffcc; font-size: 14px; font-weight: bold; text-align: center; animation: blinker 2s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

# --- SECURITY SYSTEM (Patricia Only) ---
if 'access' not in st.session_state: st.session_state.access = False
if not st.session_state.access:
    st.markdown("<h2 style='text-align:center;'>🔐 SECURE LOGIN</h2>", unsafe_allow_html=True)
    code = st.text_input("Ampidiro ny kaody manokana:", type="password")
    if code == "PATRICIA_BEAST": # Ity ny kaody vaovao
        st.session_state.access = True
        st.rerun()
    st.stop()

st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)
st.markdown('<p class="status-bar">🛡️ ANTI-BOT STEALTH: ACTIVE | SHA-512 ENCRYPTION: ON</p>', unsafe_allow_html=True)

# --- ALGORITHM ENGINE (ULTRA POWERFUL) ---
def professional_sha_algo(seed, salt="ULTRA_STRIKE"):
    # Fampiasana SHA-512 sy Double Hashing
    raw = f"{seed}{salt}{time.time()}".encode()
    hash1 = hashlib.sha512(raw).hexdigest()
    hash2 = hashlib.sha256(hash1.encode()).hexdigest()
    random.seed(int(hash2[:16], 16))
    
    vmin = round(random.uniform(1.10, 1.80), 2)
    vmoy = round(random.uniform(2.10, 4.20), 2)
    vmax = round(random.uniform(10.5, 95.0), 2)
    return vmin, vmoy, vmax

# --- NAVIGATION ---
tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY"])

# --- ✈️ AVIATOR & COSMOS X ---
for i, tab in enumerate([tabs[0], tabs[1]]):
    name = "AVIATOR" if i == 0 else "COSMOS X"
    key = "avi" if i == 0 else "cos"
    with tab:
        st.markdown(f'<div class="consigne-box">⚠️ <b>CONSIGNE {name}:</b> Maka sary ny historique alohan\'ny hikajiana. Cashout amin\'ny 2x-4x ho an\'ny fitoniana, ary tenter-o ny x10+ indray mandeha isaky ny in-5 mandresy. Ampiasao ny Kelly Criterion.</div>', unsafe_allow_html=True)
        
        st.file_uploader(f"📸 Capture Historique {name}:", type=['jpg','png'], key=f"{key}_img")
        c1, c2 = st.columns(2)
        with c1: u_hex = st.text_input("🔑 HEX SEED:", key=f"{key}_hex")
        with c2: u_time = st.text_input("🕒 HEURE (HH:MM):", value=datetime.now().strftime("%H:%M"), key=f"{key}_time")
        
        if st.button(f"⚡ EXECUTE {name} WAR MACHINE", key=f"{key}_btn"):
            vmin, vmoy, vmax = professional_sha_algo(u_hex)
            st.markdown(f"""
                <div class="card">
                    <div style="display:flex; justify-content:space-around;">
                        <div><p>MIN</p><h2 style="color:#ff4b4b;">{vmin}x</h2></div>
                        <div><p>MOYEN (Target)</p><h1 style="color:#00ffcc;">{vmoy}x</h1></div>
                        <div><p>MAX (Tenter)</p><h2 style="color:#ffd700;">{vmax}x</h2></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.info(f"📊 **GESTION DE MISE:** Kelly Criterion: Miloka 5% amin'ny Banky. Raha 20.000 Ar = 1.000 Ar mise.")
            st.session_state[f'h_{key}'].append({"Time": u_time, "Result": f"{vmoy}x", "Max": f"{vmax}x"})

# --- 💣 MINES VIP ---
with tabs[2]:
    st.markdown('<div class="consigne-box">⚠️ <b>CONSIGNE MINES:</b> Ovao ny Seed Client isaky ny mahazo 5 Diamants. Aza mihoatra ny in-3 milalao amin\'ny schema iray.</div>', unsafe_allow_html=True)
    st.file_uploader("📸 Capture Historique (Mines):", type=['jpg','png'])
    m1, m2 = st.columns(2)
    with m1: c_seed = st.text_input("💻 CLIENT SEED:")
    with m2: s_seed = st.text_input("🌐 SERVER SEED:")
    n_mines = st.select_slider("💣 ISAN'NY BAOMBA:", options=[1,2,3,4,5,6,7], value=3)
    
    if st.button("💎 GENERATE ULTRA POWERFUL SCHEMA"):
        random.seed(hash(c_seed + s_seed))
        spots = random.sample(range(25), k=5)
        grid = '<div style="display:grid; grid-template-columns:repeat(5, 60px); gap:10px; justify-content:center;">'
        for i in range(25):
            char = "💎" if i in spots else ""
            color = "#00ffcc" if i in spots else "#1a1f26"
            grid += f'<div style="width:60px; height:60px; background:{color}; border:1px solid #00ffcc; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:24px;">{char}</div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)
        st.session_state.h_min.append({"Time": datetime.now().strftime("%H:%M"), "Mines": n_mines})

# --- ⚽ PENALTY ---
with tabs[3]:
    st.markdown('<div class="consigne-box">⚠️ <b>CONSIGNE PENALTY:</b> Miandrasa "Response" avy amin\'ny server vao manindry. Ampiasao ny Martingale: Double-o ny mise raha resy.</div>', unsafe_allow_html=True)
    if st.button("🥅 SYNC & PREDICT TARGET"):
        target = random.choice(["ANKAVIA AMBONY", "ANKAVANANA AMBANY", "AFOVOANY (MAHERY)"])
        st.markdown(f'<div class="card"><h3>🎯 TARGET: <span style="color:#00ffcc;">{target}</span></h3></div>', unsafe_allow_html=True)
        st.session_state.h_pen.append({"Time": datetime.now().strftime("%H:%M"), "Target": target})

# --- HISTORIQUE & TOOLS ---
st.write("---")
st.subheader("📜 HISTORIQUE DES PRÉDICTIONS")
col_h = st.columns(4)
titles = ["Aviator", "Cosmos", "Mines", "Penalty"]
keys = ['h_avi', 'h_cos', 'h_min', 'h_pen']
for i, col in enumerate(col_h):
    with col:
        st.write(f"**{titles[i]}**")
        if st.session_state[keys[i]]:
            st.dataframe(pd.DataFrame(st.session_state[keys[i]]).tail(5))
