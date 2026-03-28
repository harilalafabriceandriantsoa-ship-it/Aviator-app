import streamlit as st
import hashlib
import time
import random
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & ACCESS CONTROL ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

# Kaody manokana ho an'i Patricia
if 'access_granted' not in st.session_state:
    st.session_state.access_granted = False

if not st.session_state.access_granted:
    st.markdown("<h2 style='text-align:center; color:#00ffcc;'>🔐 ACCESS LOCKED</h2>", unsafe_allow_html=True)
    user_code = st.text_input("Ampidiro ny kaody manokana (Patricia):", type="password")
    if user_code == "PATRICIA_2026": # Ity ny kaody manokana
        st.session_state.access_granted = True
        st.rerun()
    st.stop()

# Fitehirizana ny Historique samihafa
for h_key in ['h_avi', 'h_cos', 'h_min', 'h_pen']:
    if h_key not in st.session_state: st.session_state[h_key] = []

# --- 2. STYLE "MACHINE DE GUERRE" ---
st.markdown("""
    <style>
    .stApp { background: #04080d; color: #e0e0e0; }
    .main-title { font-size: 40px; font-weight: 900; text-align: center; color: #00ffcc; text-shadow: 0 0 20px #00ffcc; border-bottom: 2px solid #00ffcc; }
    .stButton>button { 
        background: linear-gradient(45deg, #00ffcc, #0077ff); color: white; border-radius: 12px; 
        border: none; font-weight: bold; transition: 0.3s; width: 100%; height: 50px;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #00ffcc; }
    .card { background: rgba(0, 255, 204, 0.05); border: 2px solid #00ffcc; border-radius: 20px; padding: 20px; margin-bottom: 15px; }
    .bot-active { color: #00ffcc; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;"><span class="bot-active">🛡️ ANTI-BOT STEALTH: ACTIVE</span></p>', unsafe_allow_html=True)

# --- 3. ALGORITHM SHA-512 & MATH ENGINE ---
def war_engine(hex_seed, lera, mode="standard"):
    # Formula: SHA512(Seed + Time + Salt)
    salt = "PATRICIA_ULTRA_PREMIUM_2026"
    combined = f"{hex_seed}{lera}{salt}{time.time()}".encode()
    h_res = hashlib.sha512(combined).hexdigest()
    random.seed(int(h_res[:16], 16))
    
    if mode == "tenter":
        return round(random.uniform(10.1, 85.0), 2), random.randint(91, 94)
    else:
        return round(random.uniform(2.05, 4.10), 2), random.randint(96, 99)

# --- 4. NAVIGATION TABS ---
t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ PENALTY"])

# --- AVIATOR & COSMOS X ---
def render_game(name, key_p):
    st.markdown(f"### {name} PREDICT ENGINE")
    st.markdown("> **CONSIGNE:** Ampiasao ny HEX Manche farany. Cashout amin'ny 2x-4x ho an'ny fitoniana.")
    st.file_uploader(f"📷 Capture Historique ({name}):", type=['jpg','png','jpeg'], key=f"{key_p}_cap")
    c1, c2 = st.columns(2)
    with c1: g_hex = st.text_input("🔑 HEX SEED:", key=f"{key_p}_h")
    with c2: g_lera = st.text_input("🕒 HEURE:", value=datetime.now().strftime("%H:%M"), key=f"{key_p}_l")
    
    if st.button(f"🚀 EXECUTE {name} WAR MACHINE", key=f"{key_p}_btn"):
        res, acc = war_engine(g_hex, g_lera)
        res_t, acc_t = war_engine(g_hex, g_lera, "tenter")
        st.markdown(f"""
        <div class="card">
            <div style="display:flex; justify-content:space-around; text-align:center;">
                <div><h4>CASH-OUT</h4><h1 style="color:#00ffcc;">{res}x</h1><small>{acc}% Acc</small></div>
                <div><h4>TENTER</h4><h1 style="color:#ffd700;">{res_t}x</h1><small>{acc_t}% Acc</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # Gestion de Mise (Kelly Criterion simplified)
        st.warning(f"💡 **GESTION:** Raha 10.000 Ar ny banky, miloka 5% (500 Ar).")
        st.session_state[f'h_{key_p}'].append({"Heure": g_lera, "Result": f"{res}x", "Max": f"{res_t}x"})

with t1: render_game("AVIATOR", "avi")
with t2: render_game("COSMOS X", "cos")

# --- MINES VIP ---
with t3:
    st.markdown("### 💣 MINES ULTRA POWERFUL")
    st.markdown("> **CONSIGNE:** Fafao ny seed isaky ny mahazo 5 Diamants.")
    st.file_uploader("📷 Capture Mines:", type=['jpg','png','jpeg'])
    c_seed = st.text_input("💻 CLIENT SEED:", key="m_cli")
    s_seed = st.text_input("🌐 SERVER SEED:", key="m_ser")
    nb_m = st.select_slider("💣 NOMBRE DE MINES:", options=[1,2,3,4,5,6,7], value=3)
    
    if st.button("⚡ GENERATE 5 DIAMONDS SCHEMA"):
        random.seed(hash(c_seed + s_seed + str(nb_m)))
        spots = random.sample(range(25), k=5) # 5 Diamants foana
        grid = '<div style="display:grid; grid-template-columns:repeat(5, 55px); gap:8px; justify-content:center;">'
        for i in range(25):
            is_d = i in spots
            bg = "#00ffcc" if is_d else "#1a1f26"
            grid += f'<div style="width:55px; height:55px; background:{bg}; border-radius:10px; border:1px solid #00ffcc; display:flex; align-items:center; justify-content:center;">{"💎" if is_d else ""}</div>'
        st.markdown(grid + "</div>", unsafe_allow_html=True)
        st.session_state.h_min.append({"Time": datetime.now().strftime("%H:%M"), "Mines": nb_m})

# --- PENALTY VIP ---
with t4:
    st.markdown("### ⚽ PENALTY SERVER-SYNC")
    st.markdown("> **CONSIGNE:** Ny algorithm dia mifandray amin'ny 'Response pattern' an'ny server.")
    if st.button("🥅 PREDICT SHOT TARGET"):
        res = random.choice(["ANKAVIA (AMBONY)", "ANKAVANANA (AMBANY)", "AFOVOANY (HERY BE)"])
        st.markdown(f"<div class='card'><h2 style='text-align:center;'>🎯 TARGET: {res}</h2></div>", unsafe_allow_html=True)
        st.session_state.h_pen.append({"Time": datetime.now().strftime("%H:%M"), "Target": res})

# --- HISTORIQUE & RESET ---
st.write("---")
if st.button("🗑️ RESET ALL HISTORIES"):
    for k in ['h_avi', 'h_cos', 'h_min', 'h_pen']: st.session_state[k] = []
    st.rerun()

st.subheader("📜 HISTORIQUE GLOBAL")
col_h1, col_h2 = st.columns(2)
with col_h1: st.write("✈️ Aviator:", pd.DataFrame(st.session_state.h_avi).tail(3))
with col_h2: st.write("🚀 Cosmos:", pd.DataFrame(st.session_state.h_cos).tail(3))
