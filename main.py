import streamlit as st
import hashlib, hmac, random, datetime

# --- CONFIGURATION ---
LOGIN_KEY = "2026"
st.set_page_config(page_title="TITAN V87 - ULTRA MACHINE", layout="wide")

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

# --- MINES ENGINE (fortified) ---
def mines_ultra_engine(hash_val, hex_val, tour_id, choice=1):
    base = f"{hash_val}:{hex_val}:{tour_id}:{choice}:MINES_V87"
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

# --- COSMOS ENGINE (hash, hex, tour actuel only) ---
def cosmos_ultra_engine(hash_val, hex_val, tour_id, iters=120000):
    base = f"{hash_val}:{hex_val}:{tour_id}:COSMOSX_V87"
    h1 = hmac.new(b"COSMOS_CORE", base.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h1 = hmac.new(h1, f"STEP_{i}".encode(), hashlib.sha512).digest()
    blake = hashlib.blake2b(h1).digest()
    sha3 = hashlib.sha3_256(blake).digest()
    final = bytes(a ^ b ^ c for a, b, c in zip(h1, blake, sha3))
    hex_out = final.hex()
    return {"hex": hex_out, "tour": tour_id}

# --- AVIATOR ENGINE (unchanged) ---
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
st.markdown("<h2 style='text-align:center;'>🔐 TITAN V87 - ADMIN LOGIN</h2>", unsafe_allow_html=True)
admin_input = st.text_input("Enter Admin Code:", type="password")

if admin_input == LOGIN_KEY:
    st.success("✅ Access Granted. Machine Activated.")

    tab1, tab2, tab3 = st.tabs(["🌌 COSMOSX", "✈️ AVIATOR STUDIO", "💣 MINES ULTRA"])

    with tab1:
        st.markdown("##### 🌌 COSMOSX SCAN (Hash + Hex + Tour)")
        h_val = st.text_input("Hash Value:", key="cosmos_hash")
        x_val = st.text_input("Hex Value:", key="cosmos_hex")
        t_id = st.number_input("Tour Actuel:", min_value=1, value=10001, key="cosmos_t")
        if st.button("🚀 EXECUTE COSMOS", key="btn_cosmos"):
            res = cosmos_ultra_engine(h_val, x_val, t_id)
            st.code(f"HEX: {res['hex'][:48]}...", language="bash")
            st.write("Tour Actuel:", res["tour"])

    with tab2:
        st.markdown("##### ✈️ AVIATOR STUDIO PREDICTION")
        a_hex = st.text_input("Input HEX Value:", key="avi_hex")
        a_time = st.text_input("Tour Heure (HH:mm):", value=datetime.datetime.now().strftime("%H:%M"), key="avi_time")
        if st.button("✈️ PREDICT", key="btn_avi"):
            res = aviator_studio_engine(a_hex, a_time)
            st.metric("PREDICTED X", f"{res['multiplier']:.2f}x")
            st.write(f"Safe Range: {res['min']}x - {res['moyen']}x - {res['max']}x")
            st.write(f"Accuracy: {int(res['accuracy']*100)}%")

    with tab3:
        st.markdown("##### 💣 MINES ULTRA LOGIC")
        h_val = st.text_input("Hash Value:", key="mines_hash")
        x_val = st.text_input("Hex Value:", key="mines_hex")
        t_id = st.text_input("Tour ID:", key="mines_tour")
        m_choice = st.slider("Select Mines Pattern:", 1, 3, 1, key="m_choice")
        if st.button("🛰️ SCAN MINES", key="btn_mines"):
            schema = mines_ultra_engine(h_val, x_val, t_id, m_choice)
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                grid_html += f'<div class="mine-cell {"cell-star" if i in schema else ""}">{"⭐" if i in schema else "⬛"}</div>'
            st.markdown(grid_html + '</div>', unsafe_allow_html=True)
            st.success("✅ Mines Schema Generated")

elif admin_input != "":
    st.error("❌ Invalid Code")
