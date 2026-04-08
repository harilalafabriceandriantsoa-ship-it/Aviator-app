import streamlit as st
import hashlib, hmac, random, datetime, statistics

# --- CONFIGURATION ---
LOGIN_KEY = "2026"
st.set_page_config(page_title="TITAN V100 ULTRA STYLÉ", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0f0f, #1a1a1a);
        color: #00ffcc;
        font-family: 'Courier New', monospace;
    }
    h2, h3, h4, h5 {
        color: #00ffcc;
        text-shadow: 0 0 10px #00ffcc;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #0066ff);
        color: #fff;
        border-radius: 12px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0 0 20px #00ffcc;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #0066ff, #00ffcc);
        box-shadow: 0 0 30px #0066ff;
    }
    .mines-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 10px;
        max-width: 330px;
        margin: auto;
        padding: 20px;
    }
    .mine-cell {
        aspect-ratio: 1/1;
        background: #111;
        border: 1px solid #00ffcc44;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        border-radius: 12px;
        transition: 0.3s;
    }
    .cell-star {
        border: 2px solid #00d4ff !important;
        background: rgba(0, 212, 255, 0.3) !important;
        color: #00d4ff;
        box-shadow: 0 0 30px #00d4ff;
    }
    </style>
""", unsafe_allow_html=True)

# --- COSMOS ENGINE ---
def cosmosultraengine(server_seed, client_seed, tour_id, salt, heure=None, iters=250000):
    if heure is None:
        heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{server_seed}:{client_seed}:{tour_id}:{salt}:{heure}:COSMOSXV100"
    
    h1 = hmac.new(b"COSMOS_CORE", base.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h1 = hmac.new(h1, f"STEP_{i}".encode(), hashlib.sha512).digest()
    
    blake = hashlib.blake2b(h1).digest()
    sha3 = hashlib.sha3_256(blake).digest()
    final = bytes(a ^ b ^ c for a, b, c in zip(h1[:32], blake[:32], sha3))
    hex_out = final.hex()

    p_int = int(hex_out[:16], 16)
    offset = (p_int % 29) + (9 if salt == "T1" else 15)
    jumps = [(p_int % 7) + 2, (p_int % 11) + 3, (p_int % 13) + 4]

    dec_val = int(hex_out[-8:], 16)
    cote = (4294967295 * 0.97) / dec_val if dec_val > 0 else 1.0
    cote = round(max(cote, 1.0), 2)

    values = [offset] + jumps
    return {
        "tour": tour_id + offset, "cote": cote, "jumps": jumps,
        "min": min(values), "max": max(values), "mean": round(statistics.mean(values),2),
        "accuracy": round((statistics.mean(values)/max(values))*100, 2), "hex": hex_out
    }

# --- MINES ENGINE ---
def minesultraengine(serverseed, clientseed, nonce, heure=None, iters=250000):
    if heure is None:
        heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{serverseed}:{clientseed}:{nonce}:{heure}:MINESV100"
    
    h_mut = hashlib.sha512(base.encode()).digest()
    for i in range(iters):
        h_mut = hashlib.sha512(h_mut + f"S{i}".encode()).digest()

    random.seed(int.from_bytes(h_mut[:16], "big"))
    grid = list(range(25))
    random.shuffle(grid)
    return sorted(grid[:5]) # Diamants 5 foana

# --- LOGIN SYSTEM ---
st.markdown("<h2 style='text-align:center;'>🔐 TITAN V100 ULTRA</h2>", unsafe_allow_html=True)
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    admininput = st.text_input("Enter Admin Code:", type="password")
    if st.button("ACTIVATE"):
        if admininput == LOGIN_KEY:
            st.session_state.auth = True
            st.rerun()
        else: st.error("Code diso!")
else:
    tab1, tab2 = st.tabs(["🌌 COSMOSX", "💣 MINES ULTRA"])

    with tab1:
        st.markdown("##### 🌌 COSMOSX ANALYSIS")
        hv = st.text_input("Server Seed:", value="d17354bbdbbdbfefb1ef2d210fb3ea2c3aeb4e6be5c27ac08a3e49b49fdf0b91", key="c_h")
        xv = st.text_input("Client Seed:", value="SaSd3AAerLJrfAw053Bf", key="c_x")
        tv = st.number_input("Tour Actuel:", min_value=1, value=8147979)
        ch = st.text_input("Heure:", value=datetime.datetime.now().strftime("%H:%M:%S"))
        
        if st.button("🚀 SCAN COSMOS"):
            for s in ["T1", "T2"]:
                res = cosmosultraengine(hv, xv, tv, s, ch)
                st.info(f"**{s}** | Tour: {res['tour']} | Côte: {res['cote']}x | Acc: {res['accuracy']}%")
                st.write(f"Metrics: Min({res['min']}) Moyen({res['mean']}) Max({res['max']})")

    with tab2:
        st.markdown("##### 💣 MINES SCANNER (Slider 1-7)")
        ms = st.text_input("Server Seed:", value="d17354bbdbbdbfefb1ef2d210fb3ea2c3aeb4e6be5c27ac08a3e49b49fdf0b91", key="m_s")
        mc = st.text_input("Client Seed:", value="SaSd3AAerLJrfAw053Bf", key="m_c")
        mn = st.text_input("Nonce:", value="1", key="m_n")
        m_sl = st.slider("Nombre de mine:", 1, 7, 3)
        mh = st.text_input("Heure:", value=datetime.datetime.now().strftime("%H:%M:%S"), key="m_t")
        
        if st.button("🛰️ SCAN MINES BOARD"):
            schema = minesultraengine(ms, mc, mn, mh)
            
            # Fanamboarana ny Grid HTML
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                if i in schema:
                    grid_html += '<div class="mine-cell cell-star">💎</div>'
                else:
                    grid_html += '<div class="mine-cell"></div>'
            grid_html += '</div>'
            
            st.markdown(grid_html, unsafe_allow_html=True)
            st.success(f"Safe Slots: {schema}")
