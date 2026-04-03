import streamlit as st
import hashlib
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 FULL PRO", layout="wide")

# Admin Code sy History
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""
if 'history' not in st.session_state: st.session_state.history = []

# --- 2. STYLE NEON PREMIUM ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: monospace; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05); border: 2px solid #00ffcc;
        padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 15px;
    }
    .jump-tag { background: #ff4b4b; color: white; padding: 2px 10px; border-radius: 10px; font-weight: bold; font-size: 12px; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; max-width: 280px; margin: auto; }
    .mine-cell { aspect-ratio: 1/1; background: #111; border: 1px solid #333; display: flex; align-items: center; justify-content: center; font-size: 20px; border-radius: 4px; }
    .cell-star { border: 2px solid #ffff00 !important; color: #ffff00; box-shadow: 0 0 10px #ffff00; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN SYSTEM (Admin Code: 2026) ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛰️ TITAN LOGIN</h2>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        pwd = st.text_input("Admin Key:", type="password")
        if st.button("HIDITRA"):
            if pwd == "2026":
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- 4. CORE ENGINE (Calcul Matanjaka) ---
def get_hash_jump(seed):
    # Jump miovaova arakaraka ny Hash
    h_hex = hashlib.md5(seed.encode()).hexdigest()
    return (int(h_hex[:1], 16) % 3) + 2 # Manome +2, +3, na +4

def titan_engine(seed, context, mode="cosmos"):
    signature = f"{seed}{context}TITAN_ULTRA_V85"
    h = hashlib.sha256(signature.encode()).hexdigest()
    random.seed(int(h[:16], 16))
    if mode == "cosmos":
        return round(random.uniform(2.15, 5.95), 2)
    else:
        # Lojika Mines 8/5
        count = 8 if "M12" in context else 5
        return random.sample(range(25), count)

# --- 5. MAIN INTERFACE ---
st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🛰️ TITAN V85.0 ULTRA-PRO</h2>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🚀 COSMOS (HASH-JUMP)", "💣 MINES 8/5", "📜 HISTORY"])

with t1:
    h_cos = st.text_input("Hash SHA512 Combined:")
    c1, c2 = st.columns(2)
    hex_val = c1.text_input("HEX (Last 8):")
    t_id = c2.text_input("Tour ID Farany:")
    
    if st.button("🔥 ANALYZE & SYNC"):
        if h_cos and t_id.isdigit():
            base_tour = int(t_id)
            jump = get_hash_jump(h_cos) # Jump arakaraka ny hash
            target = base_tour + jump
            
            val1 = titan_engine(h_cos, f"{hex_val}{target}", "cosmos")
            val2 = titan_engine(h_cos, f"{hex_val}{target+2}", "cosmos")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f'<div class="prediction-card"><span class="jump-tag">JUMP +{jump}</span><br><br><b>TARGET: {target}</b><h1>{val1}x</h1></div>', unsafe_allow_html=True)
            with col_b:
                st.markdown(f'<div class="prediction-card"><span class="jump-tag">NEXT</span><br><br><b>TARGET: {target+2}</b><h1>{val2}x</h1></div>', unsafe_allow_html=True)
            st.session_state.history.insert(0, f"T-{target}: {val1}x")

with t2:
    nb_m = st.select_slider("Mines:", options=[1, 2, 3], value=3)
    m1, m2 = st.columns(2)
    ms, mc = m1.text_input("Server Seed:"), m2.text_input("Client Seed:")
    
    if st.button("🔍 SCAN 8/5 DIAMANTS"):
        if ms and mc:
            m_ctx = "M12" if nb_m < 3 else "M3"
            safe = titan_engine(f"{ms}{mc}", m_ctx, "mines")
            grid = '<div class="mines-grid">'
            for i in range(25):
                is_s = i in safe
                grid += f'<div class="mine-cell {"cell-star" if is_s else ""}">{"⭐" if is_s else "⬛"}</div>'
            st.session_state.mines_grid = grid + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)

with t3:
    for h in st.session_state.history[:10]: st.write(f"✅ {h}")
    if st.button("🗑️ RESET"):
        st.session_state.history = []
        st.rerun()
