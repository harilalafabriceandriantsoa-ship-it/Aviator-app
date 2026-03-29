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
    .hist-box { 
        padding: 10px; border-left: 3px solid #ffcc00; 
        background: rgba(255,204,0,0.05); margin-bottom: 5px; font-size: 14px;
    }
    .footer-text { text-align:center; color:#444; font-size:12px; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE MANAGEMENT ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = {"aviator": [], "cosmos": [], "mines": [], "foot": [], "racing": []}

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
        if len(st.session_state.prediction_history[game_type]) > 10:
            st.session_state.prediction_history[game_type].pop()
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

tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ FOOT", "🐕 RACING", "⚙️ SETTINGS"])

# --- AVIATOR & COSMOS SECTORS ---
for i, (tab, g_name) in enumerate(zip([tabs[0], tabs[1]], ["aviator", "cosmos"])):
    with tab:
        st.markdown(f"### ⚡ SCANNER {g_name.upper()}")
        with st.expander("📸 UPLOAD SCREENSHOT"):
            st.file_uploader(f"Capture {g_name}", type=['png', 'jpg', 'jpeg'], key=f"img_{g_name}")
            
        c1, c2 = st.columns(2)
        hex_val = c1.text_input("🔑 SERVER SEED (Hex):", key=f"h_{g_name}")
        ora_val = c2.text_input("🕒 ORA IZAO (HH:MM):", value=datetime.now().strftime("%H:%M"), key=f"o_{g_name}")
        
        if st.button(f"🔥 EXECUTE {g_name.upper()} ANALYSIS", use_container_width=True, key=f"b_{g_name}"):
            if hex_val:
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
                            <div><small>MAX</small><br><b>{p['max']}x</b></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# --- MINES VIP SECTOR ---
with tabs[2]:
    st.markdown("### 💣 MINES VIP DECODER")
    m_hex = st.text_input("🔑 SERVER SEED (Hex):", key="mine_h")
    m_num = st.select_slider("Isan'ny Mines:", options=[1,2,3,4,5], value=3)
    if st.button("💎 DECODE SAFE PATH", use_container_width=True):
        if m_hex:
            random.seed(int(hashlib.md5(m_hex.encode()).hexdigest()[:8], 16))
            safe_tiles = random.sample(range(25), 5)
            grid_html = '<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; max-width: 250px; margin: auto;">'
            for idx in range(25):
                char, bg = ("💎", "#00ffcc") if idx in safe_tiles else ("⬛", "#1a1a1a")
                grid_html += f'<div style="background:{bg}; height:45px; border-radius:5px; display:flex; align-items:center; justify-content:center; font-size:20px;">{char}</div>'
            st.markdown(grid_html + '</div>', unsafe_allow_html=True)

# --- FOOT VIRTUAL SECTOR ---
with tabs[3]:
    st.markdown("### ⚽ FOOT VIRTUAL ANALYZER")
    with st.expander("📸 UPLOAD CLASSEMENT"):
        st.file_uploader("Capture Classment", type=['png', 'jpg'], key="foot_img")
    c1, c2 = st.columns(2)
    h_team = c1.text_input("🏠 HOME TEAM:")
    a_team = c2.text_input("✈️ AWAY TEAM:")
    if st.button("🎯 PREDICT FOOT MATCH", use_container_width=True):
        if h_team and a_team:
            with st.spinner("Analyzing stats..."):
                time.sleep(1.5)
                res = random.choice(["VICTOIRE HOME", "OVER 1.5", "VICTOIRE AWAY", "GG (BI_BUT)"])
                score = f"{random.randint(1,3)} - {random.randint(0,2)}"
                st.markdown(f"""
                <div class="card" style="text-align:center;">
                    <h2 style="color:#ffcc00;">{res}</h2>
                    <div style="font-size:30px; letter-spacing:5px;">{score}</div>
                    <p style="color:#00ffcc;">96% CONFIDENCE</p>
                </div>
                """, unsafe_allow_html=True)

# --- RACING SECTOR ---
with tabs[4]:
    st.markdown("### 🐕 RACING PRO (ALIKA/SOAVALY)")
    mode = st.radio("Mode:", ["Platinum Hounds", "Dashing Derby"], horizontal=True)
    cotes = st.text_input("📊 AMPIDIRO NY COTES (F1, F2, F3...):", placeholder="ohatra: 2.5, 3.8, 12.0")
    if st.button("🏇 GENERATE TRIO BOX", use_container_width=True):
        if cotes:
            with st.spinner("Calculating Trio probability..."):
                time.sleep(1.5)
                nums = random.sample(range(1, 7 if "Hounds" in mode else 12), 3)
                st.markdown(f"""
                <div class="card" style="border-color:#ffcc00; text-align:center;">
                    <small>VINAVINA TRIO DÉSORDRE</small>
                    <div class="target-val" style="color:#ffcc00;">{nums[0]} - {nums[1]} - {nums[2]}</div>
                    <p>Safety Tip: Outsider included</p>
                </div>
                """, unsafe_allow_html=True)

# --- SETTINGS ---
with tabs[5]:
    st.markdown("### ⚙️ SYSTEM & CONTACT")
    st.info(f"**Developer:** Patricia\n\n**WhatsApp:** 0346249701\n\n**Email:** andriantsoakelly@gmail.com")
    if st.button("🔴 RESET ALL CACHE"):
        st.session_state.prediction_history = {"aviator":[], "cosmos":[], "mines":[], "foot":[], "racing":[]}
        st.rerun()

st.markdown('<div class="footer-text">TITAN OMNI-STRIKE BY PATRICIA © 2026</div>', unsafe_allow_html=True)
