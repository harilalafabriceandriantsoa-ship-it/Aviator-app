import streamlit as st
import hashlib, hmac, random, datetime

# --- CONFIGURATION ---
LOGIN_KEY = "2026"
st.set_page_config(page_title="TITAN V91 - ULTRA MACHINE", layout="wide")

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

# --- MINES ENGINE ---
def mines_ultra_engine(server_seed, client_seed, nonce, choice=1):
    base = f"{server_seed}:{client_seed}:{nonce}:{choice}:MINES_V91"
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

# --- COSMOS ENGINE (Variable Tours) ---
def cosmos_ultra_engine(hash_val, hex_val, tour_id, iters=100000):
    base = f"{hash_val}:{hex_val}:{tour_id}:COSMOSX_V91"
    h1 = hmac.new(b"COSMOS_CORE", base.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h1 = hmac.new(h1, f"STEP_{i}".encode(), hashlib.sha512).digest()
    hex_out = h1.hex()
    p_int = int(hex_out[:12], 16)
    
    # Offset variable arakaraka ny hash (Tsy raikitra)
    offset1 = (p_int % 8) + 3
    offset2 = offset1 + (p_int % 10) + 4
    jumps = [(p_int % 7) + 2, (p_int % 9) + 3]
    
    return {
        "hex": hex_out,
        "tour1": tour_id + offset1,
        "tour2": tour_id + offset2,
        "jumps": jumps
    }

# --- AVIATOR ENGINE (Variable Minutes) ---
def aviator_studio_engine(hex_val, heure):
    try:
        h_int = int(hex_val[:16], 16)
        mask = int(heure.replace(":", ""))
        base = h_int ^ mask
        
        # Delta variable arakaraka ny hash
        delta1 = (base % 6) + 2
        delta2 = delta1 + (base % 8) + 3
        
        heure_dt = datetime.datetime.strptime(heure, "%H:%M")
        h1 = (heure_dt + datetime.timedelta(minutes=delta1)).strftime("%H:%M")
        h2 = (heure_dt + datetime.timedelta(minutes=delta2)).strftime("%H:%M")
        
        mult = 1 + (base % 9000) / 1000.0
        accuracy = 0.88 if 2.0 <= mult <= 4.5 else 0.62
        
        return {
            "heure1": h1, "heure2": h2, "multiplier": mult,
            "min": round(mult * 0.85, 2), "moyen": round(mult * 1.15, 2), 
            "max": round(mult * 2.4, 2), "accuracy": accuracy
        }
    except: return None

# --- UI LOGIN ---
st.markdown("<h2 style='text-align:center;'>🔐 TITAN V91 - ADMIN LOGIN</h2>", unsafe_allow_html=True)
admin_input = st.text_input("Enter Admin Code:", type="password", key="login")

if admin_input == LOGIN_KEY:
    st.success("✅ Access Granted. TITAN V91 Active.")
    tab1, tab2, tab3 = st.tabs(["🌌 COSMOSX", "✈️ AVIATOR STUDIO", "💣 MINES ULTRA"])

    with tab1:
        st.markdown("##### 🌌 COSMOSX (VARIABLE SCAN)")
        h_val = st.text_input("Hash Value:", key="c_h")
        x_val = st.text_input("Hex Value:", key="c_x")
        t_id = st.number_input("Tour Actuel:", min_value=1, value=8137473, key="c_t")
        if st.button("🚀 EXECUTE COSMOS"):
            if h_val and x_val:
                res = cosmos_ultra_engine(h_val, x_val, t_id)
                st.code(f"HEX: {res['hex'][:40]}...", language="bash")
                col1, col2 = st.columns(2)
                col1.metric("TARGET T1", res["tour1"], f"Gap +{res['tour1']-t_id}")
                col2.metric("TARGET T2", res["tour2"], f"Gap +{res['tour2']-t_id}")
                st.info(f"Recommended Jumps: {res['jumps']}")

    with tab2:
        st.markdown("##### ✈️ AVIATOR STUDIO (VARIABLE TIME)")
        a_hex = st.text_input("Input HEX Value:", key="a_h")
        a_time = st.text_input("Heure Actuelle (HH:mm):", value=datetime.datetime.now().strftime("%H:%M"), key="a_t")
        if st.button("✈️ PREDICT MULTIPLIER"):
            res = aviator_studio_engine(a_hex, a_time)
            if res:
                for i, h_target in enumerate([res["heure1"], res["heure2"]]):
                    st.markdown(f"**Target {i+1} at {h_target}**")
                    st.metric("PREDICTED X", f"{res['multiplier']:.2f}x")
                    st.write(f"📊 Range: {res['min']}x - {res['moyen']}x - {res['max']}x")
                    st.write(f"⚡ Accuracy: {int(res['accuracy']*100)}%")
                    if 2.0 <= res['moyen'] <= 4.0: st.success("🎯 AUTO CASH-OUT ZONE (2-4x)")
                    st.divider()

    with tab3:
        st.markdown("##### 💣 MINES ULTRA (SHA-512 + DOUBLE SHUFFLE)")
        m_s = st.text_input("Server Seed:", key="m_s")
        m_c = st.text_input("Client Seed:", key="m_c")
        m_n = st.text_input("Nonce / ID Partie:", key="m_n")
        m_ch = st.slider("Select Pattern (1-3):", 1, 3, 1)
        if st.button("🛰️ SCAN GRID"):
            if m_s and m_c:
                schema = mines_ultra_engine(m_s, m_c, m_n, m_ch)
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    grid_html += f'<div class="mine-cell {"cell-star" if i in schema else ""}">{"⭐" if i in schema else ""}</div>'
                st.markdown(grid_html + '</div>', unsafe_allow_html=True)
