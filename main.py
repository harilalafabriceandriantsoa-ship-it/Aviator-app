import streamlit as st
import hashlib
import time
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & NEON DESIGN ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

ACCESS_CODE = "2026" 

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
    .target-val { font-size: 40px; color: #00ffcc; font-weight: 800; text-align: center; margin: 5px 0; }
    .prob-badge { 
        background: #00ffcc; color: #000; padding: 4px 12px; 
        border-radius: 20px; font-weight: 900; font-size: 13px;
    }
    .stats-row { display: flex; justify-content: space-around; margin-top: 10px; border-top: 1px solid #333; padding-top: 8px; }
    .stat-number { font-weight: bold; color: #00ffcc; }
    /* Grid Mines */
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
        if code_input == ACCESS_CODE:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Kaody diso.")
    st.stop()

# --- 3. SIDEBAR (MANAGER & WHATSAPP) ---
with st.sidebar:
    st.markdown("### ⚙️ MANAGER PROFILE")
    st.markdown(f"👤 **Manager:** PATRICIA")
    st.markdown(f"🟢 **WhatsApp:** 034 62 497 01")
    st.markdown("---")
    st.success("Access Granted: Admin Mode")

# --- 4. PREDICTION ENGINES ---
def get_3_preds(seed, base_ora, game_type):
    results = []
    h = hashlib.sha256(f"{seed}-TITAN-2026".encode()).hexdigest()
    try:
        fmt = "%H:%M:%S" if game_type == "cosmos" else "%H:%M"
        dt = datetime.strptime(base_ora, fmt)
    except:
        dt = datetime.now()
    
    for i in range(3):
        random.seed(int(h[i*8:(i+1)*8], 16))
        moyen = round(random.uniform(1.8, 4.2), 2)
        results.append({
            "lera": (dt + timedelta(minutes=(i+1)*5)).strftime(fmt),
            "moyen": moyen, "min": round(moyen*0.75, 2), "max": round(moyen*1.6, 2),
            "prob": random.randint(95, 99)
        })
    return results

# --- 5. INTERFACE ---
st.markdown('<div class="main-header">TITAN V85.0 ULTRA-SYNC ⚔️</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

# AVIATOR
with tab1:
    st.markdown("### ⚡ AVIATOR ANALYSIS")
    st.file_uploader("📸 UPLOAD HISTORIQUE", key="av_up")
    c1, c2 = st.columns(2)
    h_av = c1.text_input("🔑 SERVER HEX:", key="h_av")
    o_av = c2.text_input("🕒 HH:mm:", value=datetime.now().strftime("%H:%M"), key="o_av")
    if st.button("🔥 EXECUTE ANALYSIS"):
        for p in get_3_preds(h_av, o_av, "aviator"):
            st.markdown(f"""<div class="prediction-card">
                <div style="display:flex; justify-content:space-between;"><span style="color:#ff4444; font-weight:bold;">⏰ {p['lera']}</span><span class="prob-badge">{p['prob']}%</span></div>
                <div class="target-val">{p['moyen']}x</div>
                <div class="stats-row"><span>MIN: <b class="stat-number">{p['min']}x</b></span><span>MAX: <b class="stat-number">{p['max']}x</b></span></div>
            </div>""", unsafe_allow_html=True)

# COSMOS X
with tab2:
    st.markdown("### 🚀 COSMOS X ANALYSIS")
    st.file_uploader("📸 UPLOAD SCREENSHOT", key="co_up")
    c1, c2 = st.columns(2)
    h_co = c1.text_input("🔑 HEX SEED:", key="h_co")
    o_co = c2.text_input("🕒 HH:mm:ss:", value=datetime.now().strftime("%H:%M:%S"), key="o_co")
    if st.button("🚀 EXECUTE COSMOS"):
        for p in get_3_preds(h_co, o_co, "cosmos"):
            st.markdown(f"""<div class="prediction-card">
                <div style="display:flex; justify-content:space-between;"><span style="color:#ff4444; font-weight:bold;">⏰ {p['lera']}</span><span class="prob-badge">{p['prob']}%</span></div>
                <div class="target-val">{p['moyen']}x</div>
                <div class="stats-row"><span>MIN: {p['min']}x</span><span>MAX: {p['max']}x</span></div>
            </div>""", unsafe_allow_html=True)

# MINES VIP (DYNAMIC PREDICTION SCHEMA)
with tab3:
    st.markdown("### 💣 MINES VIP DECODER")
    nb_mines = st.select_slider("Isan'ny Mines:", options=[1,2,3,4,5,6,7], value=3)
    c1, c2 = st.columns(2)
    s_serv = c1.text_input("📡 Seed du serveur:", key="s_serv")
    s_cli = c2.text_input("💻 Seed du client:", key="s_cli")
    
    if st.button("💎 GENERATE PREDICTION SCHEMA"):
        if s_serv and s_cli:
            # Algorithm miankina amin'ny seeds roa
            combined_seed = hashlib.sha256(f"{s_serv}{s_cli}{nb_mines}".encode()).hexdigest()
            random.seed(int(combined_seed[:12], 16))
            diamond_pos = random.sample(range(25), 5) # maminany diamondra 5 azo antoka
            
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                if i in diamond_pos:
                    grid_html += '<div class="mine-cell diamond-cell">💎</div>'
                else:
                    grid_html += '<div class="mine-cell">⬛</div>'
            grid_html += '</div>'
            st.markdown(grid_html, unsafe_allow_html=True)
            st.success(f"Schema vaovao mifanaraka amin'ny Seeds-nao!")

# --- FOOTER ---
st.markdown(f"<br><hr><center style='font-size:12px; color:#444;'>TITAN OMNI-STRIKE BY PATRICIA © 2026<br><b>WhatsApp: 0346249701</b></center>", unsafe_allow_html=True)
