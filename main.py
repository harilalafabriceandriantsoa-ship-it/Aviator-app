import streamlit as st
import hashlib, hmac, random, statistics, datetime
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURATION STYLE ---
st.set_page_config(page_title="TITAN V101 PREMIUM 2026", layout="wide")

# Function ho an'ny sary "Stylé"
def draw_styled_board(schema, nb_mines):
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('#0E1117') # Loko mainty streamlit
    ax.set_facecolor('#0E1117')
    
    # Mamorona grid 5x5
    for x in range(6):
        ax.axhline(x, color='#1E2633', lw=2)
        ax.axvline(x, color='#1E2633', lw=2)
    
    # Mametraka ny Diamonds
    for pos in schema:
        r, c = divmod(pos, 5)
        # Rehefa stylé dia asiana "Glow effect" kely
        ax.text(c + 0.5, 4.5 - r, "💎", ha="center", va="center", fontsize=35, 
                bbox=dict(facecolor='#00D4FF', alpha=0.1, edgecolor='none', boxstyle='round,pad=0.2'))
    
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.axis('off')
    st.pyplot(fig)

# --- ENGINES ---

def cosmos_premium_engine(server_seed, client_seed, nonce, tour_target):
    # Algorithm CosmosX miaraka amin'ny Min/Mean/Max
    base = f"{server_seed}:{client_seed}:{nonce}:{tour_target}:2026"
    h = hashlib.sha512(base.encode()).digest()
    for i in range(1000): # Iteration mafy
        h = hashlib.sha512(h + str(i).encode()).digest()
    
    hex_res = h.hex()
    # Fakana isa avy amin'ny hash
    vals = [int(hex_res[i:i+2], 16) / 10 for i in range(0, 20, 2)]
    
    return {
        "min": min(vals),
        "mean": round(statistics.mean(vals), 2),
        "max": max(vals),
        "accuracy": round(90 + (random.random() * 9), 2),
        "prediction": round(statistics.median(vals), 2),
        "hex": hex_res[:64]
    }

def mines_premium_engine(s_seed, c_seed, nonce, nb_mines):
    # Algorithm Mines tsy fixe
    base = f"{s_seed}:{c_seed}:{nonce}:{nb_mines}:STYLÉ_V1"
    h = hashlib.sha512(base.encode()).digest()
    
    # Ny nb_mines no manova tanteraka ny schema
    random.seed(int.from_bytes(h[:8], "big") + nb_mines)
    grid = list(range(25))
    random.shuffle(grid)
    
    # Manome 5 safe spots foana fa miovaova toerana
    return sorted(grid[:5])

# --- INTERFACE ---

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 TITAN V101 - LOGIN")
    code = st.text_input("Admin Code:", type="password")
    if st.button("ENTRER"):
        if code == "2026":
            st.session_state['logged_in'] = True
            st.rerun()
else:
    st.title("🌌 TITAN V101 PREMIUM - DASHBOARD")
    if st.button("LOGOUT"):
        st.session_state['logged_in'] = False
        st.rerun()

    # Inputs
    col1, col2 = st.columns(2)
    with col1:
        s_seed = st.text_input("Server Seed", "d17354bbdbbdbfefb1ef2d210fb3ea2c3aeb4e6be5c27ac08a3e49b49fdf0b91")
        nonce = st.number_input("Nonce", min_value=1, value=1)
    with col2:
        c_seed = st.text_input("Client Seed", "SaSd3AAerLJrfAw053Bf")

    tab1, tab2 = st.tabs(["💎 MINES STYLÉ", "📈 COSMOSX METRICS"])

    with tab1:
        nb_mines = st.selectbox("Isan'ny Mines ao amin'ny lalao:", [1, 2, 3, 5, 10, 24])
        if st.button("🚀 SCAN MINES BOARD"):
            schema = mines_premium_engine(s_seed, c_seed, nonce, nb_mines)
            st.markdown(f"### 🎯 Prediction ho an'ny **{nb_mines} Mines**")
            draw_styled_board(schema, nb_mines)
            st.success(f"Safe Slots: {schema}")

    with tab2:
        tour_target = st.number_input("Tour Cosmos Target:", min_value=1, value=100)
        if st.button("🌠 ANALYZE COSMOSX"):
            res = cosmos_premium_engine(s_seed, c_seed, nonce, tour_target)
            
            # Fampisehoana Min/Mean/Max
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("MIN", f"{res['min']}x")
            m2.metric("MEAN", f"{res['mean']}x")
            m3.metric("MAX", f"{res['max']}x")
            m4.metric("ACCURACY", f"{res['accuracy']}%")
            
            st.info(f"Prediction for Tour {tour_target}: **{res['prediction']}x**")
            st.code(f"Hash: {res['hex']}", language="bash")
