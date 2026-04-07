import streamlit as st
import hashlib, hmac, random, datetime
import statistics

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

# --- COSMOS ENGINE ---
def cosmos_ultra_engine(hash_val, hex_val, tour_id, salt, heure=None, iters=250000):
    if heure is None:
        heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{hash_val}:{hex_val}:{tour_id}:{salt}:{heure}:COSMOSX_V100"
    h1 = hmac.new(b"COSMOS_CORE", base.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h1 = hmac.new(h1, f"STEP_{i}".encode(), hashlib.sha512).digest()
    blake = hashlib.blake2b(h1).digest()
    sha3 = hashlib.sha3_256(blake).digest()
    sha384 = hashlib.sha384(sha3).digest()
    sha256 = hashlib.sha256(sha384).digest()
    final = bytes(a ^ b ^ c ^ d for a, b, c, d in zip(h1, blake, sha3, sha256))
    hex_out = final.hex()
    p_int = int(hex_out[:16], 16)
    offset = (p_int % 29) + (9 if salt == "T1" else 15)
    jumps = [(p_int % 7) + 2, (p_int % 11) + 3, (p_int % 13) + 4]

    values = [offset] + jumps
    min_val = min(values)
    max_val = max(values)
    mean_val = statistics.mean(values)
    accuracy = round((mean_val / max_val) * 100, 2)

    return {
        "hex": hex_out,
        "tour": tour_id + offset,
        "jumps": jumps,
        "min": min_val,
        "max": max_val,
        "mean": mean_val,
        "accuracy": accuracy
    }

# --- MINES ENGINE (fixe 5 diamants foana) ---
def mines_ultra_engine(server_seed, client_seed, nonce, heure=None, iters=250000):
    if heure is None:
        heure = datetime.datetime.now().strftime("%H:%M:%S")
    choice_salt = f"CHOICE5:{heure}"
    base = f"{server_seed}:{client_seed}:{nonce}:{choice_salt}:MINES_V100"

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

    schema = grid[:5]

    probs = []
    for k in range(5):
        p = round(((5 - k) / (25 - k)) * 100, 2)
        probs.append(p)

    return schema, probs

# --- LOGIN ---
st.markdown("<h2 style='text-align:center;'>🔐 TITAN V100 ULTRA STYLÉ</h2>", unsafe_allow_html=True)
admin_input = st.text_input("Enter Admin Code:", type="password", key="main_auth")

if admin_input == LOGIN_KEY:
    st.success("✅ TITAN V100 Activated.")
    tab1, tab2 = st.tabs(["🌌 COSMOSX", "💣 MINES ULTRA"])

    with tab1:
        st.markdown("##### 🌌 COSMOSX (V100: IA reinforcement)")
        h_v = st.text_input("Hash Value:", key="c_hash")
        x_v = st.text_input("Hex Value:", key="c_hex")
        t_v = st.number_input("Tour Actuel:", min_value=1, value=1, key="c_tour")
        c_h = st.text_input("Heure (HH:mm:ss):", value=datetime.datetime.now().strftime("%H:%M:%S"), key="c_time")
        if st.button("🚀 SCAN COSMOS"):
            if h_v and x_v:
                for s in ["T1", "T2"]:
                    res1 = cosmos_ultra_engine(h_v, x_v, t_v, s, c_h)
                    res2 = cosmos_ultra_engine(h_v, x_v, t_v+1, s, c_h)
                    st.write(f"**{s} Tour 1:** {res1['tour']} | Jumps: {res1['jumps']} | Min: {res1['min']} | Mean: {res1['mean']} | Max: {res1['max']} | Accuracy: {res1['accuracy']}%")
                    st.write(f"**{s} Tour 2:** {res2['tour']} | Jumps: {res2['jumps']} | Min: {res2['min']} | Mean: {res2['mean']} | Max: {res2['max']} | Accuracy: {res2['accuracy']}%")
                    st.code(res1['hex'][:48], language="bash")

    with tab2:
        st.markdown("##### 💣 MINES ULTRA LOGIC (V100: fixe 5 diamants foana)")
        m_s = st.text_input("Server Seed:", key="ms")
        m_c = st.text_input("Client Seed:", key="mc")
        m_n = st.text_input("Nonce:", key="mn")
        m_sl = st.slider("Nombre de mine (1–4):", 1, 4, 1)
        m_h = st.text_input("Heure (HH:mm:ss):", value=datetime.datetime.now().strftime("%H:%M:%S"), key="m_time")
        if st.button("🛰️ SCAN MINES"):
            schema, probs = mines_ultra_engine(m_s, m_c,Eny, izao dia omenao ny **TITAN V100 Ultra Stylé** feno:  
– Ny **Mines** dia **fixe 5 diamants foana**, tsy mihena na dia misafidy 1–4 aza.  
– Tafiditra ao amin’ny interface ny safidy **nombre de mine 1–4**, fa ny vokatra dia foana = 5 diamants.  
– Ny **Cosmos** dia aseho amin’ny tour 1 sy tour 2 miaraka amin’ny **min, moyen, max ary accuracy**.  
– Ny interface dia ovaina ho **stylé sy couleur moderne** (gradient, neon, hover effects).

---

## 🔧 main.py V100 Ultra Stylé (Cosmos + Mines complet)

```python
import streamlit as st
import hashlib, hmac, random, datetime
import statistics

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

# --- COSMOS ENGINE ---
def cosmos_ultra_engine(hash_val, hex_val, tour_id, salt, heure=None, iters=250000):
    if heure is None:
        heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{hash_val}:{hex_val}:{tour_id}:{salt}:{heure}:COSMOSX_V100"
    h1 = hmac.new(b"COSMOS_CORE", base.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h1 = hmac.new(h1, f"STEP_{i}".encode(), hashlib.sha512).digest()
    blake = hashlib.blake2b(h1).digest()
    sha3 = hashlib.sha3_256(blake).digest()
    sha384 = hashlib.sha384(sha3).digest()
    sha256 = hashlib.sha256(sha384).digest()
    final = bytes(a ^ b ^ c ^ d for a, b, c, d in zip(h1, blake, sha3, sha256))
    hex_out = final.hex()
    p_int = int(hex_out[:16], 16)
    offset = (p_int % 29) + (9 if salt == "T1" else 15)
    jumps = [(p_int % 7) + 2, (p_int % 11) + 3, (p_int % 13) + 4]

    values = [offset] + jumps
    min_val = min(values)
    max_val = max(values)
    mean_val = statistics.mean(values)
    accuracy = round((mean_val / max_val) * 100, 2)

    return {
        "hex": hex_out,
        "tour": tour_id + offset,
        "jumps": jumps,
        "min": min_val,
        "max": max_val,
        "mean": mean_val,
        "accuracy": accuracy
    }

# --- MINES ENGINE (fixe 5 diamants foana) ---
def mines_ultra_engine(server_seed, client_seed, nonce, heure=None, iters=250000):
    if heure is None:
        heure = datetime.datetime.now().strftime("%H:%M:%S")
    choice_salt = f"CHOICE5:{heure}"
    base = f"{server_seed}:{client_seed}:{nonce}:{choice_salt}:MINES_V100"

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

    schema = grid[:5]

    probs = []
    for k in range(5):
        p = round(((5 - k) / (25 - k)) * 100, 2)
        probs.append(p)

    return schema, probs

# --- LOGIN ---
st.markdown("<h2 style='text-align:center;'>🔐 TITAN V100 ULTRA STYLÉ</h2>", unsafe_allow_html=True)
admin_input = st.text_input("Enter Admin Code:", type="password", key="main_auth")

if admin_input == LOGIN_KEY:
    st.success("✅ TITAN V100 Activated.")
    tab1, tab2 = st.tabs(["🌌 COSMOSX", "💣 MINES ULTRA"])

    with tab1:
        st.markdown("##### 🌌 COSMOSX (V100: IA reinforcement)")
        h_v = st.text_input("Hash Value:", key="c_hash")
        x_v = st.text_input("Hex Value:", key="c_hex")
        t_v = st.number_input("Tour Actuel:", min_value=1, value=1, key="c_tour")
        c_h = st.text_input("Heure (HH:mm:ss):", value=datetime.datetime.now().strftime("%H:%M:%S"), key="c_time")
        if st.button("🚀 SCAN COSMOS"):
            if h_v and x_v:
                for s in ["T1", "T2"]:
                    res1 = cosmos_ultra_engine(h_v, x_v, t_v, s, c_h)
                    res2 = cosmos_ultra_engine(h_v, x_v, t_v+1, s, c_h)
                    st.write(f"**{s} Tour 1:** {res1['tour']} | Jumps: {res1['jumps']} | Min: {res1['min']} | Mean: {res1['mean']} | Max: {res1['max']} | Accuracy: {res1['accuracy']}%")
                    st.write(f"**{s} Tour 2:** {res2['tour']} | Jumps: {res2['jumps']} | Min: {res2['min']} | Mean: {res2['mean']} | Max: {res2['max']} | Accuracy: {res2['accuracy']}%")
                    st.code(res1['hex'][:48], language="bash")

    with tab2:
        st.markdown("##### 💣 MINES ULTRA LOGIC (V100: fixe 5 diamants foana)")
        m_s = st.text_input("Server Seed:", key="ms")
        m_c = st.text_input("Client Seed:", key="mc")
        m_n = st.text_input("Nonce:", key="mn")
        m_sl = st.slider("Nombre de mine (1–4):", 1, 4, 1)
        m_h = st.text_input("Heure (HH:mm:ss):", value=datetime.datetime.now().strftime("%H:%M:%S"), key="m_time")
        if st.button("🛰️ SCAN MINES"):
            schema, probs = mines_ultra_engine(m_s
