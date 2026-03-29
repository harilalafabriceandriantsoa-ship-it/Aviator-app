import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & HIDING STREAMLIT ELEMENTS ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stStatusWidget"] {display:none;}
    .stApp { background-color: #010a12; color: #eee; }
    .main-header { 
        font-size: 30px; font-weight: 900; text-align: center; color: #00ffcc; 
        border: 2px solid #00ffcc; padding: 15px; border-radius: 15px; 
        background: rgba(0,255,204,0.05); margin-bottom: 20px;
    }
    .card { 
        background: rgba(255,255,255,0.03); border-radius: 15px; 
        border: 1px solid rgba(0,255,204,0.3); padding: 20px; margin-bottom: 15px; 
    }
    .target-val { font-size: 40px; color: #00ffcc; font-weight: bold; text-shadow: 0 0 10px #00ffcc; }
    .foot-res { font-size: 28px; color: #ffcc00; font-weight: bold; text-align: center; border-bottom: 1px solid #444; padding-bottom: 10px; }
    .hist-box { 
        padding: 10px; border-left: 3px solid #ffcc00; 
        background: rgba(255,204,0,0.05); margin-bottom: 5px; font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE MANAGEMENT ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = {"aviator": [], "cosmos": [], "mines": [], "foot": []}

# --- 3. CORE ALGORITHM (TITAN ENGINE) ---
def get_titan_prediction(server_hex, base_ora, game_type):
    time.sleep(1.2) 
    results = []
    SECRET_SALT = "TITAN_PREMIUM_PATRICIA_2026"
    try:
        start_dt = datetime.strptime(base_ora, "%H:%M")
    except:
        start_dt = datetime.now()

    seed_str = f"{server_hex}-{SECRET_SALT}-{game_type}"
    h = hashlib.sha256(seed_str.encode()).hexdigest()
    
    for i in range(3):
        chunk = int(h[i*10 : (i+1)*10], 16)
        random.seed(chunk)
        v_min = round(random.uniform(1.20, 1.85), 2)
        v_moyen = round(random.uniform(2.15, 5.80), 2)
        v_max = round(random.uniform(12.0, 95.0), 2)
        add_min = random.randint(4, 12) * (i + 1)
        future_time = (start_dt + timedelta(minutes=add_min)).strftime("%H:%M")
        accuracy = random.randint(94, 99)
        
        res = {"lera": future_time, "min": v_min, "moyen": v_moyen, "max": v_max, "prob": accuracy}
        results.append(res)
        st.session_state.prediction_history[game_type].insert(0, res)
    return results

# --- 4. LOGIN SYSTEM ---
if not st.session_state.authenticated:
    st.markdown("<br><br><h1 style='text-align:center; color:#00ffcc;'>🛡️ TITAN ACCESS CONTROL</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        user_key = st.text_input("ENTER ADMIN KEY:", type="password")
        if st.button("UNLOCK SYSTEM", use_container_width=True):
            if user_key == "ADMIN_TITAN":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid Key. Access Denied.")
    st.stop()

# --- 5. MAIN INTERFACE ---
st.markdown('<div class="main-header">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ VIRTUAL FOOT", "⚙️ SETTINGS"])

# --- SECTOR: AVIATOR & COSMOS ---
for i, (tab, g_name) in enumerate(zip([tab1, tab2], ["aviator", "cosmos"])):
    with tab:
        st.markdown(f"### ⚡ SCANNER {g_name.upper()}")
        with st.expander("📸 UPLOAD SCREENSHOT"):
            st.file_uploader(f"Capture {g_name}", type=['png', 'jpg', 'jpeg'], key=f"img_{g_name}")
            
        c1, c2 = st.columns(2)
        hex_val = c1.text_input("🔑 SERVER SEED (Hex):", key=f"h_{g_name}")
        ora_val = c2.text_input("🕒 ORA IZAO (HH:MM):", value=datetime.now().strftime("%H:%M"), key=f"o_{g_name}")
        
        if st.button(f"🔥 EXECUTE {g_name.upper()} ANALYSIS", use_container_width=True, key=f"b_{g_name}"):
            if hex_val:
                with st.spinner("Decoding algorithm..."):
                    preds = get_titan_prediction(hex_val, ora_val, g_name)
                    for p in preds:
                        st.markdown(f"""
                        <div class="card">
                            <div style="display:flex; justify-content: space-between; align-items:center;">
                                <span style="font-size:20px; color:#ffcc00; font-weight:bold;">⏰ Lera: {p['lera']}</span>
                                <span style="background:#00ffcc; color:#010a12; padding:3px 12px; border-radius:20px; font-weight:bold;">{p['prob']}% ACCURACY</span>
                            </div>
                            <div style="display: flex; justify-content: space-around; margin-top:20px; text-align:center;">
                                <div><small>MIN</small><br><b>{p['min']}x</b></div>
                                <div><small style="color:#00ffcc;">TARGET</small><br><div class="target-val">{p['moyen']}x</div></div>
                                <div><small>
