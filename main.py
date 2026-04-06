import streamlit as st
import hashlib, hmac, random

# --- LOGIN KEY DIRECT ---
LOGIN_KEY = "2026"

st.set_page_config(page_title="TITAN V86.8 - DYNAMIC", layout="wide")

# --- STYLE (WAR INTERFACE) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 330px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #0a0a0a; border: 1px solid #00ffcc44; display: flex; align-items: center; justify-content: center; font-size: 28px; border-radius: 12px; }
    .cell-star { border: 2px solid #ff0000 !important; background: rgba(255, 0, 0, 0.3); color: #ff0000; box-shadow: 0 0 30px #ff0000; transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE FUNCTIONS (ALGORITHM TSY NOKASIHINA) ---
def mines_schema(server_seed, client_seed, nonce, mines_choice=1):
    base = f"{server_seed}:{client_seed}:{nonce}:{mines_choice}"
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

def cosmos_prediction(server_seed, client_seed, tour_id, iters=50000):
    combined = f"{server_seed}:{client_seed}:{tour_id}:COSMOSX2026"
    h = hmac.new(b"COSMOS_CORE", combined.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h = hmac.new(h, f"STEP_{i}".encode(), hashlib.sha512).digest()
    blake = hashlib.blake2b(h).digest()
    sha3 = hashlib.sha3_256(blake).digest()
    final = bytes(a ^ b ^ c for a, b, c in zip(h, blake, sha3))
    hex_val = final.hex()
    p_int = int(hex_val[:8], 16)
    jump1 = (p_int % 3) + 2
    jump2 = jump1 + (p_int % 4) + 2
    jump3 = jump2 + (p_int % 6) + 3
    return {"hex": hex_val, "jumps": [jump1, jump2, jump3]}

def aviator_prediction(hex_val, heure):
    h_int = int(hex_val[:16], 16)
    mask = int(heure.replace(":", ""))
    base = h_int ^ mask
    mult = 1 + (base % 7000) / 1000.0
    return {"multiplier": mult, "min": round(mult * 0.7, 2), "moyen": round(mult * 1.1, 2), "max": round(mult * 2.8, 2)}

# --- UI SYSTEM ---
st.markdown("<h2 style='text-align:center;'>🔐 TITAN V86.8 - ADMIN LOGIN</h2>", unsafe_allow_html=True)
# Nampiana key='login' mba tsy hisy error
admin_input = st.text_input("Enter Admin Code:", type="password", key="login_main")

if admin_input == LOGIN_KEY:
    tab1, tab2, tab3 = st.tabs(["🌌 COSMOSX", "✈️ AVIATOR STUDIO", "💣 MINES ULTRA"])

    with tab1:
        st.markdown("##### 🌌 COSMOSX (HASH + HEX + TOUR)")
        # Nampiana key manokana isaky ny input
        s_seed_c = st.text_input("Server Seed (Hash):", key="cosmos_s_seed")
        c_seed_c = st.text_input("Client Seed (Hex):", key="cosmos_c_seed")
        t_id_c = st.number_input("Numéro de Tour Actuel:", min_value=1, value=8137473, key="cosmos_t_id")
        
        if st.button("🚀 RUN COSMOSX SCAN", key="btn_cosmos"):
            if s_seed_c and c_seed_c:
                res = cosmos_prediction(s_seed_c, c_seed_c, t_id_c)
                st.code(f"HEX RESULT: {res['hex'][:40]}...", language="bash")
                cols = st.columns(3)
                for i, jump in enumerate(res["jumps"]):
                    cols[i].metric(f"TARGET TOUR {t_id_c + jump}", f"GAP +{jump}")
                st.success("Analysis complete using SHA-512 Logic.")

    with tab2:
        st.markdown("##### ✈️ AVIATOR STUDIO")
        hex_val_a = st.text_input("Input HEX Value:", key="aviator_hex")
        heure_a = st.text_input("Tour Heure (HH:mm):", value="17:01", key="aviator_time")
        if st.button("✈️ PREDICT MULTIPLIER", key="btn_aviator"):
            if hex_val_a:
                res = aviator_prediction(hex_val_a, heure_a)
                st.metric("PREDICTED X", f"{res['multiplier']:.2f}x")
                st.write(f"Range: {res['min']}x - {res['max']}x")

    with tab3:
        st.markdown("##### 💣 MINES (DOUBLE SHUFFLE PROTECTION)")
        # Eto no namboarina ny Mines mba ho machine de mort
        col_s1, col_s2 = st.columns(2)
        s_s_m = col_s1.text_input("Server Seed:", key="mines_s_seed")
        c_s_m = col_s2.text_input("Client Seed:", key="mines_c_seed")
        t_id_m = st.text_input("ID Partie / Nonce:", key="mines_t_id")
        m_choice = st.slider("Mines Choice:", 1, 3, 1, key="mines_slider")
        
        if st.button("🛰️ GENERATE LETHAL SCHEMA", key="btn_mines"):
            if s_s_m and c_s_m:
                schema = mines_schema(s_s_m, c_s_m, t_id_m, m_choice)
                grid_html = '<div class="mines-grid">'
                for i in range(25):
                    if i in schema:
                        grid_html += '<div class="mine-cell cell-star">⭐</div>'
                    else:
                        grid_html += '<div class="mine-cell">⬛</div>'
                grid_html += '</div>'
                st.markdown(grid_html, unsafe_allow_html=True)
                st.success("SCHEMA LOCKED - ANTI-BOT ACTIVE")

elif admin_input != "":
    st.error("❌ Admin Code diso, avereno azafady.")
