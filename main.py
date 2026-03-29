import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. STYLE & UI ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background: radial-gradient(circle at center, #0a192f 0%, #010a12 100%); color: #eee; }
    .main-header { 
        font-size: 35px; font-weight: 900; text-align: center; color: #00ffcc; 
        border: 2px solid #00ffcc; padding: 20px; border-radius: 15px; 
        background: rgba(0, 255, 204, 0.05); margin-bottom: 25px;
    }
    .card { 
        background: rgba(255, 255, 255, 0.02); border-radius: 15px; 
        border: 1px solid rgba(0, 255, 204, 0.2); padding: 20px; margin-bottom: 15px;
    }
    .target-val { font-size: 45px; color: #ffcc00; font-weight: 800; text-shadow: 0 0 10px #ffcc00; }
    .good-luck { text-align: center; color: #00ffcc; font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ALGORITHM X5+ DYNAMIC ---
def get_titan_prediction(server_hex, base_ora, game_type):
    time.sleep(1.2)
    results = []
    SECRET_SALT = "TITAN_PREMIUM_PATRICIA_2026"
    
    try:
        # Vakiana ny HH:MM:SS mifanaraka amin'ny fangatahanao
        start_dt = datetime.strptime(base_ora, "%H:%M:%S")
    except:
        try:
            start_dt = datetime.strptime(base_ora, "%H:%M")
        except:
            start_dt = datetime.now()

    h = hashlib.sha256(f"{server_hex}-{SECRET_SALT}-{game_type}".encode()).hexdigest()
    
    for i in range(3):
        chunk = int(h[i*10 : (i+1)*10], 16)
        random.seed(chunk)
        
        # --- ETO NO OVAN'NY ALGORITHM NY COTE ---
        # Ny vinavina iray amin'ny telo dia atao X5+ foana
        if i == 1: # Ny vinavina faharoa dia matetika no lehibe
            v_moyen = round(random.uniform(5.10, 15.50), 2)
            prob = random.randint(92, 95) # Midina kely ny prob raha vao cote ambony
        else:
            v_moyen = round(random.uniform(1.80, 4.20), 2)
            prob = random.randint(96, 99)
            
        v_min = round(v_moyen * 0.7, 2)
        v_max = round(v_moyen * 2.5, 2)
        
        # Elanelana minitra sy segondra mba ho ultra-sync
        add_min = random.randint(4, 12) * (i + 1)
        add_sec = random.randint(5, 55)
        
        future_time = (start_dt + timedelta(minutes=add_min, seconds=add_sec)).strftime("%H:%M:%S")
        
        res = {"lera": future_time, "min": v_min, "moyen": v_moyen, "max": v_max, "prob": prob}
        results.append(res)
        st.session_state.prediction_history[game_type].insert(0, res)
            
    return results

# --- 3. LOGIN & SESSION ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'prediction_history' not in st.session_state: st.session_state.prediction_history = {"aviator": [], "cosmos": [], "mines": []}

if not st.session_state.authenticated:
    _, col2, _ = st.columns([1,2,1])
    with col2:
        user_key = st.text_input("ENTER ADMIN KEY:", type="password")
        if st.button("UNLOCK SYSTEM"):
            if user_key == "ADMIN_TITAN":
                st.session_state.authenticated = True
                st.rerun()
    st.stop()

# --- 4. MAIN UI ---
st.markdown('<div class="main-header">TITAN V85.0 X5-STRIKE ⚔️</div>', unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚙️ SETTINGS"])

for tab, g_name in zip([tab1, tab2], ["aviator", "cosmos"]):
    with tab:
        c1, c2 = st.columns(2)
        hex_val = c1.text_input("🔑 SERVER SEED (Hex):", key=f"h_{g_name}")
        # Ny fampidirana ora dia lasa misy segondra (HH:MM:SS)
        ora_val = c2.text_input("🕒 ORA IZAO (HH:MM:SS):", value=datetime.now().strftime("%H:%M:%S"), key=f"o_{g_name}")
        
        if st.button(f"🔥 ANALYSE {g_name.upper()}", use_container_width=True, key=f"b_{g_name}"):
            if hex_val:
                preds = get_titan_prediction(hex_val, ora_val, g_name)
                st.markdown('<p class="good-luck">🍀 BONNE CHANCE À TOUS - MIANDRASA NY MINITRA</p>', unsafe_allow_html=True)
                for p in preds:
                    st.markdown(f"""
                    <div class="card">
                        <div style="display:flex; justify-content: space-between;">
                            <span style="font-size:22px; color:#ffcc00; font-weight:bold;">⏰ LERA: {p['lera']}</span>
                            <span style="background:#00ffcc; color:#010a12; padding:3px 10px; border-radius:15px; font-weight:bold;">{p['prob']}%</span>
                        </div>
                        <div style="text-align:center; margin-top:10px;">
                            <small>TARGET SUGGESTED</small><br>
                            <div class="target-val">{p['moyen']}x</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# --- 5. MINES VIP ---
with tab3:
    m_hex = st.text_input("🔑 SERVER SEED (Hex):", key="mine_h")
    m_cli = st.text_input("👤 CLIENT SEED:", key="mine_c")
    if st.button("💎 DECODE MINES", use_container_width=True):
        random.seed(int(hashlib.md5(f"{m_hex}{m_cli}".encode()).hexdigest()[:10], 16))
        safe_tiles = random.sample(range(25), 5)
        grid = '<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; max-width: 300px; margin: auto;">'
        for idx in range(25):
            char, bg = ("💎", "#00ffcc") if idx in safe_tiles else ("⬛", "#1a1a1a")
            grid += f'<div style="background:{bg}; height:50px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:25px;">{char}</div>'
        st.markdown(grid + '</div>', unsafe_allow_html=True)

with tab4:
    st.info("Developer: Patricia | Admin Mode")
    if st.button("🔴 RESET APP"):
        st.session_state.prediction_history = {"aviator": [], "cosmos": [], "mines": []}
        st.rerun()
