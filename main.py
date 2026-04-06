import streamlit as st
import hashlib, hmac, random, datetime

# --- CONFIGURATION ---
LOGIN_KEY = "2026"
st.set_page_config(page_title="TITAN V92 - ULTRA MACHINE", layout="wide")

# --- STYLE CSS (Namboarina mba hadio) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 330px; margin: auto; }
    .mine-cell { aspect-ratio: 1/1; background: #0a0a0a; border: 1px solid #00ffcc44; display: flex; align-items: center; justify-content: center; font-size: 28px; border-radius: 12px; }
    .cell-star { border: 2px solid #ff0000 !important; background: rgba(255, 0, 0, 0.3); color: #ff0000; box-shadow: 0 0 30px #ff0000; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINES (Algorithms) ---

def mines_ultra_engine(server_seed, client_seed, nonce, choice=1):
    try:
        base = f"{server_seed}:{client_seed}:{nonce}:{choice}:MINES_V92"
        h1 = hashlib.sha512(base.encode()).digest()
        h2 = hashlib.blake2b(h1).digest()
        h3 = hashlib.sha3_256(h2).digest()
        hash_int = int.from_bytes(h1 + h2 + h3, "big")
        grid = list(range(25))
        for i in range(24, 0, -1):
            j = hash_int % (i + 1)
            grid[i], grid[j] = grid[j], grid[i]
            hash_int //= (i + 1)
        random.seed(int.from_bytes(h3[:16], "big"))
        random.shuffle(grid)
        return grid[:5]
    except: return []

def cosmos_ultra_engine(hash_val, hex_val, tour_id, salt, iters=50000):
    try:
        base = f"{hash_val}:{hex_val}:{tour_id}:{salt}:COSMOSX_V92"
        h1 = hmac.new(b"COSMOS_CORE", base.encode(), hashlib.sha512).digest()
        for i in range(iters):
            h1 = hmac.new(h1, f"STEP_{i}".encode(), hashlib.sha512).digest()
        hex_out = h1.hex()
        p_int = int(hex_out[:12], 16)
        offset = (p_int % 20) + 5
        jumps = [(p_int % 7) + 2, (p_int % 9) + 3]
        return {"hex": hex_out, "tour": tour_id + offset, "jumps": jumps}
    except: return None

def aviator_studio_engine(hex_val, heure, salt):
    try:
        # Fanalana ny tarehintsoratra mety manimba
        hex_clean = "".join(c for c in hex_val if c in "0123456789abcdefABCDEF")
        h_int = int(hex_clean[:16], 16)
        mask = int(heure.replace(":", "")) ^ int.from_bytes(salt.encode(), "big")
        base = h_int ^ mask
        delta = (base % 6) + 2
        heure_dt = datetime.datetime.strptime(heure, "%H:%M")
        h_new = (heure_dt + datetime.timedelta(minutes=delta)).strftime("%H:%M")
        mult = 1 + (base % 9000) / 1000.0
        return {
            "heure": h_new, "multiplier": mult,
            "min": round(mult * 0.9, 2), "moyen": round(mult * 1.3, 2),
            "max": round(mult * 2.7, 2), "accuracy": 0.88 if 2.0 <= mult <= 4.0 else 0.65
        }
    except: return None

# --- UI INTERFACE ---

st.markdown("<h2 style='text-align:center;'>🔐 TITAN V92 - ADMIN LOGIN</h2>", unsafe_allow_html=True)
admin_input = st.text_input("Enter Admin Code:", type="password", key="main_auth")

if admin_input == LOGIN_KEY:
    st.success("✅ TITAN V92 Activated.")
    tab1, tab2, tab3 = st.tabs(["🌌 COSMOSX", "✈️ AVIATOR STUDIO", "💣 MINES ULTRA"])

    with tab1:
        st.markdown("##### 🌌 COSMOSX (SALTED T1/T2)")
        h_v = st.text_input("Hash Value:", key="c_hash")
        x_v = st.text_input("Hex Value:", key="c_hex")
        t_v = st.number_input("Tour Actuel:", min_value=1, value=8137473, key="c_tour")
        if st.button("🚀 SCAN COSMOS"):
            if h_v and x_v:
                for s in ["T1", "T2"]:
                    res = cosmos_ultra_engine(h_v, x_v, t_v, s)
                    if res:
                        st.write(f"**{s} Target:** Tour {res['tour']} | Jumps: {res['jumps']}")
                        st.code(res['hex'][:32], language="bash")

    with tab2:
        st.markdown("##### ✈️ AVIATOR STUDIO (SALTED T1/T2)")
        a_h = st.text_input("Input HEX Value:", key="a_hex")
        a_t = st.text_input("Heure (HH:mm):", value=datetime.datetime.now().strftime("%H:%M"), key="a_time")
        if st.button("✈️ PREDICT"):
            if a_h:
                for s in ["T1", "T2"]:
                    res = aviator_studio_engine(a_h, a_t, s)
                    if res:
                        st.markdown(f"**Target {s} at {res['heure']}**")
                        st.metric("PREDICTED X", f"{res['multiplier']:.2f}x")
                        st.write(f"Accuracy: {int(res['accuracy']*100)}% | Zone: {res['min']}x-{res['max']}x")
                        st.divider()

    with tab3:
        st.markdown("##### 💣 MINES ULTRA LOGIC")
        m_s = st.text_input("Server Seed:", key="ms")
        m_c = st.text_input("Client Seed:", key="mc")
        m_n = st.text_input("Nonce:", key="mn")
        m_sl = st.slider("Pattern:", 1, 3, 1)
        if st.button("🛰️ SCAN MINES"):
            schema = mines_ultra_engine(m_s, m_c, m_n, m_sl)
            if schema:
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    grid_html += f'<div class="mine-cell {"cell-star" if i in schema else ""}">{"⭐" if i in schema else ""}</div>'
                st.markdown(grid_html + '</div>', unsafe_allow_html=True)

elif admin_input != "":
    st.error("❌ Code diso.")
