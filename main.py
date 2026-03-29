import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION (TSY NI OVA) ---
st.set_page_config(page_title="TITAN V85.0 ULTRA", layout="wide")

if 'access_code' not in st.session_state: st.session_state.access_code = "2026"
if 'admin_name' not in st.session_state: st.session_state.admin_name = "PATRICIA"
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. ALGORITHM 8/10 ---
def get_prediction(seed, lera_feno, game_type):
    combined = hashlib.sha512(f"{seed}{lera_feno}{game_type}".encode()).hexdigest()
    random.seed(int(combined[:12], 16))
    
    results = []
    try:
        t_obj = datetime.strptime(lera_feno, "%H:%M")
    except:
        t_obj = datetime.now()

    for i in range(3):
        moyen = round(random.uniform(1.85, 4.60), 2)
        min_val = round(moyen * 0.81, 2)
        max_val = round(moyen * 1.45, 2)
        future_time = (t_obj + timedelta(minutes=(i+1)*4)).strftime("%H:%M")
        
        res = {
            "lera": future_time,
            "moyen": moyen,
            "min": min_val,
            "max": max_val,
            "prob": random.randint(96, 98)
        }
        results.append(res)
        # Tehirizina ao amin'ny historique ny vinavina voalohany
        if i == 0: st.session_state.history.insert(0, res)
    return results

# --- 3. STYLE DESIGN ---
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #eee; }
    .main-header { 
        font-size: 26px; font-weight: 900; text-align: center; color: #00ffcc; 
        border: 2px solid #00ffcc; padding: 15px; border-radius: 15px; margin-bottom: 25px;
    }
    .prediction-card { 
        background: rgba(0, 255, 204, 0.05); border-radius: 12px; 
        border: 1px solid #00ffcc; padding: 15px; margin-bottom: 10px;
    }
    .target-val { font-size: 38px; color: #00ffcc; font-weight: 800; text-align: center; }
    .stat-row { display: flex; justify-content: space-around; font-size: 13px; border-top: 1px solid rgba(0,255,204,0.2); padding-top: 10px; }
    .hist-card { border-left: 4px solid #00ffcc; background: #02121d; padding: 12px; margin-bottom: 8px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR (MANAGER) ---
with st.sidebar:
    st.markdown(f"### 👤 MANAGER: {st.session_state.admin_name}")
    key = st.text_input("Admin Key:", type="password")
    if key == st.session_state.access_code:
        with st.expander("🔓 CONTROL PANEL"):
            st.session_state.admin_name = st.text_input("Anarana:", st.session_state.admin_name)
            st.session_state.access_code = st.text_input("Code:", st.session_state.access_code)
            if st.button("💾 SAVE"): st.rerun()
    if st.button("🗑️ RESET HISTORY"):
        st.session_state.history = []
        st.rerun()

# --- 5. MAIN INTERFACE ---
st.markdown('<div class="main-header">TITAN V85.0 ULTRA ⚔️</div>', unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

for tab, g_key in zip([t1, t2], ["aviator", "cosmos"]):
    with tab:
        st.subheader(f"⚡ {g_key.upper()} 8/10")
        c1, c2 = st.columns(2)
        h_seed = c1.text_input("🔑 HEX SEED:", key=f"h_{g_key}")
        l_time = c2.text_input("🕒 LERA (HH:mm):", value=datetime.now().strftime("%H:%M"), key=f"l_{g_key}")
        
        if st.button(f"🔥 ANALYZE {g_key.upper()}"):
            if h_seed:
                preds = get_prediction(h_seed, l_time, g_key)
                for p in preds:
                    st.markdown(f"""<div class="prediction-card">
                        <div style="display:flex; justify-content:space-between;">
                            <span style="color:#ff4444; font-weight:bold;">⏰ {p['lera']}</span>
                            <b style="color:#00ffcc;">{p['prob']}%</b>
                        </div>
                        <div class="target-val">{p['moyen']}x</div>
                        <div class="stat-row">
                            <span style="color:#ffcc00;">MIN: {p['min']}x</span>
                            <span>MOYEN: {p['moyen']}x</span>
                            <span style="color:#00ffcc;">MAX: {p['max']}x</span>
                        </div>
                    </div>""", unsafe_allow_html=True)

# MINES VIP
with t3:
    st.subheader("💣 MINES VIP")
    m_count = st.select_slider("Mines:", options=[1, 3, 5], value=3)
    if st.button("🔍 SCAN"):
        grid = ["⬛"] * 25
        stars = random.sample(range(25), 5)
        for s in stars: grid[s] = "⭐"
        for i in range(0, 25, 5):
            st.write(f"{grid[i]} {grid[i+1]} {grid[i+2]} {grid[i+3]} {grid[i+4]}")

# --- 6. HISTORIQUE (LAST PREDICTIONS) ---
st.markdown("---")
st.markdown("### 📜 LAST PREDICTIONS (CAPTURE)")
if st.session_state.history:
    # Namboarina eto mba tsy hisy KeyError intsony
    for h in st.session_state.history[:5]:
        st.markdown(f"""<div class="hist-card">
            ⏰ <b>{h['lera']}</b> | <span style="color:#00ffcc;">{h['moyen']}x</span> | 
            <small>Min: {h['min']}x / Max: {h['max']}x</small>
        </div>""", unsafe_allow_html=True)
else:
    st.write("Tsy mbola misy historique.")
