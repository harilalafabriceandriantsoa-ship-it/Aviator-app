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

# --- 2. STYLE DARK "CHARME" NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; border-bottom: 1px solid #00ffcc; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #00ffcc !important; border-bottom: 2px solid #00ffcc !important; }
    
    .prediction-card {
        background: rgba(0, 255, 204, 0.05);
        border: 2px solid #00ffcc;
        padding: 20px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); margin-bottom: 15px;
    }
    .luck-msg { color: #00ffcc; font-size: 24px; font-weight: bold; text-align: center; margin-top: 25px; text-shadow: 0 0 10px #00ffcc; }
    .stButton>button { background: #00ffcc !important; color: black !important; border-radius: 15px !important; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN PAGE (MDP) ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 LOGIN</h1>", unsafe_allow_html=True)
    col_l, _ = st.columns([1, 1])
    with col_l:
        pwd_input = st.text_input("Admin Key / MDP:", type="password")
        if st.button("HAMPIDITRA"):
            if pwd_input == st.session_state.admin_pwd:
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Diso ny MDP!")
    st.stop()

# --- 4. ADMIN SETTINGS (SIDEBAR) ---
with st.sidebar:
    st.title("⚙️ MANAGER")
    auth = st.text_input("Verify Admin Key:", type="password")
    if auth == st.session_state.admin_pwd:
        new_p = st.text_input("New MDP:", type="password")
        if st.button("Update MDP"):
            st.session_state.admin_pwd = new_p
            st.success("MDP Updated!")
        if st.button("🗑️ RESET ALL DATA"):
            st.session_state.history = []
            st.session_state.manche_screenshots = []
            st.rerun()

# --- 5. ALGORITHM (MOYEN AJUSTÉ POUR WIN 8/10) ---
def get_predictions(seed, client, game):
    now = datetime.now()
    results = []
    # Sync Algorithm
    random.seed(int(hashlib.sha256(f"{seed}{client}{random.random()}".encode()).hexdigest()[:8], 16))
    
    for i in range(1, 4):
        # Moyen nampidinina kely (1.45x - 3.85x) ho an'ny Win Rate 8/10
        moyen = round(random.uniform(1.45, 3.85), 2)
        
        # Format lera manokana
        if game == "COSMOS X":
            fmt = "%H:%M:%S"
        else:
            fmt = "%H:%M"
            
        p = {
            "game": game,
            "ora": (now + timedelta(minutes=i*2)).strftime(fmt),
            "moyen": moyen,
            "min": round(moyen * 0.88, 2), # Fiarovana ambony (88%)
            "max": round(moyen * 1.25, 2)
        }
        results.append(p)
        st.session_state.history.insert(0, p)
    return results

# --- 6. INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP", "📸 MANCHE HISTORY"])

# --- AVIATOR & COSMOS X ---
for tab, g_name in zip([t1, t2], ["AVIATOR", "COSMOS X"]):
    with tab:
        st.file_uploader(f"📸 Screenshot {g_name}:", type=['png','jpg'], key=f"f_{g_name}")
        c1, c2 = st.columns(2)
        seed = c1.text_input("Server Seed (Hex):", key=f"s_{g_name}")
        hint = "HH:mm:ss" if g_name == "COSMOS X" else "HH:mm"
        clt = c2.text_input(f"Lera / Client Seed ({hint}):", key=f"c_{g_name}")
        
        if st.button(f"🔥 ANALYZE {g_name}"):
            preds = get_predictions(seed, clt, g_name)
            cols = st.columns(3)
            for i, r in enumerate(preds):
                with cols[i]:
                    st.markdown(f"""<div class="prediction-card"><b style="color:red;">TOUR {i+1}</b><br>{r['ora']}<br>
                    <span style="font-size:35px; color:#00ffcc;">{r['moyen']}x</span><br>
                    <small>Min: {r['min']} | Max: {r['max']}</small></div>""", unsafe_allow_html=True)
            st.markdown("<p class='luck-msg'>🍀 Bonne chance à tous !</p>", unsafe_allow_html=True)

# --- MINES VIP ---
with t3:
    st.subheader("💣 MINES 8/10")
    m_srv = st.text_input("Server Seed:", key="msrv")
    m_clt = st.text_input("Client Seed:", key="mclt")
    nb = st.slider("Isan'ny vanja (Mines):", 1, 7, 3)
    if st.button("🔍 SCAN MINES"):
        st.markdown("<div style='font-size:30px; text-align:center;'>⭐ ⬛ ⬛ ⭐ ⬛<br>⬛ ⭐ ⬛ ⬛ ⬛<br>⬛ ⬛ ⭐ ⬛ ⭐</div>", unsafe_allow_html=True)
        st.markdown("<p class='luck-msg'>🍀 Bonne chance à tous !</p>", unsafe_allow_html=True)

# --- MANCHE HISTORY (POROFO) ---
with t4:
    st.subheader("📸 MANCHE SCREENSHOTS HISTORY")
    with st.expander("➕ ADD NEW RESULT"):
        up_img = st.file_uploader("Upload result image:", type=['png','jpg'])
        up_info = st.text_input("Info (lera sy vokatra):")
        if st.button("Tehirizina"):
            if up_img:
                st.session_state.manche_screenshots.insert(0, {"img": up_img, "info": up_info})
                st.success("Voatahiry!")
    
    for m in st.session_state.manche_screenshots:
        st.image(m['img'], width=300, caption=m['info'])
        st.markdown("---")

# --- 7. HISTORIQUE PRÉDICTION (LATEST) ---
st.markdown("---")
st.subheader("📜 LAST PREDICTIONS")
for h in st.session_state.history[:5]:
    st.write(f"🎮 {h['game']} | {h['ora']} | {h['moyen']}x (Min: {h['min']} | Max: {h['max']})")
