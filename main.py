import streamlit as st
import hashlib
import random
import time
import hmac

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.3 - FULL WAR MACHINE", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'mines_grid' not in st.session_state: st.session_state.mines_grid = ""

# --- 2. STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ffcc; font-family: 'Courier New', monospace; }
    .war-card {
        background: #0a0a0a; border: 2px solid #00ffcc; 
        padding: 15px; border-radius: 15px; text-align: center; margin-bottom: 10px;
    }
    .jump-card { border-color: #ff00ff; box-shadow: 0 0 15px #ff00ff33; }
    .mult-val { color: #00ffcc; font-size: 50px; font-weight: bold; margin: 0; line-height: 1.1; }
    .tour-id { color: #ffff00; font-size: 14px; font-weight: bold; margin-bottom: 5px; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 5px; max-width: 300px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #111; border: 1px solid #00ffcc44; display: flex; align-items: center; justify-content: center; font-size: 22px; border-radius: 6px; }
    .cell-star { border: 2px solid #ffff00 !important; background: rgba(255, 255, 0, 0.15); color: #ffff00; box-shadow: 0 0 10px #ffff0033; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN (ETO ILAY CODE KEY) ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛰️ TITAN ACCESS</h2>", unsafe_allow_html=True)
    # Ny KEY dia: 2026
    access_key = st.text_input("ENTER KEY TO ACTIVATE TITAN:", type="password")
    if access_key == "2026":
        if st.button("ACTIVATE MACHINE"):
            st.session_state.logged_in = True
            st.rerun()
    elif access_key != "":
        st.error("KEY DISCORDANT - ACCESS DENIED")
    st.stop()

# --- 4. ENGINE CORE ---
def titan_core_v85(h, hx, t_val):
    mix_seed = f"{h}{hx}{t_val}TITAN_WAR_V85.3".encode()
    f_hash = hashlib.sha512(mix_seed).hexdigest()
    random.seed(int(f_hash[:16], 16))
    hex_factor = int(f_hash[-4:], 16) / 65535.0
    if hex_factor > 0.86: m = round(random.uniform(4.50, 25.00), 2)
    elif hex_factor > 0.48: m = round(random.uniform(1.85, 4.49), 2)
    else: m = round(random.uniform(1.01, 1.84), 2)
    return {"m": m, "hex": f_hash[:8].upper()}

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.3 - FULL WAR MACHINE</h3>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🚀 COSMOS SCANNER", "💣 MINES DEEP-SCAN"])

with tab1:
    h_in = st.text_input("Combined Hash / Server Seed:")
    col_a, col_b = st.columns(2)
    hx_in = col_a.text_input("Hex8 (Extra):")
    t_act = col_b.number_input("Tour Actuel:", min_value=1, value=8136111)
    
    if st.button("🚀 EXECUTE COSMOS SCAN"):
        if h_in:
            with st.spinner("Analyzing Orbits..."):
                time.sleep(0.7)
                r1, r2 = st.columns(2)
                # Offset Dynamic (+1 hatramin'ny +3)
                offset_1 = (int(hashlib.md5(h_in.encode()).hexdigest()[:1], 16) % 3) + 1
                p1_t = t_act + offset_1
                p1 = titan_core_v85(h_in, hx_in, p1_t)
                with r1:
                    st.markdown(f'<div class="war-card"><div class="tour-id">PREDICTION TOUR {p1_t}</div><p class="mult-val">{p1["m"]}x</p><p style="color:#00ffcc; font-size:10px;">HEX8: {p1["hex"]}</p></div>', unsafe_allow_html=True)
                
                # JUMP Detection (Non-Fixed)
                possible_jumps = []
                for i in range(t_act + 4, t_act + 20):
                    res = titan_core_v85(h_in, hx_in, i)
                    if res['m'] >= 2.90: possible_jumps.append((i, res))
                with r2:
                    if possible_jumps:
                        random.seed(int(hashlib.sha256(h_in.encode()).hexdigest()[:8], 16))
                        final_j = random.choice(possible_jumps)
                        st.markdown(f'<div class="war-card jump-card"><div class="tour-id" style="color:#ff00ff;">PREDICTION TOUR {final_j[0]}</div><p class="mult-val" style="color:#ff00ff;">{final_j[1]["m"]}x</p><p style="color:#ff00ff; font-size:10px;">HEX8: {final_j[1]["hex"]}</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("##### 🔍 MINES RECURSIVE (6-STAR SIGNAL)")
    s_seed = st.text_input("Server Seed (Mines):")
    c_seed = st.text_input("Client Seed / Tour Num:")
    
    if st.button("🛰️ SCAN FOR SAFE SPOTS"):
        if s_seed and c_seed:
            spots = []
            for j in range(6):
                key = f"TITAN_MINE_V85_{j}".encode()
                msg = f"{s_seed}{c_seed}{j}".encode()
                h_val = hmac.new(key, msg, hashlib.sha256).hexdigest()
                v = int(h_val[j:j+8], 16) % 25
                while v in spots:
                    v = (v + int(h_val[-2:], 16) + 1) % 25
                spots.append(v)
            
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                is_star = i in spots
                grid_html += f'<div class="mine-cell {"cell-star" if is_star else ""}">{"⭐" if is_star else "⬛"}</div>'
            st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
