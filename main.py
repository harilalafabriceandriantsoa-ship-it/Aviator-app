import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & NEON VISUAL OVERHAUL ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

st.markdown("""
    <style>
    /* Hiding elements for professional look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stStatusWidget"] {display:none;}
    
    /* Global Background */
    .stApp { 
        background: radial-gradient(circle at center, #0a192f 0%, #010a12 100%); 
        color: #e6f1ff; 
    }
    
    /* Futuristic Header */
    .main-header { 
        font-size: 40px; font-weight: 900; text-align: center; color: #00ffcc; 
        border: 2px solid #00ffcc; padding: 25px; border-radius: 20px; 
        background: rgba(0, 255, 204, 0.05); margin-bottom: 30px;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.3), inset 0 0 10px rgba(0, 255, 204, 0.1);
        text-transform: uppercase; letter-spacing: 3px;
    }
    
    /* Neon Cards */
    .card { 
        background: rgba(255, 255, 255, 0.02); border-radius: 20px; 
        border: 1px solid rgba(0, 255, 204, 0.2); padding: 25px; margin-bottom: 20px;
        backdrop-filter: blur(10px); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        transition: 0.3s ease-in-out;
    }
    .card:hover { border-color: #00ffcc; box-shadow: 0 0 15px rgba(0, 255, 204, 0.2); }
    
    /* Prediction Values */
    .target-val { 
        font-size: 55px; color: #00ffcc; font-weight: 900; 
        text-shadow: 0 0 15px #00ffcc; margin: 10px 0;
    }
    
    /* Buttons Styling */
    .stButton>button {
        background: linear-gradient(45deg, #00ffcc, #0088ff) !important;
        color: #010a12 !important; font-weight: 800 !important;
        border: none !important; border-radius: 12px !important;
        padding: 12px 30px !important; transition: 0.3s !important;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0, 255, 204, 0.4); }
    
    /* History Boxes */
    .hist-box { 
        padding: 15px; border-left: 5px solid #ffcc00; 
        background: rgba(255, 204, 0, 0.03); margin-bottom: 10px; 
        border-radius: 0 15px 15px 0; font-size: 15px;
    }
    
    /* Tabs custom color */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px 10px 0 0; color: #eee;
    }
    .stTabs [aria-selected="true"] { background-color: rgba(0,255,204,0.2) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE MANAGEMENT ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = {"aviator": [], "cosmos": [], "mines": []}

# --- 3. CORE ALGORITHM (Tsy nikitika litera) ---
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
    st.markdown("<br><br><h1 style='text-align:center; color:#00ffcc; text-shadow: 0 0 10px #00ffcc;'>🛡️ TITAN ACCESS CONTROL</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        user_key = st.text_input("ENTER ADMIN KEY:", type="password")
        if st.button("UNLOCK SYSTEM", use_container_width=True):
            if user_key == "ADMIN_TITAN":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid Key. Access Denied.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 5. MAIN INTERFACE ---
st.markdown('<div class="main-header">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚙️ SETTINGS"])

# --- SECTORS: AVIATOR & COSMOS ---
for tab, g_name in zip([tab1, tab2], ["aviator", "cosmos"]):
    with tab:
        st.markdown(f"### 🛰️ {g_name.upper()} DECODER")
        
        with st.expander("📸 UPLOAD SCANNER"):
            img = st.file_uploader(f"Capture {g_name}", type=['png', 'jpg', 'jpeg'], key=f"img_{g_name}")
            if img: st.image(img)
            
        c1, c2 = st.columns(2)
        hex_val = c1.text_input("🔑 SERVER SEED (Hex):", placeholder="Paste seed here...", key=f"h_{g_name
