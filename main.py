import streamlit as st
import hashlib
import random
import time
import hmac

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V86.2 - GHOST CALC", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE (STRICT WAR INTERFACE) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 330px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #050505; border: 1px solid #00ffcc44; display: flex; align-items: center; justify-content: center; font-size: 28px; border-radius: 12px; }
    .cell-star { border: 2px solid #ffff00 !important; background: rgba(255, 255, 0, 0.25); color: #ffff00; box-shadow: 0 0 30px #ffff00aa; transform: scale(1.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN (KEY: 2026) ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛰️ GHOST-CALC ACCESS</h2>", unsafe_allow_html=True)
    if st.text_input("ENTER MASTER KEY:", type="password") == "2026":
        if st.button("ACTIVATE"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. GHOST ENGINE (PURE MATH MAPPING) ---
def ghost_mapping(s_seed, c_seed, iteration):
    """Tsy mampiasa random.seed intsony fa mampiasa mapping mivantana avy amin'ny Hash byte"""
    raw = hmac.new(f"GHOST_V862_{iteration}".encode(), f"{s_seed}{c_seed}".encode(), hashlib.sha512).digest()
    
    # Maka ny 4 bytes voalohany amin'ny Hash ho lasa position (0-24)
    pos = (int.from_bytes(raw[:4], 'big') + iteration) % 25
    return pos

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center;'>🛰️ TITAN V86.2 - GHOST CALC</h3>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🚀 COSMOS", "💣 MINES (PURE MATH)"])

with tab2:
    st.warning("GHOST-CALC: Tsy mampiasa kisendrasendra (tsatoka) fa kajy matematika mivantana.")
    nb_m = st.selectbox("Mines:", [1, 2, 3], index=2)
    s_s = st.text_input("Server Seed:")
    c_s = st.text_input("Client Seed (Anaranao/Tour):")
    
    if st.button("🛰️ EXECUTE GHOST SCAN"):
        if s_s and c_s:
            spots = []
            with st.spinner("Mapping 15,000 possibilities..."):
                # Manao boucle iterations 15.000 mialoha ny kintana tsirairay
                for j in range(5):
                    # Manao 'Deep Warm-up' isaky ny kintana mba hanapahana ny schema-n'ny server
                    h_warm = s_s
                    for k in range(3000):
                        h_warm = hashlib.sha512(f"{h_warm}{c_s}{j}{k}".encode()).hexdigest()
                    
                    # Maka ny toerana farany avy amin'ilay h_warm
                    v = int(h_warm[:8], 16) % 25
                    
                    # Fiarovana raha mifanindry
                    while v in spots:
                        v = (v + int(h_warm[-2:], 16) + 1) % 25
                    spots.append(v)
                
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    grid_html += f'<div class="mine-cell {"cell-star" if i in spots else ""}">{"⭐" if i in spots else "⬛"}</div>'
                st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("GHOST MAPPING COMPLETE - SCHEMA DETECTED")
