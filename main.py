import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-SYNC", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'admin_pwd' not in st.session_state: st.session_state.admin_pwd = "2026"
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. STYLE DARK NEON (Anti-Bug Layout) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05);
        border: 2px solid #00ffcc;
        padding: 15px; border-radius: 15px; text-align: center;
        box-shadow: 0 0 10px rgba(0, 255, 204, 0.3); margin-bottom: 10px;
    }
    .mines-grid {
        display: grid; grid-template-columns: repeat(5, 1fr);
        gap: 8px; max-width: 280px; margin: auto; padding: 10px;
    }
    .mine-cell {
        aspect-ratio: 1/1; background: #111; border: 1px solid #333;
        border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 20px;
    }
    .cell-star { border: 2px solid #00ffcc; box-shadow: 0 0 8px #00ffcc; color: #ffff00; }
    .luck-msg { color: #00ffcc; font-size: 20px; font-weight: bold; text-align: center; margin-top: 15px; }
    .stButton>button { background: #00ffcc !important; color: black !important; font-weight: bold; width: 100%; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🛰️ TITAN V85.0</h1>", unsafe_allow_html=True)
    pwd = st.text_input("Admin Key:", type="password")
    if st.button("HAMPIDITRA"):
        if pwd == st.session_state.admin_pwd:
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. ALGORITHM CORE ---
def generate_viper_data(seed, client, game):
    random.seed(int(hashlib.sha256(f"{seed}{client}{datetime.now()}".encode()).hexdigest()[:8], 16))
    results = []
    for i in range(1, 4):
        moyen = round(random.uniform(1.50, 4.50), 2)
        results.append({
            "ora": (datetime.now() + timedelta(minutes=i*2)).strftime("%H:%M" if game != "COSMOS X" else "%H:%M:%S"),
            "moyen": moyen,
            "min": round(moyen * 0.88, 2),
            "max": round(moyen * 1.25, 2)
        })
    return results

# --- 5. MAIN APP ---
st.markdown("<h2 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 ULTRA-SYNC</h2>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS X", "💣 MINES VIP"])

# --- AVIATOR & COSMOS X ---
for tab, g_name in zip([t1, t2], ["AVIATOR", "COSMOS X"]):
    with tab:
        s_input = st.text_input(f"Server Seed {g_name}:", key=f"s_{g_name}")
        c_input = st.text_input(f"Client Seed / Lera {g_name}:", key=f"c_{g_name}")
        if st.button(f"🔥 ANALYZE {g_name}"):
            preds = generate_viper_data(s_input, c_input, g_name)
            cols = st.columns(3)
            for i, r in enumerate(preds):
                with cols[i]:
                    st.markdown(f"""
                    <div class="prediction-card">
                        <b style="color:red;">TOUR {i+1}</b><br><small>{r['ora']}</small><br>
                        <span style="font-size:30px; color:#00ffcc;">{r['moyen']}x</span><br>
                        <div style="font-size:11px; margin-top:5px;">
                            Min (88%): {r['min']}x | Max (125%): {r['max']}x
                        </div>
                    </div>""", unsafe_allow_html=True)
            st.markdown("<p class='luck-msg'>🍀 Bonne chance à tous !</p>", unsafe_allow_html=True)

# --- MINES VIP (Fixed Grid 5x5) ---
with t3:
    st.subheader("💣 MINES VIP 8/10")
    m_seed = st.text_input("Seed du serveur:", key="ms")
    m_client = st.text_input("Seed du client:", key="mc")
    m_count = st.slider("Isan'ny vanja:", 1, 7, 3)
    
    if st.button("🔍 SCAN MINES"):
        # Algorithm synchronization
        random.seed(int(hashlib.sha256(f"{m_seed}{m_client}{random.random()}".encode()).hexdigest()[:8], 16))
        # Mifidy kintana 5 ao anatin'ny 25 (Grid 5x5)
        stars = random.sample(range(25), 5)
        
        grid_html = '<div class="mines-grid">'
        for i in range(25):
            if i in stars:
                grid_html += '<div class="mine-cell cell-star">⭐</div>'
            else:
                grid_html += '<div class="mine-cell">⬛</div>'
        grid_html += '</div>'
        
        st.markdown(grid_html, unsafe_allow_html=True)
        st.markdown("<p class='luck-msg'>🍀 Bonne chance à tous !</p>", unsafe_allow_html=True)

st.markdown("---")
if st.button("🗑️ RESET SESSION"):
    st.session_state.history = []
    st.rerun()
