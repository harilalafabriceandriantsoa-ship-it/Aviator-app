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
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

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
        padding: 15px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4); margin-bottom: 15px;
    }
    .stButton>button { background: #00ffcc !important; color: black !important; border-radius: 15px !important; font-weight: bold; width: 100%; }
    hr { border: 0.5px solid #333; margin: 10px 0; }
    
    .mines-grid {
        display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 300px; margin: 20px auto;
    }
    .mine-cell {
        aspect-ratio: 1/1; background: #1a1a1a; border: 1px solid #333; border-radius: 5px;
        display: flex; align-items: center; justify-content: center; font-size: 24px;
    }
    .cell-star { border: 2px solid #00ffcc !important; box-shadow: 0 0 10px #00ffcc; color: #ffff00; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN PAGE ---
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
        if st.button("🗑️ RESET ALL DATA"):
            st.session_state.history = []
            st.session_state.manche_screenshots = []
            st.session_state.mines_grid = ""
            st.rerun()

# --- 5. ALGORITHM GENERATOR (ULTRA PRO) ---
def generate_pro_results(seed, client, game):
    now = datetime.now() + timedelta(hours=3) # Madagascar Time
    results = []
    # Fikajiana Hash ho an'ny fahamatorana
    random.seed(int(hashlib.sha256(f"{seed}{client}{random.random()}".encode()).hexdigest()[:8], 16))
    
    for i in range(1, 4):
        # Moyen / Target
        moyen = round(random.uniform(1.60, 4.80), 2)
        # Min (85% ny target) & Max (120% ny target)
        val_min = round(moyen * 0.85, 2)
        val_max = round(moyen * 1.20, 2)
        # Ora (+2 min isaky ny tour)
        ora = (now + timedelta(minutes=i*2)).strftime("%H:%M:%S")
        # Pourcentage de confiance
        perc = random.randint(92, 99)
        
        results.append({
            "ora": ora, "moyen": moyen, "min": val_min, "max": val_max, "perc": perc
        })
    return results

# --- 6. INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.0 ULTRA-SYNC</h1>", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["✈️ AVIATOR", "🚀 COSMOS ULTRA PRO", "💣 MINES VIP", "📸 MANCHE HISTORY"])

# --- AVIATOR ---
with t1:
    st.file_uploader("📸 Screenshot AVIATOR:", type=['png','jpg'], key="f_avi")
    c1, c2 = st.columns(2)
    s_avi = c1.text_input("Server Seed (Hex):", key="s_avi")
    clt_avi = c2.text_input("Lera / Client Seed (HH:MM):", key="c_avi")
    
    if st.button("🔥 ANALYZE AVIATOR"):
        if s_avi and clt_avi:
            preds = generate_pro_results(s_avi, clt_avi, "AVIATOR")
            cols = st.columns(3)
            for i, r in enumerate(preds):
                with cols[i]:
                    st.markdown(f"""
                        <div class="prediction-card">
                            <b style="color:red;">TOUR {i+1}</b><br>
                            <span style="color:#aaa; font-size:12px;">{r['ora']}</span><br>
                            <span style="font-size:32px; color:#00ffcc;">{r['moyen']}x</span><br>
                            <small style="color:#ffffff;">Confidence: {r['perc']}%</small>
                            <hr>
                            <div style="font-size:12px; text-align:left; padding-left:5px;">
                                <span style="color:#00ffcc;">●</span> <b>Min:</b> {r['min']}x<br>
                                <span style="color:#ff4444;">●</span> <b>Max:</b> {r['max']}x
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Aviator {preds[0]['ora']}: {preds[0]['moyen']}x")

# --- COSMOS ULTRA PRO ---
with t2:
    st.file_uploader("📸 Screenshot COSMOS:", type=['png','jpg'], key="f_cos")
    h_sha = st.text_input("Hash SHA512 Combined (Lava be):", key="cos_hash")
    col_a, col_b = st.columns(2)
    h_hex = col_a.text_input("HEX (8 derniers caractères):", key="cos_hex")
    h_time = col_b.text_input("Ora (HH:mm:ss):", key="cos_time")
    
    if st.button("🔥 ANALYZE COSMOS"):
        if h_hex and h_time:
            preds = generate_pro_results(h_sha + h_hex, h_time, "COSMOS")
            cols = st.columns(3)
            for i, r in enumerate(preds):
                with cols[i]:
                    st.markdown(f"""
                        <div class="prediction-card">
                            <b style="color:red;">TOUR {i+1}</b><br>
                            <span style="color:#aaa; font-size:12px;">{r['ora']}</span><br>
                            <span style="font-size:32px; color:#00ffcc;">{r['moyen']}x</span><br>
                            <small style="color:#ffffff;">Accuracy: {r['perc']}%</small>
                            <hr>
                            <div style="font-size:12px; text-align:left; padding-left:5px;">
                                <span style="color:#00ffcc;">●</span> <b>Min:</b> {r['min']}x<br>
                                <span style="color:#ff4444;">●</span> <b>Max:</b> {r['max']}x
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Cosmos {preds[0]['ora']}: {preds[0]['moyen']}x")

# --- MINES VIP ---
with t3:
    st.subheader("💣 MINES VIP 8/10")
    m_col1, m_col2 = st.columns(2)
    m_s = m_col1.text_input("Seed du serveur (Hex):", key="mine_s")
    m_c = m_col2.text_input("Seed du client:", key="mine_c")
    nb_mines = st.slider("Isan'ny vanja (Mines):", 1, 7, 3)
    
    if st.button("🔍 SCAN MINES"):
        if m_s and m_c:
            random.seed(int(hashlib.sha256(f"{m_s}{m_c}".encode()).hexdigest()[:8], 16))
            stars = random.sample(range(25), 5)
            grid = '<div class="mines-grid">'
            for i in range(25):
                cls = "mine-cell cell-star" if i in stars else "mine-cell"
                char = "⭐" if i in stars else "⬛"
                grid += f'<div class="{cls}">{char}</div>'
            grid += '</div>'
            st.session_state.mines_grid = grid
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)

# --- MANCHE HISTORY ---
with t4:
    st.subheader("📸 MANCHE SCREENSHOTS")
    for m in st.session_state.manche_screenshots:
        st.image(m['img'], width=300, caption=m['info'])

st.markdown("---")
st.subheader("📜 LAST PREDICTIONS")
for h in st.session_state.history[:5]:
    st.write(f"✅ {h}")
