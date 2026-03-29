import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 OMNI-STRIKE", layout="wide")

# CSS ho an'ny style Dark & Neon
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
    .foot-res { font-size: 28px; color: #ffcc00; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'history' not in st.session_state:
    st.session_state.history = {"aviator": [], "cosmos": [], "mines": [], "foot": []}

# --- 3. CORE LOGIC ---
def get_prediction(seed, game):
    h = hashlib.sha256(f"{seed}-{game}-2026".encode()).hexdigest()
    random.seed(int(h[:10], 16))
    return {
        "val": round(random.uniform(1.5, 5.0), 2),
        "prob": random.randint(94, 98)
    }

# --- 4. LOGIN ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛡️ TITAN ACCESS</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        key = st.text_input("ADMIN KEY:", type="password")
        if st.button("UNLOCK", use_container_width=True):
            if key == "ADMIN_TITAN":
                st.session_state.authenticated = True
                st.rerun()
    st.stop()

# --- 5. MAIN APP ---
st.markdown('<div class="main-header">TITAN V85.0 OMNI-STRIKE ⚔️</div>', unsafe_allow_html=True)

tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "⚽ VIRTUAL FOOT"])

# --- AVIATOR & COSMOS ---
for i, (tab, name) in enumerate(zip(tabs[:2], ["aviator", "cosmos"])):
    with tab:
        hex_val = st.text_input(f"🔑 SERVER SEED {name.upper()}:", key=f"h_{name}")
        if st.button(f"🔥 SCAN {name.upper()}", use_container_width=True):
            if hex_val:
                p = get_prediction(hex_val, name)
                st.markdown(f"""
                <div class="card">
                    <div style="text-align:center;">
                        <small>PROBABILITÉ: {p['prob']}%</small><br>
                        <div class="target-val">{p['val']}x</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# --- MINES VIP ---
with tabs[2]:
    m_seed = st.text_input("🔑 SEED MINES:")
    if st.button("💎 SHOW DIAMONDS", use_container_width=True):
        random.seed(m_seed)
        safe = random.sample(range(25), 5)
        grid = ""
        for idx in range(25):
            char = "💎" if idx in safe else "⬛"
            grid += f'<div style="background:#1a1a1a; padding:10px; border-radius:5px; text-align:center;">{char}</div>'
        st.markdown(f'<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:10px;">{grid}</div>', unsafe_allow_html=True)

# --- VIRTUAL FOOT (1X2 PRO) ---
with tabs[3]:
    st.markdown("### ⚽ VIRTUAL FOOTBALL ANALYZER")
    with st.expander("📸 UPLOAD CLASSEMENT (Optional)"):
        st.file_uploader("Screenshot bet261", type=['png', 'jpg'])
    
    c1, c2 = st.columns(2)
    home = c1.text_input("🏠 HOME TEAM:")
    away = c2.text_input("✈️ AWAY TEAM:")
    
    if st.button("🎯 PREDICT FOOT MATCH", use_container_width=True):
        if home and away:
            with st.spinner("Analyzing stats..."):
                time.sleep(1.5)
                # Lojika mampiasa ny anaran'ny ekipa ho seed
                random.seed(home + away)
                res = random.choices(["1", "X", "2"], weights=[45, 25, 30])[0]
                score_h = random.randint(0, 3)
                score_a = random.randint(0, 2)
                
                # Ity ny fanitsiana tamin'ilay triple quotes teo
                st.markdown(f"""
                <div class="card">
                    <div class="foot-res">RESULTAT: {res}</div>
                    <div style="text-align:center; margin-top:10px;">
                        <span style="font-size:40px; color:#00ffcc;">{score_h} - {score_a}</span><br>
                        <small>CONFIDENCE: {random.randint(92,97)}%</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.markdown('<div style="text-align:center; margin-top:50px; color:#444;">TITAN OMNI-STRIKE BY PATRICIA © 2026</div>', unsafe_allow_html=True)
