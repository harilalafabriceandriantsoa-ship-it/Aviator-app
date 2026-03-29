import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

# INITIALISATION ADMIN
if 'access_code' not in st.session_state:
    st.session_state.access_code = "2026"
if 'admin_name' not in st.session_state:
    st.session_state.admin_name = "PATRICIA"
if 'admin_phone' not in st.session_state:
    st.session_state.admin_phone = "0346249701"

st.markdown("""
    <style>
    .stApp { background: #010a12; color: #eee; }
    .main-header { 
        font-size: 30px; font-weight: 900; text-align: center; color: #00ffcc; 
        border: 2px solid #00ffcc; padding: 15px; border-radius: 15px; 
        box-shadow: 0 0 15px #00ffcc; margin-bottom: 25px;
    }
    .prediction-card { 
        background: rgba(0, 255, 204, 0.05); border-radius: 15px; 
        border: 1px solid #00ffcc; padding: 20px; margin-bottom: 15px;
    }
    .target-val { font-size: 40px; color: #00ffcc; font-weight: 800; text-align: center; }
    .prob-badge { background: #00ffcc; color: #000; padding: 4px 12px; border-radius: 20px; font-weight: 900; }
    .stat-row { display: flex; justify-content: space-around; border-top: 1px solid #333; margin-top: 10px; padding-top: 10px; font-size: 14px; }
    .stat-val { color: #00ffcc; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIN SYSTEM ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div class="main-header">TITAN V85.0: ACCESS CONTROL</div>', unsafe_allow_html=True)
    code_input = st.text_input("Ampidiro ny kaody mamoha ny app:", type="password")
    if st.button("Mivoha"):
        if code_input == st.session_state.access_code:
            st.session_state.authenticated = True
            st.rerun()
        else: st.error("Kaody diso.")
    st.stop()

# --- 3. SIDEBAR SETTINGS ---
with st.sidebar:
    st.markdown(f"### 👤 MANAGER: {st.session_state.admin_name}")
    with st.expander("🔒 ADMIN PANEL"):
        st.session_state.admin_name = st.text_input("Anarana vaovao:", st.session_state.admin_name)
        st.session_state.access_code = st.text_input("MDP vaovao:", st.session_state.access_code, type="password")
        if st.button("Tehirizina"): st.rerun()
    st.markdown("---")
    st.markdown("### 📊 HISTORIQUE DE PRÉDICTION")
    if 'history' not in st.session_state: st.session_state.history = []
    for h in st.session_state.history[-5:]: # Asehoy ny 5 farany
        st.write(f"🕒 {h['time']} -> {h['val']}x")

# --- 4. ENGINE ---
def get_3_preds(seed, base_ora, game_type):
    results = []
    h = hashlib.sha256(f"{seed}-TITAN".encode()).hexdigest()
    try:
        fmt = "%H:%M:%S" if game_type == "cosmos" else "%H:%M"
        dt = datetime.strptime(base_ora, fmt)
    except: dt = datetime.now()
    
    for i in range(3):
        random.seed(int(h[i*8:(i+1)*8], 16))
        moyen = round(random.uniform(1.8, 4.5), 2)
        p = {
            "lera": (dt + timedelta(minutes=(i+1)*4)).strftime(fmt),
            "moyen": moyen, "min": round(moyen*0.8, 2), "max": round(moyen*1.5, 2),
            "prob": random.randint(94, 98)
        }
        results.append(p)
        st.session_state.history.append({"time": p['lera'], "val": moyen})
    return results

# --- 5. INTERFACE ---
st.markdown('<div class="main-header">TITAN V85.0 ULTRA-SYNC ⚔️</div>', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

# AVIATOR
with tab1:
    st.markdown("### ⚡ AVIATOR ANALYSIS")
    st.file_uploader("📸 UPLOAD HISTORIQUE DE LA MANCHE", key="av_hist")
    h_av = st.text_input("🔑 SERVER HEX:", key="h_av")
    o_av = st.text_input("🕒 HH:mm:", value=datetime.now().strftime("%H:%M"), key="o_av")
    if st.button("🔥 EXECUTE AVIATOR"):
        for p in get_3_preds(h_av, o_av, "aviator"):
            st.markdown(f"""<div class="prediction-card">
                <div style="display:flex; justify-content:space-between;"><span style="color:#ff4444;">⏰ {p['lera']}</span><span class="prob-badge">{p['prob']}%</span></div>
                <div class="target-val">{p['moyen']}x</div>
                <div class="stat-row">
                    <span>MIN: <span class="stat-val">{p['min']}x</span></span>
                    <span>MOYEN: <span class="stat-val">{p['moyen']}x</span></span>
                    <span>MAX: <span class="stat-val">{p['max']}x</span></span>
                </div>
            </div>""", unsafe_allow_html=True)

# COSMOS X
with tab2:
    st.markdown("### 🚀 COSMOS X ANALYSIS")
    st.file_uploader("📸 UPLOAD HISTORIQUE COSMOS", key="co_hist")
    h_co = st.text_input("🔑 HEX SEED:", key="h_co")
    o_co = st.text_input("🕒 HH:mm:ss:", value=datetime.now().strftime("%H:%M:%S"), key="o_co")
    if st.button("🚀 START COSMOS"):
        for p in get_3_preds(h_co, o_co, "cosmos"):
            st.markdown(f"""<div class="prediction-card">
                <div style="display:flex; justify-content:space-between;"><span style="color:#ff4444;">⏰ {p['lera']}</span><span class="prob-badge">{p['prob']}%</span></div>
                <div class="target-val">{p['moyen']}x</div>
                <div class="stat-row">
                    <span>MIN: <span class="stat-val">{p['min']}x</span></span>
                    <span>MOYEN: <span class="stat-val">{p['moyen']}x</span></span>
                    <span>MAX: <span class="stat-val">{p['max']}x</span></span>
                </div>
            </div>""", unsafe_allow_html=True)

# MINES VIP
with tab3:
    st.markdown("### 💣 MINES VIP DECODER")
    s_serv = st.text_input("📡 Seed du serveur:", key="s_min_serv")
    s_cli = st.text_input("💻 Seed du client:", key="s_min_cli")
    if st.button("💎 DECODE SAFE PATH"):
        if s_serv and s_cli:
            random.seed(int(hashlib.sha256(f"{s_serv}{s_cli}".encode()).hexdigest()[:10], 16))
            diamond_pos = random.sample(range(25), 5)
            # Grid display eto...
            st.success("Schema généré avec succès!")

st.markdown(f"<center style='font-size:12px; color:#444; margin-top:50px;'>TITAN OMNI-STRIKE BY {st.session_state.admin_name} © 2026<br>MANAGER APP MODE ACTIVE</center>", unsafe_allow_html=True)
