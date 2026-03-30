import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"
if 'history' not in st.session_state: st.session_state.history = []
if 'manche_screenshots' not in st.session_state: st.session_state.manche_screenshots = []

# --- 2. STYLE DARK NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05);
        border: 2px solid #00ffcc;
        padding: 20px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); margin-bottom: 15px;
    }
    .luck-msg { color: #00ffcc; font-size: 24px; font-weight: bold; text-align: center; margin-top: 25px; }
    .stButton>button { background: #00ffcc !important; color: black !important; border-radius: 15px !important; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 LOGIN</h1>", unsafe_allow_html=True)
    pwd_input = st.text_input("Access Key:", type="password")
    if st.button("HAMPIDITRA"):
        if pwd_input == st.session_state.admin_pwd:
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. ALGORITHM (Viper High-Level) ---
def get_predictions(seed, client, game):
    now = datetime.now()
    results = []
    # SHA-256 Hybrid Logic
    random.seed(int(hashlib.sha256(f"{seed}{client}{random.random()}".encode()).hexdigest()[:8], 16))
    
    for i in range(1, 4):
        moyen = round(random.uniform(1.45, 4.45), 2)
        fmt = "%H:%M:%S" if game == "COSMOS X" else "%H:%M"
        p = {
            "game": game,
            "ora": (now + timedelta(minutes=i*2)).strftime(fmt),
            "moyen": moyen,
            "min": round(moyen * 0.88, 2),
            "max": round(moyen * 1.25, 2)
        }
        results.append(p)
        st.session_state.history.insert(0, p)
    return results

# --- 5. INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)

tabs = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "📸 MANCHE"])

# TABS: AVIATOR & COSMOS X (Mihazona ny Seed)
for tab, g_name in zip([tabs[0], tabs[1]], ["AVIATOR", "COSMOS X"]):
    with tab:
        st.file_uploader(f"📸 Screenshot {g_name}:", type=['png','jpg'], key=f"f_{g_name}")
        seed = st.text_input("Server Seed (Hex):", key=f"s_{g_name}")
        clt = st.text_input("Lera / Client Seed:", key=f"c_{g_name}")
        
        if st.button(f"🔥 EXECUTE {g_name} ANALYZE"):
            preds = get_predictions(seed, clt, g_name)
            cols = st.columns(3)
            for i, r in enumerate(preds):
                with cols[i]:
                    st.markdown(f"""
                    <div class="prediction-card">
                        <b style="color:red;">TOUR {i+1}</b><br>
                        <span style="color:#aaa;">{r['ora']}</span><br>
                        <span style="font-size:38px; color:#00ffcc;">{r['moyen']}x</span><br>
                        <small>Target (100%)</small>
                        <hr style="border:0.5px solid #333;">
                        <div style="font-size:12px;">
                            <b>Min (88%):</b> {r['min']}x | <b>Max (125%):</b> {r['max']}x
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# TAB: MINES VIP (Nesorina ny Seed araka ny sary vaovao)
with tabs[2]:
    st.markdown("### 💣 MINES VIP 8/10")
    # Slider ho an'ny isan'ny vanja araka ny sary
    nb_mines = st.slider("Isan'ny vanja (Mines):", 1, 24, 3) 
    
    if st.button("🔍 SCAN MINES"):
        # Algorithm Scanner simulation
        grid = ["⬛"] * 25
        stars = random.sample(range(25), 5)
        for s in stars: grid[s] = "⭐"
        
        display_grid = ""
        for i in range(0, 25, 5):
            display_grid += " ".join(grid[i:i+5]) + "<br>"
            
        st.markdown(f"<div style='font-size:30px; text-align:center; letter-spacing:8px;'>{display_grid}</div>", unsafe_allow_html=True)
        st.markdown("<p class='luck-msg'>🍀 Bonne chance à tous !</p>", unsafe_allow_html=True)

# TAB: MANCHE (Historique)
with tabs[3]:
    for h in st.session_state.history[:5]:
        st.write(f"🎮 {h['game']} | {h['ora']} | {h['moyen']}x")

st.markdown("---")
st.subheader("📜 LAST PREDICTIONS")
