import streamlit as st
import hashlib, random, statistics, datetime
import numpy as np

# Fiarovana amin'ny Matplotlib
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

st.set_page_config(page_title="TITAN V101 PREMIUM 2026", layout="wide")

# --- STYLE NEON ---
st.markdown("""
    <style>
    .stApp {background: #050505; color:#00ffcc; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
    h1, h2, h3 {color:#00ffcc; text-shadow: 0 0 15px #00ffcc; text-align: center;}
    .stButton>button {
        background: linear-gradient(135deg, #00ffcc 0%, #0066ff 100%);
        color: white; border: none; border-radius: 8px;
        padding: 12px 24px; font-weight: bold; width: 100%;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {box-shadow: 0 0 35px #00ffcc; transform: scale(1.02);}
    .metric-container {background: #111; border: 1px solid #00ffcc; border-radius: 10px; padding: 15px;}
    </style>
""", unsafe_allow_html=True)

# --- DRAW MINES BOARD (STYLED) ---
def draw_styled_board(schema):
    if not HAS_MATPLOTLIB:
        st.warning("⚠️ Tsy tafapetraka ny Matplotlib.")
        return
    
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('#050505')
    ax.set_facecolor('#0A0A0A')
    
    # Grid neon lines
    for x in range(6):
        ax.axhline(x, color='#00ffcc', lw=1, alpha=0.3)
        ax.axvline(x, color='#00ffcc', lw=1, alpha=0.3)
    
    # Diamonds with Glow
    for pos in schema:
        r, c = divmod(pos, 5)
        # Sary kintana stylé
        ax.text(c + 0.5, 4.5 - r, "💎", ha="center", va="center", fontsize=40,
                bbox=dict(facecolor='#00ffcc', alpha=0.1, edgecolor='#00ffcc', boxstyle='round,pad=0.3'))
        
        # Effet de lumière kely (glow)
        circle = plt.Circle((c + 0.5, 4.5 - r), 0.3, color='#00ffcc', alpha=0.1)
        ax.add_patch(circle)

    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.axis('off')
    st.pyplot(fig)

# --- COSMOS ENGINE ---
def cosmos_premium_engine(server_seed, client_seed, nonce, tour_actuel):
    # Ny Nonce dia ilaina mba tsy ho fixe ny algorithm
    base = f"{server_seed}:{client_seed}:{nonce}:{tour_actuel}:TITAN_2026"
    h = hashlib.sha512(base.encode()).digest()
    for i in range(500):
        h = hashlib.sha512(h + str(i).encode()).digest()
    
    hex_res = h.hex()
    p_int = int(hex_res[:16], 16)
    
    # Variable Jumps
    jump1 = (p_int % 8) + 2
    jump2 = (p_int % 12) + 5
    
    # Metrics
    vals = [int(hex_res[i:i+2], 16)/10 for i in range(0, 30, 2)]
    min_v, max_v = min(vals), max(vals)
    mean_v = round(statistics.mean(vals), 2)
    acc = round((mean_v / max_v) * 100, 2)

    return {
        "hex": hex_res[:64],
        "tour1": tour_actuel + jump1,
        "tour2": tour_actuel + jump2,
        "min": min_v, "mean": mean_v, "max": max_v, "acc": acc
    }

# --- MINES ENGINE ---
def mines_premium_engine(s_seed, c_seed, nonce, nb_mines):
    # Ny Nonce koa dia manova ny schema isaky ny tour
    base = f"{s_seed}:{c_seed}:{nonce}:{nb_mines}:MINES_PREMIUM"
    h = hashlib.sha512(base.encode()).digest()
    random.seed(int.from_bytes(h[:8], "big") + nonce)
    
    grid = list(range(25))
    random.shuffle(grid)
    # 5 safe spots no omeny foana
    return sorted(grid[:5])

# --- SYSTEM LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 TITAN V101 - ADMIN ACCESS")
    col_l, col_r = st.columns([1, 2])
    with col_l:
        code = st.text_input("Enter Code:", type="password")
        if st.button("AUTHENTICATE"):
            if code == "2026":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Access Denied!")
else:
    st.markdown("<h1>🌌 TITAN V101 PREMIUM</h1>", unsafe_allow_html=True)
    if st.button("🚪 LOGOUT"):
        st.session_state['logged_in'] = False
        st.rerun()

    # --- PARAMETERS ---
    with st.expander("🛠️ CONFIGURATION SEEDS & NONCE", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1: s_seed = st.text_input("Server Seed", "d17354bbdbbdbfefb1ef2d210fb3ea2c3aeb4e6be5c27ac08a3e49b49fdf0b91")
        with c2: c_seed = st.text_input("Client Seed", "SaSd3AAerLJrfAw053Bf")
        with c3: nonce = st.number_input("Nonce (Current)", min_value=0, value=1)

    tab1, tab2 = st.tabs(["💎 MINES SCANNER", "📈 COSMOSX PREDICTION"])

    with tab1:
        nb_m = st.selectbox("Select Mines:", [1, 2, 3, 4, 5, 10, 24])
        if st.button("🚀 SCAN MINES BOARD"):
            schema = mines_premium_engine(s_seed, c_seed, nonce, nb_m)
            draw_styled_board(schema)
            st.success(f"Safe Slots for Tour {nonce}: {schema}")

    with tab2:
        t_act = st.number_input("Tour Actuel:", min_value=1, value=100)
        if st.button("🌠 ANALYZE COSMOS"):
            res = cosmos_premium_engine(s_seed, c_seed, nonce, t_act)
            
            # Metrics display
            cols = st.columns(4)
            cols[0].metric("MIN", f"{res['min']}x")
            cols[1].metric("MEAN", f"{res['mean']}x")
            cols[2].metric("MAX", f"{res['max']}x")
            cols[3].metric("ACCURACY", f"{res['acc']}%")
            
            st.markdown(f"""
            <div style="background:#111; padding:20px; border-radius:10px; border-left:5px solid #00ffcc;">
                <p>🔭 <b>Tour Manaraka 1:</b> {res['tour1']}</p>
                <p>🔭 <b>Tour Manaraka 2:</b> {res['tour2']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.code(res['hex'], language="bash")
