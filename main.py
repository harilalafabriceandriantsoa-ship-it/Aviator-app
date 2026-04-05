import streamlit as st
import hashlib
import random
import hmac

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V86.3 - ULTRA HYBRID", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE (CLASSIC WAR) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 330px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #0a0a0a; border: 1px solid #00ffcc44; display: flex; align-items: center; justify-content: center; font-size: 28px; border-radius: 12px; }
    .cell-star { border: 2px solid #ffff00 !important; background: rgba(255, 255, 0, 0.25); color: #ffff00; box-shadow: 0 0 25px #ffff0088; transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN (KEY: 2026) ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛰️ TITAN HYBRID ACCESS</h2>", unsafe_allow_html=True)
    if st.text_input("ENTER MASTER KEY:", type="password") == "2026":
        if st.button("ACTIVATE SYSTEM"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. HYBRID HASH CALCULATOR (SERVER + CLIENT + ID) ---
def hybrid_pattern_calc(s_seed, c_seed, t_id, salt, iterations=20000):
    """Kajy manambatra ny singa 3 (Server, Client, ID) ho lasa Schema iray"""
    # Atambatra ny singa rehetra mba ho mafy ny encryption
    combined_input = f"{s_seed}{c_seed}{t_id}"
    h = hmac.new(f"HYBRID_{salt}".encode(), combined_input.encode(), hashlib.sha512).digest()
    for i in range(iterations):
        h = hmac.new(h, f"STEP_{i}".encode(), hashlib.sha512).digest()
    return h.hex()

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center;'>🛰️ TITAN V86.3 - ULTRA HYBRID</h3>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🚀 COSMOS SCANNER", "💣 MINES HYBRID (5 STARS)"])

with tab1:
    h_in = st.text_input("Server Seed / Hash:")
    col_1, col_2 = st.columns(2)
    hx_in = col_1.text_input("Hex8 / Extra:")
    t_act = col_2.number_input("Tour Actuel:", min_value=1, value=8136400)
    
    if st.button("🚀 EXECUTE COSMOS SCAN"):
        if h_in:
            with st.spinner("Deep Scan (10,000 passes)..."):
                off = (int(hashlib.md5(h_in.encode()).hexdigest()[:1], 16) % 2) + 2
                res_hash = hybrid_pattern_calc(h_in, hx_in, t_act+off, "COSMOS")
                random.seed(int(res_hash[:16], 16))
                f = int(res_hash[-12:], 16) / 281474976710655.0
                m = round(random.uniform(15.0, 80.0), 2) if f > 0.95 else round(random.uniform(1.01, 5.0), 2)
                st.markdown(f'<div style="text-align:center; border:2px solid #00ffcc; padding:10px; border-radius:10px;">TARGET TOUR {t_act+off}<br><span style="font-size:40px; color:#00ffcc;">{m}x</span></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("##### 🛡️ MINES 1-3: 5 STARS (ID + SEEDS MODE)")
    st.info("Ity version ity dia manambatra ny Seed Server, Seed Client, ary ny ID.")
    nb_m = st.selectbox("Isan'ny Mines:", [1, 2, 3], index=2)
    
    col_a, col_b = st.columns(2)
    s_s = col_a.text_input("Server Seed (SHA256):")
    c_s = col_b.text_input("Client Seed:")
    t_id = st.text_input("ID Partie (ID manaraka):")
    
    if st.button("🛰️ SCAN FOR HYBRID SCHEMA"):
        if s_s and c_s and t_id:
            spots = []
            with st.spinner("Calculating Hybrid Schema..."):
                # Kajy manambatra ny singa 3 (20.000 iterations)
                main_hash = hybrid_pattern_calc(s_s, c_s, t_id, f"HYBRID_V86_{nb_m}")
                
                # Legacy Schema Logic (tsy novaina)
                step = int(main_hash[-2:], 16) % 5 + 1
                start_pos = int(main_hash[:2], 16) % 25
                
                for j in range(5):
                    pos = (start_pos + (j * step)) % 25
                    while pos in spots:
                        pos = (pos + 1) % 25
                    spots.append(pos)
                
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    grid_html += f'<div class="mine-cell {"cell-star" if i in spots else ""}">{"⭐" if i in spots else "⬛"}</div>'
                st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("HYBRID PREDICTION LOCKED - 5 STARS READY")
