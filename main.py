import streamlit as st
import hashlib, hmac, random, statistics, datetime
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURATION STYLE ---
st.set_page_config(page_title="TITAN V101 Premium", layout="wide")
plt.style.use('dark_background') # Mba ho hita tsara ny sary amin'ny dark mode

# --- COSMOS PREMIUM ENGINE ---
def cosmos_premium_engine(server_seed, client_seed, nonce, salt="T1", iters=500000):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    # Nampiana ny 'heure' ao anatin'ny hashing mba ho unique isaky ny segondra
    base = f"{server_seed}:{client_seed}:{nonce}:{salt}:{heure}:COSMOSX_V101"
    
    h1 = hmac.new(b"COSMOS_CORE", base.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h1 = hashlib.sha512(h1 + f"STEP_{i}".encode()).digest()
    
    final_hex = h1.hex()
    p_int = int(final_hex[:16], 16)
    
    # Kajy ny tour sy ny jumps
    offset = (p_int % 29) + (9 if salt == "T1" else 15)
    jumps = [(p_int % 7) + 2, (p_int % 11) + 3, (p_int % 13) + 4]
    
    values = [offset] + jumps
    accuracy = round((statistics.mean(values) / max(values)) * 100, 2)

    return {
        "hex": final_hex[:64],
        "tour_vinaniana": nonce + offset,
        "jumps": jumps,
        "min": min(values),
        "max": max(values),
        "mean": round(statistics.mean(values), 2),
        "accuracy": accuracy
    }

# --- MINES PREMIUM ENGINE ---
def mines_premium_engine(server_seed, client_seed, nonce, iters=500000):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{server_seed}:{client_seed}:{nonce}:{heure}:MINES_V101"

    # Multi-layer hashing ho an'ny fiarovana avo lenta
    h = hashlib.sha512(base.encode()).digest()
    for i in range(iters):
        h = hashlib.sha512(h + str(i).encode()).digest()
    
    random.seed(int.from_bytes(h[:8], "big"))
    grid = list(range(25))
    random.shuffle(grid)
    
    schema = sorted(grid[:5]) # Alaina ny 5 voalohany
    probs = [round(((5 - k) / (25 - k)) * 100, 2) for k in range(5)]
    
    return schema, probs

# --- INTERFACE ---
st.title("🌌 TITAN V101 Premium IA")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔑 Paramètres")
    s_seed = st.text_input("Server Seed", "d17354bbdbbdbfefb1ef2d210fb3ea2c3aeb4e6be5c27ac08a3e49b49fdf0b91")
    c_seed = st.text_input("Client Seed", "SaSd3AAerLJrfAw053Bf")
    n_val = st.number_input("Nonce / Current Tour", min_value=1, value=1)
    
    st.markdown("---")
    btn_mines = st.button("🛰️ SCAN MINES PREMIUM", use_container_width=True)
    btn_cosmos = st.button("🌠 SCAN COSMOS PREMIUM", use_container_width=True)

with col2:
    if btn_mines:
        schema, probs = mines_premium_engine(s_seed, c_seed, n_val)
        
        st.subheader("💣 Mines Analysis")
        
        # Visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Grid 5x5
        img = np.zeros((5, 5))
        for pos in schema:
            r, c = divmod(pos, 5)
            img[r, c] = 1
        
        ax1.imshow(img, cmap='Blues')
        ax1.set_xticks(np.arange(-.5, 5, 1), minor=True); ax1.set_yticks(np.arange(-.5, 5, 1), minor=True)
        ax1.grid(which='minor', color='w', linestyle='-', linewidth=2)
        ax1.set_title("Diamond Location Strategy")
        
        for p in schema:
            r, c = divmod(p, 5)
            ax1.text(c, r, "💎", ha="center", va="center", fontsize=20)

        # Probabilities
        ax2.bar(range(1, 6), probs, color='#00ffcc')
        ax2.set_title("Step-by-Step Probability")
        ax2.set_ylabel("% Success Rate")
        ax2.set_xlabel("Click Number")
        
        st.pyplot(fig)
        st.success(f"Mines Schema: {schema}")

    if btn_cosmos:
        res = cosmos_premium_engine(s_seed, c_seed, n_val)
        
        st.subheader("🌌 CosmosX Prediction")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted Tour", res['tour_vinaniana'])
        m2.metric("Accuracy", f"{res['accuracy']}%")
        m3.metric("Mean Jump", res['mean'])
        
        # Chart
        fig, ax = plt.subplots(figsize=(8, 4))
        metrics = ["Min", "Mean", "Max"]
        vals = [res['min'], res['mean'], res['max']]
        ax.barh(metrics, vals, color=['#ff00ff', '#00ffff', '#ffff00'])
        ax.set_title("Dynamic Range Analysis")
        
        st.pyplot(fig)
        st.code(f"Hash: {res['hex']}...", language="bash")
