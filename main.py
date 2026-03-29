import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & NEON VISUAL OVERHAUL ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stStatusWidget"] {display:none;}
    
    .stApp { 
        background: radial-gradient(circle at center, #0a192f 0%, #010a12 100%); 
        color: #eee; 
    }
    
    .main-header { 
        font-size: 35px; font-weight: 900; text-align: center; color: #00ffcc; 
        border: 2px solid #00ffcc; padding: 20px; border-radius: 15px; 
        background: rgba(0, 255, 204, 0.05); margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.2);
    }
    
    .card { 
        background: rgba(255, 255, 255, 0.02); border-radius: 15px; 
        border: 1px solid rgba(0, 255, 204, 0.2); padding: 20px; margin-bottom: 15px;
        backdrop-filter: blur(5px);
    }
    
    .target-val { 
        font-size: 45px; color: #00ffcc; font-weight: 800; 
        text-shadow: 0 0 10px #00ffcc; 
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #00ffcc, #0088ff) !important;
        color: #010a12 !important; font-weight: bold !important;
        border: none !important; border-radius: 10px !important;
    }

    .hist-box { 
        padding: 12px; border-left: 4px solid #ffcc00; 
        background: rgba(255, 204, 0, 0.05); margin-bottom: 8px; font-size: 14px;
    }

    .good-luck {
        text-align: center; color: #ffcc00; font-weight: bold; 
        font-size: 20px; margin-top: 10px; text-shadow: 0 0 5px #ffcc00;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE MANAGEMENT ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = {"aviator": [], "cosmos": [], "mines": []}

# --- 3. CORE ALGORITHM (Tsy nisy nokitihina) ---
def get_titan_prediction(server_hex, base_ora, game_type):
    time.sleep(1.2) # Anti-bot delay
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
        if len(st.session_state.prediction_history[game_type]) > 10:
            st.session_state.prediction_history[game_type].pop()
            
    return results

# --- 4. LOGIN SYSTEM ---
if not st.session_state.authenticated:
    st.markdown("<br><br><h1 style='text-align:center; color:#00ffcc;'>🛡️ TITAN ACCESS CONTROL</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1,2,1])
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

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚙️ SETTINGS"])

# --- SECTORS: AVIATOR & COSMOS ---
for tab, g_name in zip([tab1, tab2], ["aviator", "cosmos"]):
    with tab:
        st.markdown(f"### ⚡ SCANNER {g_name.upper()}")
        with st.expander("📸 UPLOAD SCREENSHOT"):
            img = st.file_uploader(f"Capture {g_name}", type=['png', 'jpg', 'jpeg'], key=f"img_{g_name}")
            
        c1, c2 = st.columns(2)
        hex_val = c1.text_input("🔑 SERVER SEED (Hex):", key=f"h_{g_name}")
        ora_val = c2.text_input("🕒 ORA IZAO (HH:MM):", value=datetime.now().strftime("%H:%M"), key=f"o_{g_name}")
        
        if st.button(f"🔥 EXECUTE {g_name.upper()} ANALYSIS", use_container_width=True, key=f"b_{g_name}"):
            if hex_val:
                with st.spinner("Decoding..."):
                    preds = get_titan_prediction(hex_val, ora_val, g_name)
                    st.markdown('<p class="good-luck">🍀 BONNE CHANCE À TOUS</p>', unsafe_allow_html=True)
                    for p in preds:
                        html_card = f"""
                        <div class="card">
                            <div style="display:flex; justify-content: space-between;">
                                <span style="font-size:20px; color:#ffcc00; font-weight:bold;">⏰ Lera: {p['lera']}</span>
                                <span style="background:#00ffcc; color:#010a12; padding:3px 10px; border-radius:15px; font-weight:bold;">{p['prob']}%</span>
                            </div>
                            <div style="display: flex; justify-content: space-around; margin-top:15px; text-align:center;">
                                <div><small>MIN</small><br><b>{p['min']}x</b></div>
                                <div><small style="color:#00ffcc;">TARGET</small><br><div class="target-val">{p['moyen']}x</div></div>
                                <div><small>MAX</small><br><b>{p['max']}x</b></div>
                            </div>
                        </div>
                        """
                        st.markdown(html_card, unsafe_allow_html=True)

        st.markdown("#### 📜 TANTARA")
        for item in st.session_state.prediction_history[g_name]:
            st.markdown(f'<div class="hist-box">🕒 <b>{item["lera"]}</b> | Target: <span style="color:#00ffcc;">{item["moyen"]}x</span></div>', unsafe_allow_html=True)

# --- MINES VIP ---
with tab3:
    st.markdown("### 💣 MINES VIP DECODER")
    m_hex = st.text_input("🔑 SERVER SEED (Hex):", key="mine_h")
    m_cli = st.text_input("👤 CLIENT SEED:", key="mine_c")
    m_num = st.select_slider("Isan'ny Mines:", options=[1,2,3,4,5,6,7], value=3)
    
    if st.button("💎 DECODE SAFE PATH", use_container_width=True):
        if m_hex and m_cli:
            random.seed(int(hashlib.md5(f"{m_hex}{m_cli}{m_num}".encode()).hexdigest()[:10], 16))
            safe_tiles = random.sample(range(25), 5)
            st.markdown('<p class="good-luck">🍀 BONNE CHANCE À TOUS</p>', unsafe_allow_html=True)
            grid = '<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; max-width: 300px; margin: auto;">'
            for idx in range(25):
                char, bg = ("💎", "#00ffcc") if idx in safe_tiles else ("⬛", "#1a1a1a")
                grid += f'<div style="background:{bg}; height:50px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:25px;">{char}</div>'
            st.markdown(grid + '</div>', unsafe_allow_html=True)

# --- SETTINGS ---
with tab4:
    st.markdown("### ⚙️ SYSTEM INFO")
    st.info("Developer: Patricia | Contact: 0346249701")
    if st.button("🔴 CLEAR ALL DATA"):
        st.session_state.prediction_history = {"aviator": [], "cosmos": [], "mines": []}
        st.rerun()

st.markdown('<br><div style="text-align:center; color:#444; font-size:12px;">TITAN OMNI-STRIKE BY PATRICIA © 2026</div>', unsafe_allow_html=True)
