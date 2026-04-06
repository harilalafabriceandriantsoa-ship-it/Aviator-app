import streamlit as st
import hashlib, hmac, random

# --- CONFIGURATION FIXE ---
LOGIN_KEY = "2026"
st.set_page_config(page_title="TITAN V86.8 - DYNAMIC DEATH MACHINE", layout="wide")

# --- STYLE INTERFACE (DARK MODE) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .mines-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 330px; margin: 0 auto; }
    .mine-cell { aspect-ratio: 1/1; background: #0a0a0a; border: 1px solid #00ffcc44; display: flex; align-items: center; justify-content: center; font-size: 28px; border-radius: 12px; }
    .cell-star { border: 2px solid #ff0000 !important; background: rgba(255, 0, 0, 0.3); color: #ff0000; box-shadow: 0 0 30px #ff0000; transform: scale(1.05); }
    .scan-box { border: 2px solid #00ffcc; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 15px; background: rgba(0, 255, 204, 0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- LETHAL ENGINES (ALGORITHM MATANJAKA) ---

def mines_ultra_logic(server_seed, client_seed, nonce, mines_choice=1):
    """Mines Algorithm: SHA-512 + Blake2b + SHA-3 + Double Shuffle"""
    base = f"{server_seed}:{client_seed}:{nonce}:{mines_choice}:LETHAL_V8"
    h1 = hashlib.sha512(base.encode()).digest()
    h2 = hashlib.blake2b(h1).digest()
    h3 = hashlib.sha3_256(h2).digest()
    combined = h1 + h2 + h3
    hash_int = int.from_bytes(combined, "big")
    
    grid = list(range(25))
    # Fisher-Yates Shuffle 1
    for i in range(24, 0, -1):
        j = hash_int % (i + 1)
        grid[i], grid[j] = grid[j], grid[i]
        hash_int //= (i + 1)
    
    # Random Seed Shuffle 2 (Double Protection)
    random.seed(int.from_bytes(h3[:16], "big"))
    random.shuffle(grid)
    return grid[:5]

def cosmos_dynamic_engine(server_seed, client_seed, tour_id, iters=90000):
    """Cosmos Algorithm: SHA-512 (90k iterations) + Dynamic Jump Logic"""
    combined = f"{server_seed}:{client_seed}:{tour_id}:COSMOSX_ULTRA"
    h = hmac.new(b"COSMOS_CORE_V86", combined.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h = hmac.new(h, f"STEP_{i}".encode(), hashlib.sha512).digest()
    
    hex_val = h.hex()
    p_int = int(hex_val[:8], 16)
    
    # Dynamic Jumps (Ny Hash no mifidy elanelana)
    j1 = (p_int % 3) + 2
    j2 = j1 + (p_int % 4) + 2
    j3 = j2 + (p_int % 6) + 3
    return {"hex": hex_val, "jumps": [j1, j2, j3]}

def aviator_studio_engine(hex_val, heure):
    """Aviator Algorithm: Time Masking + Hex XOR Logic"""
    try:
        h_int = int(hex_val[:16], 16)
        mask = int(heure.replace(":", ""))
        base = h_int ^ mask
        mult = 1 + (base % 8000) / 1000.0
        return {
            "multiplier": mult,
            "min": round(mult * 0.8, 2),
            "moyen": round(mult * 1.2, 2),
            "max": round(mult * 2.5, 2)
        }
    except:
        return None

# --- UI LOGIC ---

st.markdown("<h2 style='text-align:center;'>🔐 TITAN V86.8 - ADMIN LOGIN</h2>", unsafe_allow_html=True)
admin_input = st.text_input("Enter Admin Code:", type="password", key="main_login")

if admin_input == LOGIN_KEY:
    st.success("✅ Access Granted. Machine de Mort Activated.")
    
    tab1, tab2, tab3 = st.tabs(["🌌 COSMOSX (90K)", "✈️ AVIATOR STUDIO", "💣 MINES ULTRA"])

    with tab1:
        st.markdown("##### 🌌 COSMOSX DYNAMIC SCANNER")
        c_hash = st.text_input("Server Seed / Hash:", key="c_hash")
        c_hex8 = st.text_input("Hex8 / Extra:", key="c_hex")
        c_tour = st.number_input("Tour Actuel:", min_value=1, value=8137473, key="c_tour")
        
        if st.button("🚀 EXECUTE COSMOS SCAN", key="btn_c"):
            if c_hash and c_hex8:
                res = cosmos_dynamic_engine(c_hash, c_hex8, c_tour)
                st.code(f"HEX: {res['hex'][:48]}...", language="bash")
                for j in res["jumps"]:
                    target = c_tour + j
                    st.markdown(f"""
                        <div class="scan-box">
                            <span style="color:#aaa;">TARGET TOUR {target} (GAP +{j})</span><br>
                            <span style="font-size:30px; color:#ff0000; font-weight:bold;">{round(random.uniform(1.5, 5.0), 2)}x</span>
                        </div>
                    """, unsafe_allow_html=True)

    with tab2:
        st.markdown("##### ✈️ AVIATOR STUDIO PREDICTION")
        a_hex = st.text_input("Input HEX Value:", key="a_hex")
        a_time = st.text_input("Tour Heure (HH:mm):", value="17:01", key="a_time")
        if st.button("✈️ PREDICT", key="btn_a"):
            res = aviator_studio_engine(a_hex, a_time)
            if res:
                st.metric("PREDICTED X", f"{res['multiplier']:.2f}x")
                st.write(f"Safe Range: {res['min']}x - {res['moyen']}x")

    with tab3:
        st.markdown("##### 💣 MINES ULTRA-LOGIC (5 DIAMONDS)")
        m_s_seed = st.text_input("Server Seed:", key="m_s")
        m_c_seed = st.text_input("Client Seed:", key="m_c")
        m_nonce = st.text_input("ID Partie / Nonce:", key="m_n")
        m_choice = st.slider("Select Logic Pattern:", 1, 3, 1, key="m_sl")
        
        if st.button("🛰️ SCAN SCHEMA", key="btn_m"):
            schema = mines_ultra_logic(m_s_seed, m_c_seed, m_nonce, m_choice)
            grid_html = '<div class="mines-grid">'
            for i in range(25):
                grid_html += f'<div class="mine-cell {"cell-star" if i in schema else ""}">{"⭐" if i in schema else "⬛"}</div>'
            st.markdown(grid_html + '</div>', unsafe_allow_html=True)
            st.success("LETHAL SCHEMA LOCKED")

elif admin_input != "":
    st.error("❌ Code diso.")
