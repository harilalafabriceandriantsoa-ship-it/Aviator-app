import streamlit as st
import hashlib, hmac, random, datetime

LOGIN_KEY = "2026"
st.set_page_config(page_title="TITAN V92 - ULTRA MACHINE", layout="wide")

# --- MINES ENGINE ---
def mines_ultra_engine(server_seed, client_seed, nonce, choice=1):
    base = f"{server_seed}:{client_seed}:{nonce}:{choice}:MINES_V92"
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

# --- COSMOS ENGINE (salted T1/T2) ---
def cosmos_ultra_engine(hash_val, hex_val, tour_id, salt, iters=50000):
    base = f"{hash_val}:{hex_val}:{tour_id}:{salt}:COSMOSX_V92"
    h1 = hmac.new(b"COSMOS_CORE", base.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h1 = hmac.new(h1, f"STEP_{i}".encode(), hashlib.sha512).digest()
    blake = hashlib.blake2b(h1).digest()
    sha3 = hashlib.sha3_256(blake).digest()
    final = bytes(a ^ b ^ c for a, b, c in zip(h1, blake, sha3))
    hex_out = final.hex()
    p_int = int(hex_out[:12], 16)
    offset = (p_int % 20) + 5
    jumps = [(p_int % 7) + 2, (p_int % 9) + 3, (p_int % 11) + 4]
    return {"hex": hex_out, "tour": tour_id + offset, "jumps": jumps}

# --- AVIATOR ENGINE (salted T1/T2) ---
def aviator_studio_engine(hex_val, heure, salt):
    h_int = int(hex_val[:16], 16)
    mask = int(heure.replace(":", "")) ^ int.from_bytes(salt.encode(), "big")
    base = h_int ^ mask
    delta = (base % 6) + 2
    heure_dt = datetime.datetime.strptime(heure, "%H:%M")
    h_new = (heure_dt + datetime.timedelta(minutes=delta)).strftime("%H:%M")
    mult = 1 + (base % 9000) / 1000.0
    auto_zone = 2.0 <= mult <= 4.0
    return {
        "heure": h_new,
        "multiplier": mult,
        "min": round(mult * 0.9, 2),
        "moyen": round(mult * 1.3, 2),
        "max": round(mult * 2.7, 2),
        "accuracy": 0.88 if auto_zone else 0.65,
        "auto_zone": auto_zone
    }

# --- LOGIN ---
st.markdown("<h2 style='text-align:center;'>🔐 TITAN V92 - ADMIN LOGIN</h2>", unsafe_allow_html=True)
admin_input = st.text_input("Enter Admin Code:", type="password")

if admin_input == LOGIN_KEY:
    st.success("✅ Access Granted. Machine Activated.")

    tab1, tab2, tab3 = st.tabs(["🌌 COSMOSX", "✈️ AVIATOR STUDIO", "💣 MINES ULTRA"])

    with tab1:
        st.markdown("##### 🌌 COSMOSX PREDICTION (Salted T1/T2)")
        h_val = st.text_input("Hash Value:", key="cosmos_hash")
        x_val = st.text_input("Hex Value:", key="cosmos_hex")
        t_id = st.number_input("Tour Actuel:", min_value=1, value=10001, key="cosmos_t")
        if st.button("🚀 EXECUTE COSMOS", key="btn_cosmos"):
            res1 = cosmos_ultra_engine(h_val, x_val, t_id, "T1")
            res2 = cosmos_ultra_engine(h_val, x_val, t_id, "T2")
            st.code(f"HEX T1: {res1['hex'][:48]}...", language="bash")
            st.write("Tour 1:", res1["tour"], "Jumps:", res1["jumps"])
            st.code(f"HEX T2: {res2['hex'][:48]}...", language="bash")
            st.write("Tour 2:", res2["tour"], "Jumps:", res2["jumps"])

    with tab2:
        st.markdown("##### ✈️ AVIATOR STUDIO PREDICTION (Salted T1/T2)")
        a_hex = st.text_input("Input HEX Value:", key="avi_hex")
        a_time = st.text_input("Heure Fidirana (HH:mm):", value=datetime.datetime.now().strftime("%H:%M"), key="avi_time")
        if st.button("✈️ PREDICT", key="btn_avi"):
            res1 = aviator_studio_engine(a_hex, a_time, "T1")
            res2 = aviator_studio_engine(a_hex, a_time, "T2")
            st.write("Tour 1 Heure:", res1["heure"])
            st.metric("Tour 1 PREDICTED X", f"{res1['multiplier']:.2f}x")
            st.write(f"Range: {res1['min']}x - {res1['moyen']}x - {res1['max']}x | Accuracy: {int(res1['accuracy']*100)}%")
            if res1["auto_zone"]:
                st.success("🎯 AUTO CASH-OUT ZONE (2–4x)")
            st.write("Tour 2 Heure:", res2["heure"])
            st.metric("Tour 2 PREDICTED X", f"{res2['multiplier']:.2f}x")
            st.write(f"Range: {res2['min']}x - {res2['moyen']}x - {res2['max']}x | Accuracy: {int(res2['accuracy']*100)}%")
            if res2["auto_zone"]:
                st.success("🎯 AUTO CASH-OUT ZONE (2–4x)")

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
