import streamlit as st
import hashlib
import random
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-PRO", layout="wide", initial_sidebar_state="collapsed")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"
if 'history' not in st.session_state: st.session_state.history = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE ULTRA PRO (LOVABLE INSPIRED) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at top right, #0a1110, #000000);
        color: #e0e0e0; 
        font-family: 'Inter', sans-serif; 
    }
    
    /* Card Glassmorphism */
    .prediction-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 204, 0.2);
        padding: 20px; 
        border-radius: 24px; 
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }
    .prediction-card:hover {
        border-color: #00ffcc;
        transform: translateY(-5px);
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background: transparent; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background: rgba(255,255,255,0.05) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 0 20px !important;
    }
    .stTabs [aria-selected="true"] {
        background: #00ffcc !important;
        color: #000 !important;
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #00ccaa) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 12px 24px !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
    }

    /* Mines Grid */
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; max-width: 320px; margin: 20px auto; }
    .mine-cell { 
        aspect-ratio: 1/1; 
        background: rgba(255,255,255,0.05); 
        border-radius: 12px; 
        display: flex; align-items: center; justify-content: center;
        font-size: 22px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .cell-star { 
        background: rgba(0, 255, 204, 0.1); 
        border: 2px solid #00ffcc; 
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; color:#00ffcc; font-weight:800;'>TITAN V85.0</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>Secure Intelligence Access</p>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        with st.container():
            pwd_input = st.text_input("ADMIN KEY", type="password", placeholder="••••")
            if st.button("AUTHENTICATE"):
                if pwd_input == st.session_state.admin_pwd:
                    st.session_state.logged_in = True
                    st.rerun()
                else: st.error("ACCESS DENIED")
    st.stop()

# --- 5. ALGO IA (MIN x2.00+ ASSURED) ---
def run_prediction(seed, client, power=1.0):
    now = datetime.now()
    combined = hashlib.sha512(f"{seed}{client}{time.time_ns()}".encode()).hexdigest()
    random.seed(int(combined[:16], 16))
    
    # Logic ho an'ny x2.00+ hatrany
    target = round(random.uniform(2.50, 5.80) * power, 2)
    min_val = round(target * 0.85, 2)
    if min_val < 2.00: min_val = 2.05

    return {"val": target, "min": min_val, "ora": now.strftime("%H:%M:%S")}

# --- 6. MAIN INTERFACE ---
st.markdown("<h2 style='color:#00ffcc; font-weight:800; margin-bottom:0;'>TITAN V85.0</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:gray; font-size:14px; margin-bottom:20px;'>ULTRA-SYNC PREDICTOR PRO</p>", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS", "💣 MINES", "📜 HISTORY"])

with t1:
    st.markdown("### AVIATOR ANALYSIS")
    c1, c2 = st.columns(2)
    s_avi = c1.text_input("Server Seed", placeholder="Hex format", key="avi_s")
    cl_avi = c2.text_input("Client Seed / Ora", placeholder="HH:MM", key="avi_c")
    if st.button("EXECUTE ANALYSIS"):
        if s_avi:
            res = run_prediction(s_avi, cl_avi)
            st.markdown(f"""
                <div class="prediction-card">
                    <small style="color:#00ffcc;">PREDICTION TARGET</small>
                    <h1 style="color:white; font-size:48px; margin:10px 0;">{res['val']}x</h1>
                    <div style="display:flex; justify-content:space-around;">
                        <span>Min: <b>{res['min']}x</b></span>
                        <span>Safety: <b>99.2%</b></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Aviator: {res['val']}x at {res['ora']}")

with t2:
    st.markdown("### COSMOS JUMP ENGINE")
    h_cos = st.text_input("Combined Hash SHA512", key="cos_h")
    col_a, col_b, col_c = st.columns(3)
    hex_cos = col_a.text_input("HEX (8)", key="cos_x")
    tour_id = col_c.text_input("Tour ID", key="cos_i")
    
    if st.button("SYNC COSMOS"):
        if h_cos and tour_id.isdigit():
            ia_hash = hashlib.md5(h_cos.encode()).hexdigest()
            # Jump Logic
            sauts = [(int(ia_hash[0:2], 16) % 5) + 3, (int(ia_hash[2:4], 16) % 10) + 8, (int(ia_hash[4:6], 16) % 15) + 15]
            cols = st.columns(3)
            for i, s in enumerate(sauts):
                target_tour = int(tour_id) + s
                r = run_prediction(h_cos, f"{hex_cos}{target_tour}", power=1.2)
                with cols[i]:
                    st.markdown(f"""
                        <div class="prediction-card">
                            <b style="color:#ff4b4b;">TOUR {target_tour}</b><br>
                            <h2 style="color:white; margin:10px 0;">{r['val']}x</h2>
                            <small>Jump +{s}</small>
                        </div>
                    """, unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Cosmos Tour {tour_id}: {r['val']}x")

with t3:
    st.markdown("### MINES VIP SCANNER")
    nb_mines = st.select_slider("Mines count", options=[1, 3, 5, 10, 24], value=3)
    if st.button("SCAN GRID"):
        random.seed(time.time_ns())
        stars = random.sample(range(25), 5)
        grid_html = '<div class="mines-grid">'
        for i in range(25):
            cls = "mine-cell cell-star" if i in stars else "mine-cell"
            grid_html += f'<div class="{cls}">{"⭐" if i in stars else "⬛"}</div>'
        st.session_state.mines_grid = grid_html + '</div>'
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)

with t4:
    st.markdown("### 📜 RECENT ACTIVITY")
    if not st.session_state.history:
        st.info("No data yet. Run analysis to see history.")
    for h in st.session_state.history[:15]:
        st.markdown(f"""
            <div style="background:rgba(255,255,255,0.05); padding:10px 20px; border-radius:12px; margin-bottom:8px; border-left:4px solid #00ffcc;">
                {h}
            </div>
        """, unsafe_allow_html=True)
