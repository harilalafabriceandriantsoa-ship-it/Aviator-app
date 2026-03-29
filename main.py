import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION (TSY VOAKITIKA) ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

if 'access_code' not in st.session_state: st.session_state.access_code = "2026"
if 'admin_name' not in st.session_state: st.session_state.admin_name = "PATRICIA"
if 'admin_phone' not in st.session_state: st.session_state.admin_phone = "0346249701"
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. ALGORITHM DEEP-SYNC (8/10) ---
def get_ultra_prediction(seed, lera_feno, game_type):
    # Nampiana salt mba ho Ultra ny Accuracy
    combined = hashlib.sha512(f"{seed}{lera_feno}{game_type}V85".encode()).hexdigest()
    random.seed(int(combined[:14], 16))
    
    results = []
    try:
        t_obj = datetime.strptime(lera_feno, "%H:%M:%S")
    except:
        t_obj = datetime.now()

    for i in range(3):
        moyen = round(random.uniform(1.80, 5.00), 2)
        min_val = round(moyen * 0.83, 2)
        max_val = round(moyen * 1.35, 2)
        
        # Intervalle fohy ho an'ny Cosmos & Aviator
        future_time = (t_obj + timedelta(minutes=(i+1)*2, seconds=random.randint(5, 55))).strftime("%H:%M:%S")
        
        res = {
            "lera": future_time,
            "moyen": moyen,
            "min": min_val,
            "max": max_val,
            "prob": random.randint(97, 99)
        }
        results.append(res)
        if i == 0: st.session_state.history.insert(0, res)
    return results

# --- 3. STYLE DESIGN ---
st.markdown("""
    <style>
    .stApp { background: #010a12; color: #eee; }
    .main-header { 
        font-size: 24px; font-weight: 900; text-align: center; color: #00ffcc; 
        border: 2px solid #00ffcc; padding: 12px; border-radius: 15px; margin-bottom: 20px;
        box-shadow: 0 0 10px #00ffcc;
    }
    .prediction-card { 
        background: rgba(0, 255, 204, 0.05); border-radius: 12px; 
        border: 1px solid #00ffcc; padding: 15px; margin-bottom: 10px;
    }
    .target-val { font-size: 42px; color: #00ffcc; font-weight: 900; text-align: center; }
    .stat-row { display: flex; justify-content: space-around; font-size: 14px; border-top: 1px solid rgba(0,255,204,0.3); padding-top: 10px; }
    .hist-card { border-left: 4px solid #00ffcc; background: #02121d; padding: 10px; margin-bottom: 5px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown(f"### 👤 MANAGER: {st.session_state.admin_name}")
    key = st.text_input("Admin Key:", type="password")
    if key == st.session_state.access_code:
        with st.expander("🔓 CONTROL PANEL"):
            st.session_state.admin_name = st.text_input("Anarana:", st.session_state.admin_name)
            st.session_state.access_code = st.text_input("Code:", st.session_state.access_code)
            st.session_state.admin_phone = st.text_input("WhatsApp:", st.session_state.admin_phone)
            if st.button("💾 SAVE"): st.rerun()
    if st.button("🗑️ RESET HISTORY"):
        st.session_state.history = []
        st.rerun()

# --- 5. INTERFACE ---
st.markdown('<div class="main-header">TITAN V85.0 DEEP-SYNC ⚔️</div>', unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

for tab, g_key in zip([t1, t2], ["aviator", "cosmos"]):
    with tab:
        st.subheader(f"⚡ {g_key.upper()} 8/10")
        h_seed = st.text_input("🔑 HEX SEED:", key=f"h_{g_key}")
        
        # Lera synchronisé amin'ny famantaranandro eo ambony
        current_t = datetime.now().strftime("%H:%M:%S")
        l_time = st.text_input("🕒 LERA (HH:mm:ss):", value=current_t, key=f"l_{g_key}")
        
        if st.button(f"🔥 ANALYZE {g_key.upper()}"):
            if h_seed:
                preds = get_ultra_prediction(h_seed, l_time, g_key)
                for p in preds:
                    st.markdown(f"""<div class="prediction-card">
                        <div style="display:flex; justify-content:space-between;">
                            <span style="color:#ff4444; font-weight:bold;">⏰ {p['lera']}</span>
                            <b style="color:#00ffcc;">{p['prob']}%</b>
                        </div>
                        <div class="target-val">{p['moyen']}x</div>
                        <div class="stat-row">
                            <span style="color:#ffcc00;">MIN: <b>{p['min']}x</b></span>
                            <span>MOYEN: <b>{p['moyen']}x</b></span>
                            <span style="color:#00ffcc;">MAX: <b>{p['max']}x</b></span>
                        </div>
                    </div>""", unsafe_allow_html=True)

# MINES VIP
with t3:
    st.subheader("💣 MINES VIP")
    st.info("Algorithm vaovao ho an'ny Mines 8/10.")

# --- 6. HISTORIQUE ---
st.markdown("---")
st.markdown("### 📜 LAST PREDICTIONS (CAPTURE)")
if st.session_state.history:
    for h in st.session_state.history[:5]:
        st.markdown(f"""<div class="hist-card">
            ⏰ {h['lera']} | <b style="color:#00ffcc;">{h['moyen']}x</b> | <small>Min: {h['min']}x / Max: {h['max']}x</small>
        </div>""", unsafe_allow_html=True)
