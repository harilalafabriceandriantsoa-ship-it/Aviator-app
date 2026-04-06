import streamlit as st
import hashlib
import random
import hmac

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V86.5 - MACHINE DE MORT", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE (WAR INTERFACE) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 330px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #0a0a0a; border: 1px solid #00ffcc44; display: flex; align-items: center; justify-content: center; font-size: 28px; border-radius: 12px; }
    .cell-star { border: 2px solid #ff0000 !important; background: rgba(255, 0, 0, 0.2); color: #ff0000; box-shadow: 0 0 20px #ff0000; transform: scale(1.05); }
    .scan-box { border: 2px solid #00ffcc; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px; background: rgba(0, 255, 204, 0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN (KEY: 2026) ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>💀 TITAN MACHINE DE MORT</h2>", unsafe_allow_html=True)
    if st.text_input("ENTER MASTER KEY:", type="password") == "2026":
        if st.button("ACTIVATE LETHAL MODE"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. CORE ENGINE (SHA-512 LETHAL INJECTION) ---
def lethal_hash_engine(s_seed, c_seed, t_id, iterations=60000):
    """Algorithm SHA-512 mahery vaika mampiasa Iterations 60.000"""
    combined = f"{s_seed}:{c_seed}:{t_id}:DEATH_PROTOCOL_V86_FINAL"
    h = hmac.new(b"LETHAL_SHIELD_ULTRA", combined.encode(), hashlib.sha512).digest()
    for i in range(iterations):
        h = hmac.new(h, f"KILL_STEP_{i}".encode(), hashlib.sha512).digest()
    return h.hex()

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center;'>🛰️ TITAN V86.5 - MACHINE DE MORT</h3>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🚀 COSMOS (SAFE JUMP)", "💣 MINES (CHAOS SHUFFLE)"])

with tab1:
    st.markdown("##### 🛡️ SAFE RECOVERY MODE (JUMP +1 ACTIVE)")
    st.info("Ny Tour +1 dia misy fandrika. Ny scan dia manomboka any amin'ny Tour +2, +3, +4.")
    h_in = st.text_input("Server Seed / Hash:")
    col_1, col_2 = st.columns(2)
    hx_in = col_1.text_input("Hex8 / Extra:")
    t_act = col_2.number_input("Tour Actuel:", min_value=1, value=8137473)
    
    if st.button("🚀 EXECUTE LETHAL COSMOS SCAN"):
        if h_in:
            with st.spinner("Calculating Trajectory..."):
                # SAFE JUMP: Manomboka amin'ny i=2 (Tour +2) fa tsy i=1
                for i in range(2, 5): 
                    target_t = t_act + i
                    res_hash = lethal_hash_engine(h_in, hx_in, target_t, 60000)
                    
                    random.seed(int(res_hash[:16], 16))
                    f = int(res_hash[-12:], 16) / 281474976710655.0
                    
                    if f > 0.94:
                        m = round(random.uniform(8.0, 100.0), 2)
                        color = "#ff0000" # Rose/Red (High)
                    elif f > 0.70:
                        m = round(random.uniform(2.0, 7.99), 2)
                        color = "#ffff00" # Violet/Yellow (Medium)
                    else:
                        m = round(random.uniform(1.01, 1.99), 2)
                        color = "#00ffcc" # Blue (Low)
                    
                    st.markdown(f"""
                        <div class="scan-box" style="border-color: {color};">
                            <span style="color:#aaa;">TARGET TOUR {target_t}</span><br>
                            <span style="font-size:35px; color:{color}; font-weight:bold;">{m}x</span>
                        </div>
                    """, unsafe_allow_html=True)

with tab2:
    st.markdown("##### 🛡️ MINES ULTRA-LOGIC (LETHAL SHUFFLE)")
    st.info("Algorithm Fisher-Yates miorina amin'ny Hash SHA-512 (60k iterations).")
    nb_m = st.selectbox("Isan'ny Mines:", [1, 2, 3], index=2)
    
    col_a, col_b = st.columns(2)
    s_s = col_a.text_input("Server Seed (SHA256):")
    c_s = col_b.text_input("Client Seed:")
    t_id = st.text_input("ID Partie:")
    
    if st.button("🛰️ SCAN FOR LETHAL SCHEMA"):
        if s_s and c_s and t_id:
            with st.spinner("Engaging Chaos Logic..."):
                # 60.000 Iterations SHA-512
                main_hash = lethal_hash_engine(s_s, c_s, t_id, 60000)
                
                # Fisher-Yates Shuffle miorina amin'ny Hash
                grid = list(range(25))
                hash_int = int(main_hash, 16)
                for i in range(24, 0, -1):
                    j = hash_int % (i + 1)
                    grid[i], grid[j] = grid[j], grid[i]
                    hash_int //= (i + 1)
                
                spots = grid[:5]
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    grid_html += f'<div class="mine-cell {"cell-star" if i in spots else ""}">{"⭐" if i in spots else "⬛"}</div>'
                st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("DEATH PROTOCOL ACTIVATED - SCHEMA LOCKED")
