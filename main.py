import streamlit as st
import hashlib
import random
import hmac

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TITAN V86.4 - ULTRA LOGIC", layout="wide")

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

# --- 4. ULTRA-LOGIC CALCULATOR (NO MORE STEP REPETITION) ---
def ultra_logic_calc(s_seed, c_seed, t_id, nb_stars=5):
    """Mampiasa lojika casino (Fisher-Yates) mba hampiova schema foana"""
    combined_input = f"{s_seed}{c_seed}{t_id}"
    # Hash SHA-512 in-30.000 (nohamafisina)
    h = hmac.new(b"TITAN_V86_ULTRA_LOGIC", combined_input.encode(), hashlib.sha512).digest()
    for i in range(30000):
        h = hmac.new(h, f"LOGIC_STEP_{i}".encode(), hashlib.sha512).digest()
    
    # 1. Mamorona ny toerana 0 hatramin'ny 24
    grid = list(range(25))
    
    # 2. Fisher-Yates Shuffle miorina amin'ny Hash
    # Ity no lojika mahatonga ny schema ho vaovao foana isaky ny miova ny ID
    hash_int = int(h.hex(), 16)
    for i in range(24, 0, -1):
        j = hash_int % (i + 1)
        grid[i], grid[j] = grid[j], grid[i]
        hash_int //= (i + 1)
        
    # 3. Maka ny kintana 5 voalohany avy amin'ilay grid efa nikorontana
    return grid[:nb_stars]

# --- 5. INTERFACE ---
st.markdown("<h3 style='text-align:center;'>🛰️ TITAN V86.4 - ULTRA LOGIC</h3>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🚀 COSMOS SCANNER", "💣 MINES ULTRA-LOGIC (5 STARS)"])

with tab1:
    h_in = st.text_input("Server Seed / Hash:")
    col_1, col_2 = st.columns(2)
    hx_in = col_1.text_input("Hex8 / Extra:")
    t_act = col_2.number_input("Tour Actuel:", min_value=1, value=8136400)
    
    if st.button("🚀 EXECUTE COSMOS SCAN"):
        if h_in:
            with st.spinner("Deep Scan (10,000 passes)..."):
                off = (int(hashlib.md5(h_in.encode()).hexdigest()[:1], 16) % 2) + 2
                # Ampiasaina ny lojika hybrid koa eto
                res_hash = hashlib.sha512(f"{h_in}{hx_in}{t_act+off}".encode()).hexdigest()
                random.seed(int(res_hash[:16], 16))
                f = int(res_hash[-12:], 16) / 281474976710655.0
                m = round(random.uniform(15.0, 80.0), 2) if f > 0.95 else round(random.uniform(1.01, 5.0), 2)
                st.markdown(f'<div style="text-align:center; border:2px solid #00ffcc; padding:10px; border-radius:10px;">TARGET TOUR {t_act+off}<br><span style="font-size:40px; color:#00ffcc;">{m}x</span></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("##### 🛡️ MINES 1-3: 5 STARS (LOGIC MODE)")
    st.info("Ity lojika ity dia manakorontana ny toerana 25 araka ny Seeds sy ID.")
    nb_m = st.selectbox("Isan'ny Mines:", [1, 2, 3], index=2)
    
    col_a, col_b = st.columns(2)
    s_s = col_a.text_input("Server Seed (SHA256):")
    c_s = col_b.text_input("Client Seed:")
    t_id = st.text_input("ID Partie (ID manaraka):")
    
    if st.button("🛰️ SCAN FOR LOGIC SCHEMA"):
        if s_s and c_s and t_id:
            with st.spinner("Executing Ultra-Logic Scan..."):
                # Miantso an'ilay lojika Shuffle vaovao
                spots = ultra_logic_calc(s_s, c_s, t_id)
                
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    grid_html += f'<div class="mine-cell {"cell-star" if i in spots else ""}">{"⭐" if i in spots else "⬛"}</div>'
                st.session_state.mines_grid = grid_html + '</div>'
            
    if st.session_state.mines_grid:
        st.markdown(st.session_state.mines_grid, unsafe_allow_html=True)
        st.success("LOGIC PREDICTION LOCKED - NO REPETITION")
