import streamlit as st
import hashlib, hmac, random, statistics, datetime
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURATION STYLE ---
st.set_page_config(page_title="TITAN V101 - ADMIN 2026", layout="wide")
plt.style.use('dark_background')

# --- ENGINE FUNCTIONS ---

def cosmos_premium_engine(server_seed, client_seed, nonce, salt="T1", iters=500000):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{server_seed}:{client_seed}:{nonce}:{salt}:{heure}:COSMOSX_V101"
    h1 = hmac.new(b"COSMOS_CORE", base.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h1 = hashlib.sha512(h1 + f"STEP_{i}".encode()).digest()
    
    hex_out = h1.hex()
    p_int = int(hex_out[:16], 16)
    offset = (p_int % 29) + (9 if salt == "T1" else 15)
    jumps = [(p_int % 7) + 2, (p_int % 11) + 3, (p_int % 13) + 4]

    values = [offset] + jumps
    accuracy = round((statistics.mean(values) / max(values)) * 100, 2)

    return {
        "hex": hex_out[:64],
        "tour": nonce + offset,
        "jumps": jumps,
        "min": min(values),
        "max": max(values),
        "mean": round(statistics.mean(values), 2),
        "accuracy": accuracy
    }

def mines_premium_engine(server_seed, client_seed, nonce, iters=500000):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{server_seed}:{client_seed}:{nonce}:{heure}:MINES_V101"
    h = hashlib.sha512(base.encode()).digest()
    for i in range(iters):
        h = hashlib.sha512(h + f"STEP{i}".encode()).digest()

    random.seed(int.from_bytes(h[:8], "big"))
    grid = list(range(25))
    random.shuffle(grid)
    schema = sorted(grid[:5])
    probs = [round(((5 - k) / (25 - k)) * 100, 2) for k in range(5)]
    
    return schema, probs

# --- INTERFACE ADMIN LOGIN ---

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 TITAN V101 - ADMIN LOGIN (2026)")
    admin_code = st.text_input("Enter Admin Code:", type="password")
    if st.button("LOGIN"):
        if admin_code == "2026": # Ity ny code fidirana
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Code diso! Avereno indray.")
else:
    # --- DASHBOARD ADMIN ---
    st.title("🌌 TITAN V101 PREMIUM 2026")
    if st.button("LOGOUT"):
        st.session_state['logged_in'] = False
        st.rerun()

    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🔑 Seeds Configuration")
        s_seed = st.text_input("Server Seed", "d17354bbdbbdbfefb1ef2d210fb3ea2c3aeb4e6be5c27ac08a3e49b49fdf0b91")
        c_seed = st.text_input("Client Seed", "SaSd3AAerLJrfAw053Bf")
        n_val = st.number_input("Nonce / Current Tour", min_value=1, value=1)
        
        st.markdown("---")
        mode = st.radio("Select Engine:", ["Mines Ultra", "CosmosX Predictor"])

    with col2:
        if mode == "Mines Ultra":
            if st.button("🚀 PREDICT MINES"):
                schema, probs = mines_premium_engine(s_seed, c_seed, n_val)
                
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                img = np.zeros((5, 5))
                for pos in schema:
                    r, c = divmod(pos, 5)
                    img[r, c] = 1
                
                ax1.imshow(img, cmap='Blues')
                ax1.set_title("Diamond Strategy")
                for p in schema:
                    r, c = divmod(p, 5)
                    ax1.text(c, r, "💎", ha="center", va="center", fontsize=20)
                
                ax2.bar(range(1, 6), probs, color='cyan')
                ax2.set_title("Success Probability per Click")
                
                st.pyplot(fig)
                st.success(f"Recommended Clicks (Positions): {schema}")

        elif mode == "CosmosX Predictor":
            if st.button("🌠 PREDICT COSMOS"):
                res = cosmos_premium_engine(s_seed, c_seed, n_val)
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Target Tour", res['tour'])
                m2.metric("Accuracy", f"{res['accuracy']}%")
                m3.metric("Mean Jump", res['mean'])
                
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.barh(["Min", "Mean", "Max"], [res['min'], res['mean'], res['max']], color='magenta')
                ax.set_title("Analysis Metrics")
                st.pyplot(fig)
                st.code(f"Hash: {res['hex']}...", language="bash")
