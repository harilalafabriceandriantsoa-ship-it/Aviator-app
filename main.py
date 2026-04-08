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
        color: #333;
    }
    .mine-cell:hover {
        transform: scale(1.1);
        box-shadow: 0 0 15px #00ffcc;
    }
    .cell-star {
        border: 2px solid #ff0000 !important;
        background: rgba(255, 0, 0, 0.3);
        color: #ff0000;
        box-shadow: 0 0 30px #ff0000;
    }
    </style>
""", unsafe_allow_html=True)

# --- COSMOS ENGINE (ultra puissante) ---
def cosmosultraengine(server_seed, client_seed, tour_id, salt, heure=None, iters=250000):
    if heure is None:
        heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{server_seed}:{client_seed}:{tour_id}:{salt}:{heure}:COSMOSXV100"
    
    # Hashing chain ultra puissante
    h1 = hmac.new(b"COSMOS_CORE", base.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h1 = hmac.new(h1, f"STEP_{i}".encode(), hashlib.sha512).digest()
    blake = hashlib.blake2b(h1).digest()
    sha3 = hashlib.sha3_256(blake).digest()
    sha384 = hashlib.sha384(sha3).digest()
    sha256 = hashlib.sha256(sha384).digest()
    final = bytes(a ^ b ^ c ^ d for a, b, c, d in zip(h1, blake, sha3, sha256))
    hex_out = final.hex()

    # Offset sy jump variable
    p_int = int(hex_out[:16], 16)
    offset = (p_int % 29) + (9 if salt == "T1" else 15)
    jumps = [(p_int % 7) + 2, (p_int % 11) + 3, (p_int % 13) + 4]

    # Côte
    constante = 4294967295
    rtp = 0.97
    dec_val = int(hex_out[-8:], 16)
    cote = (constante * rtp) / dec_val
    if cote < 1.0: cote = 1.0
    cote = round(cote, 2)

    # Metrics
    values = [offset] + jumps
    min_val = round(min(values),2)
    max_val = round(max(values),2)
    mean_val = round(statistics.mean(values),2)
    accuracy = round((mean_val / max_val) * 100, 2)

    return {
        "tour": tour_id + offset,
        "cote": cote,
        "jumps": jumps,
        "min": min_val,
        "max": max_val,
        "mean": mean_val,
        "accuracy": accuracy,
        "hex": hex_out
    }

# --- MINES ENGINE (tsy kitihina, toy ny code-nao) ---
def minesultraengine(serverseed, clientseed, nonce, heure=None, iters=250000):
    if heure is None:
        heure = datetime.datetime.now().strftime("%H:%M:%S")
    choice_salt = f"CHOICE5:{heure}"
    base = f"{serverseed}:{clientseed}:{nonce}:{choice_salt}:MINESV100"

    h1 = hashlib.sha512(base.encode()).digest()
    h2 = hashlib.blake2b(h1).digest()
    h3 = hashlib.sha3_256(h2).digest()
    h4 = hashlib.sha384(h3).digest()
    h5 = hashlib.sha256(h4).digest()

    h_mut = h1
    for i in range(iters):
        h_mut = hashlib.sha512(h_mut + f"STEP{i}".encode()).digest()

    combined = h1 + h2 + h3 + h4 + h5 + h_mut
    hash_int = int.from_bytes(combined, "big")

    grid = list(range(25))
    for i in range(24, 0, -1):
        j = hash_int % (i + 1)
        grid[i], grid[j] = grid[j], grid[i]
        hash_int //= (i + 1)
    
    random.seed(int.from_bytes(h3[:16], "big") ^ 5)
    random.shuffle(grid)
    random.shuffle(grid)
    random.shuffle(grid)

    return grid[:5]

# --- LOGIN ---
st.markdown("<h2 style='text-align:center;'>🔐 TITAN V100 ULTRA STYLÉ</h2>", unsafe_allow_html=True)
admininput = st.text_input("Enter Admin Code:", type="password", key="main_auth")

if admininput == LOGIN_KEY:
    st.success("✅ TITAN V100 Activated.")
    tab1, tab2 = st.tabs(["🌌 COSMOSX", "💣 MINES ULTRA"])

    with tab1:
        st.markdown("##### 🌌 COSMOSX (Ultra puissante)")
        hv = st.text_input("Server Seed:", key="c_hash")
        xv = st.text_input("Client Seed:", key="c_hex")
        tv = st.number_input("Tour Actuel:", min_value=1, value=1, key="ctour")
        ch = st.text_input("Heure (HH:mm:ss):", value=datetime.datetime.now().strftime("%H:%M:%S"), key="c_time")
        if st.button("🚀 SCAN COSMOS"):
            if hv and xv:
                for s in ["T1", "T2"]:
                    res = cosmosultraengine(hv, xv, tv, s, ch)
                    st.write(f"{s} → Tour: {res['tour']} | Côte: {res['cote']}x | Jumps: {res['jumps']} | Min: {res['min']} | Moyen: {res['mean']} | Max: {res['max']} | Accuracy: {res['accuracy']}%")
                    st.code(res['hex'][:48], language="bash")

    with tab2:
        st.markdown("##### 💣 MINES ULTRA LOGIC (fixe 5 diamants foana)")
        ms = st.text_input("Server Seed:", key="ms")
        mc = st.text_input("Client Seed:", key="mc")
        mn = st.text_input("Nonce:", key="mn")
        mh = st.text_input("Heure (HH:mm:ss):", value=datetime.datetime.now().strftime("%H:%M:%S"), key="m_time")
        
        if st.button("🛰️ SCAN MINES"):
            schema = minesultraengine(ms, mc, mn, mh)
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                is_star = i in schema
                grid_html += f'<div class="mine-cell {"cell-star" if is_star else ""}">{"⭐" if is_star else ""}</div>'
            grid_html
