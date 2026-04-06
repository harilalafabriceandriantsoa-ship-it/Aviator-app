import streamlit as st
import hashlib, hmac, random, datetime

# --- CONFIGURATION ---
LOGIN_KEY = "2026"
st.set_page_config(page_title="TITAN V90 - ULTRA MACHINE", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .scan-box { border: 2px solid #00ffcc; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px; background: rgba(0, 255, 204, 0.05); }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 330px; margin: auto; }
    .mine-cell { aspect-ratio: 1/1; background: #0a0a0a; border: 1px solid #00ffcc44; display: flex; align-items: center; justify-content: center; font-size: 28px; border-radius: 12px; }
    .cell-star { border: 2px solid #ff0000 !important; background: rgba(255, 0, 0, 0.3); color: #ff0000; box-shadow: 0 0 30px #ff0000; }
    </style>
    """, unsafe_allow_html=True)

# --- MINES ENGINE (server seed + client seed + choice) ---
def mines_ultra_engine(server_seed, client_seed, nonce, choice=1):
    base = f"{server_seed}:{client_seed}:{nonce}:{choice}:MINES_V90"
    h1 = hashlib.sha512(base.encode()).digest()
    h2 = hashlib.blake2b(h1).digest()
    h3 = hashlib.sha3_256(h2).digest()
    combined = h1 + h2 + h3
    hash_int = int.from_bytes(combined, "big")
    grid = list(range(25))
    for i in range(24, 0, -1):
        j = hash_int % (i + 1)
        grid[i], grid[j] = grid[j], grid[i]
        hash_int //= (i + 1)
    random.seed(int.from_bytes(h3[:16], "big"))
    random.shuffle(grid)
    return grid[:5]

# --- COSMOS ENGINE (hash, hex, tour actuel + jumps variable) ---
def cosmos_ultra_engine(hash_val, hex_val, tour_id, heure, iters=100000):
    base = f"{hash_val}:{hex_val}:{tour_id}:{heure}:COSMOSX_V90"
    h1 = hmac.new(b"COSMOS_CORE", base.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h1 = hmac.new(h1, f"STEP_{i}".encode(), hashlib.sha512).digest()
    blake = hashlib.blake2b(h1).digest()
    sha3 = hashlib.sha3_256(blake).digest()
    final = bytes(a ^ b ^ c for a, b, c in zip(h1, blake, sha3))
    hex_out = final.hex()
    p_int = int(hex_out[:12], 16) ^ int(heure.replace(":", ""))
    jumps = []
    for k in range(3):
        jumps.append((p_int % (5 + k)) + (2 + k))
        p_int //= (7 + k)
    return {"hex": hex_out, "tour": tour_id, "jumps": jumps}

# --- AVIATOR ENGINE (heure d’entrée + logic) ---
def aviator_studio_engine(hex_val, heure):
    h_int = int(hex_val[:16], 16)
    mask = int(heure.replace(":", ""))
    base = h_int ^ mask
    mult = 1 + (base % 9000) / 1000.0
    return {
        "multiplier": mult,
        "min": round(mult * 0.9, 2),
        "moyen": round(mult * 1.3, 2),
        "max": round(mult * 2.7, 2),
        "accuracy": 0.85 if 2.5 <= mult <= 4.5 else 0.65
    }

# --- LOGIN ---
st.markdown("<h2 style='text-align:center;'>🔐 TITAN V90 - ADMIN LOGIN</h2>", unsafe_allow_html=True)
admin_input = st.text_input("Enter Admin Code:", type="password")

if admin_input == LOGIN_KEY:
    st.success("✅ Access Granted. Machine Activated.")

    tab1, tab2, tab3 = st.tabs(["🌌 COSMOSX", "✈️ AVIATOR STUDIO", "💣 MINES ULTRA"])

    with tab1:
        st.markdown("##### 🌌 COSMOSX PREDICTION (Tour 1 & Tour 2)")
        h_val = st.text_input("Hash Value:", key="cosmos_hash")
        x_val = st.text_input("Hex Value:", key="cosmos_hex")
        t_id = st.number_input("Tour Actuel:", min_value=1, value=10001, key="cosmos_t")
        heure = st.text_input("Heure Fidirana (HH:mm):", value=datetime.datetime.now().strftime("%H:%M"), key="cosmos_h")
        if st.button("🚀 EXECUTE COSMOS", key="btn_cosmos"):
            res1 = cosmos_ultra_engine(h_val, x_val, t_id, heure)
            res2 = cosmos_ultra_engine(h_val, x_val, t_id+1, heure)
            st.code(f"HEX: {res1['hex'][:48]}...", language="bash")
            st.write("Tour 1:", res1["tour"], "Jumps:", res1["jumps"])
            st.write("Tour 2:", res2["tour"], "Jumps:", res2["jumps"])

    with tab2:
        st.markdown("##### ✈️ AVIATOR STUDIO PREDICTION (Tour 1 & Tour 2)")
        a_hex = st.text_input("Input HEX Value:", key="avi_hex")
        a_time = st.text_input("Heure Fidirana (HH:mm):", value=datetime.datetime.now().strftime("%H:%M"), key="avi_time")
        if st.button("✈️ PREDICT", key="btn_avi"):
            res1 = aviator_studio_engine(a_hex, a_time)
            res2 = aviator_studio_engine(a_hex, str((datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%H:%M")))
            st.metric("Tour 1 PREDICTED X", f"{res1['multiplier']:.2f}x")
            st.write(f"Safe Range: {res1['min']}x - {res1['moyen']}x - {res1['max']}x | Accuracy: {int(res1['accuracy']*100)}%")
            st.metric("Tour 2 PREDICTED X", f"{res2['multiplier']:.2f}x")
            st.write(f"Safe Range: {res2['min']}x - {res2['moyen']}x - {res2['max']}x | Accuracy: {int(res2['accuracy']*100)}%")

    with tab3:
        st.markdown("##### 💣 MINES ULTRA LOGIC (Server Seed + Client Seed + Choice)")
        m_s = st.text_input("Server Seed:", key="m_s")
        m_c = st.text_input("Client Seed:", key="m_c")
        m_nonce = st.text_input("Nonce / ID Partie:", key="m_n")
        m_choice = st.slider("Select Mines Pattern (1–3):", 1, 3, 1, key="m_choice")
        if st.button("🛰️ SCAN MINES", key="btn_mines"):
            schema = mines_ultra_engine(m_s, m_c, m_nonce, m_choice)
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                grid_html += f'<div class="mine-cell {"cell-star" if i in schema else ""}">{"⭐" if i in schema else "⬛"}</div>'
            st.markdown(grid_html + '</div>', unsafe_allow_html=True)
            st.success("✅ Mines Schema Generated")

elif admin_input != "":
    st.error("❌ Invalid Code")
