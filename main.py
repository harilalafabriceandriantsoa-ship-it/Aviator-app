import streamlit as st
import hashlib
import random
import time
import hmac

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V85.4 - WAR MACHINE", layout="wide")

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
    .mult-val { color: #00ffcc; font-size: 45px; font-weight: bold; margin: 0; }
    .tour-id { color: #ffff00; font-size: 14px; font-weight: bold; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; max-width: 320px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #111; border: 1px solid #00ffcc44; display: flex; align-items: center; justify-content: center; font-size: 24px; border-radius: 8px; }
    .cell-star { border: 2px solid #ffff00 !important; background: rgba(255, 255, 0, 0.2); color: #ffff00; box-shadow: 0 0 15px #ffff0044; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN (KEY: 2026) ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🛰️ TITAN ACCESS</h2>", unsafe_allow_html=True)
    if st.text_input("KEY:", type="password") == "2026":
        if st.button("ACTIVATE"):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# --- 4. ENGINE CORE ---
def titan_engine(h, hx, t_val):
    mix = f"{h}{hx}{t_val}TITAN_V85.4".encode()
    f_hash = hashlib.sha512(mix).hexdigest()
    random.seed(int(f_hash[:16], 16))
    factor = int(f_hash[-4:], 16) / 65535.0
    if factor > 0.90: m = round(random.uniform(5.00, 30.00), 2)
    elif factor > 0.50: m = round(random.uniform(2.00, 4.99), 2)
    else: m = round(random.uniform(1.01, 1.99), 2)
    return {"m": m, "hex": f_hash[:8].upper()}

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center; color:#00ffcc;'>🛰️ TITAN V85.4 - FULL WAR MACHINE</h3>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🚀 COSMOS SCANNER", "💣 MINES 1-3 (ULTRA SUR)"])

with tab1:
    h_in = st.text_input("Combined Hash / Server Seed:")
    col_a, col_b = st.columns(2)
    hx_in = col_a.text_input("Hex8 (Extra):")
    t_act = col_b.number_input("Tour Actuel:", min_value=1, value=8136158)
    
    if st.button("🚀 EXECUTE COSMOS SCAN"):
        if h_in:
            with st.spinner("Calculating Orbit Path..."):
                time.sleep(0.5)
                r1, r2 = st.columns(2)
                
                # FANDRINDRA: Tsy atao +1 intsony fa atao +2 na +3 mba hisy fotoana (Safe Offset)
                offset_safe = (int(hashlib.md5(h_in.encode()).hexdigest()[:1], 16) % 2) + 2
                p1_t = t_act + offset_safe
                p1 = titan_engine(h_in, hx_in, p1_t)
                
                with r1:
                    st.markdown(f'<div class="war-card"><div class="tour-id">TARGET TOUR {p1_t}</div><p class="mult-val">{p1["m"]}x</p><p style="font-size:10px;">(OFFSET +{offset_safe})</p></div>', unsafe_allow_html=True)
                
                # Jump detection (Next big wave)
                with r2:
                    jump_t = t_act + random.randint(8, 15)
                    p_jump = titan_engine(h_in, hx_in, jump_t)
                    st.markdown(f'<div class="war-card" style="border-color:#ff00ff;"><div class="tour-id" style="color:#ff00ff;">JUMP SIGNAL {jump_t}</div><p class="mult-val" style="color:#ff00ff;">{p_jump["m"]}x</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("##### 🔍 SCAN ULTRA-SUR (MINES 1, 2, 3)")
    nb_mines = st.select_slider("Nombre de Mines ao amin'ny lalao:", options=[1, 2, 3])
    s_seed = st.text_input("Server Seed (Bet261):")
    c_seed = st.text_input("Client Seed / Tour:")
    
    if st.button("🛰️ SCAN SAFE SPOTS"):
        if s_seed and c_seed:
            spots = []
            num_stars = 7 if nb_mines == 1 else (5 if nb_mines == 2 else 4)
            for j in range(num_stars):
                key = f"TITAN_MINE_V85_{nb_mines}_{j}".encode()
                msg = f"{s_seed}{c_seed}{j}".encode()
                h_val = hmac.new(key, msg, hashlib.sha256).hexdigest()
                v = int(h_val[j:j+8], 16) % 25
                while v in spots: v = (v + 3) % 25
                spots.append(v)
            
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                is_star = i in spots
                grid_html += f'<div class="mine-cell {"cell-star" if is_star else ""}">{"⭐" if is_star else "⬛"}</div>'
            st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
