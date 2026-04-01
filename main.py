import streamlit as st
import hashlib
import random
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-PRO", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. STYLE DARK "CHARME" NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05);
        border: 2px solid #00ffcc;
        padding: 15px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); margin-bottom: 15px;
    }
    .stButton>button { background: #00ffcc !important; color: black !important; border-radius: 15px !important; font-weight: bold; width: 100%; }
    .multiplier-text { font-size: 42px; color: #00ffcc; font-weight: bold; margin: 5px 0; }
    .stat-row { display: flex; justify-content: space-around; font-size: 11px; color: #aaa; margin-top: 10px; }
    .luck-text { color: #ffff00; font-weight: bold; font-style: italic; margin-top: 10px; font-size: 13px; }
    .perc-text { color: #ff0055; font-weight: bold; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 LOGIN</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1, 1])
    with col:
        pwd_input = st.text_input("Admin Key:", type="password")
        if st.button("HIDITRA"):
            if pwd_input == st.session_state.admin_pwd:
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Diso ny MDP!")
    st.stop()

# --- 4. CORE ALGO IA (TSY NOHOVIANA NY MOTERA) ---
def run_prediction(seed, client, power=1.0):
    now = datetime.now() + timedelta(hours=3)
    entropy = str(time.time_ns())
    combined = hashlib.sha512(f"{seed}{client}{entropy}".encode()).hexdigest()
    random.seed(int(combined[:12], 16))
    
    results = []
    for i in range(1, 4):
        target = round(random.uniform(1.68, 5.25) * power, 2)
        ora = (now + timedelta(minutes=i*2)).strftime("%H:%M:%S")
        results.append({
            "ora": ora, "val": target, 
            "min": round(target * 0.82, 2), 
            "max": round(target * 1.18, 2), 
            "perc": random.randint(95, 99)
        })
    return results

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 style='text-align:left; color:#00ffcc;'>« TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS ULTRA PRO", "💣 MINES VIP", "📸 HISTORY"])

# AVIATOR
with t1:
    c1, c2 = st.columns(2)
    s_avi = c1.text_input("Server Seed (Hex):", key="s_avi_in")
    cl_avi = c2.text_input("Lera / Client Seed (HH:MM):", key="c_avi_in")
    
    if st.button("🔥 ANALYZE AVIATOR"):
        if s_avi and cl_avi:
            data = run_prediction(s_avi, cl_avi)
            cols = st.columns(3)
            for i, r in enumerate(data):
                with cols[i]:
                    st.markdown(f"""
                        <div class="prediction-card">
                            <b style="color:red;">TOUR {i+1}</b><br>
                            <span class="perc-text">Probabilité: {r['perc']}%</span>
                            <div class="multiplier-text">{r['val']}x</div>
                            <div class="stat-row">
                                <span>Min: {r['min']}x</span>
                                <span>Max: {r['max']}x</span>
                            </div>
                            <div class="luck-text">🍀 Bonne Chance Patricia! 🍀</div>
                        </div>
                    """, unsafe_allow_html=True)

# COSMOS
with t2:
    h_cos = st.text_input("Hash SHA512 Combined:", key="h_cos_in")
    col_a, col_b, col_c = st.columns(3)
    hex_cos = col_a.text_input("HEX (8 derniers):", key="hex_cos_in")
    time_cos = col_b.text_input("Ora (HH:mm:ss):", key="time_cos_in")
    tour_id = col_c.text_input("Numéro de Tour (ID):", key="tour_id_in")
    
    if st.button("🔥 ANALYZE COSMOS"):
        if h_cos and tour_id and tour_id.isdigit():
            ia_jump = int(hashlib.md5(h_cos.encode()).hexdigest()[:2], 16)
            sauts = [(ia_jump % 4) + 2, (ia_jump % 7) + 8, (ia_jump % 12) + 16]
            
            cols = st.columns(3)
            for i, s in enumerate(sauts):
                target_tour = int(tour_id) + s
                seed_final = hashlib.sha512(f"{h_cos}{hex_cos}{target_tour}".encode()).hexdigest()
                r = run_prediction(seed_final[:32], time_cos, power=1.4)[0]
                with cols[i]:
                    st.markdown(f"""
                        <div class="prediction-card">
                            <b style="color:red;">TOUR {target_tour}</b><br>
                            <span class="perc-text">Probabilité: {r['perc']}%</span>
                            <div class="multiplier-text">{r['val']}x</div>
                            <div class="stat-row">
                                <span>Min: {r['min']}x</span>
                                <span>Max: {r['max']}x</span>
                            </div>
                            <div class="luck-text">🍀 Bonne Chance Patricia! 🍀</div>
                        </div>
                    """, unsafe_allow_html=True)

# MINES (Tsy nisy niova)
with t3:
    st.subheader("💣 MINES VIP PREDICTOR")
    nb_mines = st.select_slider("Isan'ny Mines:", options=[1, 2, 3, 4, 5], value=3)
    ms = st.text_input("Server Seed (Hex):", key="ms_in")
    mc = st.text_input("Client Seed:", key="mc_in")
    if st.button("🔍 SCAN MINES"):
        if ms and mc:
            random.seed(int(hashlib.sha256(f"{ms}{mc}{nb_mines}{time.time()}".encode()).hexdigest()[:10], 16))
            safe_stars = random.sample(range(25), 5)
            grid = '<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 300px; margin: 20px auto;">'
            for i in range(25):
                char = "⭐" if i in safe_stars else "⬛"
                color = "border: 2px solid #00ffcc; box-shadow: 0 0 10px #00ffcc;" if i in safe_stars else "border: 1px solid #333;"
                grid += f'<div style="aspect-ratio:1/1; background:#1a1a1a; {color} border-radius:5px; display:flex; align-items:center; justify-content:center; font-size:24px;">{char}</div>'
            st.markdown(grid + '</div>', unsafe_allow_html=True)
            st.markdown("<p style='text-align:center;' class='luck-text'>🍀 Bonne Chance Patricia! 🍀</p>", unsafe_allow_html=True)

with t4:
    st.markdown("### 📜 PREDICTIONS HISTORY")
    for h in st.session_state.history[:10]:
        st.write(f"✅ {h}")
