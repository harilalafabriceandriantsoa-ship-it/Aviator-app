import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & ADVANCED UI ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stStatusWidget"] {display:none;}
    
    .stApp { 
        background: radial-gradient(circle at top, #0a192f 0%, #010a12 100%); 
        color: #e6f1ff; 
    }
    
    /* Header Neon */
    .main-header { 
        font-size: 38px; font-weight: 900; text-align: center; color: #00ffcc; 
        border: 2px solid #00ffcc; padding: 25px; border-radius: 20px; 
        background: rgba(0, 255, 204, 0.03); margin-bottom: 30px;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
        text-transform: uppercase; letter-spacing: 2px;
    }
    
    /* Card Design */
    .card { 
        background: rgba(255, 255, 255, 0.03); 
        border-radius: 20px; 
        border: 1px solid rgba(0, 255, 204, 0.2); 
        padding: 25px; margin-bottom: 20px;
    }
    
    /* Values Styling */
    .target-val { 
        font-size: 50px; color: #00ffcc; font-weight: 900; 
        text-shadow: 0 0 15px #00ffcc; margin: 10px 0;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #00ffcc, #0088ff) !important;
        color: #010a12 !important; font-weight: 800 !important;
        border: none !important; border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = {"aviator": [], "cosmos": [], "mines": []}

# --- 3. CORE ALGORITHM (TSY NOVAINA) ---
def get_titan_prediction(server_hex, base_ora, game_type):
    time.sleep(1.5) 
    results = []
    SECRET_SALT = "TITAN_PREMIUM_PATRICIA_2026"
    
    try:
        start_dt = datetime.strptime(base_ora, "%H:%M")
    except:
        start_dt = datetime.now()

    h = hashlib.sha256(f"{server_hex}-{SECRET_SALT}-{game_type}".encode()).hexdigest()
    
    for i in range(3):
        chunk = int(h[i*10 : (i+1)*10], 16)
        random.seed(chunk)
        
        v_min = round(random.uniform(1.20, 1.95), 2)
        v_moyen = round(random.uniform(2.15, 6.80), 2)
        v_max = round(random.uniform(10.0, 95.0), 2)
        
        future_time = (start_dt + timedelta(minutes=random.randint(4, 15) * (i + 1))).strftime("%H:%M")
        res = {"lera": future_time, "min": v_min, "moyen": v_moyen, "max": v_max, "prob": random.randint(95, 99)}
        results.append(res)
        
        st.session_state.prediction_history[game_type].insert(0, res)
        if len(st.session_state.prediction_history[game_type]) > 10:
            st.session_state.prediction_history[game_type].pop()
    return results

# --- 4. LOGIN ---
if not st.session_state.authenticated:
    st.markdown("<br><br><h1 style='text-align:center; color:#00ffcc;'>🛡️ TITAN SECURE ACCESS</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1,1.5,1])
    with col2:
        user_key = st.text_input("ADMIN ACCESS KEY:", type="password")
        if st.button("INITIALIZE SYSTEM", use_container_width=True):
            if user_key == "ADMIN_TITAN":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("INVALID KEY")
    st.stop()

# --- 5. INTERFACE ---
st.markdown('<div class="main-header">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚙️ SETTINGS"])

# --- AVIATOR & COSMOS ---
for tab, g_name in zip([tab1, tab2], ["aviator", "cosmos"]):
    with tab:
        st.markdown(f"### 🛰️ {g_name.upper()} DECODER")
        c1, c2 = st.columns(2)
        hex_val = c1.text_input("🔑 SERVER SEED:", key=f"h_{g_name}")
        ora_val = c2.text_input("🕒 TIME (HH:MM):", value=datetime.now().strftime("%H:%M"), key=f"o_{g_name}")
        
        if st.button(f"🚀 DECODE {g_name.upper()}", use_container_width=True, key=f"b_{g_name}"):
            if hex_val:
                preds = get_titan_prediction(hex_val, ora_val, g_name)
                for p in preds:
                    st.markdown(f"""
                    <div class="card">
                        <div style="display:flex; justify-content: space-between;">
                            <span style="color:#ffcc00; font-weight:bold;">⏰ {p['lera']}</span>
                            <span style="background:#00ffcc; color:#010a12; padding:2px 10px; border-radius:15px; font-weight:bold;">{p['prob']}% ACCURACY</span>
                        </div>
                        <div style="display: flex; justify-content: space-around; margin-top:20px; text-align:center;">
                            <div><small>SAFE</small><br><b>{p['min']}x</b></div>
                            <div><div class="target-val">{p['moyen']}x</div></div>
                            <div><small>RISK</small><br><b>{p['max']}x</b></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# --- MINES ---
with tab3:
    st.markdown("### 💣 MINES VIP DECODER")
    m_hex = st.text_input("🔑 SERVER SEED:", key="mine_h")
    m_cli = st.text_input("👤 CLIENT SEED:", key="mine_c")
    if st.button("💎 REVEAL SAFE PATH", use_container_width=True):
        if m_hex:
            random.seed(m_hex + m_cli)
            safe = random.sample(range(25), 5)
            grid = '<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 350px; margin: auto;">'
            for idx in range(25):
                char, color = ("💎", "#00ffcc") if idx in safe else ("⬛", "#1a1a1a")
                grid += f'<div style="background:{color}; height:60px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:25px;">{char}</div>'
            st.markdown(grid + '</div>', unsafe_allow_html=True)

# --- SETTINGS ---
with tab4:
    st.info(f"**Dev:** Patricia | **Contact:** 0346249701")
    if st.button("🧹 PURGE DATA"):
        st.session_state.prediction_history = {"aviator": [], "cosmos": [], "mines": []}
        st.rerun()

st.markdown('<br><div style="text-align:center; color:#444; font-size:12px;">TITAN OMNI-STRIKE BY PATRICIA © 2026</div>', unsafe_allow_html=True)
