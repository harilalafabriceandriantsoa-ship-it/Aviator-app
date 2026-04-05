import streamlit as st
import hashlib
import random
import time
import hmac

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.9 - BUNKER MODE", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE (BUNKER INTERFACE) ---
st.markdown("""
    <style>
    .stApp { background-color: #010101; color: #00ffcc; font-family: 'Courier New', monospace; }
    .war-card {
        background: #0a0a0a; border: 2px solid #00ffcc; 
        padding: 15px; border-radius: 15px; text-align: center; margin-bottom: 10px;
    }
    .mult-val { color: #00ffcc; font-size: 50px; font-weight: bold; margin: 0; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 330px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #0c0c0c; border: 1px solid #00ffcc22; display: flex; align-items: center; justify-content: center; font-size: 28px; border-radius: 12px; }
    .cell-star { border: 2px solid #ffff00 !important; background: rgba(255, 255, 0, 0.3); color: #ffff00; box-shadow: 0 0 20px #ffff0066; font-weight: bold; transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN (KEY: 2026) ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛰️ TITAN BUNKER ACCESS</h2>", unsafe_allow_html=True)
    if st.text_input("ENTER MASTER KEY:", type="password") == "2026":
        if st.button("ACTIVATE BUNKER"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. THE BUNKER CORE (ULTRA-SÛR) ---
def bunker_engine(s_seed, c_seed, t_val):
    # Triple-Layer SHA512
    l1 = hmac.new(f"BUNKER_V9_{t_val}".encode(), s_seed.encode(), hashlib.sha512).hexdigest()
    l2 = hmac.new(c_seed.encode(), l1.encode(), hashlib.sha512).hexdigest()
    random.seed(int(l2[:16], 16))
    return l2

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.9 - BUNKER MODE</h3>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🚀 COSMOS SCANNER", "💣 MINES 1-3 (5 STARS BUNKER)"])

with tab1:
    h_in = st.text_input("Server Seed / Hash:")
    col_1, col_2 = st.columns(2)
    hx_in = col_1.text_input("Hex8 / Extra:")
    t_act = col_2.number_input("Tour Actuel:", min_value=1, value=8136300)
    
    if st.button("🚀 EXECUTE BUNKER SCAN"):
        if h_in:
            with st.spinner("Analyzing Orbits..."):
                time.sleep(0.5)
                # Offset +2/+3 mba tsy ho tratra
                off = (int(hashlib.md5(h_in.encode()).hexdigest()[:1], 16) % 2) + 2
                res_hash = bunker_engine(h_in, hx_in, t_act + off)
                random.seed(int(res_hash[:16], 16))
                f = int(res_hash[-8:], 16) / 4294967295.0
                if f > 0.94: m = round(random.uniform(15.0, 70.0), 2)
                elif f > 0.45: m = round(random.uniform(2.5, 9.9), 2)
                else: m = round(random.uniform(1.01, 2.4), 2)
                st.markdown(f'<div class="war-card"><div>TARGET TOUR {t_act+off}</div><p class="mult-val">{m}x</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("##### 🛡️ MINES 1-3: 5 STARS (BUNKER PROTECTED)")
    st.info("Configuration: 5 Stars Fixed | Risk: Minimum")
    nb_mines = st.selectbox("Isan'ny Mines:", [1, 2, 3], index=2)
    s_s = st.text_input("Server Seed (Mines):")
    c_s = st.text_input("Client Seed (Laharana Tour):")
    
    if st.button("🛰️ SCAN 5 BUNKER SPOTS"):
        if s_s and c_s:
            spots = []
            h_shield = bunker_engine(s_s, c_s, nb_mines)
            for j in range(5):
                # Natao "Recursive Shift" mba tsy ho hita pattern
                v = int(h_shield[j*4:j*4+8], 16) % 25
                while v in spots:
                    v = (v + int(h_shield[-2:], 16) + 1) % 25
                spots.append(v)
            
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                grid_html += f'<div class="mine-cell {"cell-star" if i in spots else ""}">{"⭐" if i in spots else "⬛"}</div>'
            st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("5 BUNKER SPOTS DETECTED - PROCEED WITH CAUTION")
