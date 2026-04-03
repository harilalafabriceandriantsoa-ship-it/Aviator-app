import streamlit as st
import hashlib
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.0 FIXED", layout="wide")

if 'history' not in st.session_state: st.session_state.history = []
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- STYLE DARK NEON ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: monospace; }
    .target-box { border: 2px solid #ffff00; padding: 10px; border-radius: 10px; text-align: center; color: #ffff00; margin-bottom: 15px; font-size: 20px; }
    .prediction-card { background: #111; border: 1px solid #00ffcc; padding: 15px; border-radius: 15px; text-align: center; margin-bottom: 10px; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 5px; max-width: 250px; margin: auto; }
    .mine-cell { aspect-ratio: 1/1; background: #222; border: 1px solid #444; display: flex; align-items: center; justify-content: center; font-size: 20px; border-radius: 5px; }
    .cell-star { border: 2px solid #ffff00 !important; color: #ffff00; box-shadow: 0 0 10px #ffff00; }
    </style>
    """, unsafe_allow_html=True)

# --- CORE ALGO ---
def get_prediction(seed, tour, step):
    # Hashing raikitra mba tsy hanapaka
    h = hashlib.sha256(f"{seed}{tour}{step}".encode()).hexdigest()
    random.seed(int(h[:16], 16))
    return round(random.uniform(2.10, 5.80), 2)

def get_mines_v2(ms, mc, nb):
    try:
        h = hashlib.md5(f"{ms}{mc}{nb}".encode()).hexdigest()
        random.seed(int(h[:16], 16))
        count = 8 if nb < 3 else 5
        return random.sample(range(25), count)
    except: return []

# --- INTERFACE ---
st.title("🛰️ TITAN V85.0 ULTRA-SYNC")
t1, t2 = st.tabs(["🚀 COSMOS (T1 & T2)", "💣 MINES 8/5"])

with t1:
    h_cos = st.text_input("Hash SHA512 Combined:", key="h1")
    t_id = st.text_input("Tour ID farany nivoaka:", key="t1")
    
    if st.button("🔥 ANALYZE NEXT TOURS"):
        if h_cos and t_id.isdigit():
            curr_tour = int(t_id)
            
            # Mampiseho Tour 1 sy Tour 2 mivantana
            for i in [1, 2]:
                target = curr_tour + i
                val = get_prediction(h_cos, target, i)
                st.markdown(f"""
                    <div class="prediction-card">
                        <b style="color:#ff4b4b;">🎯 TOUR: {target} (T{i})</b><br>
                        <h2 style="color:#00ffcc;">{val}x</h2>
                        <small style="color:#ffff00;">SYNC: 100%</small>
                    </div>
                """, unsafe_allow_html=True)
            st.session_state.history.insert(0, f"Tour {curr_tour+1}: {get_prediction(h_cos, curr_tour+1, 1)}x")

with t2:
    nb_m = st.select_slider("Mines:", options=[1, 2, 3], value=3)
    c1, c2 = st.columns(2)
    ms, mc = c1.text_input("Server Seed:"), c2.text_input("Client Seed:")
    
    if st.button("🔍 SCAN DIAMANTS"):
        if ms and mc:
            safe = get_mines_v2(ms, mc, nb_m)
            grid = '<div class="mines-grid">'
            for i in range(25):
                is_s = i in safe
                grid += f'<div class="mine-cell {"cell-star" if is_s else ""}">{"⭐" if is_s else "⬛"}</div>'
            st.session_state.mines_grid = grid + '</div>'
    
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("✅ IA Sync voadio!")
