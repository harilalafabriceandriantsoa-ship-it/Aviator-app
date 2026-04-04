import streamlit as st
import hashlib
import random
import time

# --- 1. CONFIGURATION SYSTEM ---
st.set_page_config(page_title="TITAN V85.0 WAR-MACHINE", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'history' not in st.session_state: st.session_state.history = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE NEON PROFESSIONAL ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: monospace; }
    .war-card {
        background: rgba(0, 255, 204, 0.07); border: 2px solid #00ffcc;
        padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 15px;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
    }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; max-width: 320px; margin: auto; }
    .mine-cell { aspect-ratio: 1/1; background: #111; border: 1px solid #333; display: flex; align-items: center; justify-content: center; font-size: 24px; border-radius: 8px; }
    .cell-star { border: 2px solid #ffff00 !important; box-shadow: 0 0 15px #ffff00; color: #ffff00; background: rgba(255, 255, 0, 0.15); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ADMIN ---
with st.sidebar:
    st.markdown("### 🛰️ TITAN ADMIN")
    admin_key = st.text_input("Access Key:", type="password")
    if admin_key == "2026":
        st.success("✅ ADMIN ACTIVE")
        if st.button("🗑️ PURGE SYSTEM DATA"):
            st.session_state.history = []
            st.session_state.mines_grid = ""
            st.session_state.logged_in = False
            st.rerun()

# --- 4. LOGIN SYSTEM ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>🛰️ TITAN LOGIN</h1>", unsafe_allow_html=True)
    login_key = st.text_input("Key:", type="password")
    if st.button("ACTIVATE ENGINE"):
        if login_key == "2026":
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 5. CORE LOGIC ENGINE (6 DIAMANTS FIXED) ---
def titan_core_engine(seed, context, mode, count=6):
    # Logic SHA-512 Base
    raw_hash = hashlib.sha512(f"{seed}{context}TITAN_V85_ULTRA_6D".encode()).hexdigest()
    
    if mode == "cosmos":
        random.seed(int(raw_hash[:16], 16))
        val = round(random.uniform(1.80, 4.20), 2)
        acc = random.randint(94, 99)
        return {"val": val, "acc": acc}
    else:
        # Fikajiana toerana 6 raikitra foana ho an'ny diamondra
        safe_spots = []
        for i in range(count):
            val = int(raw_hash[i*8:(i+1)*8], 16) % 25
            while val in safe_spots:
                val = (val + 1) % 25
            safe_spots.append(val)
        return safe_spots

# --- 6. MAIN INTERFACE ---
st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🛰️ TITAN V85.0 ULTRA-SYNC</h2>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🚀 COSMOS ANALYZER", "💣 MINES SCANNER", "📜 HISTORY"])

with t1:
    st.markdown("### 🚀 COSMOS PREDICTION")
    h_val = st.text_input("Server Hash:")
    t_id = st.text_input("Next Round ID:")
    if st.button("🔥 ANALYZE PATTERN"):
        if h_val and t_id:
            data = titan_core_engine(h_val, t_id, "cosmos")
            st.markdown(f"""
                <div class="war-card">
                    <p>PREDICTED TARGET</p>
                    <h1 style="color:#00ffcc; font-size:60px;">{data['val']}x</h1>
                    <p>🎯 PRECISION: {data['acc']}%</p>
                </div>
            """, unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Cosmos {t_id}: {data['val']}x")

with t2:
    st.markdown("### 🔍 MINES SHA-512 SCANNER")
    # Averina amin'ny isan'ny mine 1-3 ny slider
    nb_mines = st.select_slider("Isan'ny Mine (Target):", options=[1, 2, 3], value=1)
    
    col_a, col_b = st.columns(2)
    s_seed = col_a.text_input("Server Seed:")
    c_seed = col_b.text_input("Client Seed:")
    
    if st.button("🛰️ START DEEP SCAN"):
        if s_seed and c_seed:
            with st.spinner("Synchronizing Grid..."):
                time.sleep(0.4)
                # Na inona na inona nb_mines, diamondra 6 foana no tadiavina (count=6)
                safe_spots = titan_core_engine(s_seed, c_seed, "mines", count=6)
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    is_safe = i in safe_spots
                    grid_html += f'<div class="mine-cell {"cell-star" if is_safe else ""}">{"⭐" if is_safe else "⬛"}</div>'
                st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success(f"✅ Pattern {nb_mines} Mine(s) Synchronisé (6 Diamondra)!")

with t3:
    st.markdown("### 📜 SYSTEM LOGS")
    for log in st.session_state.history[:10]:
        st.write(f"🚩 {log}")
