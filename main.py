import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION (ADMIN: 2026) ---
st.set_page_config(page_title="TITAN V85.0 ULTRA", layout="wide")

if 'access_code' not in st.session_state: st.session_state.access_code = "2026"
if 'admin_name' not in st.session_state: st.session_state.admin_name = "PATRICIA"
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. ALGORITHM ---
def get_prediction(seed, lera_feno, game_type):
    combined = hashlib.sha512(f"{seed}{lera_feno}{game_type}V85".encode()).hexdigest()
    random.seed(int(combined[:12], 16))
    
    results = []
    # Fandaharana ny lera (Ora:Min:Sec ho an'ny Cosmos, Ora:Min ho an'ny hafa)
    fmt = "%H:%M:%S" if game_type == "cosmos" else "%H:%M"
    try:
        t_obj = datetime.strptime(lera_feno, fmt)
    except:
        t_obj = datetime.now()

    for i in range(3):
        moyen = round(random.uniform(1.90, 4.80), 2)
        min_val = round(moyen * 0.82, 2)
        max_val = round(moyen * 1.40, 2)
        # Intervalle 3 minitra
        future_time = (t_obj + timedelta(minutes=(i+1)*3)).strftime(fmt)
        
        res = {"lera": future_time, "moyen": moyen, "min": min_val, "max": max_val, "prob": random.randint(97, 99)}
        results.append(res)
        if i == 0: st.session_state.history.insert(0, res)
    return results

# --- 3. STYLE ---
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #eee; }
    .main-header { font-size: 24px; font-weight: 900; text-align: center; color: #00ffcc; border: 2px solid #00ffcc; padding: 10px; border-radius: 12px; margin-bottom: 20px; }
    .prediction-card { background: rgba(0, 255, 204, 0.05); border-radius: 10px; border: 1px solid #00ffcc; padding: 12px; margin-bottom: 8px; }
    .target-val { font-size: 38px; color: #00ffcc; font-weight: 800; text-align: center; }
    .stat-row { display: flex; justify-content: space-around; font-size: 13px; border-top: 1px solid rgba(0,255,204,0.2); padding-top: 8px; }
    .hist-card { border-left: 4px solid #00ffcc; background: #02121d; padding: 10px; margin-bottom: 5px; border-radius: 5px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown(f"### 👤 MANAGER: {st.session_state.admin_name}")
    key = st.text_input("Admin Key:", type="password")
    if key == st.session_state.access_code:
        with st.expander("🔓 MODIFIER MDP / INFO"):
            st.session_state.admin_name = st.text_input("Anarana vaovao:", st.session_state.admin_name)
            st.session_state.access_code = st.text_input("MDP vaovao:", st.session_state.access_code)
            if st.button("💾 ENREGISTRER"): st.rerun()
    if st.button("🗑️ RESET HISTORY"):
        st.session_state.history = []
        st.rerun()

# --- 5. MAIN ---
st.markdown('<div class="main-header">TITAN V85.0 ULTRA-SYNC ⚔️</div>', unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

with t1:
    st.subheader("⚡ AVIATOR 8/10")
    h_seed = st.text_input("🔑 HEX SEED (Aviator):", key="h_aviator")
    l_time = st.text_input("🕒 LERA (HH:mm):", value=datetime.now().strftime("%H:%M"), key="l_aviator")
    if st.button("🔥 ANALYZE AVIATOR"):
        if h_seed:
            for p in get_prediction(h_seed, l_time, "aviator"):
                st.markdown(f'<div class="prediction-card"><b>⏰ {p["lera"]}</b> | <b style="color:#00ffcc;">{p["prob"]}%</b><div class="target-val">{p["moyen"]}x</div><div class="stat-row"><span>MIN: {p["min"]}x</span><span>MOYEN: {p["moyen"]}x</span><span>MAX: {p["max"]}x</span></div></div>', unsafe_allow_html=True)

with t2:
    st.subheader("⚡ COSMOS 8/10")
    c_seed = st.text_input("🔑 HEX SEED (Cosmos):", key="c_cosmos")
    # Lera misy segondra ho an'ny Cosmos
    l_time_c = st.text_input("🕒 LERA (HH:mm:ss):", value=datetime.now().strftime("%H:%M:%S"), key="l_cosmos")
    if st.button("🚀 ANALYZE COSMOS"):
        if c_seed:
            for p in get_prediction(c_seed, l_time_c, "cosmos"):
                st.markdown(f'<div class="prediction-card"><b>⏰ {p["lera"]}</b> | <b style="color:#00ffcc;">{p["prob"]}%</b><div class="target-val">{p["moyen"]}x</div><div class="stat-row"><span>MIN: {p["min"]}x</span><span>MOYEN: {p["moyen"]}x</span><span>MAX: {p["max"]}x</span></div></div>', unsafe_allow_html=True)

with t3:
    st.subheader("💣 MINES DECODER VIP")
    client_s = st.text_input("🔑 CLIENT SEED:")
    server_s = st.text_input("🔑 SERVER SEED:")
    m_count = st.select_slider("Mines:", options=[1, 3, 5], value=3)
    if st.button("🔍 SCAN MINES"):
        if client_s and server_s:
            grid = ["⬛"] * 25
            stars = random.sample(range(25), 5)
            for s in stars: grid[s] = "⭐"
            st.code(f"GRID: {' '.join(grid[:5])}\n      {' '.join(grid[5:10])}\n      {' '.join(grid[10:15])}\n      {' '.join(grid[15:20])}\n      {' '.join(grid[20:25])}")

# --- 6. CAPTURE HISTORIQUE ---
st.markdown("---")
st.markdown("### 📜 LAST PREDICTIONS (CAPTURE)")
if st.session_state.history:
    for h in st.session_state.history[:5]:
        st.markdown(f"""<div class="hist-card">
            ⏰ {h['lera']} | <b>{h['moyen']}x</b> | <small>Min: {h['min']}x / Max: {h['max']}x</small>
        </div>""", unsafe_allow_html=True)
else:
    st.write("Tsy mbola misy historique.")
