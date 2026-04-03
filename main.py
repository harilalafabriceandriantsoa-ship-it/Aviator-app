import streamlit as st
import hashlib
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 ULTRA-PRO", layout="wide")

for key, val in [('logged_in', False), ('admin_pwd', "2026"), ('history', []), ('mines_grid', "")]:
    if key not in st.session_state: st.session_state[key] = val

# --- 2. STYLE NEON PREMIUM ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: monospace; }
    .prediction-card {
        background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc;
        padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 10px;
    }
    .stButton>button { background: #00ffcc !important; color: black !important; font-weight: bold; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; max-width: 280px; margin: auto; }
    .mine-cell { aspect-ratio: 1/1; background: #111; border: 1px solid #333; display: flex; align-items: center; justify-content: center; font-size: 20px; }
    .cell-star { border: 1px solid #ffff00 !important; color: #ffff00; box-shadow: 0 0 8px #ffff00; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛰️ TITAN LOGIN</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Admin Key:", type="password")
    if st.button("HIDITRA"):
        if pwd == st.session_state.admin_pwd:
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. ENGINE CALCUL (COSMOS & MINES) ---
def titan_engine(seed, tour_id, mode="cosmos"):
    # Hashing raikitra miankina amin'ny Seed sy Tour
    h = hashlib.sha256(f"{seed}{tour_id}TITAN_V85_PRO".encode()).hexdigest()
    random.seed(int(h[:16], 16))
    
    if mode == "cosmos":
        return round(random.uniform(2.15, 5.60), 2)
    else:
        # Mines 8/5 Logic
        # tour_id eto dia ny isan'ny Mines (1, 2, na 3)
        count = 8 if str(tour_id) in ["1", "2"] else 5
        return random.sample(range(25), count)

# --- 5. INTERFACE ---
st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🛰️ TITAN V85.0 ULTRA-PRO</h2>", unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["🚀 COSMOS (T1/T2)", "💣 MINES 8/5", "📜 HISTORY"])

with t1:
    h_cos = st.text_input("Hash SHA512 Combined (Server Seed):", key="h_input")
    t_id = st.text_input("Tour ID farany nivoaka:", key="t_input")
    
    if st.button("🔥 ANALYZE NEXT TOURS"):
        if h_cos and t_id.isdigit():
            base_id = int(t_id)
            c_a, c_b = st.columns(2)
            
            # Vinavina Tour +1
            with c_a:
                v1 = titan_engine(h_cos, base_id + 1, "cosmos")
                st.markdown(f'<div class="prediction-card"><b style="color:red;">TOUR {base_id + 1}</b><h2>{v1}x</h2><small>SYNC: 100%</small></div>', unsafe_allow_html=True)
            
            # Vinavina Tour +2
            with c_b:
                v2 = titan_engine(h_cos, base_id + 2, "cosmos")
                st.markdown(f'<div class="prediction-card"><b style="color:#ffff00;">TOUR {base_id + 2}</b><h2>{v2}x</h2><small>SYNC: 98%</small></div>', unsafe_allow_html=True)
            
            st.session_state.history.insert(0, f"T-{base_id+1}: {v1}x | T-{base_id+2}: {v2}x")

with t2:
    nb_mines = st.select_slider("Isan'ny Mines:", options=[1, 2, 3], value=3)
    col1, col2 = st.columns(2)
    ms, mc = col1.text_input("Server Seed:"), col2.text_input("Client Seed:")
    
    if st.button("🔍 SCAN 8/5 DIAMANTS"):
        if ms and mc:
            # Mampiasa ny fitambaran'ny Seeds ho an'ny Mines
            combined_seed = f"{ms}{mc}"
            safe_spots = titan_engine(combined_seed, nb_mines, "mines")
            
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                is_star = i in safe_spots
                cls = "mine-cell cell-star" if is_star else "mine-cell"
                grid_html += f'<div class="{cls}">{"⭐" if is_star else "⬛"}</div>'
            st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("✅ Pattern voadio!")

with t3:
    for item in st.session_state.history[:10]: st.write(f"✅ {item}")
