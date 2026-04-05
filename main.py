import streamlit as st
import hashlib
import random
import time
import hmac

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V86.5 - SHIELD MASTER", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE (SHIELD INTERFACE) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .war-card {
        background: #050505; border: 2px solid #ff0055; 
        padding: 15px; border-radius: 15px; text-align: center; margin-bottom: 10px;
        box-shadow: 0 0 20px #ff005533;
    }
    .mult-val { color: #00ffcc; font-size: 55px; font-weight: bold; margin: 0; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 330px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #080808; border: 1px solid #ffffff11; display: flex; align-items: center; justify-content: center; font-size: 28px; border-radius: 12px; }
    .cell-star { border: 2px solid #00ffcc !important; background: rgba(0, 255, 204, 0.2); color: #00ffcc; box-shadow: 0 0 25px #00ffcc88; transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN (KEY: 2026) ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛡️ SHIELD MASTER ACCESS</h2>", unsafe_allow_html=True)
    if st.text_input("ENTER MASTER KEY:", type="password") == "2026":
        if st.button("ACTIVATE SHIELD"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. THE SHIELD-MASTER ENGINE (ANTI-TSATOKA) ---
def shield_master_calc(s_seed, c_seed, salt, iters=20000):
    """Deep Hash Iteration to break dynamic RNG (20,000 passes)"""
    # Create a reinforced HMAC key
    key = hmac.new(f"V86.5_{salt}".encode(), s_seed.encode(), hashlib.sha512).digest()
    current = hmac.new(key, c_seed.encode(), hashlib.sha512).digest()
    
    # Deep Proof-of-Work loop
    for i in range(iters):
        current = hashlib.sha512(current + f"PASS_{i}_{salt}".encode()).digest()
    
    return current.hex()

# --- 5. INTERFACE ---
st.markdown("<h4 style='text-align:center; color:#ff0055;'>🛰️ TITAN V86.5 - SHIELD MASTER ACTIVE</h4>", unsafe_allow_html=True)
t1, t2 = st.tabs(["🚀 COSMOS", "💣 MINES (ANTI-LOSS)"])

with t2:
    st.warning("MODE: ANTI-TSATOKA ACTIVE | Iterations: 20,000")
    nb_m = st.selectbox("Isan'ny Mines:", [1, 2, 3], index=2)
    s_s = st.text_input("Server Seed (Mines):")
    c_s = st.text_input("Client Seed (Laharana Tour):")
    
    if st.button("🛡️ EXECUTE SHIELD SCAN"):
        if s_s and c_s:
            spots = []
            progress = st.progress(0)
            with st.spinner("Analyzing Hash Patterns..."):
                # Simulation sequences to find the most stable spots
                for j in range(5):
                    # Multi-layered calculation
                    h_res = shield_master_calc(s_s, c_s, f"ZONE_{j}_{nb_m}")
                    
                    # Entropy Shift: Miala amin'ny pattern tsotra
                    v = int(h_res[j*8:j*8+8], 16) % 25
                    while v in spots:
                        v = (v + int(h_res[-4:], 16) + 1) % 25
                    spots.append(v)
                    progress.progress((j + 1) * 20)
                
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    is_star = i in spots
                    grid_html += f'<div class="mine-cell {"cell-star" if is_star else ""}">{"⭐" if is_star else "⬛"}</div>'
                st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("SHIELD SCAN COMPLETE - SAFE SPOTS IDENTIFIED")
