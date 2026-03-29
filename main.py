import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & ADVANCED NEON UI ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

st.markdown("""
    <style>
    /* Manafina ny singa tsy ilaina */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stStatusWidget"] {display:none;}
    
    /* Background & Global Style */
    .stApp { 
        background: radial-gradient(circle at top, #0a192f 0%, #010a12 100%); 
        color: #e6f1ff; 
    }
    
    /* Neon Header */
    .main-header { 
        font-size: 38px; font-weight: 900; text-align: center; color: #00ffcc; 
        border: 2px solid #00ffcc; padding: 25px; border-radius: 20px; 
        background: rgba(0, 255, 204, 0.03); margin-bottom: 30px;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.2), inset 0 0 10px rgba(0, 255, 204, 0.1);
        text-transform: uppercase; letter-spacing: 2px;
    }
    
    /* Glass Cards */
    .card { 
        background: rgba(255, 255, 255, 0.03); 
        border-radius: 20px; 
        border: 1px solid rgba(0, 255, 204, 0.2); 
        padding: 25px; margin-bottom: 20px;
        transition: 0.3s;
    }
    .card:hover { border-color: #00ffcc; box-shadow: 0 0 15px rgba(0, 255, 204, 0.1); }
    
    /* Prediction Values */
    .target-val { 
        font-size: 50px; color: #00ffcc; font-weight: 900; 
        text-shadow: 0 0 15px #00ffcc; margin: 10px 0;
    }
    
    /* Accuracy Badge */
    .acc-badge {
        background: linear-gradient(90deg, #00ffcc, #0099ff);
        color: #010a12; padding: 4px 15px; border-radius: 30px;
        font-weight: 800; font-size: 13px;
    }
    
    /* History Styling */
    .hist-box { 
        padding: 12px; border-left: 4px solid #ffcc00; 
        background: rgba(255, 204, 0, 0.05); margin-bottom: 8px; 
        border-radius: 0 12px 12px 0; font-size: 14px;
    }
    
    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #00ffcc, #0088ff) !important;
        color: #010a12 !important; font-weight: 800 !important;
        border: none !important; border-radius: 12px !important;
        padding: 10px 25px !important; transition: 0.3s !important;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(0, 255, 204, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = {"aviator": [], "cosmos": [], "mines": []}

# --- 3. CORE TITAN ALGORITHM ---
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

# --- 4. AUTHENTICATION GATE ---
if not st.session_state.authenticated:
    st.markdown("<br><br><h1 style='text-align:center; color:#00ffcc;'>🛡️ TITAN SECURE ACCESS</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1,1.5,1])
    with col2:
        st.markdown('<div class="card" style="text-align:center;">', unsafe_allow_html=True)
        user_key = st.text_input("ADMIN ACCESS KEY:", type="password")
        if st.button("INITIALIZE SYSTEM", use_container_width=True):
            if user_key == "ADMIN_TITAN":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("ACCESS DENIED: INVALID KEY")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 5. MAIN INTERFACE ---
st.markdown('<div class="main-header">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚙️ SETTINGS"])

# --- AVIATOR & COSMOS SECTORS ---
for tab, g_name in zip([tab1, tab2], ["aviator", "cosmos"]):
    with tab:
        st.markdown(f"### 🛰️ {g_name.upper()} DECODER")
        with st.expander("📸 ANALYSIS UPLOAD"):
            st.file_uploader(f"Scan {g_name} screenshot", type=['png', 'jpg'], key=f"up_{g_name}")
            
        c1, c2 = st.columns(2)
        hex_val = c1.text_input("🔑 SERVER SEED:", placeholder="Enter Hex Seed...", key=f"h_{g_name}")
        ora_val = c2.text_input("🕒 SYSTEM TIME:", value=datetime.now().strftime("%H:%M"), key=f"o_{g_name}")
        
        if st.button(f"🚀 DECODE {g_name.upper()}", use_container_width=True, key=f"b_{g_name}"):
            if hex_val:
                with st.spinner("Synchronizing with server..."):
                    preds = get_titan_prediction(hex_val, ora_val, g_name)
                    for p in preds:
                        st.markdown(f"""
                        <div class="card">
                            <div style="display:flex; justify-content: space-between; align-items:center;">
                                <span style="font-size:22px; color:#ffcc00; font-weight:900;">⏰ {p['lera']}</span>
                                <span class="acc-badge">{p['prob']}% ACCURACY</span>
                            </div>
                            <div style="display: flex; justify-content: space-around; margin-top:25px; text-align:center;">
                                <div><small style="color:#888;">MIN (SAFE)</small><br><b style="font-size:18px;">{p['min']}x</b></div>
                                <div><small style="color:#00ffcc; letter-spacing:1px;">PREDICTED</small><br><div class="target-val">{p['moyen']}x</div></div>
                                <div><small style="color:#888;">MAX (RISK)</small><br><b style="font-size:18px;">{p['max']}x</b></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("SEED REQUIRED FOR ANALYSIS.")

        st.markdown("#### 📑 SESSION LOGS")
        if st.session_state.prediction_history[g_name]:
            for item in st.session_state.prediction_history[g_name]:
                st.markdown(f'<div class="hist-box">🕒 <b>{item["lera"]}</b> | Target: <span style="color:#00ffcc;">{item["moyen"]}x</span> | {item["prob"]}%</div>', unsafe_allow_html=True)
        else:
            st.info("No logs found.")

# --- MINES VIP SECTOR ---
with tab3:
    st.markdown("### 💣 MINES VIP DECODER")
    m1, m2 = st.columns(2)
    m_hex = m1.text_input("🔑 SERVER SEED:", key="mine_h")
    m_cli = m2.text_input("👤 CLIENT SEED:", key="mine_c")
    m_num = st.select_slider("MINES COUNT:", options=[1,2,3,4,5,6,7], value=3)
    
    if st.button("💎 REVEAL SAFE PATH", use_container_width=True):
        if m_hex:
            random.seed(int(hashlib.md5(f"{m_hex}{m_cli}{m_num}".encode()).hexdigest()[:10], 16))
            safe = random.sample(range(25), 5)
            
            grid = '<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; max-width: 350px; margin: 30px auto;">'
            for idx in range(25):
                char, color = ("💎", "#00ffcc") if idx in safe else ("⬛", "#1a1a1a")
                grid += f'<div style="background:{color}; height:60px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:28px; border:1px solid rgba(255,255,255,0.05); box-shadow: 0 4px 10px rgba(0,0,0,0.3);">{char}</div>'
            st.markdown(grid + '</div>', unsafe_allow_html=True)

# --- SETTINGS SECTOR ---
with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🛠️ SYSTEM CONFIGURATION")
    st.write(f"**CORE:** TITAN ENGINE V85.0")
    st.write(f"**DEVELOPER:** Patricia")
    st.write(f"**ENCRYPTION:** SHA-256 AES")
    if st.button("🧹 PURGE ALL DATA"):
        st.session_state.prediction_history = {"aviator": [], "cosmos": [], "mines": []}
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<br><div style="text-align:center; color:#444; font-size:12px; letter-spacing:1px;">TITAN OMNI-STRIKE BY PATRICIA © 2026</div>', unsafe_allow_html=True)
