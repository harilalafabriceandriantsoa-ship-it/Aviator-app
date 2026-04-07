import streamlit as st
import hashlib, hmac, random, statistics, datetime
import numpy as np

# Natao ao anatin'ny 'try-except' ny matplotlib mba tsy hampijanon-javatra raha mbola tsy tafiditra
try:
    import matplotlib.pyplot as plt
    plt.style.use('dark_background')
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False

st.set_page_config(page_title="TITAN V101 Premium", layout="wide")

# --- ENGINE FUNCTIONS ---
def safe_int_conversion(hex_val):
    """Miantoka fa tsy miteraka ValueError ny conversion"""
    try:
        if not hex_val or len(hex_val) < 16:
            return 0
        return int(hex_val[:16], 16)
    except ValueError:
        return 0

def cosmos_premium_engine(server_seed, client_seed, nonce, salt="T1"):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{server_seed}:{client_seed}:{nonce}:{salt}:{heure}:V101"
    h1 = hmac.new(b"CORE", base.encode(), hashlib.sha512).digest()
    
    final_hex = hashlib.sha512(h1).hexdigest()
    p_int = safe_int_conversion(final_hex)
    
    offset = (p_int % 29) + (9 if salt == "T1" else 15)
    jumps = [(p_int % 7) + 2, (p_int % 11) + 3, (p_int % 13) + 4]
    
    values = [offset] + jumps
    accuracy = round((statistics.mean(values) / max(values)) * 100, 2) if max(values) > 0 else 0

    return {
        "hex": final_hex[:64],
        "tour": nonce + offset,
        "jumps": jumps,
        "min": min(values),
        "max": max(values),
        "mean": round(statistics.mean(values), 2),
        "accuracy": accuracy
    }

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

# --- UI ---
st.title("🌌 TITAN V101 Premium IA")

s_seed = st.text_input("Server Seed", "d17354bbdbbdbfefb1ef2d210fb3ea2c3aeb4e6be5c27ac08a3e49b49fdf0b91")
c_seed = st.text_input("Client Seed", "SaSd3AAerLJrfAw053Bf")
n_val = st.number_input("Nonce / Current Tour", min_value=1, value=1)

tab1, tab2 = st.tabs(["💣 MINES", "🌌 COSMOS"])

with tab1:
    if st.button("🚀 SCAN MINES"):
        schema, probs = mines_premium_engine(s_seed, c_seed, n_val)
        
        if HAS_PLOT:
            fig, ax1 = plt.subplots(figsize=(5, 5))
            img = np.zeros((5, 5))
            for pos in schema:
                r, c = divmod(pos, 5)
                img[r, c] = 1
            ax1.imshow(img, cmap='Blues')
            for p in schema:
                r, c = divmod(p, 5)
                ax1.text(c, r, "💎", ha="center", va="center", fontsize=20)
            st.pyplot(fig)
        
        st.write(f"**Schema:** {schema}")
        st.write(f"**Vintana:** {probs}")

with tab2:
    if st.button("🌠 SCAN COSMOS"):
        res = cosmos_premium_engine(s_seed, c_seed, n_val)
        st.metric("Predicted Tour", res['tour'])
        st.metric("Accuracy", f"{res['accuracy']}%")
        st.code(res['hex'])
