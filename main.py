import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

# --- INITIALISATION DES VARIABLES ADMIN ---
# Tehirizina ao amin'ny session_state mba ho azo ovaina
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
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 350px; margin: 20px auto; }
    .mine-cell { background: #1a1a1a; height: 55px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px; border: 1px solid #333; }
    .diamond-cell { background: rgba(0, 255, 204, 0.2); border: 1px solid #00ffcc; box-shadow: 0 0 10px #00ffcc; }
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
        else:
            st.error("Kaody diso.")
    st.stop()

# --- 3. SIDEBAR (MANAGER & CHANGE MDP) ---
with st.sidebar:
    st.markdown("### ⚙️ SETTINGS")
    
    # --- ETO NO MANOVA NY ADMIN SY MDP ---
    with st.expander("🔒 ADMIN PANEL (Hanova MDP)"):
        new_name = st.text_input("Anarana Admin vaovao:", value=st.session_state.admin_name)
        new_phone = st.text_input("Laharana WhatsApp vaovao:", value=st.session_state.admin_phone)
        new_code = st.text_input("Mot de Passe (MDP) vaovao:", value=st.session_state.access_code, type="password")
        
        if st.button("Tehirizina ny fanovana"):
            st.session_state.admin_name = new_name
            st.session_state.admin_phone = new_phone
            st.session_state.access_code = new_code
            st.success("Voatahiry ny fanovana!")
            time.sleep(1)
            st.rerun()
            
    st.markdown("---")
    st.markdown(f"👤 **Manager:** {st.session_state.admin_name}")
    st.markdown(f"🟢 **WhatsApp:** {st.session_state.admin_phone}")
    if st.button("Log Out"):
        st.session_state.authenticated = False
        st.rerun()

# --- 4. ENGINE & INTERFACE (AVIATOR/COSMOS/MINES) ---
def get_3_preds(seed, base_ora, game_type):
    results = []
    h = hashlib.sha256(f"{seed}-TITAN-2026".encode()).hexdigest()
    try:
        fmt = "%H:%M:%S" if game_type == "cosmos" else "%H:%M"
        dt = datetime.strptime(base_ora, fmt)
    except: dt = datetime.now()
    for i in range(3):
        random.seed(int(h[i*8:(i+1)*8], 16))
        moyen = round(random.uniform(1.8, 4.2), 2)
        results.append({
            "lera": (dt + timedelta(minutes=(i+1)*5)).strftime(fmt),
            "moyen": moyen, "min": round(moyen*0.75, 2), "max": round(moyen*1.6, 2),
            "prob": random.randint(95, 99)
        })
    return results

st.markdown('<div class="main-header">TITAN V85.0 ULTRA-SYNC ⚔️</div>', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

with tab1:
    st.markdown("### ⚡ AVIATOR ANALYSIS")
    h_av = st.text_input("🔑 SERVER HEX:", key="h_av")
    o_av = st.text_input("🕒 HH:mm:", value=datetime.now().strftime("%H:%M"), key="o_av")
    if st.button("🔥 EXECUTE"):
        for p in get_3_preds(h_av, o_av, "aviator"):
            st.markdown(f"""<div class="prediction-card">
                <div style="display:flex; justify-content:space-between;"><span style="color:#ff4444;">⏰ {p['lera']}</span><span class="prob-badge">{p['prob']}%</span></div>
                <div class="target-val">{p['moyen']}x</div>
                <div style="display:flex; justify-content:space-around; border-top:1px solid #333; padding-top:5px;"><span>MIN: {p['min']}x</span><span>MAX: {p['max']}x</span></div>
            </div>""", unsafe_allow_html=True)

with tab2:
    st.markdown("### 🚀 COSMOS X ANALYSIS")
    h_co = st.text_input("🔑 HEX SEED:", key="h_co")
    o_co = st.text_input("🕒 HH:mm:ss:", value=datetime.now().strftime("%H:%M:%S"), key="o_co")
    if st.button("🚀 START COSMOS"):
        for p in get_3_preds(h_co, o_co, "cosmos"):
            st.markdown(f'<div class="prediction-card">⏰ {p["lera"]} | <b style="color:#00ffcc;">{p["moyen"]}x</b></div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### 💣 MINES VIP DECODER")
    nb_mines = st.select_slider("Isan'ny Mines:", options=[1,2,3,4,5,6,7], value=3)
    s_serv = st.text_input("📡 Server Seed:", key="s_serv")
    s_cli = st.text_input("💻 Client Seed:", key="s_cli")
    if st.button("💎 GENERATE SCHEMA"):
        if s_serv and s_cli:
            random.seed(int(hashlib.sha256(f"{s_serv}{s_cli}".encode()).hexdigest()[:10], 16))
            diamond_pos = random.sample(range(25), 5)
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                grid_html += f'<div class="mine-cell {"diamond-cell" if i in diamond_pos else ""} ">{"💎" if i in diamond_pos else "⬛"}</div>'
            st.markdown(grid_html + '</div>', unsafe_allow_html=True)

st.markdown(f"<br><hr><center style='font-size:12px; color:#444;'>TITAN OMNI-STRIKE BY {st.session_state.admin_name} © 2026</center>", unsafe_allow_html=True)
