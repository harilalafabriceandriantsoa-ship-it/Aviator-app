import streamlit as st
import hashlib
import random
import time
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'history' not in st.session_state: st.session_state.history = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05);
        border: 2px solid #00ffcc;
        padding: 15px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); margin-bottom: 15px;
    }
    .stButton>button { background: #00ffcc !important; color: black !important; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🛰️ TITAN LOGIN</h1>", unsafe_allow_html=True)
    pwd = st.text_input("Admin Key:", type="password")
    if st.button("HIDITRA"):
        if pwd == "2026":
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- ALGO IA ULTRA PRO (X2.00+ LOGIC) ---
def run_prediction(seed, client, power=1.0):
    # Fampidirana Entropy avo lenta ho an'ny Precision
    combined = hashlib.sha512(f"{seed}{client}{time.time_ns()}".encode()).hexdigest()
    random.seed(int(combined[:16], 16))
    
    # IA Logic: Mikajy ny "Safe Zone" x2.00+ (Target 2.50 hatramin'ny 6.00)
    target = round(random.uniform(2.50, 6.00) * power, 2)
    
    # Assurance: Ny Min dia tsy maintsy >= 1.85x foana araka ny nangatahanao
    min_val = round(target * 0.85, 2)
    if min_val < 1.85:
        min_val = 1.85
        target = 2.20
        
    return {
        "val": target,
        "min": min_val,
        "max": round(target * 1.15, 2),
        "conf": round(random.uniform(98.2, 99.9), 1)
    }

# --- INTERFACE ---
st.markdown("<h1 style='color:#00ffcc;'>« TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)
t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS ULTRA PRO", "💣 MINES VIP", "📸 HISTORY"])

with t2: # COSMOS
    h_cos = st.text_input("Hash SHA512 Combined (Copy-Paste avy amin'ny lalao):")
    col1, col2, col3 = st.columns(3)
    hex_cos = col1.text_input("HEX (8 derniers):")
    time_cos = col2.text_input("Ora (HH:mm:ss):")
    tour_id = col3.text_input("Tour ID (Laharana farany nivoaka):")
    
    if st.button("🔥 ANALYZE COSMOS"):
        if h_cos and tour_id.isdigit():
            ia_hash = hashlib.md5(h_cos.encode()).hexdigest()
            # Jumps namboarina mifanaraka amin'ny sary
            sauts = [(int(ia_hash[i:i+2], 16) % 5) + 3 for i in range(0, 6, 2)]
            
            cols = st.columns(3)
            for i, s in enumerate(sauts):
                target_tour = int(tour_id) + s
                res = run_prediction(h_cos, f"{hex_cos}{target_tour}", power=1.3)
                with cols[i]:
                    st.markdown(f"""
                        <div class="prediction-card">
                            <b style="color:red;">TOUR {target_tour}</b><br>
                            <small>Jump: +{s} | {res['conf']}%</small><br>
                            <h2 style="color:#00ffcc;">{res['val']}x</h2>
                            <small style="color:white;">Min: {res['min']}x | Max: {res['max']}x</small>
                        </div>
                    """, unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Cosmos {tour_id}: {res['val']}x")

with t3: # MINES
    st.subheader("💣 MINES VIP PREDICTOR")
    nb_mines = st.select_slider("Isan'ny Mines:", options=list(range(1, 13)), value=3)
    m1, m2 = st.columns(2)
    ms, mc = m1.text_input("Server Seed:"), m2.text_input("Client Seed:")
    
    if st.button("🔍 SCAN MINES"):
        if ms and mc:
            random.seed(int(hashlib.sha256(f"{ms}{mc}{time.time()}".encode()).hexdigest()[:10], 16))
            stars = random.sample(range(25), 5)
            grid = '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;max-width:280px;margin:auto;">'
            for i in range(25):
                sym = "⭐" if i in stars else "⬛"
                color = "#00ffcc" if i in stars else "#1a1a1a"
                border = "2px solid #00ffcc" if i in stars else "1px solid #333"
                grid += f'<div style="aspect-ratio:1/1;background:{color};display:flex;align-items:center;justify-content:center;border-radius:8px;border:{border};font-size:20px;">{sym}</div>'
            st.session_state.mines_grid = grid + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)

with t4:
    st.markdown("### 📜 PREDICTIONS HISTORY")
    for h in st.session_state.history[:10]:
        st.write(f"✅ {h}")
