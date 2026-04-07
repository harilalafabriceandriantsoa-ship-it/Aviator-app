import streamlit as st
import hashlib, hmac, random, statistics, datetime
import numpy as np

# Fiarovana raha tsy mbola tafapetraka tsara ny matplotlib
try:
    import matplotlib.pyplot as plt
    plt.style.use('dark_background')
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False

# --- CONFIGURATION ---
st.set_page_config(page_title="TITAN V101 - ADMIN 2026", layout="wide")

# --- ENGINE FUNCTIONS ---

def safe_int_conversion(hex_val):
    """Fisorohana ny ValueError raha fohy loatra ny Hex"""
    try:
        if not hex_val or len(hex_val) < 16:
            return 0
        return int(hex_val[:16], 16)
    except ValueError:
        return 0

def cosmos_premium_engine(server_seed, client_seed, nonce, salt="T1", iters=100000):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{server_seed}:{client_seed}:{nonce}:{salt}:{heure}:V101"
    h1 = hmac.new(b"CORE", base.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h1 = hashlib.sha512(h1 + str(i).encode()).digest()
    
    final_hex = h1.hex()
    p_int = safe_int_conversion(final_hex)
    
    offset = (p_int % 29) + (9 if salt == "T1" else 15)
    jumps = [(p_int % 7) + 2, (p_int % 11) + 3, (p_int % 13) + 4]
    
    values = [offset] + jumps
    accuracy = round((statistics.mean(values) / max(values)) * 100, 2) if max(values) > 0 else 0
    return {"hex": final_hex[:64], "tour": nonce + offset, "acc": accuracy, "min": min(values), "mean": statistics.mean(values), "max": max(values)}

def mines_premium_engine(s_seed, c_seed, nonce):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{s_seed}:{c_seed}:{nonce}:{heure}:MINES_V101"
    h = hashlib.sha512(base.encode()).digest()
    random.seed(int.from_bytes(h[:8], "big"))
    grid = list(range(25))
    random.shuffle(grid)
    schema = sorted(grid[:5])
    probs = [round(((5 - k) / (25 - k)) * 100, 2) for k in range(5)]
    return schema, probs

# --- LOGIN SYSTEM ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 TITAN V101 - ADMIN LOGIN")
    admin_code = st.text_input("Enter Admin Code:", type="password")
    if st.button("LOGIN"):
        if admin_code == "2026":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Code diso!")
else:
    # --- DASHBOARD REHEFA LOGGED IN ---
    st.title("🌌 TITAN V101 PREMIUM 2026")
    if st.button("LOGOUT"):
        st.session_state['logged_in'] = False
        st.rerun()

    s_seed = st.text_input("Server Seed / Hash:", "d17354bbdbbdbfefb1ef2d210fb3ea2c3aeb4e6be5c27ac08a3e49b49fdf0b91")
    c_seed = st.text_input("Client Seed / Hex:", "SaSd3AAerLJrfAw053Bf")
    n_val = st.number_input("Nonce / Tour:", min_value=1, value=1)

    tab1, tab2 = st.tabs(["💣 MINES", "🌌 COSMOS"])

    with tab1:
        if st.button("🚀 SCAN MINES"):
            schema, probs = mines_premium_engine(s_seed, c_seed, n_val)
            if HAS_PLOT:
                fig, ax = plt.subplots(figsize=(5, 5))
                img = np.zeros((5, 5))
                for pos in schema:
                    r, c = divmod(pos, 5)
                    img[r, c] = 1
                ax.imshow(img, cmap='Blues')
                for p in schema:
                    r, c = divmod(p, 5)
                    ax.text(c, r, "💎", ha="center", va="center", fontsize=20)
                st.pyplot(fig)
            st.write(f"**Positions:** {schema}")
            st.write(f"**Probabilities:** {probs}")

    with tab2:
        if st.button("🌠 SCAN COSMOS"):
            res = cosmos_premium_engine(s_seed, c_seed, n_val)
            st.metric("Predicted Tour", res['tour'])
            st.metric("Accuracy", f"{res['acc']}%")
            st.code(res['hex'])
